"""
Yalova Üniversitesi için kazınacak kaynakların listesi.
Her kaynak için URL, belge türü ve birim bilgisi tanımlanır.
Bu liste manuel olarak veya başka bir tarayıcı script ile genişletilebilir.
"""

SOURCES = [
    {
        "url": "https://oidb.yalova.edu.tr/tr/Page/Icerik/ogrenci-isleri-mevzuat",
        "belge_turu": "Mevzuat",
        "birim": "Öğrenci İşleri",
        "scrape_type": "html_links_to_pdf" # Sayfadaki PDF uzantılı linkleri bulup indirecek
    },
    {
        "url": "https://yalova.edu.tr/tr/Page/Icerik/akademik-takvim",
        "belge_turu": "Takvim",
        "birim": "Rektörlük",
        "scrape_type": "html"
    },
    # ==========================================
    # Erasmus Ofisi Linkleri
    # ==========================================
    {
        "url": "https://erasmus.yalova.edu.tr/tr/Icerik/Detay/erasmus-nedir",
        "belge_turu": "Genel Bilgi",
        "birim": "Erasmus Koordinatörlüğü",
        "scrape_type": "html" 
    },
    {
        "url": "https://erasmus.yalova.edu.tr/tr/Icerik/Detay/hakkimizda",
        "belge_turu": "Genel Bilgi",
        "birim": "Erasmus Koordinatörlüğü",
        "scrape_type": "html" 
    },
    {
        "url": "https://erasmus.yalova.edu.tr/tr/Icerik/Detay/uluslararasi-anlasmalarimiz",
        "belge_turu": "Kılavuz/Liste",
        "birim": "Erasmus Koordinatörlüğü",
        "scrape_type": "html" 
    },
    {
        "url": "https://erasmus.yalova.edu.tr/tr/Icerik/Detay/hibe-hesaplama-simulatoru-ogrenci",
        "belge_turu": "Kılavuz",
        "birim": "Erasmus Koordinatörlüğü",
        "scrape_type": "html" 
    },
    {
        "url": "https://erasmus.yalova.edu.tr/tr/Icerik/Detay/erasmus-bolum-koordinatorleri",
        "belge_turu": "İletişim/Liste",
        "birim": "Erasmus Koordinatörlüğü",
        "scrape_type": "html" 
    }
]
