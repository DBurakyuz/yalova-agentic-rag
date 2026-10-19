# Yalova Üniversitesi için Agentic RAG Tabanlı Bilgi Asistanı

Bu proje, Yalova Üniversitesi'nin kamuya açık belgelerini (yönetmelikler, akademik takvim, Erasmus yönergeleri vb.) kullanarak öğrencilerin sorularına doğru ve kaynak göstererek cevap veren Agentic RAG tabanlı bir yapay zekâ asistanıdır.

## Klasör Yapısı

```text
c:\Bitirme_Projesi\
│
├── data/                 # Veri Deposu (Otomatik oluşturulacak)
│   ├── raw/              # İndirilen PDF'ler, HTML sayfaları
│   ├── processed/        # Temizlenmiş ve parçalanmış veriler (JSON)
│   └── vector_db/        # ChromaDB indeks dosyaları
│
├── src/                  # Ana Kaynak Kodları
│   ├── scraper/          # Web scraping ve PDF indirme
│   ├── parser/           # Metin temizleme, parçalama (chunking)
│   ├── retriever/        # BM25, Vektör arama, BGE-m3 embedding ve Reranker
│   ├── agents/           # LangGraph ajanları (Intent, Analyzer, Answer, Validator)
│   ├── evaluation/       # Değerlendirme ve test kodları (RAGAS vb.)
│   ├── config.py         # Konfigürasyon ve hiperparametre ayarları
│   └── main.py           # Akışı çalıştıran ana dosya
│
├── tests/                # Birim ve entegrasyon testleri
├── .env.example          # Ortam değişkenleri şablonu
├── requirements.txt      # Gerekli Python kütüphaneleri listesi
└── README.md             # Kurulum ve çalıştırma talimatları
```

## Kurulum Talimatları

Proje Windows ortamında (Python 3.11+) çalışacak şekilde tasarlanmıştır.

### 1. Python Ortamını Kurma ve Aktif Etme

Projeyi bağımsız bir ortamda çalıştırmak için sanal ortam (virtual environment) oluşturun:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Gerekli Kütüphaneleri Yükleme

Proje bağımlılıklarını `requirements.txt` üzerinden yükleyin:
```powershell
pip install -r requirements.txt
```

*(Dinamik sayfaları çekmek için Playwright tarayıcılarını da indirmeniz gerekecektir:)*
```powershell
playwright install
```

### 3. Yerel LLM Kurulumu (Ollama)

Sisteminizde yerel olarak Llama 3.1 veya Qwen3 modellerini çalıştırmak için [Ollama](https://ollama.com/download) kurmanız gerekmektedir. Ollama kurulduktan sonra terminalden modeli indirin:
```powershell
ollama run llama3.1:8b
# veya
ollama run qwen2.5:8b
```

### 4. Çevresel Değişkenleri Ayarlama

`.env.example` dosyasının bir kopyasını oluşturarak adını `.env` yapın. Eğer karşılaştırma deneylerinde OpenAI API vb. kullanacaksanız, anahtarlarınızı bu dosyaya ekleyebilirsiniz.
