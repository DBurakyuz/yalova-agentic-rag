# 🛡️ BİTİRME PROJESİ VE TÜBİTAK 2209-A TAM YEDEKLEME VE DURUM REHBERİ
**Tarih:** 30 Ekim 2026  
**Proje Adı:** Yalova Üniversitesi için Agentic RAG Tabanlı Kurumsal Bilgi Asistanı  
**Proje Yürütücüsü:** Dursun Burak Yüz  
**GitHub Deposu:** https://github.com/DBurakyuz/yalova-agentic-rag (Branch: `main`)

---

## 1. YEDEKLEME DURUMU (NEREDE NE VAR?)

Bilgisayar tamire/formata gitse dahi hiçbir çalışmanızın kaybolmaması için çift katmanlı tam yedekleme yapılmıştır:

### A) Bulut Yedeği (GitHub - Uzak Depo)
* **Adres:** `https://github.com/DBurakyuz/yalova-agentic-rag`
* **Durum:** Son commit `main` dalına başarıyla push edilmiştir (`git push origin main`).
* **İçerik:** Tüm kaynak kodlar (`src/`), TÜBİTAK başvuru metinleri (`TUBITAK_2209A_Basvuru_Metinleri.md`), Dockerfile, requirements.txt, ayar dosyaları.

### B) Fiziksel Çevrimdışı Tam Zip Yedeği (17.73 MB)
* **Dosya Adı:** `Bitirme_Projesi_TAM_YEDEK.zip`
* **Konum 1 (Masaüstü):** `C:\Users\Dursun Burak\Desktop\Bitirme_Projesi_TAM_YEDEK.zip`
* **Konum 2 (Proje Dizini):** `C:\Bitirme_Projesi\Bitirme_Projesi_TAM_YEDEK.zip`
* **İçerik:** 
  - Tüm Python kodları (`src/agents/`, `src/retriever/`, `src/parser/`, `src/scraper/`, `src/llm/`, `src/evaluation/`, `src/app.py`)
  - Ham veriler ve taranan PDF'ler (`data/raw/`)
  - 340 adet işlenmiş ve etiketlenmiş mevzuat parçası (`data/processed/all_chunks.json`)
  - Önceden oluşturulmuş ChromaDB Vektör Veritabanı ve SQLite indeksi (`data/vector_db/`)
  - TÜBİTAK 2209-A Başvuru Formu tam metinleri (`TUBITAK_2209A_Basvuru_Metinleri.md`)
  - Docker ve ortam yapılandırmaları

> ⚠️ **ÇOK ÖNEMLİ TAVSİYE:** Bilgisayarı teknik servise teslim etmeden önce masaüstündeki `Bitirme_Projesi_TAM_YEDEK.zip` dosyasını:
> 1. Bir **USB Flash Belleğe** kopyalayınız, veya
> 2. **Google Drive / OneDrive / iCloud** hesabınıza yükleyiniz, veya
> 3. Kendinize **e-posta eki** olarak gönderiniz.

---

## 2. ŞU ANA KADAR TAMAMLANAN TÜM ÇALIŞMALAR

1. **Veri Toplama (Scraper):**
   - Yalova Üniversitesi Erasmus Koordinatörlüğü ve Öğrenci İşleri portallarından yönetmelikler, akademik takvim, yönergeler ve 63 bölüm koordinatörünün yer aldığı JavaScript dinamik listeleri başarıyla çekildi (`src/scraper/`).
2. **Doküman Ayrıştırma ve OCR (Parser):**
   - Vektörel ve taranmış (resim) PDF'ler için PyMuPDF + Tesseract OCR (Türkçe `tur` paketi) entegre edildi.
   - Türk mevzuat yapısına uygun kural tabanlı regex bölücü ile dokümanlar madde/fıkra bütünlüğü korunarak 340 blok halinde yapılandırıldı (`src/parser/`).
3. **Hibrit İndeksleme ve Arama (Retriever):**
   - BAAI/bge-m3 çok dilli yoğun vektörleri + BM25Okapi anahtar kelime indeksi kuruldu.
   - RRF (Reciprocal Rank Fusion) ve BGE-Reranker-v2-m3 Cross-Encoder yeniden sıralama katmanı entegre edildi (`src/retriever/`).
4. **Çok Ajanlı Karar Çizgesi (LangGraph Multi-Agent):**
   - `Intent Agent`: Eksik ve takip sorularını geçmişe göre yeniden yazan niyet ajanı.
   - `Analyzer Agent`: Kanıt yeterliliğini denetleyen döngüsel düzeltici RAG (CRAG) ajanı.
   - `Answer Agent`: Resmi madde ve kaynak atıflı yanıt üreten ajan.
   - `Validator Agent`: Halüsinasyonu engelleyen, kaynakla yanıtı karşılaştıran denetçi ajan (`src/agents/`).
5. **Kullanıcı Arayüzü ve Konteyner:**
   - Çok turlu hafızayı destekleyen Streamlit web arayüzü tamamlandı (`src/app.py`).
   - Platformdan bağımsız tek tıkla kurulum için Dockerfile ve `.dockerignore` hazırlandı.
6. **TÜBİTAK 2209-A Başvuru Dosyası:**
   - Başlık, Özet, 1. Gerekçe (Önem, Bilimsel Nitelik, SMART Amaç/Hedefler), 2. Yöntem (RAGAS, Shapiro-Wilk, Wilcoxon), 3. Proje Yönetimi (Takvim, Riskler, Olanaklar), 4. Yaygın Etki ve 12.000 TL Bütçe planı eksiksiz tamamlandı (`TUBITAK_2209A_Basvuru_Metinleri.md`).

---

## 3. BİLGİSAYAR TAMİRDEN DÖNDÜĞÜNDE SİSTEMİ GERİ YÜKLEME ADIMLARI

Bilgisayarınız sıfırlanmış veya yeni bir bilgisayara geçmiş olsanız bile projeyi 3 adımda çalıştırabilirsiniz:

### Adım 1: Depoyu İndirin (Veya Zip'i Açın)
```powershell
git clone https://github.com/DBurakyuz/yalova-agentic-rag.git C:\Bitirme_Projesi
cd C:\Bitirme_Projesi
```
*(Eğer zip dosyasını kullandıysanız, zip'i `C:\Bitirme_Projesi` klasörüne çıkartmanız yeterlidir).*

### Adım 2: Python Sanal Ortamını Kurun
```powershell
python -m venv src/venv
.\src\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Adım 3: Ollama'yı Başlatın ve Arayüzü Açın
1. [Ollama.com](https://ollama.com)'dan Ollama'yı kurup terminalde modeli çekin:
   ```powershell
   ollama run llama3.1:8b
   ```
2. Web arayüzünü başlatın:
   ```powershell
   streamlit run src/app.py
   ```
Tarayıcınızda `http://localhost:8501` adresinde sisteminiz kaldığı yerden canlı olarak çalışacaktır!
