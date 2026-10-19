import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from src.config import VECTOR_DB_DIR, PROCESSED_DATA_DIR, EMBEDDING_MODEL, RETRIEVER_TOP_K

class HybridRetriever:
    def __init__(self, rebuild_index=False):
        print(f"Embedding modeli yükleniyor: {EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.db_dir = VECTOR_DB_DIR
        self.chroma_client = chromadb.PersistentClient(path=str(self.db_dir))
        self.collection_name = "yalova_rag"
        
        # BM25 verileri için yerel bellek değişkenleri
        self.corpus = []
        self.metadata_list = []
        self.bm25 = None
        
        if rebuild_index:
            self.build_index()
        else:
            self.load_bm25_from_disk()

    def load_bm25_from_disk(self):
        """Önceden oluşturulmuş 'all_chunks.json' üzerinden BM25 objesini bellekte ayağa kaldırır."""
        chunks_file = PROCESSED_DATA_DIR / "all_chunks.json"
        if chunks_file.exists():
            with open(chunks_file, "r", encoding="utf-8") as f:
                chunks = json.load(f)
                self.corpus = [c["content"] for c in chunks]
                self.metadata_list = [c["metadata"] for c in chunks]
                
                # BM25 için metinleri kelimelere ayır (boşluk bazlı basit tokenizer)
                tokenized_corpus = [doc.lower().split(" ") for doc in self.corpus]
                if tokenized_corpus:
                    self.bm25 = BM25Okapi(tokenized_corpus)

    def build_index(self):
        """JSON dosyasını okuyup ChromaDB'ye ve BM25'e yazar."""
        try:
            self.chroma_client.delete_collection(self.collection_name)
        except:
            pass
            
        self.collection = self.chroma_client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"} # Kosinüs benzerliği
        )
        
        chunks_file = PROCESSED_DATA_DIR / "all_chunks.json"
        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            
        self.corpus = []
        self.metadata_list = []
        
        documents = []
        metadatas = []
        ids = []
        
        print(f"Toplam {len(chunks)} parça indeksleniyor...")
        for i, chunk in enumerate(chunks):
            doc = chunk["content"]
            meta = chunk["metadata"].copy()
            
            # ChromaDB 'None' değer kabul etmez, boş string'e çeviriyoruz.
            for k, v in meta.items():
                if v is None:
                    meta[k] = ""
                    
            self.corpus.append(doc)
            self.metadata_list.append(meta)
            
            documents.append(doc)
            metadatas.append(meta)
            ids.append(f"chunk_{i}")
            
        # Modeli kullanarak Embedding vektörlerini üret
        embeddings = self.embedding_model.encode(documents, show_progress_bar=True).tolist()
        
        # Vektörleri toplu olarak ChromaDB'ye kaydet
        batch_size = 5000
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                documents=documents[i:i+batch_size],
                embeddings=embeddings[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
            
        # BM25'i kur
        tokenized_corpus = [doc.lower().split(" ") for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
        print("İndeksleme tamamlandı.")

    def _rrf_score(self, vector_results, bm25_results, k=60):
        """
        Reciprocal Rank Fusion (RRF) algoritması:
        Farklı yöntemlerden (Vektör + Anahtar Kelime) gelen sıralamaları birleştirir.
        Formül: Score = 1 / (k + rank)
        """
        rrf_scores = {}
        
        for rank, item in enumerate(vector_results):
            doc_id = item["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
            
        for rank, item in enumerate(bm25_results):
            doc_id = item["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
            
        return rrf_scores

    def search(self, query: str, filters: dict = None, top_k: int = RETRIEVER_TOP_K) -> List[Dict[str, Any]]:
        """Hem vektörel hem kelime bazlı arama yapıp sonucu birleştirerek döner."""
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
        except:
            print("Veritabanı bulunamadı, önce indeks oluşturmalısınız.")
            return []
            
        # --- 1. VEKTÖR ARAMASI (BGE-M3) ---
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Metadata Filtresi Hazırlığı
        chroma_filter = None
        if filters:
            if len(filters) == 1:
                k, v = list(filters.items())[0]
                chroma_filter = {k: v}
            else:
                chroma_filter = {"$and": [{k: v} for k, v in filters.items()]}
                
        vector_resp = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2, # RRF için fazla sonuç çekiyoruz
            where=chroma_filter
        )
        
        vector_results = []
        if vector_resp["ids"] and vector_resp["ids"][0]:
            for i, doc_id in enumerate(vector_resp["ids"][0]):
                vector_results.append({
                    "id": doc_id,
                    "content": vector_resp["documents"][0][i],
                    "metadata": vector_resp["metadatas"][0][i]
                })

        # --- 2. BM25 (Kelimelerle) ARAMA ---
        bm25_results = []
        if self.bm25:
            tokenized_query = query.lower().split(" ")
            bm25_scores = self.bm25.get_scores(tokenized_query)
            
            top_n = np.argsort(bm25_scores)[::-1][:top_k * 2]
            for idx in top_n:
                if bm25_scores[idx] > 0:
                    meta = self.metadata_list[idx]
                    # BM25 filtre desteği sunmadığından filtrelemeyi manuel yapıyoruz
                    passed_filter = True
                    if filters:
                        for k, v in filters.items():
                            if meta.get(k) != v:
                                passed_filter = False
                                break
                    if passed_filter:
                        bm25_results.append({
                            "id": f"chunk_{idx}",
                            "content": self.corpus[idx],
                            "metadata": meta
                        })
                        
        # --- 3. RRF (Birleştirme) ---
        rrf_scores = self._rrf_score(vector_results, bm25_results)
        
        all_docs = {item["id"]: item for item in vector_results + bm25_results}
        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        
        final_results = [all_docs[doc_id] for doc_id in sorted_ids[:top_k]]
        return final_results
