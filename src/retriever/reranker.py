from FlagEmbedding import FlagReranker
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from src.config import RERANKER_MODEL, RERANKER_TOP_K

class BGEReranker:
    def __init__(self):
        """
        BGE-Reranker-v2-m3 modelini yükler.
        Çok dilli olduğu için Türkçe metinlerdeki semantik bağları çok iyi yakalar.
        FP16 (Half Precision) kullanarak VRAM/RAM tüketimini azaltıyoruz.
        """
        print(f"Reranker modeli yükleniyor: {RERANKER_MODEL}")
        self.reranker = FlagReranker(RERANKER_MODEL, use_fp16=True)

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = RERANKER_TOP_K) -> List[Dict[str, Any]]:
        """
        Hibrit aramadan gelen 20 civarı belgeyi, sorguyla tek tek karşılaştırarak
        çapraz etkileşim (cross-attention) ile gerçek anlamda puanlar ve en iyi N belgeyi bırakır.
        """
        if not documents:
            return []
            
        # Model girdisi: (Sorgu, Belge) çiftleri
        pairs = [[query, doc["content"]] for doc in documents]
        
        # Puanları hesapla (Büyük skor daha iyi)
        scores = self.reranker.compute_score(pairs)
        
        # Tek belge gelirse score listesi yerine float dönebilir, listeye çevirelim
        if isinstance(scores, float):
            scores = [scores]
            
        # Puanları belgelere ekle
        scored_docs = []
        for i, doc in enumerate(documents):
            doc_copy = doc.copy()
            doc_copy["rerank_score"] = float(scores[i])
            scored_docs.append(doc_copy)
            
        # Yüksek puandan düşüğe doğru sırala
        scored_docs.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        # Sadece Ajanların okuyabileceği sınırlı sayıdaki en alakalı belgeyi (Top K) dön
        return scored_docs[:top_k]
