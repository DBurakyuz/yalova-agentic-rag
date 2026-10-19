from pydantic import BaseModel, Field
from typing import Optional

class DocumentMetadata(BaseModel):
    kaynak_url: str
    belge_adi: str
    belge_turu: str = Field(description="Örn: Yonetmelik, Yonerge, Duyuru, Takvim")
    birim: str = Field(description="Örn: Ogrenci Isleri, Erasmus Ofisi, Bilgisayar Muhendisligi")
    
    # Bu alanlar Aşama 3'te (Ayrıştırma/Parser) doldurulacak
    madde_no: Optional[str] = None
    sayfa_no: Optional[int] = None
    
    akademik_yil: Optional[str] = None
    indirme_tarihi: str
    hash_degeri: Optional[str] = Field(None, description="Haftalık güncellemede değişimi tespit için MD5/SHA256")
