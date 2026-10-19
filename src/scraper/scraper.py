"""
Yalova Üniversitesi Web Scraper ve PDF İndirici Modülü
- Saniyede 1 istek kuralına uyar.
- robots.txt kontrolü yapar.
- Kişisel verileri basit regex kurallarıyla ayıklar (varsa belgeyi reddeder).
- İndirilen dosyaları (HTML metin ve PDF) ve JSON formatındaki metadatalarını kaydeder.
"""
import os
import time
import json
import hashlib
import re
from datetime import datetime
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
import trafilatura

# Proje içi içe aktarmalar
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.config import RAW_DATA_DIR, SCRAPE_DELAY_SECONDS
from src.scraper.metadata_schema import DocumentMetadata
from src.scraper.source_urls import SOURCES

# Basit kişisel veri (PII) tespit kuralları (Email ve Telefon)
PII_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",  # Email
    r"\b05\d{9}\b"  # Cep telefonu
]

class YalovaScraper:
    def __init__(self):
        self.raw_dir = RAW_DATA_DIR
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.robot_parsers = {}
        self.session = requests.Session()
        # Üniversite sunucularına saygılı bir bot adı
        self.session.headers.update({"User-Agent": "YalovaUni-AgenticRAG-Bot/1.0"})
        
    def check_robots_txt(self, url: str) -> bool:
        """Sitenin robots.txt dosyasına göre bu URL'ye izin verilip verilmediğini kontrol eder."""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_url not in self.robot_parsers:
            rp = RobotFileParser()
            rp.set_url(urljoin(base_url, "robots.txt"))
            try:
                rp.read()
                self.robot_parsers[base_url] = rp
            except:
                self.robot_parsers[base_url] = None # Eğer okunamazsa varsayılan olarak izin ver
                
        rp = self.robot_parsers.get(base_url)
        if rp:
            return rp.can_fetch(self.session.headers["User-Agent"], url)
        return True

    def calculate_hash(self, content: bytes) -> str:
        """Haftalık güncellemelerde dosyanın değişip değişmediğini kontrol etmek için MD5."""
        return hashlib.md5(content).hexdigest()

    def contains_pii(self, text: str) -> bool:
        """Metin içinde kişisel veri (öğrenci listesi, telefon vs.) varsa True döner."""
        for pattern in PII_PATTERNS:
            # Çok sayıda eşleşme varsa bu büyük ihtimalle bir listedir
            if len(re.findall(pattern, text)) > 3:
                return True
        return False

    def save_metadata(self, metadata: DocumentMetadata, content_hash: str, safe_name: str):
        """Pydantic modelini JSON olarak raw klasörüne kaydeder."""
        meta_path = self.raw_dir / f"{safe_name}_{content_hash[:8]}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(metadata.model_dump_json(indent=4))

    def download_pdf(self, url: str, metadata: DocumentMetadata):
        """Belirtilen URL'den PDF indirir ve kaydeder."""
        if not self.check_robots_txt(url):
            print(f"[ATLANDI - Robots.txt] {url}")
            return
            
        time.sleep(SCRAPE_DELAY_SECONDS) # Saniye kısıtlaması
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            content_hash = self.calculate_hash(response.content)
            metadata.hash_degeri = content_hash
            
            safe_name = "".join([c if c.isalnum() else "_" for c in metadata.belge_adi])
            file_path = self.raw_dir / f"{safe_name}_{content_hash[:8]}.pdf"
            
            # Sadece yeni ise kaydet (Hash kontrolü simülasyonu)
            if not file_path.exists():
                with open(file_path, "wb") as f:
                    f.write(response.content)
                self.save_metadata(metadata, content_hash, safe_name)
                print(f"[BAŞARILI - PDF] İndirildi: {file_path.name}")
            else:
                print(f"[ATLANDI - Güncel] {file_path.name}")
                
        except Exception as e:
            print(f"[HATA - PDF] {url} : {e}")

    def scrape_html(self, url: str, metadata: DocumentMetadata):
        """Web sayfasındaki metni okur ve temizleyerek kaydeder."""
        if not self.check_robots_txt(url):
            print(f"[ATLANDI - Robots.txt] {url}")
            return
            
        time.sleep(SCRAPE_DELAY_SECONDS)
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                print(f"[HATA - HTML] Sayfa çekilemedi: {url}")
                return
            
            text = trafilatura.extract(downloaded)
            if not text:
                return
                
            if self.contains_pii(text):
                print(f"[ATLANDI - PII] Kişisel veri içeriyor: {url}")
                return

            content_hash = self.calculate_hash(text.encode('utf-8'))
            metadata.hash_degeri = content_hash
            
            safe_name = "".join([c if c.isalnum() else "_" for c in metadata.belge_adi])
            file_path = self.raw_dir / f"{safe_name}_{content_hash[:8]}.txt"
            
            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                self.save_metadata(metadata, content_hash, safe_name)
                print(f"[BAŞARILI - HTML] Kaydedildi: {file_path.name}")
            else:
                print(f"[ATLANDI - Güncel] {file_path.name}")
            
        except Exception as e:
            print(f"[HATA - HTML] {url} : {e}")

    def scrape_html_links_for_pdf(self, url: str, metadata: DocumentMetadata):
        """Bir web sayfasındaki PDF linklerini bulup indirmeyi tetikler."""
        if not self.check_robots_txt(url):
            return
        
        time.sleep(SCRAPE_DELAY_SECONDS)
        try:
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                if href.lower().endswith('.pdf'):
                    full_url = urljoin(url, href)
                    # Alt belge için isim bulalım
                    pdf_name = link.text.strip() or href.split('/')[-1]
                    pdf_metadata = metadata.model_copy()
                    pdf_metadata.belge_adi = pdf_name
                    pdf_metadata.kaynak_url = full_url
                    self.download_pdf(full_url, pdf_metadata)
                    
        except Exception as e:
            print(f"[HATA - PDF Link Arama] {url} : {e}")

    def run(self):
        print("Veri toplama işlemi başlatılıyor...")
        for source in SOURCES:
            # Temel metadata objesi
            base_metadata = DocumentMetadata(
                kaynak_url=source["url"],
                belge_adi=source["url"].split("/")[-1] or source["belge_turu"],
                belge_turu=source["belge_turu"],
                birim=source["birim"],
                indirme_tarihi=datetime.now().isoformat()
            )
            
            if source["scrape_type"] == "html":
                self.scrape_html(source["url"], base_metadata)
            elif source["scrape_type"] == "html_links_to_pdf":
                self.scrape_html_links_for_pdf(source["url"], base_metadata)
                
        print("Veri toplama tamamlandı.")

if __name__ == "__main__":
    scraper = YalovaScraper()
    scraper.run()
