"""
Klasik RAG (Baseline) Sistemi
Karşılaştırma deneyleri (Aşama 8) için referans noktası olarak tasarlanmıştır.
Ajan mimarisi yoktur. Sadece şu düz akışı izler:
Kullanıcı Sorusu -> Hibrit Arama -> Reranker -> Bağlam + Soru -> LLM Cevabı
"""

import sys
from pathlib import Path

# Kök dizini yola ekle
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import BGEReranker
from src.llm.client import LLMClient

class ClassicRAG:
    def __init__(self):
        print("Klasik RAG sistemi başlatılıyor...")
        self.retriever = HybridRetriever(rebuild_index=False)
        self.reranker = BGEReranker()
        self.llm = LLMClient()
        
        # Katı Prompt: Halüsinasyonu en aza indirmek için
        self.system_prompt = (
            "Sen Yalova Üniversitesi için geliştirilmiş resmi bir asistanısın.\n"
            "Kullanıcının sorusuna SADECE aşağıda sana verilen kaynak metinlere (bağlam) dayanarak cevap ver.\n"
            "Eğer sana verilen belgelerde sorunun cevabı KESİNLİKLE yoksa, varsayım yapma ve sadece "
            "'Bu bilgiyi resmî kaynaklarda bulamadım.' de.\n"
            "Verdiğin her cevabın sonuna, bilgiyi hangi belgeden aldığını [Belge Adı] şeklinde ekle."
        )
        
    def ask(self, query: str) -> dict:
        print(f"\n[Arama Yapılıyor] Soru: '{query}'")
        # 1. Hibrit Arama
        raw_docs = self.retriever.search(query=query)
        
        # 2. Yeniden Sıralama (Rerank)
        top_docs = self.reranker.rerank(query=query, documents=raw_docs)
        
        if not top_docs:
            return {
                "query": query,
                "answer": "Sistemde arama yapılabilecek herhangi bir belge bulunamadı.",
                "retrieved_docs": []
            }
            
        # 3. Prompt İçin Bağlam (Context) Hazırlama
        context_text = ""
        for i, doc in enumerate(top_docs):
            meta = doc["metadata"]
            belge_adi = meta.get("belge_adi", "Bilinmeyen Belge")
            madde = meta.get("madde_no", "")
            
            context_text += f"\n--- Kaynak {i+1} ---\n"
            context_text += f"Belge Adı: {belge_adi}\n"
            if madde and madde not in ["None", "Bilinmiyor"]:
                context_text += f"Madde: {madde}\n"
            context_text += f"İçerik: {doc['content']}\n"
            
        # 4. LLM Çağrısı
        prompt = f"Bağlam:\n{context_text}\n\nSoru: {query}\n\nCevap:"
        
        print("[LLM Düşünüyor...]")
        answer = self.llm.generate(prompt=prompt, system_prompt=self.system_prompt, format_json=False)
        
        return {
            "query": query,
            "answer": answer,
            "retrieved_docs": top_docs
        }

if __name__ == "__main__":
    # Test kodları
    rag = ClassicRAG()
    soru = "Bilgisayar Mühendisliği öğrencisi olarak Erasmus başvurusu için hangi belgeler gerekiyor?"
    sonuc = rag.ask(soru)
    
    print("\n" + "="*50)
    print("SİSTEM CEVABI:")
    print("="*50)
    print(sonuc["answer"])
    print("\n[Kullanılan Kaynaklar]:")
    for doc in sonuc["retrieved_docs"]:
        print(f"- {doc['metadata']['belge_adi']} (Rerank Puanı: {doc.get('rerank_score', 0):.2f})")
