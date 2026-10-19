from typing import List, Dict, Any

class RetrievalMetrics:
    @staticmethod
    def calculate_recall_at_k(retrieved_docs: List[Dict[str, Any]], ground_truth: List[Dict[str, Any]], k: int = 5) -> float:
        """
        Recall@K: Sistem, bilginin bulunduğu GERÇEK belgeleri, ilk K belge arasına getirebilmiş mi?
        """
        if not ground_truth:
            return 1.0
            
        retrieved_k = retrieved_docs[:k]
        
        found_count = 0
        for gt in ground_truth:
            gt_belge = gt.get("belge_adi", "").lower()
            gt_madde = gt.get("madde_no", "")
            
            # Aranılan belge getirilenler arasında var mı?
            for r_doc in retrieved_k:
                r_meta = r_doc.get("metadata", {})
                r_belge = r_meta.get("belge_adi", "").lower()
                r_madde = r_meta.get("madde_no", "")
                
                # İsim eşleşmesi (ve varsa madde eşleşmesi)
                if gt_belge in r_belge or r_belge in gt_belge:
                    if not gt_madde or gt_madde == "None" or gt_madde == r_madde:
                        found_count += 1
                        break
                        
        return found_count / len(ground_truth)

    @staticmethod
    def calculate_mrr(retrieved_docs: List[Dict[str, Any]], ground_truth: List[Dict[str, Any]]) -> float:
        """
        Mean Reciprocal Rank (MRR): Doğru belgenin ilk olarak kaçıncı sırada çıktığını puanlar.
        1. sırada çıkarsa tam puan (1.0), 3. sırada çıkarsa (0.33) puan alır.
        """
        if not ground_truth:
            return 0.0
            
        for rank, r_doc in enumerate(retrieved_docs):
            r_meta = r_doc.get("metadata", {})
            r_belge = r_meta.get("belge_adi", "").lower()
            r_madde = r_meta.get("madde_no", "")
            
            for gt in ground_truth:
                gt_belge = gt.get("belge_adi", "").lower()
                gt_madde = gt.get("madde_no", "")
                
                if gt_belge in r_belge or r_belge in gt_belge:
                    if not gt_madde or gt_madde == "None" or gt_madde == r_madde:
                        return 1.0 / (rank + 1)
        return 0.0

class AnswerMetrics:
    @staticmethod
    def citation_accuracy(answer: str, ground_truth: List[Dict[str, Any]]) -> float:
        """
        Cevabın içinde [Belge Adı] şeklinde doğru atıfların yapılıp yapılmadığını basitçe ölçer.
        (Gelişmiş ölçüm için RAGAS kütüphanesinin Context Precision metrikleri kullanılır).
        """
        if not ground_truth:
            return 1.0
            
        found_citations = 0
        answer_lower = answer.lower()
        
        for gt in ground_truth:
            belge = gt.get("belge_adi", "").lower()
            if belge and belge in answer_lower:
                found_citations += 1
                
        return found_citations / len(ground_truth) if len(ground_truth) > 0 else 0.0
