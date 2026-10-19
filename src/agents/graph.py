import sys
from pathlib import Path
from langgraph.graph import StateGraph, END

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.config import MAX_SEARCH_TURNS
from src.agents.state import AgenticRAGState
from src.agents.intent_agent import IntentAgent
from src.agents.analyzer_agent import AnalyzerAgent
from src.agents.answer_agent import AnswerAgent
from src.agents.validator_agent import ValidatorAgent
from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import BGEReranker

class AgenticRAGFlow:
    def __init__(self):
        print("Agentic RAG Araçları Yükleniyor...")
        self.retriever = HybridRetriever(rebuild_index=False)
        self.reranker = BGEReranker()
        
        self.intent_agent = IntentAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.answer_agent = AnswerAgent()
        self.validator_agent = ValidatorAgent()
        
        self.graph = self._build_graph()
        
    def _retrieve_docs(self, state: AgenticRAGState) -> AgenticRAGState:
        print(f"[2. Retriever Node] Alt sorgular için belgeler aranıyor...")
        
        all_raw_docs = []
        for sq in state["sub_queries"]:
            # Her alt sorgu için hibrit arama yap
            docs = self.retriever.search(query=sq)
            all_raw_docs.extend(docs)
            
        # Aynı belge farklı sorgulardan gelmiş olabilir, ID'ye göre tekilleştir
        unique_docs_dict = {doc["id"]: doc for doc in all_raw_docs}
        unique_docs_list = list(unique_docs_dict.values())
        
        # Tüm bulunan benzersiz belgeleri orijinal soruya göre yeniden sırala (Rerank)
        top_docs = self.reranker.rerank(query=state["original_query"], documents=unique_docs_list)
        
        # Eğer bu ikinci/üçüncü tursa, eski bulunanlarla yenileri birleştir
        existing_docs = {doc["id"]: doc for doc in state.get("retrieved_docs", [])}
        for doc in top_docs:
            existing_docs[doc["id"]] = doc
            
        state["retrieved_docs"] = list(existing_docs.values())
        state["search_count"] += 1
        return state
        
    def _check_evidence_loop(self, state: AgenticRAGState):
        """Analyzer Agent kararından sonra grafiğin nereye gideceğini belirleyen yönlendirici (Edge)."""
        if state["is_evidence_sufficient"] or state["search_count"] >= MAX_SEARCH_TURNS:
            return "answer"
        else:
            return "retrieve"

    def _build_graph(self):
        """LangGraph kullanarak ajanların çalışma sırasını ve döngüleri tanımlar."""
        workflow = StateGraph(AgenticRAGState)
        
        # Düğümleri (Ajanları) ekle
        workflow.add_node("intent", self.intent_agent.run)
        workflow.add_node("retrieve", self._retrieve_docs)
        workflow.add_node("analyzer", self.analyzer_agent.run)
        workflow.add_node("answer", self.answer_agent.run)
        workflow.add_node("validator", self.validator_agent.run)
        
        # Akışı (Kenarları) bağla
        workflow.set_entry_point("intent") # Giriş noktası
        workflow.add_edge("intent", "retrieve")
        workflow.add_edge("retrieve", "analyzer")
        
        # Koşullu Akış (Döngü Kararı)
        workflow.add_conditional_edges(
            "analyzer",
            self._check_evidence_loop,
            {
                "retrieve": "retrieve", # Yetersizse başa dön
                "answer": "answer"      # Yeterliyse cevaplamaya geç
            }
        )
        
        workflow.add_edge("answer", "validator")
        workflow.add_edge("validator", END) # Çıkış noktası
        
        return workflow.compile()
        
    def run(self, query: str, chat_history: list = None) -> dict:
        initial_state = AgenticRAGState(
            original_query=query,
            chat_history=chat_history or [],
            intent="",
            target_unit="",
            target_doc_type="",
            sub_queries=[],
            retrieved_docs=[],
            search_count=0,
            is_evidence_sufficient=False,
            missing_info="",
            draft_answer="",
            final_answer=""
        )
        
        print("\n" + "="*60)
        print(f"AGENTIC RAG SÜRECİ BAŞLATILDI")
        print(f"Soru: {query}")
        print("="*60)
        
        # Grafiği çalıştır
        result_state = self.graph.invoke(initial_state)
        return result_state

if __name__ == "__main__":
    # Test amaçlı
    flow = AgenticRAGFlow()
    soru = "Bilgisayar Mühendisliği öğrencisi olarak Erasmus staj hareketliliğinde en az kaç ortalama gerekiyor?"
    res = flow.run(soru)
    print("\n" + "="*60)
    print("SİSTEM CEVABI:")
    print("="*60)
    print(res["final_answer"])
