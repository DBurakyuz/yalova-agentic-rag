import sys
from pathlib import Path

# Proje kök dizinini tanıt
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.retriever.hybrid_retriever import HybridRetriever

if __name__ == "__main__":
    print("Vektör veritabanı (ChromaDB) ve BM25 indeksi oluşturuluyor...")
    # rebuild_index=True diyerek sıfırdan vektörleri hesaplatıyoruz.
    retriever = HybridRetriever(rebuild_index=True)
    print("İşlem tamamlandı! Artık arayüzü başlatabilirsiniz.")
