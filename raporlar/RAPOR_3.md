# Deprem GPT, üçüncü test: Kahramanmaraş 2023

21 Kasım 2026. Önceki testler: `RAPOR.md` (uzun bağlam, "dur") ve `RAPOR_2.md` (çok katalog, "devam").
Bu testin ön kaydı `ON_KAYIT_3.md`. Kurallar hiçbir model ya da ETAS Türkiye verisiyle eğitilmeden
yazıldı. Olay sayıları ve Mc veri hazırlandıktan sonra eklendi, kurallar değiştirilmedi.

> **Sonradan eklendi:** Güçlendirilmiş ETAS varyantlarına karşı sonuç `RAPOR_4.md`'de. En güçlü geçerli ETAS'a
> karşı kazanç +0.051 [+0.022, +0.069] ile duruyor. 30 gün sonrası kazancı ise kâhin ETAS'a karşı sıfıra iniyor.

## Karar: DEVAM

Ön kayıtlı kuralın üç koşulu da sağlandı:

1. **Tüm test yılında ETAS'ı geçiyor.** Çok katalogla eğitilen model (T1), 6 Şubat 2023 ile 6 Şubat 2024
   arasındaki Türkiye depremlerinde ETAS'ı **+0.065 nat/olay** geçiyor. %95 GA (7 günlük blok)
   [+0.039, +0.081]. Üç tohum: +0.065, +0.060, +0.069.
2. **Dizinin ilk 30 gününde de önde.** Dizi kutusunda ana şoktan sonraki ilk 30 günde T1 − ETAS =
   +0.065. 1 günlük blok GA [+0.011, +0.107].
3. **Ek kataloglar yalnız Türkiye modelini geçiyor.** T1, yalnızca Türkiye'yle eğitilen modeli (T0)
   +0.087 geçiyor, GA [+0.074, +0.098]. Üç tohum eşleşik farkın üçü de pozitif: +0.091, +0.064,
   +0.108.

İkinci testin açığı bu testte yok. Modellerin bütün eğitim verisi, ETAS uydurması ve erken durdurma
6 Şubat 2023'ten önce kalıyor. Kahramanmaraş dizisi hiçbir aşamada eğitimde kullanılmadı.

Yalnızca Türkiye'yle eğitilen model ETAS'ın gerisinde kalıyor (−0.023). Türkiye'yi eğitim hedefi
olarak hiç görmeyen model (T2) ise ETAS'ı +0.052 geçiyor. Bu model yalnızca California, Japonya,
İtalya ve Yeni Zelanda kataloglarıyla eğitildi. Kazancı veren şey çok katalogla eğitim.

## Veri

- **Katalog:** KOERI (Kandilli), sitenin kendi arama formundan aylık sorgularla indirildi
  (`kod/indir_koeri.py`). Kapsam 2006–2024, M ≥ 2.0. 194 694 satır geldi, her sorgu parçasında
  ayrıştırılan satır sayısı KOERI'nin bildirdiği "Bulunan" sayısıyla tuttu.
- **Kutu ve büyüklük:** 36.0–42.2°K, 26.0–45.0°D, derinlik ≤ 70 km. Büyüklük KOERI'nin xM sütunu.
  Ana şok bu sütunda 7.8, ikincisi 7.6.
- **Mc = 3.0.** Ön kayıtlı kural 2008–2022 yıllık MAXC + 0.2 değerlerinin en büyüğünü alıyor. 2008'de
  bu değer 3.0, 2012'den sonra 2.2.
- **Olay sayıları (M ≥ 3.0):**

  | Bölüm | Dönem | Olay |
  |---|---|---:|
  | Geçmiş (yalnızca bağlam) | 2006–2007 | 4 050 |
  | Eğitim | 2008–2020 | 18 398 |
  | Doğrulama | 2021 – 2023-02-06 | 1 907 |
  | Test | 2023-02-06 – 2024-02-06 | 4 264 |

  Eğitim dönemindeki en büyük olay M 7.2 (Van 2011).
- **Ek kataloglar:** California 92 263, JMA 101 871, INGV 8 044, GeoNet 7 410 olay. Hepsi
  2023-02-06 öncesi.

Kaynak: `sonuclar/tr_veri_ozeti.json`, `kod/hazirla_tr.py`.

## ETAS

Bu test için kendi zamansal ETAS kodumu yazdım (`kod/etas_zaman.py`, Ogata 1988). Kod profil
olabilirlik kullanıyor: μ ve K, EM adımlarıyla kapalı biçimde bulunuyor, a, c ve p Nelder-Mead ile
aranıyor. Olay başına TLL tanımı EarthquakeNPP'dekiyle aynı.

- **California'da sınama:** EarthquakeNPP ile aynı dönemde (1981–2007) uydurdum. Üç başlangıç noktası
  aynı çözüme yakınsadı. Test TLL'si **1.465**, EarthquakeNPP'nin ETAS'ı ise **1.434**. Yani bu ETAS
  benchmark'takinden daha güçlü bir rakip. Bunun ikinci teste etkisi `RAPOR_2.md`'nin başına düzeltme
  olarak yazıldı: M1 bu ETAS'ı da geçiyor, ama +0.031 farkla. Kaynak:
  `sonuclar/etas_ca_dogrulama/etas.json`, `sonuclar/c2_etas_zaman_kiyas.json`.
- **Türkiye uydurması:** 2008 ile 2023-02-06 arasında. Parametreler: μ = 0.0045/gün, K = 0.065,
  a = 0.955, c = 0.025 gün, p = 1.110. Üç başlangıç noktası aynı olabilirliğe ulaştı (0.76576).
  Yaklaşık dallanma oranı 1.36. Kaynak: `sonuclar/etas_tr/etas.json`.

## Sonuçlar

Değerler olay başına zamansal log-olabilirlik (nat, gün birimi); yüksek olan daha iyi. Modeller 3
tohumun ortalaması ± standart sapma.

| | Tüm test (4 264) | İlk gün (594) | İlk 7 gün (1 652) | Dizi kutusu, ilk 30 gün (2 339) | Dizi kutusu dışı (759) | 30 gün sonrası (1 711) |
|---|---:|---:|---:|---:|---:|---:|
| ETAS | 2.678 | 5.342 | 4.654 | 4.037 | 1.355 | 0.737 |
| T0: yalnızca Türkiye | 2.655 ± 0.018 | 5.382 ± 0.014 | 4.652 ± 0.017 | 4.012 ± 0.018 | 1.306 ± 0.020 | 0.727 ± 0.019 |
| **T1: Türkiye + ek kataloglar** | **2.743 ± 0.004** | **5.513 ± 0.009** | **4.739 ± 0.010** | **4.102 ± 0.008** | **1.403 ± 0.001** | **0.807 ± 0.002** |
| T2: yalnızca ek kataloglar | 2.730 ± 0.014 | 5.486 ± 0.035 | 4.720 ± 0.027 | 4.083 ± 0.022 | 1.397 ± 0.007 | 0.802 ± 0.003 |

ETAS'a göre farklar. GA'lar tüm test, dizi dışı ve 30 gün sonrası için 7 günlük blok, dizi kutusunun
ilk 30 günü için 1 günlük blok. İlk gün ve ilk 7 gün için blok bootstrap yapılamıyor (1–2 blok), bu
iki sütunda tohum değerleri veriliyor.

| | Tüm test | İlk gün (tohumlar) | İlk 7 gün (tohumlar) | Dizi, ilk 30 gün | Dizi dışı | 30 gün sonrası |
|---|---|---|---|---|---|---|
| T0 − ETAS | −0.023 [−0.054, −0.002] | +0.040 (+0.024, +0.049, +0.046) | −0.002 (−0.006, +0.017, −0.016) | −0.025 [−0.078, +0.007] | −0.049 [−0.093, +0.000] | −0.010 [−0.036, +0.021] |
| **T1 − ETAS** | **+0.065 [+0.039, +0.081]** | **+0.171 (+0.171, +0.161, +0.180)** | +0.086 (+0.087, +0.076, +0.095) | +0.065 [+0.011, +0.107] | +0.048 [+0.025, +0.075] | +0.070 [+0.055, +0.089] |
| T2 − ETAS | +0.052 [+0.028, +0.068] | +0.143 (+0.169, +0.103, +0.158) | +0.066 (+0.078, +0.035, +0.084) | +0.046 [−0.004, +0.085] | +0.042 [+0.018, +0.072] | +0.065 [+0.048, +0.087] |

Model farkları (tüm test, 7 günlük blok GA, tohum eşleşik):

| Fark | Ortalama | %95 GA | Tohumlar |
|---|---:|---|---|
| T1 − T0 | +0.087 | [+0.074, +0.098] | +0.091, +0.064, +0.108 |
| T2 − T0 | +0.075 | [+0.065, +0.090] | +0.085, +0.039, +0.100 |
| T1 − T2 | +0.013 | [+0.005, +0.017] | +0.006, +0.024, +0.008 |

Büyüklük log-olabilirliği (tüm test): T0 −2.721, T1 −2.684, T2 −2.690. Bu kıyasın ETAS karşılığı yok.

Kaynak: `sonuclar/c3_ozet.json`, `sonuclar/c3_tablolar.md` (`kod/analiz3.py`). Şekiller:
`sekiller/c3_sekil1_etas_farki`, `c3_sekil2_kumulatif`, `c3_sekil3_dogrulama` (PNG + PDF).

### Kazanç zamanda nereden geliyor

T1'in ETAS'a göre toplam kazancı 276 nat. Dağılımı:

| Ana şoktan sonra | Olay | Toplam kazanç (nat) | Olay başına |
|---|---:|---:|---:|
| 0–1 gün (ana şok dahil) | 595 | 101 | +0.170 |
| 1–3 gün | 565 | 39 | +0.068 |
| 3–30 gün | 1 392 | 15 | +0.011 |
| 30 gün – 1 yıl | 1 711 | 120 | +0.070 |

Kazanç iki yerde toplanıyor: ilk günlerde ve dizi söndükten sonraki aylarda. 3–30 gün arasında model
ile ETAS hemen hemen eşit. Ana şokun kendisinde ETAS daha iyi (1.21'e karşı 1.08).

Yalnızca Türkiye'yle eğitilen T0, ilk üç günde ETAS'ın biraz önünde. Yaklaşık 5. günden sonra
gerisine düşüyor ve yılı −98 nat ile bitiriyor (Şekil 2).

## Ön tahminle karşılaştırma

Sonuçları görmeden önce şunu yazmıştım:

| Ön tahmin | Sonuç |
|---|---|
| T1 yılın ortalamasında ETAS'ı +0.01 ile +0.05 arası geçer | **Daha iyi çıktı:** +0.065 |
| İlk günlerde fark büyük olur | Doğru: ilk gün +0.17 |
| T0 ilk günlerde zorlanır | Kısmen yanlış: T0 ilk günlerde ETAS'ın biraz önünde, sonraki aylarda geride |
| T2, T1'e yakın olur | Doğru: fark 0.013 |
| "Devam" olasılığı %40–50 | Devam çıktı |

## Dikkat: sonucu zayıflatabilecek noktalar

**Tek dizi, tek yıl.** Test, tek bir dev diziye dayanıyor. 7 günlük blok GA o yılın içindeki
değişkenliği ölçüyor, başka bir büyük dizide sonucun tekrarlanıp tekrarlanmayacağını ölçmüyor.

**ETAS'ın kuyruğu.** Kazancın %44'ü dizi söndükten sonraki aylardan geliyor. Uydurulan Türkiye
ETAS'ının dallanma oranı 1'in üstünde (yaklaşık 1.36) ve p 1.11'e yakın. Bu, uzun vadede çok yavaş
sönen, artçı oranını muhtemelen olduğundan yüksek tahmin eden bir model demek. California'daki
ETAS'ta da aynı durum vardı (dallanma oranı yaklaşık 1.59). Daha iyi kurulmuş bir ETAS bu bölümdeki
farkı daraltabilir. Örnekler: kesilmiş Omori çekirdeği, dallanma oranının 1'in altına
sınırlanması, ana şok sonrası eksik kaydın modellenmesi. Bu varyantlar denenmedi. İlk günlerdeki
kazanç bundan bağımsız görünüyor.

**Ana şok sonrası eksik kayıt.** İlk saatlerde küçük depremlerin bir kısmı kataloğa girmiyor. Bu, ETAS'ı
ve modeli aynı veri üzerinden etkiliyor ama aynı biçimde etkilemiyor olabilir. Model eksik kaydı
diğer katalogların büyük dizilerinden öğrenmiş olabilir, ETAS'ın böyle bir mekanizması yok. Bu bir
haksızlık değil, ama "model depremin fiziğini daha iyi biliyor" anlamına da gelmiyor. Kazancın bir
kısmı katalog davranışını öğrenmekten gelebilir.

**T2 tam anlamıyla "Türkiye'yi hiç görmemiş" değil.** T2 Türkiye olaylarını eğitim hedefi olarak hiç
görmedi. Ama Türkiye'nin 2021–2023 doğrulama verisi, eğitimin hangi adımda durdurulacağını seçmek
için kullanıldı. Testte de önceki 512 Türkiye olayı bağlam olarak giriyor.

**Mc yüksek.** Ön kayıtlı kural 2008'in tamlığı yüzünden Mc'yi 3.0 verdi. 2012'den sonra katalog
2.2'ye kadar tam görünüyor. Daha düşük eşik çok daha fazla olay ve muhtemelen daha keskin bir
ayrım verirdi. Denenmedi.

**Büyüklük ölçeği karışık.** KOERI'nin xM sütunu her olay için verilen büyüklüklerin en büyüğü
(çoğunlukla ML, büyük olaylarda Mw). Ek kataloglar da farklı ölçekler kullanıyor (JMA Mj, INGV ML/Mw,
GeoNet ML/Mw, ComCat karışık). Model hepsini "Mc'nin üstünde kaç birim" olarak görüyor.

**2012 öncesi "Deprem" süzgeci yok.** KOERI formundaki olay türü seçimi 2012 ve sonrası için geçerli.
2006–2011 verisinde patlatmalar da olabilir. Bu dönem eğitim ve geçmiş bölümünde, testte değil.

**Ek katalogların Mc'si.** JMA, INGV ve GeoNet eşikleri ikinci testte 2024–2025 verisi de
kullanılarak seçilmişti. Burada bu kataloglar 2023 öncesine kesildi, ama eşik aynı kaldı. Bu yalnızca
eşik seçimini etkiliyor, Türkiye hakkında bilgi taşımıyor.

**Yalnızca zaman.** Model ve ETAS yalnızca bir sonraki depremin zamanını tahmin ediyor. Konum yok.
Operasyonel bir artçı tahmini için "nerede" sorusu da gerekiyor.

## Başarısız ya da sapan şeyler

- **AFAD kataloğu alınamadı.** AFAD'ın API'si (`deprem.afad.gov.tr/apiv2/event/filter`, servisnet'e
  yönlendiriyor) her tarih aralığına boş liste döndürdü. KOERI kullanıldı.
- **KOERI sorgu kısıtları.** Yıllık sorgu boş yanıt verdi, bu yüzden aylık sorgulara geçildi. Hız için
  açılan ikinci paralel indirme süreci yarım yanıtlara yol açtı (sunucu eşzamanlı sorguyu
  kaldırmıyor). Süreç durduruldu. Yarım yanıtlar satır sayısı denetimiyle yakalandı ve yeniden
  istendi. Son veride uyarı yok.
- **İlk ETAS kodu çok yavaştı.** Otomatik türevli ilk sürümde tek olabilirlik hesabı 2 dakika sürdü.
  Bu hızla uydurma saatler alacaktı, iş durduruldu. Profil olabilirlik + EM + Nelder-Mead ile yeniden
  yazıldı. Yeni sürümde bir uydurma yaklaşık 1 dakika.
- **İkinci testin ETAS karşılaştırması düzeltildi.** Yeni ETAS, EarthquakeNPP'ninkinden güçlü çıktı.
  İkinci testin "M1 ETAS'ı +0.062 geçiyor" sonucu bu ETAS'a karşı +0.031'e indi. Yalnız California
  (M0) ve katı varyant (M5) bu ETAS'ı geçmiyor. `RAPOR_2.md`'ye eklendi.
- **Şekil 1'in ilk sürümünde** ilk gün paneli yalnızca 2 bloktan bootstrap GA gösteriyordu. Bu panel
  "30 gün sonrası" ile değiştirildi, ilk gün sonuçları tabloda tohum değerleriyle verildi.

## Sunucu

İşler GPU 0, 1 ve 3'te çalıştı, her GPU'da tek süreç vardı:
- GPU 0: ETAS ve T0
- GPU 1: T1
- GPU 3: T2

Koşu başına süre 30–60 saniye. Bittikten sonra sunucudaki 37 çıktı dosyası Mac'tekilerle SHA-256 ile
karşılaştırıldı, hepsi aynıydı. Ardından sunucudaki proje klasörü silindi . Sunucuda bu
projeden bir şey kalmadı.

## Sonraki adımlar (öneri, yapılmadı)

1. **Daha güçlü ETAS varyantları.** Kesilmiş Omori çekirdeği, dallanma oranı 1'in altına sınırlı ETAS,
   ana şok sonrası eksik kaydı modelleyen ETAS. Kazancın 30 gün sonrası bölümü bunlara karşı da
   duruyor mu?
2. **Daha düşük eşik.** 2012 sonrası Türkiye verisiyle Mc = 2.2 varyantı.
3. **Başka gerçek ileriye dönük diziler.** Aynı düzenle başka diziler de sınanabilir: Noto 2024
   (Japonya, M7.5), Hualien 2024 (Tayvan) ve 2023–2025 arasındaki diğer büyük diziler. Her birinde
   eğitim o dizinin öncesinde kesilir.
4. **Operasyonel çıktı.** "Önümüzdeki 24 saatte M ≥ 5 olasılığı" gibi tahminlerin kalibrasyonu ve
   ETAS'la karşılaştırması.
5. **Konum.** Modeli konum da tahmin edecek biçimde genişletmek ve GEM fay veritabanını eklemek.
6. **AFAD kataloğu.** API çalıştığında daha yoğun bir Türkiye kataloğuyla aynı test.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_3.md` | Ön kayıt |
| `kod/indir_koeri.py` | KOERI indirme ve ayrıştırma |
| `kod/hazirla_tr.py` | `veri/turkiye.npz`, `veri/ek_tr.npz`, `sonuclar/tr_veri_ozeti.json` |
| `kod/etas_zaman.py` | Zamansal ETAS |
| `kod/egit.py` | Model ve eğitim (`--ana` seçeneği eklendi) |
| `kod/analiz3.py` | Tablolar, karar, şekiller |
| `kod/etas_kiyas_ca.py` | İkinci testin yeni ETAS'a karşı kıyası |
| `kod/c3_g0.cmd`, `c3_g1.cmd`, `c3_g3.cmd`, `etas_ca.cmd` | Sunucu işleri |
| `veri/koeri/koeri_2006_2024.csv`, `veri/koeri/ham/` | KOERI kataloğu (ayrıştırılmış ve ham) |
| `sonuclar/etas_tr/`, `sonuclar/etas_ca_dogrulama/` | ETAS uydurmaları ve test TLL'leri |
| `sonuclar/c3_T{0,1,2}_t{1,2,3}/` | Koşular (kayit.json, test.npz, en_iyi.pt) |
| `sonuclar/c3_ozet.json`, `sonuclar/c3_tablolar.md` | Sonuç özeti |
| `kayitlar/indir_koeri.log`, `c3_g*.log`, `etas_*.log` | Günlükler |

Veri kaynakları: KOERI (Boğaziçi Üniversitesi Kandilli Rasathanesi ve Deprem Araştırma Enstitüsü)
deprem kataloğu; ikinci testteki kaynaklar (EarthquakeNPP/ComCat, JMA, INGV, GeoNet) için
`RAPOR_2.md`.
