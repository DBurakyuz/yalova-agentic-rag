"""
config.py

Bu dosya projenin yapılandırma ayarlarını içerir: Dosya yolları, model isimleri, 
hiperparametreler ve web scraping ayarları buradan yönetilir.
"""
import os
from pathlib import Path

# ==========================================
# 1. DOSYA YOLLARI
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Veri klasörleri
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

# ==========================================
# 2. MODEL AYARLARI
# ==========================================
# Embedding ve Reranker Modelleri (HuggingFace tabanlı)
EMBEDDING_MODEL = "BAAI/bge-m3"
RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"

# ==========================================
# 3. LLM (DİL MODELİ) AYARLARI
# ==========================================
# Yerel çalışacak model (Örn: Qwen3 8B veya Llama 3.1 8B)
LLM_PROVIDER = "ollama"  
OLLAMA_MODEL_NAME = "llama3.1:8b" # Doğrulanmalı: Sisteminizde kurulu sürüme göre güncelleyin.
API_MODEL_NAME = "gpt-4o-mini"    # Karşılaştırma deneyi için API tabanlı model.

# Agent çıktılarını formatlamak ve sabit tutmak için düşük sıcaklık
LLM_TEMPERATURE = 0.0

# ==========================================
# 4. PARÇALAMA VE RETRIEVER AYARLARI
# ==========================================
CHUNK_SIZE = 600       # Token veya karakter sayısı (400-800 arası ideal)
CHUNK_OVERLAP = 75     # %10-15 örtüşme

RETRIEVER_TOP_K = 20   # Hibrit aramadan (BM25 + Vektör) dönecek ilk belge sayısı
RERANKER_TOP_K = 5     # BGE-Reranker sonrası ajanların okuyacağı nihai belge sayısı
MAX_SEARCH_TURNS = 3   # Document Analyzer'ın eksik bilgi tespiti sonrası yapabileceği max arama sayısı

# ==========================================
# 5. VERİ TOPLAMA (SCRAPER) AYARLARI
# ==========================================
SCRAPE_DELAY_SECONDS = 1.0  # Sunucuyu yormamak için her istek arası bekleme
MAX_WORKERS = 4             # Paralel indirme sayısı
