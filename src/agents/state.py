from typing import TypedDict, List, Dict, Any, Optional

class AgenticRAGState(TypedDict):
    """
    LangGraph'taki düğümler (Ajanlar) arasında dolaşan verinin durumu (state).
    Her ajan buradaki bilgileri okur veya günceller.
    """
    original_query: str          # Kullanıcının sorduğu orijinal soru
    chat_history: Optional[List[Dict[str, str]]] # Önceki konuşma geçmişi (Hafıza)
    intent: str                  # Intent Agent'ın bulduğu asıl niyet
    target_unit: str             # İlgili birim (örn: Erasmus Ofisi)
    target_doc_type: str         # Belge türü
    sub_queries: List[str]       # Üretilen alt sorgular (Arama motoruna gidecek)
    retrieved_docs: List[Dict[str, Any]] # Toplanan dokümanlar
    search_count: int            # Toplam arama döngüsü sayısı
    is_evidence_sufficient: bool # Kanıtlar yeterli mi? (Analyzer karar verir)
    missing_info: str            # Eğer kanıt yetersizse eksik olan şey nedir?
    draft_answer: str            # Answer Agent'ın oluşturduğu ilk cevap
    final_answer: str            # Validator Agent'ın onayından geçen son cevap
