import json
import time
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.evaluation.metrics import RetrievalMetrics, AnswerMetrics
from src.evaluation.classic_rag import ClassicRAG
from src.agents.graph import AgenticRAGFlow

class Evaluator:
    def __init__(self, test_set_path: str):
        """100 Soruluk Test Veri Setini (JSON) Yükler."""
        self.test_set_path = test_set_path
        
        with open(self.test_set_path, "r", encoding="utf-8") as f:
            self.test_cases = json.load(f)
            
        self.classic_rag = ClassicRAG()
        self.agentic_rag = AgenticRAGFlow()
        self.results = []
        
    def run_evaluation(self):
        print(f"Değerlendirme Başlıyor. Toplam Soru Sayısı: {len(self.test_cases)}")
        
        for idx, test_case in enumerate(self.test_cases):
            query = test_case["query"]
            ground_truth = test_case["ground_truth_docs"]
            difficulty = test_case["difficulty"]
            
            print(f"\n[{idx+1}/{len(self.test_cases)}] Test Ediliyor: {query[:60]}...")
            
            # ==========================================
            # 1. KLASİK RAG TESTİ
            # ==========================================
            start_time = time.time()
            classic_res = self.classic_rag.ask(query)
            classic_time = time.time() - start_time
            
            c_recall_5 = RetrievalMetrics.calculate_recall_at_k(classic_res["retrieved_docs"], ground_truth, k=5)
            c_mrr = RetrievalMetrics.calculate_mrr(classic_res["retrieved_docs"], ground_truth)
            c_citation = AnswerMetrics.citation_accuracy(classic_res["answer"], ground_truth)
            
            # ==========================================
            # 2. AGENTIC RAG TESTİ
            # ==========================================
            start_time = time.time()
            agentic_res = self.agentic_rag.run(query)
            agentic_time = time.time() - start_time
            
            # Ajanlar eksik bilgi hissettikçe yeni arama yaptığı için toplanan belgeler daha fazladır.
            a_recall_5 = RetrievalMetrics.calculate_recall_at_k(agentic_res["retrieved_docs"], ground_truth, k=5)
            a_mrr = RetrievalMetrics.calculate_mrr(agentic_res["retrieved_docs"], ground_truth)
            a_citation = AnswerMetrics.citation_accuracy(agentic_res["final_answer"], ground_truth)
            
            # Sonuçları Kaydet
            self.results.append({
                "id": test_case["id"],
                "Zorluk": difficulty,
                
                "Klasik_Sure(sn)": round(classic_time, 2),
                "Klasik_Recall@5": c_recall_5,
                "Klasik_MRR": c_mrr,
                "Klasik_Atif_Dogrulugu": c_citation,
                "Klasik_Arama_Sayisi": 1, # Klasik RAG tek sefer arar
                
                "Ajan_Sure(sn)": round(agentic_time, 2),
                "Ajan_Recall@5": a_recall_5,
                "Ajan_MRR": a_mrr,
                "Ajan_Atif_Dogrulugu": a_citation,
                "Ajan_Arama_Sayisi": agentic_res.get("search_count", 1) # Ajanlar defalarca arayabilir
            })
            
        self._save_results()

    def _save_results(self):
        """Sonuçları Pandas ile işleyip Excel/CSV olarak kaydeder ve rapor üretir."""
        df = pd.DataFrame(self.results)
        
        summary = {
            "Metrik": ["Ortalama Yanıt Süresi (s)", "p95 Yanıt Süresi (s)", "Ortalama Recall@5", "Ortalama MRR", "Atıf Doğruluğu", "Ortalama Arama Döngüsü"],
            "Klasik RAG": [
                round(df["Klasik_Sure(sn)"].mean(), 2),
                round(df["Klasik_Sure(sn)"].quantile(0.95), 2),
                round(df["Klasik_Recall@5"].mean(), 2),
                round(df["Klasik_MRR"].mean(), 2),
                round(df["Klasik_Atif_Dogrulugu"].mean(), 2),
                round(df["Klasik_Arama_Sayisi"].mean(), 1)
            ],
            "Agentic RAG": [
                round(df["Ajan_Sure(sn)"].mean(), 2),
                round(df["Ajan_Sure(sn)"].quantile(0.95), 2),
                round(df["Ajan_Recall@5"].mean(), 2),
                round(df["Ajan_MRR"].mean(), 2),
                round(df["Ajan_Atif_Dogrulugu"].mean(), 2),
                round(df["Ajan_Arama_Sayisi"].mean(), 1)
            ]
        }
        
        summary_df = pd.DataFrame(summary)
        
        out_dir = Path(__file__).resolve().parent / "results"
        out_dir.mkdir(exist_ok=True)
        
        # Dosyaları diske yaz
        df.to_csv(out_dir / "detailed_results.csv", index=False)
        summary_df.to_csv(out_dir / "summary_results.csv", index=False)
        
        print("\n" + "="*50)
        print("BİLİMSEL DEĞERLENDİRME ÖZETİ")
        print("="*50)
        print(summary_df.to_string(index=False))
        print(f"\nSonuçlar {out_dir} klasörüne CSV olarak kaydedildi.")

if __name__ == "__main__":
    # Testleri başlatmak için:
    # eval_script = Evaluator(test_set_path="src/evaluation/test_set_template.json")
    # eval_script.run_evaluation()
    pass
