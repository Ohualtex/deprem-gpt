# Ön kayıt 3: Kahramanmaraş testi (eğitimden önce yazıldı, 21 Kasım 2026)

Soru: 6 Şubat 2023'ten önceki verilerle eğitilen model, Kahramanmaraş dizisini ve ardından gelen bir yılı
Türkiye için kurulmuş bir ETAS'tan daha iyi tahmin ediyor mu? Çok katalog eğitimi burada da işe yarıyor mu?

Bu test, ikinci testin açığını kapatıyor. O testte ek kataloglar California test dönemiyle aynı yılları
kapsıyordu. Burada tüm eğitim verisi, ETAS uydurması ve erken durdurma test döneminden önce kalıyor.

Bu dosyanın kuralları KOERI kataloğu indirilirken ve hiçbir model ya da ETAS Türkiye verisiyle
eğitilmeden yazıldı. Olay sayıları ve Mc, veri hazırlandıktan sonra aşağıdaki "Veri" bölümüne eklendi.
Bu ekleme kuralları değiştirmedi.

## Veri (`kod/hazirla_tr.py`)
- Kaynak: KOERI (Kandilli) kataloğu, 2006–2024, M ≥ 2.0 indirildi, "Deprem" tipi. Büyüklük: KOERI'nin
  xM sütunu (verilen büyüklüklerin en büyüğü). Bu sütun ana şoku 7.8, ikincisini 7.6 veriyor.
- Kutu: 36.0–42.2°K, 26.0–45.0°D, derinlik ≤ 70 km. Büyüklük 0.1'e yuvarlanıyor.
- Mc: 2008–2022 yıllarının her biri için en büyük eğrilik + 0.2 hesaplanıyor, bunların en büyüğü
  alınıyor. Test dönemine bakılmıyor.
- Bölümler: geçmiş 2006–2007 (yalnızca bağlam), eğitim 2008–2020, doğrulama 2021-01-01 ile
  2023-02-06 00:00 arası, test 2023-02-06 00:00 ile 2024-02-06 00:00 arası (bir yıl, ana şok dahil).
- Ana şok sonrası ilk saatlerde katalog eksik (kısa süreli tamlık kaybı). Bu, ETAS'ı ve modeli aynı
  biçimde etkiliyor, düzeltme yapılmıyor.

### Veri hazırlandıktan sonra eklendi (eğitimden önce, `sonuclar/tr_veri_ozeti.json`)
- 194 694 satır indirildi. Kutu ve derinlikten sonra 175 362 olay kaldı.
- Yıllık MAXC + 0.2 değerleri: 2008'de 3.0, 2009–2011'de 2.9, 2012–2022'de 2.2. Kural gereği
  **Mc = 3.0**. 2012 sonrası katalog daha düşük eşikte de tam görünüyor. Kural değiştirilmedi.
- M ≥ 3.0 olay sayıları: geçmiş 4 050, eğitim 18 398, doğrulama 1 907, test 4 264.
- Ana şok 2023-02-06 01:17:32.67, M 7.8. Testteki M ≥ 6 olaylar: 7.8, 6.6, 7.6, 6.0 (6 Şubat) ve
  6.4 (20 Şubat).
- Eğitim dönemindeki en büyük olay M 7.2 (Van 2011). Doğrulama döneminde en büyüğü M 6.1.
- Test kümeleri: ana şoktan sonraki 1 gün 594 olay, 7 gün 1 652, 30 gün 2 551. Dizi kutusunda ilk
  30 gün 2 339. Dizi kutusu dışında 759.
- Ek kataloglar (2023-02-06 öncesi): California 92 263, JMA 101 871, INGV 8 044, GeoNet 7 410 olay.
  Toplam 209 588.

## Ek kataloglar (T1, T2)
California (EarthquakeNPP ComCat, 1971–2020, M ≥ 2.5), Japonya (JMA), İtalya (INGV), Yeni Zelanda
(GeoNet). İkinci testtekiyle aynı hazırlık, ama yalnızca 2023-02-06 öncesi olaylar alınıyor.
California'nın tüm olayları eğitim hedefi.

## ETAS
Zamansal ETAS (Ogata 1988), `kod/etas_zaman.py`, en büyük olabilirlik, üç başlangıç noktası. Türkiye
eğitim + doğrulama döneminde (2008 ile 2023-02-06 arası) uydurulur, 2006–2007 geçmiş olarak girer.
Testte parametreler sabit kalır, tüm geçmiş kullanılır. Olay başına TLL tanımı EarthquakeNPP'deki ile
aynı. Kod, California'da EarthquakeNPP'nin ETAS'ıyla (test TLL 1.434) karşılaştırılarak sınandı.
Türkiye verisi hazır olmadan yapılan bu sınamada kodumuzun ETAS'ı 1.465 verdi, yani kodumuzunki
daha güçlü (`sonuclar/etas_ca_dogrulama/`). Üç başlangıç noktası da aynı çözüme yakınsadı.

## Koşular (hepsi küçük model, L = 512, 3 tohum, Türkiye doğrulamasıyla erken durdurma)
| Kod | Eğitim hedefleri |
|---|---|
| T0 | Yalnızca Türkiye 2008–2020 |
| **T1 (birincil)** | Türkiye 2008–2020 + ek kataloglar (2023-02-06 öncesi) |
| T2 | Yalnızca ek kataloglar. Türkiye olayları yalnızca bağlam ve erken durdurma için kullanılıyor |

Test: her test olayı için önceki 512 Türkiye olayı bağlam. Diğer ayarlar ikinci testteki gibi.

## Ölçüt ve belirsizlik
Test olaylarında olay başına zamansal log-olabilirlik (gün), ETAS ile olay olay eşleşik. Test dönemi
bir yıl olduğu için birincil güven aralığı 7 günlük blok bootstrap (%95, 2000 örnek). 1 günlük blok
ikincil olarak veriliyor. Tohum eşleşik farklar da veriliyor.

Kümeler:
- tüm test yılı
- ana şoktan sonraki 1, 7 ve 30 gün (tüm kutu)
- dizi kutusunda ilk 30 gün (35.8–38.8°K, 35.3–39.7°D)
- dizi kutusu dışı
- ana şoktan 30 gün sonrası

## Karar kuralı
- **Devam:** T1 − ETAS tüm test yılında pozitif ve 7 günlük blok GA'sı sıfırı dışlıyor; **ve** dizi
  kutusunun ilk 30 gününde T1 − ETAS > 0; **ve** T1 − T0 > 0, üç tohum eşleşik farkın üçü de pozitif.
- **Dur:** T1 − ETAS tüm test yılında ≤ 0.
- Arası "belirsiz".
- İkincil: T2'nin (Türkiye'yi eğitimde hiç görmemiş model) ETAS'a ve T0'a göre durumu, ilk gün,
  dizi dışı.
