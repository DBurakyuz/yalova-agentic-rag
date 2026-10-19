import streamlit as st
import time
import sys
from pathlib import Path

# Proje kök dizinini yola ekle
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.agents.graph import AgenticRAGFlow

# Sayfa Ayarları
st.set_page_config(
    page_title="Yalova Üniversitesi Bilgi Asistanı",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Yalova Üniversitesi RAG Asistanı")
st.markdown("Mevzuat, Erasmus süreçleri ve akademik takvim hakkında sorularınızı resmi kaynaklara dayanarak cevaplıyorum.")

# Agentic RAG sistemini başlat (Uygulama açıldığında bir kere yüklenir)
if "agent_flow" not in st.session_state:
    with st.spinner("Yapay Zeka Ajanları ve Vektör Veritabanı Yükleniyor... (Birkaç saniye sürebilir)"):
        # Not: İlk çalıştırmada ChromaDB ve BGE modelleri RAM'e yüklenir
        st.session_state.agent_flow = AgenticRAGFlow()
    st.success("Sistem Kullanıma Hazır!")

# Sohbet geçmişi belleği
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları ekrana çiz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Eğer bu bir asistan cevabıysa ve kaynağı varsa göster
        if "sources" in message and message["sources"]:
            with st.expander("📚 İncelenen Resmi Kaynaklar"):
                # Tekrar eden aynı belgeleri filtrele
                seen = set()
                for src in message["sources"]:
                    key = f"{src['belge_adi']}_{src['madde_no']}"
                    if key not in seen:
                        st.write(f"- **{src['belge_adi']}** (Madde: {src['madde_no']})")
                        if src.get('url'):
                            st.markdown(f"[Kaynağa Git]({src['url']})")
                        seen.add(key)

# Kullanıcı giriş alanı
if prompt := st.chat_input("Örn: Erasmus stajı için genel not ortalaması en az kaç olmalı?"):
    # Kullanıcı mesajını listeye ekle ve ekrana bas
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistanın düşünme ve cevap verme süreci
    with st.chat_message("assistant"):
        with st.spinner("Ajanlar belgeleri araştırıyor ve kanıtları doğruluyor..."):
            start_time = time.time()
            
            # Önceki konuşma geçmişini bağlam olarak hazırla (son 4 mesaj)
            chat_history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1][-4:]
                if m.get("content")
            ]
            
            # Arka planda LangGraph çalışır (Sohbet geçmişi ile birlikte)
            result = st.session_state.agent_flow.run(prompt, chat_history=chat_history)
            
            elapsed_time = time.time() - start_time
            answer = result["final_answer"]
            
            # Kullanılan belgelerin metadatalarını toparla
            sources = []
            for doc in result["retrieved_docs"]:
                meta = doc["metadata"]
                sources.append({
                    "belge_adi": meta.get("belge_adi", "Bilinmeyen Belge"),
                    "madde_no": meta.get("madde_no", ""),
                    "url": meta.get("kaynak_url", "")
                })
                
            # Cevabı yazdır
            st.markdown(answer)
            st.caption(f"⏱️ Yanıt Süresi: {elapsed_time:.1f} sn | 🔄 Arama Turu: {result.get('search_count', 1)}")
            
            # Kaynaklar sekmesini ekrana bas
            if sources:
                with st.expander("📚 İncelenen Resmi Kaynaklar"):
                    seen = set()
                    for src in sources:
                        key = f"{src['belge_adi']}_{src['madde_no']}"
                        if key not in seen:
                            st.write(f"- **{src['belge_adi']}** (Madde: {src['madde_no']})")
                            if src.get('url'):
                                st.markdown(f"[Kaynağa Git]({src['url']})")
                            seen.add(key)
                            
    # Asistan yanıtını geçmişe kaydet
    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer,
        "sources": sources
    })
