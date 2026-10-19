import fitz  # PyMuPDF kütüphanesi
import pytesseract
from PIL import Image
import io
import re

class PDFParser:
    def __init__(self):
        # Tesseract'ın Windows üzerinde kurulu olduğu yolu buraya belirtebilirsiniz.
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def parse(self, pdf_path: str) -> list[dict]:
        """
        Verilen PDF'i sayfa sayfa okur.
        Dönüş: [{"page_no": 1, "text": "sayfa içeriği"}, ...]
        """
        pages = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # Standart metin çıkarma
                text = page.get_text("text").strip()
                
                # Eğer sayfa boş veya metin çıkarılamayacak kadar azsa (taranmış belge şüphesi)
                if len(text) < 50:
                    text = self._ocr_page(page)
                    
                # Temizleme: Çoklu satır sonları ve boşlukları tek boşluğa çevir
                text = re.sub(r'\s+', ' ', text).strip()
                
                if text:
                    pages.append({
                        "page_no": page_num + 1, 
                        "text": text
                    })
            doc.close()
        except Exception as e:
            print(f"[HATA - PDF Parser] Dosya: {pdf_path} | Hata: {e}")
            
        return pages

    def _ocr_page(self, page) -> str:
        """
        Eğer PDF metin katmanı içermiyorsa (resim formatındaysa), 
        PyMuPDF ile sayfayı resme çevirip Tesseract (OCR) ile okur.
        """
        text = ""
        # Görüntü kalitesini artırmak için matris büyütme (zoom)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) 
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        try:
            # Yalova Üniversitesi belgeleri ağırlıklı Türkçe olduğu için 'tur' dili seçili
            text = pytesseract.image_to_string(image, lang='tur')
        except Exception as e:
            print(f"[HATA - OCR] Tesseract kurulu olmayabilir: {e}")
        return text
