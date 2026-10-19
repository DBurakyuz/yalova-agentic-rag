import json
from src.llm.client import LLMClient
from src.agents.state import AgenticRAGState

class IntentAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """Sen Yalova Üniversitesi asistanının Niyet Analiz (Intent) ve Bağlam ajanısın.
Görevin:
1. Varsa önceki konuşma geçmişini (Sohbet Geçmişi) ve kullanıcının son sorusunu analiz et.
2. Eğer kullanıcı eksik veya kısa bir takip sorusu sorduysa (Örn: "Bilgisayar", "Peki ya ortalama?", "Kimdir?", "Şartları neler?"):
   - Konuşma geçmişindeki bağlamı kullanarak soruyu tek başına anlaşılır tam bir araştırma konusuna dönüştür (Örn: Az önce koordinatör konuşulduysa ve kullanıcı "Bilgisayar Mühendisliği" dediyse -> "Bilgisayar Mühendisliği Erasmus Bölüm Koordinatörü kimdir?").
3. Şu bilgileri içeren BİR JSON nesnesi döndür:
{
    "intent": "Sorunun ana amacı",
    "target_unit": "İlgili birim (ör. Erasmus Koordinatörlüğü, Öğrenci İşleri, Bilinmiyor)",
    "target_doc_type": "İlgili belge türü (ör. Yönetmelik, İletişim/Liste, Takvim, Bilinmiyor)",
    "sub_queries": ["Vektör veritabanında aramak için ürettiğin 2-3 adet net ve detaylı alt arama sorgusu listesi"]
}

SADECE GEÇERLİ JSON DÖNDÜR, BAŞKA METİN YAZMA.
"""
    def run(self, state: AgenticRAGState) -> AgenticRAGState:
        print("[1. Intent Agent] Soru ve konuşma geçmişi analiz ediliyor...")
        
        history_str = ""
        chat_hist = state.get("chat_history") or []
        if chat_hist:
            history_lines = []
            for msg in chat_hist[-4:]: # Son 2-4 mesaj
                role = "Kullanıcı" if msg.get("role") == "user" else "Asistan"
                content = msg.get("content", "")
                if content:
                    history_lines.append(f"{role}: {content[:200]}")
            history_str = "Sohbet Geçmişi:\n" + "\n".join(history_lines) + "\n\n"
            
        prompt = f"{history_str}Kullanıcının Son Sorusu: {state['original_query']}"
        
        response = self.llm.generate(prompt=prompt, system_prompt=self.system_prompt, format_json=True)
        
        try:
            response = response.strip().strip("```json").strip("```").strip()
            parsed = json.loads(response)
            
            state["intent"] = parsed.get("intent", "Genel")
            state["target_unit"] = parsed.get("target_unit", "Bilinmiyor")
            state["target_doc_type"] = parsed.get("target_doc_type", "Bilinmiyor")
            state["sub_queries"] = parsed.get("sub_queries", [state["original_query"]])
            print(f"    -> Üretilen Sorgular: {state['sub_queries']}")
            
        except Exception as e:
            print(f"[HATA - Intent Agent] JSON parse hatası: {e}. Standart soru ile devam ediliyor.")
            state["sub_queries"] = [state["original_query"]]
            state["target_unit"] = "Bilinmiyor"
            
        return state
