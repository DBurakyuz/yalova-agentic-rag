import re
from typing import List, Dict, Any

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

class CustomTextSplitter:
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Standart metinler için Langchain'in karakter tabanlı parçalayıcısı
        self.default_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def split_regulation(self, text: str) -> List[Dict[str, Any]]:
        """Yönetmelikleri (Mevzuat/Yönerge) 'Madde X:' yapısına göre böler."""
        chunks = []
        # 'Madde 1 -', 'Madde 1-', 'MADDE 1' gibi kalıpları yakalayan Regex
        pattern = re.compile(r'(?i)\b(madde\s+\d+[\s\-\.:])')
        
        parts = pattern.split(text)
        
        if len(parts) == 1:
            # Belgede 'Madde' kelimesi geçmiyorsa standart bölücü kullan
            return [{"text": c, "madde_no": None} for c in self.default_splitter.split_text(text)]

        # parts listesi: [ "Başlangıç metni", "Madde 1 -", "İçerik", "Madde 2 -", "İçerik" ]
        # İlk kısmı (amaç, kapsam vb.) ekle
        if parts[0].strip():
            for c in self.default_splitter.split_text(parts[0]):
                chunks.append({"text": c, "madde_no": "Genel"})
                
        for i in range(1, len(parts), 2):
            madde_basligi = parts[i].strip()
            madde_icerigi = parts[i+1].strip() if i+1 < len(parts) else ""
            
            # Başlıktan sadece numarayı çıkar
            num_match = re.search(r'\d+', madde_basligi)
            madde_no = num_match.group() if num_match else "Bilinmiyor"
            
            tam_metin = f"{madde_basligi} {madde_icerigi}"
            
            # Eğer madde kendi başına limitleri aşıyorsa (çok uzunsa), içten böl
            if len(tam_metin) > self.chunk_size:
                sub_chunks = self.default_splitter.split_text(tam_metin)
                for sc in sub_chunks:
                    chunks.append({"text": sc, "madde_no": madde_no})
            else:
                chunks.append({"text": tam_metin, "madde_no": madde_no})
                
        return chunks

    def split_text(self, text: str, document_type: str) -> List[Dict[str, Any]]:
        """Belgenin türüne bakarak uygun parçalama stratejisini seçer."""
        type_lower = document_type.lower() if document_type else ""
        if any(keyword in type_lower for keyword in ["yönetmelik", "yonetmelik", "mevzuat", "yönerge", "yonerge"]):
            return self.split_regulation(text)
        else:
            return [{"text": c, "madde_no": None} for c in self.default_splitter.split_text(text)]
