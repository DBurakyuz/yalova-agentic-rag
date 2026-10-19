"""
Aşama 3: Veri İşleme Boru Hattı (Pipeline)
raw/ klasöründeki ham HTML metinlerini ve PDF'leri alır, temizler,
içerik türüne göre (madde bazlı veya standart) parçalar ve 
metadata bilgisiyle birlikte processed/ klasörüne JSON olarak kaydeder.
"""

import os
import json
import glob
from pathlib import Path
import sys

# Kök dizinden içe aktarabilmek için path ekleme
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from src.parser.text_splitter import CustomTextSplitter
from src.parser.pdf_parser import PDFParser

class ParserPipeline:
    def __init__(self):
        self.raw_dir = RAW_DATA_DIR
        self.processed_dir = PROCESSED_DATA_DIR
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        self.splitter = CustomTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.pdf_parser = PDFParser()
        
    def process_all(self):
        print("Veri temizleme ve parçalama boru hattı başlatıldı...")
        all_chunks = []
        
        # raw klasöründeki meta dosyaları üzerinden ilerle
        meta_files = glob.glob(str(self.raw_dir / "*.json"))
        print(f"İşlenecek metadata sayısı: {len(meta_files)}")
        
        for meta_file in meta_files:
            with open(meta_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                
            # json dosyasının isminden asıl metin/pdf ismine ulaş
            base_name = os.path.splitext(os.path.basename(meta_file))[0]
            
            txt_path = self.raw_dir / f"{base_name}.txt"
            pdf_path = self.raw_dir / f"{base_name}.pdf"
            
            document_chunks = []
            
            # Eğer dosya PDF ise
            if pdf_path.exists():
                print(f"İşleniyor (PDF): {pdf_path.name}")
                pages = self.pdf_parser.parse(str(pdf_path))
                for page in pages:
                    chunks = self.splitter.split_text(page["text"], metadata.get("belge_turu", ""))
                    for c in chunks:
                        chunk_meta = metadata.copy()
                        chunk_meta["sayfa_no"] = page["page_no"]
                        chunk_meta["madde_no"] = c["madde_no"]
                        document_chunks.append({
                            "content": c["text"],
                            "metadata": chunk_meta
                        })
                        
            # Eğer dosya HTML/Text ise
            elif txt_path.exists():
                print(f"İşleniyor (TXT): {txt_path.name}")
                with open(txt_path, "r", encoding="utf-8") as f:
                    text = f.read()
                chunks = self.splitter.split_text(text, metadata.get("belge_turu", ""))
                for c in chunks:
                    chunk_meta = metadata.copy()
                    chunk_meta["sayfa_no"] = 1 # Web sayfası genelde tek sayfa kabul edilir
                    chunk_meta["madde_no"] = c["madde_no"]
                    document_chunks.append({
                        "content": c["text"],
                        "metadata": chunk_meta
                    })
            else:
                print(f"[UYARI] {base_name} için ne PDF ne de TXT bulunabildi.")
                
            all_chunks.extend(document_chunks)
            
        # Oluşturulan tüm chunk'ları tek bir dosyada (vector DB için) kaydet
        output_file = self.processed_dir / "all_chunks.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=4)
            
        print(f"Toplam {len(all_chunks)} parça (chunk) oluşturuldu.")
        print(f"Başarıyla kaydedildi: {output_file}")

if __name__ == "__main__":
    pipeline = ParserPipeline()
    pipeline.process_all()
