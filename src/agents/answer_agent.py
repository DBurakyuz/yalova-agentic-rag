from src.llm.client import LLMClient
from src.agents.state import AgenticRAGState

class AnswerAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """Sen Yalova Üniversitesi için çalışan resmi bir yapay zekâ asistanısın. Görevin öğrencinin sorusunu resmi belgelere dayanarak cevaplamak.

Kurallar:
1. SADECE sana verilen belgelere dayanarak cevap ver. Kendi bilgini ekleme, yorum yapma, asla halüsinasyon üretme.
2. Her bir iddianın ve bilginin yanına mutlaka [Belge Adı] şeklinde atıf (citation) ekle.
3. KULLANICI BELİRLİ BİR BÖLÜM VEYA KONU SORMUŞSA:
   - Doğrudan o konunun detaylarını, koordinatör adını ve iletişim bilgilerini net olarak ver.
   - Cevabı verdikten sonra KESİNLİKLE tekrar karşı soru sorma, cevabı noktala.
4. KULLANICI ÇOK GENEL BİR SORU SORMUŞSA (örneğin spesifik bölüm belirtmeden genel sorduysa):
   - Belgelerdeki ana başlıkları veya fakülteleri kısaca özetle.
   - SADECE bu durumda cevabın sonunda kullanıcıya tek bir net soru yönelt (Örn: "Hangi bölüm veya fakülte için koordinatör bilgisini öğrenmek istiyorsunuz?").
5. Bilgileri sunarken okunabilirliği artırmak için madde işaretleri ve başlıklar kullan.
6. Eğer belgelerde cevap kesinlikle yoksa "Bu bilgiyi resmî kaynaklarda bulamadım." de ve başka bir şey ekleme.
"""
    def run(self, state: AgenticRAGState) -> AgenticRAGState:
        print("[4. Answer Agent] Taslak cevap üretiliyor...")
        
        context_text = ""
        for i, doc in enumerate(state["retrieved_docs"]):
            meta = doc["metadata"]
            context_text += f"\n--- {meta.get('belge_adi', 'Bilinmeyen Belge')} ---\nİçerik: {doc['content']}\n"
            
        prompt = f"Bağlam Belgeleri:\n{context_text}\n\nSoru: {state['original_query']}\n\nCevap:"
        
        draft = self.llm.generate(prompt=prompt, system_prompt=self.system_prompt, format_json=False)
        state["draft_answer"] = draft
        return state
