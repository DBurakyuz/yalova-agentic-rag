import json
from src.llm.client import LLMClient
from src.agents.state import AgenticRAGState

class ValidatorAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """Sen bir Atıf (Citation) ve Halüsinasyon Doğrulama ajanısın.
Görevin, oluşturulan taslak cevabın kaynak belgelere %100 sadık kalıp kalmadığını denetlemektir.
Eğer taslak cevapta kaynak metinde olmayan uydurma bir sayı, tarih veya asılsız iddia varsa bunu reddet.
Not: Asistanın cevabın sonunda kullanıcıya sorduğu nazik açıklama/karşı sorular (Örn: 'Hangi bölüm için bilgi istiyorsunuz?') halüsinasyon değildir, onları koru.
Aşağıdaki formatta BİR JSON nesnesi döndür:
{
    "is_valid": true veya false (Eğer metinde kaynaklarda olmayan uydurma bir bilgi varsa false, her şey belgelerde veya kullanıcıya yöneltilen soru ise true),
    "corrected_answer": "Eğer is_valid false ise, uydurma kısımları silerek veya düzelterek cevabı yeniden yaz. True ise taslak cevabı aynen bırak."
}
"""
    def run(self, state: AgenticRAGState) -> AgenticRAGState:
        print("[5. Validator Agent] Atıflar ve halüsinasyon kontrol ediliyor...")
        
        context_text = ""
        for doc in state["retrieved_docs"]:
            meta = doc["metadata"]
            context_text += f"\n--- {meta.get('belge_adi', 'Bilinmeyen Belge')} ---\nİçerik: {doc['content']}\n"
            
        prompt = f"Soru: {state['original_query']}\n\nKaynak Belgeler:\n{context_text}\n\nTaslak Cevap:\n{state['draft_answer']}"
        
        response = self.llm.generate(prompt=prompt, system_prompt=self.system_prompt, format_json=True)
        
        try:
            response = response.strip().strip("```json").strip("```").strip()
            parsed = json.loads(response)
            
            is_valid = parsed.get("is_valid", True)
            if not is_valid:
                print("    -> UYARI: Taslak cevapta uydurma/desteksiz bilgi tespit edildi! Düzeltiliyor...")
                state["final_answer"] = parsed.get("corrected_answer", state["draft_answer"])
            else:
                print("    -> Doğrulama başarılı. Halüsinasyon yok.")
                state["final_answer"] = state["draft_answer"]
                
        except Exception as e:
            print(f"[HATA - Validator Agent] JSON hatası: {e}. Orijinal cevap dönülüyor.")
            state["final_answer"] = state["draft_answer"]
            
        return state
