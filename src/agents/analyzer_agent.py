import json
from src.llm.client import LLMClient
from src.agents.state import AgenticRAGState

class AnalyzerAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """Sen Belge Analiz (Analyzer) ajanısın.
Görevin: Kullanıcının sorusunu %100 doğrulukla cevaplamak için verilen belgelerin (bağlamın) YETERLİ olup olmadığını kontrol etmektir.
Aşağıdaki formatta BİR JSON döndür, başka metin yazma:
{
    "is_sufficient": true veya false,
    "missing_info": "Eğer false ise, tam olarak hangi bilginin eksik olduğunu yaz. True ise boş bırak.",
    "new_sub_queries": ["Eksik bilgiyi bulmak için arama motoruna gönderilecek 1-2 YENİ arama sorgusu. Yeterliyse boş liste ver."]
}
"""
    def run(self, state: AgenticRAGState) -> AgenticRAGState:
        print(f"[3. Analyzer Agent] Kanıtlar inceleniyor... (Tur: {state['search_count']})")
        
        context_text = ""
        for i, doc in enumerate(state["retrieved_docs"]):
            meta = doc["metadata"]
            context_text += f"Belge {i+1}: {meta.get('belge_adi', '')} - Madde: {meta.get('madde_no', '')}\n{doc['content']}\n\n"
            
        prompt = f"Kullanıcı Sorusu: {state['original_query']}\n\nBulunan Belgeler:\n{context_text}"
        
        response = self.llm.generate(prompt=prompt, system_prompt=self.system_prompt, format_json=True)
        
        try:
            response = response.strip().strip("```json").strip("```").strip()
            parsed = json.loads(response)
            
            state["is_evidence_sufficient"] = parsed.get("is_sufficient", True)
            state["missing_info"] = parsed.get("missing_info", "")
            
            new_queries = parsed.get("new_sub_queries", [])
            if new_queries and not state["is_evidence_sufficient"]:
                print(f"    -> Kanıt Yetersiz! Eksik: {state['missing_info']}")
                print(f"    -> Yeni Sorgular Üretildi: {new_queries}")
                state["sub_queries"] = new_queries
            else:
                print("    -> Kanıtlar yeterli bulundu.")
                
        except Exception as e:
            print(f"[HATA - Analyzer Agent] JSON hatası: {e}. Kanıt yeterli varsayılıyor.")
            state["is_evidence_sufficient"] = True
            
        return state
