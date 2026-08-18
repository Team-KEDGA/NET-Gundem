# NET GÜNDEM

**Gündem Başlıklarında Konu Bütünlüğünü Koruyan Bağlam Duyarlı Moderasyon Motoru**

> 🚧 **Proje Durumu:** Erken planlama aşaması. Kod geliştirmeye henüz başlanmamıştır; bu commit, projenin kapsamını ve mimari yaklaşımını sabitlemek amacıyla atılmıştır.

---

## İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Çözülen Problem](#çözülen-problem)
- [Çözüm Yaklaşımı](#çözüm-yaklaşımı)
- [Temel Tasarım İlkesi](#temel-tasarım-i̇lkesi)
- [Sistem Mimarisi](#sistem-mimarisi)
- [Teknoloji Yığını](#teknoloji-yığını)
- [Yol Haritası](#yol-haritası)
- [Takım](#takım)
- [Yarışma Bilgisi](#yarışma-bilgisi)
- [Katkı ve İletişim](#katkı-ve-i̇letişim)
- [Lisans](#lisans)

---

## Proje Hakkında

**NET GÜNDEM**, sosyal medya platformlarındaki gündem (trend) başlıkları altında biriken **konu dışı içeriği** otomatik olarak tespit edip ana akıştan ayıran, bağlam duyarlı bir moderasyon motorudur.

Klasik istenmeyen içerik (spam) filtrelerinden farklı olarak sistem, bir gönderinin *mutlak anlamda* zararlı olup olmadığını değil, **bulunduğu bağlama ait olup olmadığını** değerlendirir. Literatürde bu davranış "etiket kaçırma" (*hashtag hijacking*) olarak adlandırılır.

Proje, **TEKNOFEST 2026 NSosyal İnovasyon Yarışması** kapsamında **Sosyal Yapay Zekâ** temasında geliştirilmektedir.

## Çözülen Problem

Bir kullanıcı gündemdeki bir başlığa girdiğinde, o başlık altındaki gönderilerin konuyla ilgili olmasını bekler. Ancak pratikte akış üç tür içerikten oluşur:

- Başlığın konusuyla doğrudan ilgili gönderiler
- Görünürlükten faydalanmak için etikete iliştirilmiş, tamamen ilgisiz gönderiler
- Otomatik hesaplar tarafından üretilen tekrarlı içerikler

İkinci ve üçüncü grup, birincinin görünürlüğünü doğrudan bastırır. Mevcut çözümler (etkileşime göre sıralama, mutlak ölçütlü spam filtreleri, bot tespiti, kullanıcı bildirimi) bu problemi çözmez çünkü hiçbiri **gönderi–başlık ilişkisini göreli olarak** ölçmez.

## Çözüm Yaklaşımı

Sistem üç katmandan oluşur:

1. **Dinamik Konu Temsili** — Bir gündem başlığının anlamsal çapası, başlık metninden değil, başlık altındaki erken dönem organik gönderilerden dinamik olarak çıkarılır ve zaman içinde sınırlandırılmış biçimde güncellenir (konu kaymasına uyum sağlamak için).
2. **Çok Sinyalli İlgililik Skorlaması** — Anlamsal benzerliğin yanı sıra çoklu etiket tutarsızlığı, hesap yayılım örüntüsü, yakın kopya yoğunluğu ve etkileşim özgünlüğü sinyalleri birleştirilerek 0–1 arası bir ilgililik skoru üretilir.
3. **Üç Bantlı Karar ve Müdahale** — Sistem ikili karar vermez; *ilgili*, *belirsiz* (çekimser) ve *konu dışı* bantları tanımlanır. Belirsiz durumlarda müdahale bilinçli olarak askıya alınır.

## Temel Tasarım İlkesi

> **Silmek değil, ayırmak.**

Sistem hiçbir gönderiyi platformdan kaldırmaz, hesap kapatmaz ve içeriğe erişimi engellemez. Konu dışı olduğu değerlendirilen gönderiler yalnızca aynı başlık altındaki ikincil bir sekmeye taşınır:

- Gönderi ve etkileşimleri korunur
- Kullanıcı dilediği anda ham akışa geri dönebilir
- Üretici hatalı sınıflandırmaya itiraz edebilir
- Her karar, kısa bir gerekçe etiketiyle şeffaf biçimde sunulur

Bu ilke, yanlış kararların geri döndürülebilir olmasını garanti eder ve projenin etik çerçevesinin temelini oluşturur.

## Sistem Mimarisi

Sistem, bağımsız ölçeklenebilen dört servisten oluşur ve servisler arası iletişim eşzamansız bir mesaj kuyruğu üzerinden sağlanır:

```
Gönderi Alım Servisi
        │
        ▼
Konu Temsili Servisi ──► anlamsal çapa (kayan pencere ile güncellenir)
        │
        ▼
Skorlama Servisi ──► çok sinyalli ilgililik skoru
        │
        ▼
Karar Servisi ──► bant kararı (İlgili / Belirsiz / Konu Dışı) + müdahale
```

Detaylı mimari kararlar ve gerekçeleri proje teknik raporunda yer almaktadır.

## Teknoloji Yığını

| Katman | Teknoloji |
|---|---|
| Programlama dili | Python 3.11 |
| Model çerçevesi | PyTorch, Hugging Face Transformers |
| Dil modeli | BERTurk / TURNA (karşılaştırmalı değerlendirme) |
| Cümle temsili | Sentence-Transformers (Türkçe ince ayarlı) |
| Kümeleme | scikit-learn (HDBSCAN / KMeans) |
| Yakın kopya tespiti | MinHash / SimHash |
| Servis katmanı | FastAPI |
| Kuyruk ve önbellek | Redis |
| Veri tabanı | PostgreSQL + pgvector |
| Arayüz | React, TypeScript, Tailwind CSS |
| Dağıtım | Docker, Docker Compose |

## Yol Haritası

- [ ] **İP1** — Problem analizi, ön ölçüm çalışması, etiketli veri kümesi oluşturma
- [ ] **İP2** — Teknik rapor hazırlığı ve teslimi
- [ ] **İP3** — Model geliştirme (ön işleme, taban çizgileri, ince ayar, doğrulama)
- [ ] **İP4** — Mentörlük süreci ve mimari iyileştirme
- [ ] **İP5** — Prototip bütünleştirme ve arayüz geliştirme
- [ ] **İP6** — Test, değerlendirme ve final sunumu hazırlığı
- [ ] **İP7** — Final sunumu ve TEKNOFEST Şanlıurfa

Güncel ilerleme durumu için [Issues](../../issues) ve proje panosuna bakınız.

## Takım

**Team KEDGA** — 5 üye, disiplinler arası (bilgisayar mühendisliği, yazılım mühendisliği, elektrik-elektronik mühendisliği).

Değerlendirme esasları gereği takım üyelerinin isim ve kişisel bilgilerine bu depoda yer verilmemiştir.

## Yarışma Bilgisi

| | |
|---|---|
| Yarışma | TEKNOFEST 2026 NSosyal İnovasyon Yarışması |
| İnovasyon Dikeyi | Sosyal Yapay Zekâ |
| Takım | Team KEDGA |

## Katkı ve İletişim

Proje, yarışma süresi boyunca kapalı bir ekip içi geliştirme süreciyle ilerlemektedir. Sorular ve geri bildirimler için lütfen Issues bölümünü kullanınız.

## Lisans

Lisans bilgisi, proje geliştirme süreci ilerledikçe eklenecektir.
