# TÜBİTAK 2209-A ÜNİVERSİTE ÖĞRENCİLERİ ARAŞTIRMA PROJELERİ DESTEKLEME PROGRAMI
## BAŞVURU FORMU METİNLERİ (GÜNCEL VE NİHAİ VERSİYON)

**Proje Yürütücüsü:** Dursun Burak Yüz  
**Kurum:** Yalova Üniversitesi, Mühendislik Fakültesi, Bilgisayar Mühendisliği Bölümü  
**Hedef Kitle / Kurum Odağı:** Yükseköğretim Kurulu (YÖK) Kurumları / Üniversiteler İdari ve Akademik Birimleri  

---

## GENEL BİLGİLER VE BAŞLIK

### Proje Başlığı
```text
Yükseköğretim Kurumları İdari Mevzuatında Bilgi Doğrulamalı ve Döngüsel Ajan Tabanlı Geri Getirme Destekli Üretim (Agentic RAG) Asistanı Geliştirilmesi
```

### Bilimsel ve Teknolojik Faaliyet Alanı
```text
Doğal Dil İşlemesi (Natural Language Processing)
```

### Anahtar Kelimeler
```text
Doğal Dil İşleme, Agentic RAG, Çoklu Ajan Sistemleri, Hibrit Arama, Bilgi Doğrulama
```

---

## BÜTÇE TALEBİ VE GEREKÇESİ

* **Makine-Teçhizat:** 0 TL
* **Sarf Malzemesi:** 1.000 TL *(Kırtasiye, teknik rapor baskıları ve veri depolama sarf giderleri)*
* **Hizmet Alımı:** 11.000 TL *(Ablasyon deneyleri, RAGAS değerlendirme testleri için LLM API kredileri ve GPU/Bulut sunucu kiralama hizmeti)*
* **Ulaşım:** 0 TL
* **TOPLAM TALEP EDİLEN BÜTÇE:** **12.000 TL**

---

## PROJE ÖZETİ (Max 450 Kelime)

```text
Büyük Dil Modelleri (LLM), kurumsal bilgi erişiminde güçlü kabiliyetler sunmasına rağmen, idari mevzuat gibi yüksek doğruluk gerektiren alanlarda "halüsinasyon" (gerçek dışı bilgi üretimi) ve güncel olmayan veri problemleriyle karşılaşmaktadır. Bu kısıtları aşmak üzere geliştirilen geleneksel (Naive) Geri Getirme Destekli Üretim (RAG) mimarileri, tek yönlü ve geri beslemesiz arama yapmaları sebebiyle yetersiz bağlam getirildiğinde hatalı yanıtlar üretmekte; ayrıca mevzuat metinlerini sabit karakter pencereleriyle bölerek kanun ve yönerge maddelerinin anlam bütünlüğünü parçalamaktadır.

Bu projenin temel amacı; yükseköğretim kurumlarının kamuya açık resmi mevzuat metinleri (yönetmelikler, yönergeler, akademik takvim ve değişim programı kılavuzları) üzerinde çalışan, halüsinasyonu en aza indirilmiş, otonom öz-düzeltme (self-correction) ve atıf doğrulama yeteneklerine sahip bir Agentic RAG (Ajan Tabanlı Geri Getirme Destekli Üretim) bilgi asistanı geliştirmektir.

Önerilen sistemde bu hedefe ulaşmak için dört aşamalı yenilikçi bir yöntem uygulanacaktır: (1) Türk idari mevzuat diline uygun olarak geliştirilen düzenli ifadeler (regex) ile metinler doğrudan "Madde" sınırlarından deterministik olarak parçalanacak; taranmış resmi PDF belgeleri optik karakter tanıma (OCR) katmanıyla metne dönüştürülecektir. (2) Bilgi getirme aşamasında, Türkçe dil yapısına uygun BAAI/bge-m3 çok dilli embedding modeli ile BM25Okapi anahtar kelime araması Reciprocal Rank Fusion (RRF) algoritmasıyla birleştirilecek; elde edilen sonuçlar BAAI/bge-reranker-v2-m3 Cross-Encoder modeliyle yeniden sıralanacaktır. (3) Çoklu ajan mimarisi (LangGraph) kapsamında; Niyet Ajanı (Intent Agent) konuşma geçmişini analiz ederek yarım kalan soruları bağlamsallaştıracak, Belge Analiz Ajanı (Document Analyzer) getirilen kanıtların yeterliliğini denetleyerek eksik bilgide azami 3 tura kadar otonom arama döngüsü başlatacaktır. (4) Cevap Ajanı (Answer Agent) her iddiaya resmi madde atfı ekleyecek, Atıf Doğrulayıcı Ajan (Citation Validator) ise üretilen metni kaynak belgelerle çapraz kontrol ederek desteksiz ifadeleri eleyecektir.

Geliştirilen sistem, üniversite mevzuatından derlenen 50 kolay ve 50 zor sorudan oluşan, elle etiketlenmiş 100 soruluk özgün bir test veri seti üzerinde Klasik RAG taban çizgisi ile deneysel olarak karşılaştırılacaktır. Bilgi getirme başarımı Recall@5, MRR ve nDCG metrikleriyle; cevap kalitesi ve sadakati ise RAGAS çerçevesi (Faithfulness, Answer Relevance) üzerinden istatistiksel anlamlılık testleri (Wilcoxon) ile doğrulanacaktır. Proje sonunda elde edilecek açık kaynaklı ajan mimarisi ve akademik bildiri çıktısı, yükseköğretimde idari iş gücünü hafifletecek ve öğrencilerin resmi mevzuata güvenilir erişimini sağlayacaktır.
```

---

## 1. GEREKÇE

### 1.1. Konunun Önemi ve Araştırma Önerisinin Bilimsel Niteliği
*(YÖK Kurumları ve Üniversiteler Odaklı Güncel Versiyon)*

```text
1. Yükseköğretim Kurumlarında Bilgi Erişimi Problemi ve Konunun Önemi:  
Yükseköğretim Kurulu’na (YÖK) bağlı üniversitelerde eğitim-öğretim ve idari süreçler; yüzlerce sayfalık lisans/önlisans yönetmelikleri, sınav ve intibak yönergeleri, Erasmus ve değişim programı kuralları, burs/barınma esasları ve sürekli güncellenen akademik takvimlerle yönetilmektedir. Üniversitelerin bu çok birimli ve karmaşık mevzuat yapısı içinde öğrencilerin ve araştırmacıların doğru bilgiye zamanında erişememesi; ciddi hak kayıplarına (ders intibakı hataları, kaçırılan başvuru tarihleri, mezuniyet gecikmeleri) yol açmakta, aynı zamanda Öğrenci İşleri ve Dış İlişkiler gibi idari birimlerde devasa bir telefon, e-posta ve danışma iş yükü yaratmaktadır.

2. Mevcut Yapay Zekâ Yaklaşımlarının Yetersizliği ve Literatürdeki Boşluk:  
Geleneksel üniversite sohbet botları (kural tabanlı SSS botları) sadece önceden tanımlı sabit sorulara cevap verebilmekte; karmaşık ve dinamik mevzuatı yönetememektedir. Büyük Dil Modelleri (ChatGPT vb.) ve ilk nesil Klasik (Naive) Geri Getirme Destekli Üretim (RAG) mimarileri ise üniversite belgeleri üzerinde tek yönlü arama yapmakta ve kurumsal bilgi eksik olduğunda "halüsinasyon" (gerçek dışı kural ve tarih uydurma) üreterek öğrencileri yanıltmaktadır (Lewis vd., 2020; Gao vd., 2023). Oysa yükseköğretim süreçleri birbirine zincirleme bağlıdır; örneğin bir Erasmus başvuru sorusu, hem bölüm intibak yönergesini hem dış ilişkiler kılavuzunu hem de rektörlük akademik takvimini aynı anda sentezlemeyi (multi-hop reasoning) gerektirir. Klasik RAG sistemleri bu kurumsal sentezi yapamamakta ve bilgi yetersiz kaldığında kendi kendini düzeltememektedir (Yan vd., 2024).

3. Önerilen Agentic Bilgi Botunun Bilimsel Niteliği:  
Bu araştırma önerisiyle; YÖK kurumlarında idari ve akademik süreçlerin hatasız işletilmesini sağlayan, pasif bir arama motoru gibi değil bir "dijital idari asistan" gibi çalışan otonom bir Agentic RAG (Ajan Tabanlı Bilgi Asistanı) mimarisi geliştirilmektedir. Sistem, LangGraph durum makinesi üzerinde çalışan çoklu ajan akışıyla bilimsel literatüre yenilikçi bir yaklaşım getirmektedir:  
- Kullanıcının niyetini ve eksik takip sorularını bağlamsallaştıran Niyet Ajanı (Intent Agent),  
- Türkçe morfolojik yapıya duyarlı çok dilli BAAI/bge-m3 yoğun vektörleri ile BM25 kelime aramasını Reciprocal Rank Fusion (RRF) ve Cross-Encoder ile birleştiren Hibrit Arama Motoru (Cormack vd., 2009; Chen vd., 2024),  
- Bulunan üniversite belgelerinin soruya cevap vermeye yetip yetmediğini sorgulayan, yetersiz kanıt durumunda otonom olarak yeni aramalar tetikleyen Belge Analiz Ajanı (Corrective RAG - Yan vd., 2024),  
- Üretilen yanıttaki her iddiayı resmi yönetmelik maddesiyle etiketleyen ve kaynaksız üretilen cümleleri eleyen Atıf Doğrulayıcı Ajanı (Self-RAG - Asai vd., 2023).

4. Araştırma Sorusu ve Hipotezler:  
- Araştırma Sorusu: Yükseköğretim kurumlarının çok birimli ve dinamik mevzuat yapısında, otonom kanıt değerlendirmesi ve çift ajanlı atıf doğrulama döngüleri içeren bir Agentic RAG mimarisi, klasik doğrusal RAG sistemlerine kıyasla kurumsal bilgi getirme kesinliği (MRR, Recall@5) ve cevap sadakatinde (Faithfulness) istatistiksel olarak anlamlı bir üstünlük sağlar mı?  
- Hipotez: Yükseköğretim için geliştirilen çoklu ajan bilgi botu; 100 soruluk zorlu test setinde Klasik RAG taban çizgisine kıyasla Recall@5 getirme başarımını en az %20 artıracak, kurumsal mevzuat dışı desteksiz iddia (halüsinasyon) oranını ise %80'in üzerinde azaltacaktır (p < 0.05, Wilcoxon testi).

5. 12. Kalkınma Planı, 2030 Stratejisi ve YÖK Politikaları ile İlişkisi:  
Proje, YÖK'ün son dönemde üniversitelerde başlattığı "Yükseköğretimde Yapay Zekâ ve Dijital Dönüşüm Stratejisi", T.C. 12. Kalkınma Planı ve 2030 Sanayi ve Teknoloji Stratejisi'nde yer alan "Kamuda ve Yükseköğretimde Üretken Yapay Zekâ Destekli Akıllı Asistan Sistemleri" öncelikli hedefiyle doğrudan örtüşmektedir. Çalışma, Türk yükseköğretim kurumlarında kurumsal hafızanın korunması, öğrenci memnuniyetinin artırılması ve yapay zekânın kamu idaresinde güvenilir kullanımına ulusal düzeyde örnek teşkil edecektir.
```

---

### 1.2. Amaç ve Hedefler
*(Ölçülebilir - SMART, YÖK Kurumları Odaklı Güncel Versiyon)*

```text
Projenin Temel Amacı:  
Bu projenin temel amacı; Yükseköğretim Kurulu’na (YÖK) bağlı üniversitelerde öğrenci ve personelin idari ve akademik süreçlere ilişkin karmaşık kurumsal mevzuata (önlisans/lisans yönetmelikleri, intibak yönergeleri, Erasmus kuralları, akademik takvim vb.) 7/24 kesintisiz, manipülasyondan ve halüsinasyondan arındırılmış, doğrudan resmi madde atıflarıyla erişebilmesini sağlayan; otonom kanıt analizi ve öz-düzeltme (self-correction) kabiliyetine sahip, Türkçe için optimize edilmiş çoklu ajan tabanlı bir "Yükseköğretim Kurumsal Agentic Bilgi Asistanı" geliştirmektir.

Bu temel amaca ulaşmak doğrultusunda belirlenen somut, ölçülebilir ve gerçekçi alt hedefler şunlardır:

1. Dijital Kurumsal Mevzuat Korpusu ve OCR Hattı:  
Üniversitenin Öğrenci İşleri, Dış İlişkiler ve Fakülteler gibi en az 10 farklı idari birimine ait kamuya açık yönetmelik, yönerge ve kılavuzların web kazıma ile toplanması; taranmış (resim) resmi PDF belgelerinin yerel Tesseract OCR motoru ile işlenerek %100 aranabilir, temiz bir kurumsal bilgi tabanı oluşturulması.

2. Yükseköğretim Sorgularında Hibrit Bilgi Getirme Başarımı (Retrieval):  
Çok dilli BAAI/bge-m3 yoğun vektörleri ile BM25Okapi anahtar kelime aramasını Reciprocal Rank Fusion (RRF) ve Cross-Encoder (BGE-Reranker-v2-m3) ile birleştirerek; üniversite mevzuat sorgularında doğru kanıt maddesinin ilk 5 sonuçta bulunma oranını (Recall@5) Klasik RAG sistemlerine kıyasla en az %20 artırarak %90 seviyesinin üzerine çıkarmak.

3. Otonom Karar Mekanizması ve Çok Adımlı Akıl Yürütme:  
LangGraph durum makinesi üzerinde koordine edilen çoklu ajan mimarisi ile; Document Analyzer ajanının getirilen kurumsal belgelerin yeterliliğini otonom olarak denetlemesini, eksik kanıt durumunda azami 2 tura kadar yeni arama döngüsü yürütmesini sağlamak ve birden fazla birimin bilgisini gerektiren çok adımlı (multi-hop) zorlu sorularda MRR (Mean Reciprocal Rank) değerini 0.85'in üzerine taşımak.

4. Sıfır Halüsinasyon ve Resmi Atıf Güvenilirliği:  
Answer Agent ve Citation Validator ajanları aracılığıyla cevaptaki her iddiayı [Belge Adı - Madde No] ile etiketlemek; desteksiz ve mevzuat dışı uydurma bilgi (halüsinasyon) oranını %5'in altına indirmek (RAGAS Faithfulness/Sadakat skoru >= 0.90).

5. Deneysel Doğrulama ve Bilimsel Kıyaslama:  
Yükseköğretim süreçlerine yönelik 50 tek belgeli (kolay) ve 50 çok belgeli sentez gerektiren (zor) sorudan oluşan, elle etiketlenmiş 100 soruluk özgün bir test veri seti (Ground Truth) hazırlamak; Klasik RAG taban çizgisi ile karşılaştırma yaparak elde edilen başarım farkını Wilcoxon işaretli sıra testi (p < 0.05) ile bilimsel olarak doğrulamak.

6. Kullanıcı Arayüzü, Platform Bağımsız Dağıtım ve Açık Kaynak Çıktı:  
Öğrencilerin ve personelin doğal dilde etkileşime girebileceği, konuşma geçmişini hatırlayan bağlamsal bir web arayüzü (Streamlit) geliştirmek; sistemi tek komutla her üniversite sunucusunda çalışabilecek şekilde Docker konteyneri ile paketlemek ve kaynak kodları diğer YÖK kurumlarına model oluşturacak şekilde GitHub üzerinden açık kaynak yayımlamak.
```

---

## 2. YÖNTEM

### 2.1. Araştırma Tasarımı ve Mimari Yaklaşım
Bu araştırma, yükseköğretim kurumlarının (üniversitelerin) çok katmanlı idari mevzuat, senato kararları ve akademik süreçlerinde karşılaşılan bilgi karmaşasını çözmek amacıyla **deneysel ve karşılaştırmalı bir araştırma tasarımı (A/B testing)** modeli üzerine kurgulanmıştır. Standart/geleneksel Geri Getirme Destekli Üretim (Naive RAG) mimarileri, sorguyu tek bir vektör aramasıyla yanıtlamaya çalışmakta; bu durum üniversite mevzuatındaki çapraz başvuru (örn. Erasmus yönergesi ile ders intibak esaslarının birleşik incelenmesi) ve zamansal geçerlilik (akademik takvim tarih kısıtları) gibi çok adımlı (multi-hop) sorgularda bağlam kopukluğuna ve halüsinasyona (uydurma bilgi üretimi) yol açmaktadır (Lewis vd., 2020; Gao vd., 2023).

Önerilen yöntemde, statik işlem boru hatları yerine durum makineleri (StateGraph) ile yönetilen **Çok Ajanlı ve Döngüsel Bir Agentic RAG Mimarisi** tasarlanmıştır:
1. **Sorgu Ayrıştırma ve Niyet Analizi (Query Decomposition):** Karmaşık kullanıcı sorguları, niyet analiz ajanı tarafından mantıksal alt sorgulara bölünmektedir.
2. **Yoğun ve Seyrek Hibrit Arama (Hybrid Retrieval & RRF):** Semantik benzerliği yakalamak için çok dilli yoğun vektörler (BGE-M3; Chen vd., 2024) ile mevzuattaki kesin terim, yönetmelik ve kanun maddesi eşleşmelerini garanti altına almak için BM25 seyrek algoritması birlikte kullanılmaktadır. Sonuçlar Karşılıklı Sıralama Birleştirmesi (Reciprocal Rank Fusion - RRF; Cormack vd., 2009) ile harmanlanmaktadır.
3. **Yeniden Sıralama (Cross-Encoder Re-ranking):** Birleştirilen ilk aday bağlamlar, `bge-reranker-large` modeli üzerinden sorgu-bağlam çapraz etkileşimine tabi tutularak en alakalı ilk $k$ bağlama daraltılmaktadır.
4. **Döngüsel İnceleme ve Düzeltici RAG (Corrective RAG - CRAG):** Çözümleyici ajan, elde edilen bağlamın mevzuat maddesi düzeyinde yanıt üretmeye yetip yetmediğini denetlemekte; yetersizlik tespit edilirse arama parametrelerini güncelleyerek döngüsel olarak yeni arama gerçekleştirmektedir (Yan vd., 2024).
5. **Öz-Doğrulama ve Halüsinasyon Kontrolü (Self-RAG):** Yanıt ajanı tarafından üretilen metin, doğrudan mevzuat maddelerine atıf (`Madde X, Fıkra Y`) formatında etiketlenmekte; bağımsız bir doğrulayıcı ajan (Validator Agent) tarafından kaynak metinle satır satır çapraz kontrole tabi tutulmaktadır (Asai vd., 2023). Kaynağı doğrulanmayan veya çelişen ifadeler kullanıcıya sunulmadan filtrelenmektedir.

### 2.2. Bağımlı ve Bağımsız Değişkenler
Araştırmanın deneysel hipotezlerini test etmek amacıyla değişkenler şu şekilde tanımlanmıştır:
* **Bağımsız Değişken:** 
  * *Bilgi Getirme ve Üretim Mimarisi:* 
    * A Grubu (Kontrol): Standart Tekil Vektör Aramalı Klasik Naive RAG Mimarisi.
    * B Grubu (Deney): Önerilen Hibrit Aramalı, Yeniden Sıralamalı ve Çift Doğrulamalı Döngüsel Agentic RAG Mimarisi.
* **Bağımlı Değişkenler:**
  1. *Bağlam Uygunluğu (Context Relevance - 0-1):* Çekilen doküman parçalarının sorguyla örtüşme oranı.
  2. *Kaynak Sadakati / Doğruluk (Faithfulness - 0-1):* Üretilen yanıtın yalnızca getirilen mevzuat metnine dayanma oranı (Halüsinasyonun tersi).
  3. *Yanıt Uygunluğu (Answer Relevance - 0-1):* Üretilen yanıtın kullanıcının asıl sorusunu eksiksiz cevaplama derecesi.
  4. *Madde Düzeyinde Atıf Doğruluğu (%):* Yanıtta verilen mevzuat/yönetmelik madde ve fıkra numaralarının doğruluğu.
  5. *Uçtan Uca Yanıt Süresi (Latency - Saniye):* Sorgunun girilmesinden nihai doğrulanmış cevabın üretilmesine kadar geçen süre.

### 2.3. İstatistiksel Yöntemler ve Değerlendirme Protokolü
Sistemin başarısını ölçmek amacıyla YÖK mevzuatı, öğrenci işleri yönergeleri, Erasmus süreçleri ve akademik takvim verilerini kapsayan; uzmanlarca (akademik personel ve idari birim çalışanları) etiketlenmiş **100 adet çok adımlı ve çelişkili senaryo içeren "Altın Standart" (Ground Truth) test veri seti** oluşturulacaktır.
* **Metriklerin Ölçümü:** Endüstri standardı olan **RAGAS (Automated Evaluation of Retrieval Augmented Generation; Es vd., 2023)** değerlendirme çatısı kullanılacaktır.
* **Normallik Testi:** Kontrol ve deney gruplarından elde edilen metrik puanlarının normal dağılıma uygunluğu **Shapiro-Wilk Testi** ile incelenecektir.
* **Hipotez Testi:** Verilerin normal dağılım göstermemesi durumunda bağımlı iki grubun karşılaştırılması için parametrik olmayan **Wilcoxon İşaretli Sıralar Testi (Wilcoxon Signed-Rank Test)**; normal dağılım sağlanması halinde ise **Eşleştirilmiş Örneklem t-Testi (Paired Samples t-test)** uygulanacaktır.
* **Anlamlılık Düzeyi:** Tüm istatistiksel çıkarsamalarda istatistiksel anlamlılık eşiği **$p < 0.05$** olarak kabul edilecek; mimari farkın büyüklüğü **Cohen's d** veya **r etki büyüklüğü (effect size)** katsayısı ile raporlanacaktır.

### 2.4. Ön Çalışma ve Fizibilite (Kavram Kanıtlama - PoC)
Araştırma önerisinin teknik uygulanabilirliğini teyit etmek amacıyla proje ekibi tarafından kapsamlı bir ön çalışma ve kavram kanıtlama (Proof of Concept - PoC) prototipi geliştirilmiştir:
* Yalova Üniversitesi Öğrenci İşleri Mevzuatı, Erasmus Yönergeleri ve 2024-2025 Akademik Takvimi web kazıma (BeautifulSoup) ve OCR destekli PDF ayrıştırma (PyMuPDF, Tesseract) yöntemleriyle taranmıştır.
* Mevzuat metinleri regex tabanlı madde-fıkra semantik bölücüsü ile parçalanarak 340 adet yapısal blok üretilmiş; metadata şemasına göre etiketlenmiştir.
* Çok dilli gömme modeli (BGE-M3) ve BM25 ile hibrit indeksleme gerçekleştirilmiş; LangGraph tabanlı durum çizgesiyle niyet, arama, yanıt ve doğrulama ajanları koşturulmuştur.
* Lokal açık kaynaklı büyük dil modeli (Llama-3.1 8B) ile yerel GPU üzerinde ilk denemeler tamamlanmış, çok adımlı bir sorguda (örn. *"Erasmus'a gidersem intibak derslerimin harç ve kayıt yenileme takvimi nasıl işler?"*) geleneksel RAG alakasız paragraflar getirirken, ajan tabanlı döngünün doğru iki ayrı yönetmelik maddesini birleştirerek sıfır halüsinasyonla yanıt oluşturduğu doğrulanmıştır.

### 2.5. Yöntemin Çalışma Takvimi (İş Paketleri) ile İlişkisi
Belirtilen bilimsel yöntem adımları 6 aylık proje takvimine şu şekilde entegre edilmiştir:
* **İP-1 (1. Ay - Veri Toplama, OCR ve Hiyerarşik Ön İşleme):** YÖK ve üniversite mevzuat havuzunun kazınması, taranmış PDF'lerin OCR'dan geçirilmesi ve mevzuat şemasına göre semantik parçalama algoritmalarının kodlanması.
* **İP-2 (2. Ay - Hibrit İndeksleme ve Vektör Veritabanı Mimarisi):** BGE-M3 yoğun vektörleri ile BM25 seyrek indeksinin oluşturulması, RRF füzyon katmanı ve Cross-Encoder yeniden sıralama pipeline'ının kurulması.
* **İP-3 (3.-4. Aylar - Çok Ajanlı İş Akışı ve Geri Besleme Döngüleri):** LangGraph üzerinde Niyet Ayrıştırma, Düzeltici Arama (CRAG) ve Öz-Doğrulama (Self-RAG) ajan durum makinelerinin kodlanması ve halüsinasyon kontrol döngüsünün test edilmesi.
* **İP-4 (5. Ay - Kullanıcı Arayüzü ve Entegrasyon):** Üniversite personeli ve öğrencilerin kolay erişimi için etkileşimli web arayüzünün (Streamlit/FastAPI) ve taşınabilir Docker konteynerizasyon yapısının tamamlanması.
* **İP-5 (6. Ay - Deneysel Değerlendirme, İstatistiksel Doğrulama ve Raporlama):** 100 soruluk altın test setinin RAGAS ile koşulması, Naive RAG vs. Agentic RAG Wilcoxon analizlerinin yapılması ve TÜBİTAK sonuç raporunun hazırlanması.

### Yöntem Kaynakçası
* Asai, A., Sewon, M., et al. (2023). Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. *arXiv preprint arXiv:2310.11511*.
* Chen, J., Xiao, S., et al. (2024). BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Versatile Pre-Training. *arXiv preprint arXiv:2402.03216*.
* Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009). Reciprocal rank fusion outperforms condorcet and individual machine learning methods. *ACM SIGIR*, 758-759.
* Es, S., James, J., et al. (2023). RAGAS: Automated Evaluation of Retrieval Augmented Generation. *arXiv preprint arXiv:2309.15217*.
* Gao, Y., Xiong, Y., et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. *arXiv preprint arXiv:2312.10997*.
* Lewis, P., Perez, E., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS*, 33, 9459-9474.
* Yan, S. Q., Gu, J. C., et al. (2024). Corrective Retrieval Augmented Generation. *arXiv preprint arXiv:2401.15884*.

---

## 3. PROJE YÖNETİMİ

### 3.1. Çalışma Takvimi

**Proje Süresi (Ay):** `6`

#### Faaliyetler (İş Paketleri)
```text
İP-1: Yükseköğretim Mevzuat Havuzunun Taranması, OCR ve Hiyerarşik Ön İşleme (1. Ay)
YÖK kurumları ve Yalova Üniversitesi bünyesindeki lisans ve lisansüstü yönetmelikleri, senato kararları, Erasmus yönergeleri ve akademik takvim dokümanları taranarak toplanacaktır. Taranmış (vektörel olmayan) PDF belgeleri Tesseract OCR motoru ile sayısallaştırılacaktır. Elde edilen metinler, bağlam bütünlüğünü korumak amacıyla mevzuat madde ve fıkra hiyerarşisini tanıyan kural tabanlı semantik ayrıştırıcılarla parçalara (chunk) bölünecek ve yapılandırılmış JSON formatında metadata etiketleriyle (yönetmelik adı, madde no, tarih) zenginleştirilecektir.
- Başarı Ölçütü: Mevzuat dokümanlarının %100 taranması, yapısal ayrıştırmanın tamamlanması ve ön işleme hattının doğrulanması (%20).

İP-2: Yoğun ve Seyrek Hibrit İndeksleme ile Vektör Veritabanı Mimarisi (2. Ay)
Ayrıştırılan mevzuat blokları, BGE-M3 çok dilli gömme modeliyle yoğun vektörlere dönüştürülerek ChromaDB vektör veritabanına indekslenecektir. Eşzamanlı olarak, mevzuattaki kesin kanun/yönetmelik madde numaralarının ıskalanmaması için BM25 seyrek anahtar kelime indeksi inşa edilecektir. Semantik ve terimsel aramayı birleştiren RRF (Reciprocal Rank Fusion) füzyon algoritması ve aday bağlamları çapraz puanlayan Cross-Encoder (BGE-Reranker) mimarisi kurularak geri getirme performansı optimize edilecektir.
- Başarı Ölçütü: Hibrit arama ve yeniden sıralama hattının test sorgularında ilk k bağlamı doğrulukla getirmesi (%20).

İP-3: Çok Ajanlı İş Akışı, Düzeltici RAG (CRAG) ve Öz-Doğrulama Tasarımı (3. ve 4. Aylar)
LangGraph üzerinde durum çizgesi (StateGraph) kurgulanacaktır. Kullanıcı sorgusunu alt niyetlere bölen Niyet Analiz Ajanı, getirilen bağlamın yeterliliğini değerlendirip gerekirse aramayı döngüsel tekrarlayan Çözümleyici Ajan (CRAG) ve yanıtı mevzuat maddesi düzeyinde kaynak göstererek üreten Yanıt Ajanı kodlanacaktır. Üretilen yanıtı kaynak metinle satır satır denetleyen bağımsız Doğrulayıcı Ajan (Self-RAG) entegre edilerek halüsinasyonlar filtrelenecektir.
- Başarı Ölçütü: Çok adımlı sorgularda ajanlar arası durum geçişlerinin hatasız çalışması ve doğrulama mekanizmasının halüsinasyonları engellemesi (%30).

İP-4: Kullanıcı Arayüzü, API Katmanı ve Konteynerizasyon (5. Ay)
Öğrenci ve idari personelin sisteme kolayca erişebilmesi için çok turlu konuşma geçmişini (hafıza) destekleyen Streamlit ve FastAPI tabanlı kullanıcı arayüzü geliştirilecektir. Sistemin farklı üniversitelerde ek bir kuruluma ihtiyaç duymadan çalıştırılabilmesi için uçtan uca Docker konteynerizasyon paketi hazırlanacaktır.
- Başarı Ölçütü: Web arayüzünün ve Docker ortamının hatasız ve kararlı şekilde ayağa kalkması (%15).

İP-5: Altın Test Seti ile Deneysel Değerlendirme ve İstatistiksel Doğrulama (6. Ay)
Akademik ve idari birim rehberliğinde oluşturulan 100 adet çok adımlı ve çelişkili senaryo içeren Altın Standart (Ground Truth) test veri seti üzerinde Klasik Naive RAG ile önerilen Agentic RAG modeli karşılaştırılacaktır. RAGAS değerlendirme çerçevesiyle Bağlam Uygunluğu, Sadakat ve Yanıt Uygunluğu metrikleri ölçülecek; Shapiro-Wilk normallik ve Wilcoxon İşaretli Sıralar Testi uygulanarak mimarinin başarısı istatistiksel olarak kanıtlanacaktır.
- Başarı Ölçütü: Agentic RAG mimarisinin Sadakat ve Madde Doğruluğu metriklerinde Naive RAG'e kıyasla p < 0.05 düzeyinde istatistiksel üstünlük sağlaması (%15).
```

#### Kim(ler) Tarafından Gerçekleştirileceği
```text
Proje Yürütücüsü (Dursun Burak Yüz):
Proje kapsamında yer alan tüm teknik aşamaların fiilen yürütülmesinden sorumludur. Web kazıma, OCR ve mevzuat ön işleme boru hattının kurulması (İP-1); BGE-M3 ve BM25 hibrit indeksleme ve vektör veritabanı mimarisinin inşa edilmesi (İP-2); LangGraph tabanlı çok ajanlı durum makinelerinin (Niyet, CRAG, Yanıt ve Self-RAG Doğrulayıcı ajanlar) kodlanması (İP-3); kullanıcı web arayüzünün ve Docker konteyner altyapısının geliştirilmesi (İP-4); test senaryolarının RAGAS çatısı üzerinden koşturulması ve Wilcoxon istatistiksel analizlerinin gerçekleştirilmesinde (İP-5) birincil derecede görev alacaktır.

Proje Danışmanı:
Araştırma tasarımının ve yönteminin bilimsel standartlara uygunluğunun denetlenmesi, mevzuat alanındaki test senaryolarının doğrulanması, istatistiksel hipotez testlerinin akademik geçerliliğinin kontrol edilmesi ve 6 aylık çalışma takviminin periyodik akademik takibi ve rehberliğinden sorumludur.
```

---

### 3.2. Risk Yönetimi (Riskler ve B Planları)

```text
Risk 1: Taranmış Eski Mevzuat Dokümanlarında Düşük OCR Kalitesi ve Metin Kaybı
- İlgili İş Paketi: İP-1 (Yükseköğretim Mevzuat Havuzunun Taranması, OCR ve Hiyerarşik Ön İşleme)
- Risk Düzeyi: Orta
- B Planı: Taranmış ve düşük çözünürlüklü PDF dokümanlarında Tesseract OCR motorunun yetersiz kalması durumunda, görüntü ön işleme aşamasına OpenCV tabanlı morfolojik filtreleme, gri tonlama ve adaptif eşikleme (binarization) adımları eklenecektir. Karakter tanıma başarısı artmazsa, alternatif açık kaynaklı derin öğrenme tabanlı OCR motorlarına (PaddleOCR) geçilecek; taranmış belgelere paralel olarak üniversite ve YÖK resmi portallarındaki güncel HTML/dijital metin tabanlı kaynaklar önceliklendirilerek veri kaybı engellenecektir.

Risk 2: Çok Ajanlı Düzeltici RAG (CRAG) Döngüsünde Sonsuz Arama ve Yanıt Gecikmesi (Latency)
- İlgili İş Paketi: İP-3 (Çok Ajanlı İş Akışı, Düzeltici RAG ve Öz-Doğrulama Tasarımı)
- Risk Düzeyi: Yüksek
- B Planı: Çözümleyici ajanın getirilen bağlamı yetersiz bulup sürekli yeni sorgular türeterek arama döngüsüne girmesi riskine karşı, LangGraph durum çizgesi (StateGraph) üzerinde katı bir iterasyon sınırı (maksimum 2 döngü) tanımlanmıştır. İkinci denemede de mevzuat maddesi düzeyinde tam eşleşme sağlanamazsa, sistem kullanıcıya mevzuat belirsizliğini ve ilgili birimin resmi web bağlantısını şeffaf biçimde sunarak "kontrollü güvenli çıkış" (graceful fallback) yapacak; böylece yanıt gecikmesi kullanıcı deneyimini bozmayacak bir eşikte (en fazla 6 saniye) sınırlandırılacaktır.

Risk 3: Mevzuat Çelişkilerinde Yanıt Ajanının Halüsinasyon Üretmesi ve Doğrulama Hataları
- İlgili İş Paketi: İP-3 ve İP-5 (Öz-Doğrulama Tasarımı ve Deneysel Değerlendirme)
- Risk Düzeyi: Yüksek
- B Planı: Farklı mevzuat belgeleri (örn. Lisans Yönetmeliği vs. Erasmus Yönergesi) arasındaki çelişkilerde dil modelinin varsayımsal bilgi uydurmasını engellemek için Çift Aşamalı Öz-Doğrulama (Self-RAG) mekanizması uygulanacaktır. Doğrulayıcı Ajanın yanıtta geçen her cümleyi doğrudan kaynak bağlamdaki madde/fıkra ile NLI (Doğal Dil Çıkarsaması) mantığıyla eşleştirmesi zorunlu kılınacaktır. Doğrulanamayan cümleler yanıttan otomatik ayıklanacak; şüphe durumunda yanıt üretimi durdurularak kullanıcıya yalnızca kesinleşmiş mevzuat hükümleri aktarılacaktır.

Risk 4: Yerel Donanım / GPU Kaynak Yetersizliği ve Bellek (VRAM) Kısıtları
- İlgili İş Paketi: İP-2 ve İP-4 (Hibrit İndeksleme ve Konteynerizasyon)
- Risk Düzeyi: Orta
- B Planı: BGE-M3 gömme modeli, BGE-Reranker ve yerel LLM'in (Llama-3.1 8B) eşzamanlı çalıştırılması esnasında GPU belleğinin (VRAM) aşılması durumunda, modeller 4-bit/8-bit kuantizasyon (AWQ/GGUF/Ollama) formatlarına indirgenecektir. Gerekmesi halinde reranker aşamasında daha hafif mimariler (bge-reranker-base veya MiniLM) devreye sokulacak; hibrit arama için BM25 seyrek indeksleme CPU üzerinde asenkron çalışacak şekilde optimize edilecektir.

Risk 5: Altın Standart Test Seti Doğrulamasında İdari Birim Geri Bildirim Gecikmesi
- İlgili İş Paketi: İP-5 (Altın Test Seti ile Deneysel Değerlendirme ve İstatistiksel Doğrulama)
- Risk Düzeyi: Düşük
- B Planı: 100 soruluk test setinin mevzuat uzmanları tarafından onaylanmasının gecikmesi durumunda; proje danışmanının yönlendirmesiyle resmi Sıkça Sorulan Sorular (SSS) havuzları ve mevzuat metinlerinden yarı otomatik sentetik soru-cevap türetim algoritmaları çalıştırılacaktır. Oluşturulan taslak test seti danışman onayına sunulacak, süreç aksamadan RAGAS değerlendirme testlerine başlanacaktır.
```

---

### 3.3. Araştırma Olanakları

#### Kuruluşta Bulunan Altyapı/Ekipman Türü - Modeli (Laboratuvar - Araç - Makine-Teçhizat vb.) *
```text
Yalova Üniversitesi Bilgisayar Mühendisliği Bölümü Araştırma Laboratuvarı ve Yüksek Performanslı GPU Hesaplama İş İstasyonu (NVIDIA GeForce RTX 4060 8GB GPU, Yüksek Hızlı NVMe SSD Depolama, 16 GB RAM, ULAKBİM/Eduroam Ağ Altyapısı)
```

#### Projede Kullanım Amacı *
```text
Açık kaynaklı Büyük Dil Modelinin (Llama-3.1 8B) yerel ortamda kuantize edilerek çalıştırılması (çıkarım/inference), BGE-M3 çok dilli yoğun gömme (embedding) vektörlerinin çıkarılması, Cross-Encoder (BGE-Reranker) ile aday mevzuat maddelerinin yeniden sıralanması, LangGraph çok ajanlı durum çizgesinin koşturulması, ChromaDB vektör veritabanının indekslenmesi, Streamlit/Docker tabanlı kullanıcı arayüzünün yerel testleri ve RAGAS doğrulama testlerinin yürütülmesi amacıyla kullanılacaktır.
```

---

## 4. ARAŞTIRMA ÖNERİSİNİN YAYGIN ETKİSİ

### 1. Bilimsel/Akademik Çıktılar
```text
- Ulusal veya uluslararası indeksli saygın bir bilimsel konferansta (örneğin IEEE SİU - Sinyal İşleme ve İletişim Uygulamaları Kurultayı veya TAINN Yapay Zekâ Konferansı) en az 1 adet hakemli akademik bildirinin sunulması ve bildiriler kitabında yayımlanması hedeflenmektedir.
- Proje kapsamında elde edilen deneysel bulguların (Klasik RAG vs. Agentic RAG karşılaştırmalı RAGAS metrik sonuçları), Türkçe Doğal Dil İşleme alanında açık erişimli bir dergi makalesine dönüştürülmesi için yayın hazırlığı tamamlanacaktır.
- Lisans bitirme tezi kapsamında Türkçe idari mevzuatta çok ajanlı sistemlerin başarımını belgeleyen kapsamlı bir akademik araştırma raporu hazırlanacaktır.
```

### 2. Ekonomik/Ticari/Sosyal Çıktılar
```text
- Çalışan Yazılım Prototipi: Üniversite web portallarına kolayca entegre olabilen, Docker ile paketlenmiş, Streamlit tabanlı, çok turlu hafızaya sahip ve mevzuat maddesi düzeyinde doğrulanmış yanıt üreten bir "Agentic RAG Bilgi Asistanı" prototipi elde edilecektir.
- Sosyal ve Kurumsal İş Gücü Tasarrufu: Üniversite öğrencilerinin idari birimlere gitmeden mevzuat, ders intibak kuralları ve Erasmus başvuru şartlarına 7/24 resmi kaynak atıflarıyla erişmesi sağlanarak; Öğrenci İşleri ve Dış İlişkiler ofislerinin rutin telefon/e-posta danışma yükünün en az %40 oranında azaltılması ve kurumsal verimliliğin artırılması sağlanacaktır.
- Açık Kaynak Katkısı: Geliştirilen mevzuat ayrıştırma algoritmaları ve LangGraph çok ajanlı iş akış şablonları GitHub üzerinden açık kaynak lisansıyla paylaşılarak diğer YÖK kurumları için sıfır maliyetli bir referans model oluşturulacaktır.
```

### 3. Yeni Proje(ler) Oluşturmasına Yönelik Çıktılar
*(Düşük Kişisel Efor / Hazır Altyapı ve Platform Odaklı Versiyon)*
```text
- Hazır Altyapı ve Yaygınlaşma: Projede geliştirilen modüler ve Dockerize edilmiş mikroservis mimarisi; diğer devlet ve vakıf üniversitelerinin veya kamu kurumlarının kendi idari mevzuatlarını doğrudan yükleyerek kullanabilecekleri genişletilebilir hazır bir yazılım çatısı (framework) sağlayacaktır.
- Gelecek Araştırmalara Zemin Oluşturma: Oluşturulan 100 soruluk mevzuat test seti ve hibrit arama mimarisi; üniversite bünyesinde yapılabilecek BAP (Bilimsel Araştırma Projeleri), TÜBİTAK 2209-B (Sanayi Odaklı) veya sonraki dönem lisansüstü tez çalışmaları için hazır bir deneysel başlangıç noktası teşkil edecektir.
- Yarışma ve Girişimcilik Potansiyeli: Proje çıktısı, ek bir geliştirme yükü gerektirmeksizin mevcut haliyle TEKNOFEST Türkçe Doğal Dil İşleme Yarışması veya TÜBİTAK BİGG girişimcilik programı için doğrudan sunulabilir nitelikte bir teknolojik kavram kanıtlama (PoC) tabanı oluşturacaktır.
```
