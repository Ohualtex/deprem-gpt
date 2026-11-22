# Deprem GPT, yedinci adım: Noto 2024 testi

21 Kasım 2026. Önceki adımlar: `RAPOR_3.md` (Kahramanmaraş), `RAPOR_4.md` ve `RAPOR_6.md` (güçlendirilmiş
ETAS'lar). Bu testin ön kaydı `ON_KAYIT_7.md`, eğitimden ve ETAS uydurmalarından önce yazıldı.

## Karar: TEKRARLANDI

Kahramanmaraş'taki bulgu ikinci bir ileriye dönük dizide, üstelik daha zor bir rakibe karşı tekrarlandı.
Ön kayıtlı kuralın üç koşulu da sağlandı:

1. **Tüm test yılı:** Çok katalog modeli (J1), en güçlü geçerli ETAS'ı (E5, havuzlu + kesik Omori)
   2024 boyunca **+0.073 nat/olay** geçiyor. 7 günlük blok %95 GA [+0.034, +0.096], üç tohum
   +0.072, +0.070, +0.077.
2. **Noto'dan sonraki ilk gün:** **+0.191** [+0.110, +0.242] (1 saatlik blok GA), üç tohum +0.188,
   +0.183, +0.201.
3. **Ek kataloglar:** J1 yalnız Japonya modelini (J0) geçiyor: +0.016. Üç tohum eşleşik farkın üçü de
   pozitif (+0.006, +0.036, +0.007). Ama bu farkın 7 günlük blok GA'sı [−0.000, +0.027], sıfıra
   değiyor.

**Kâhin ETAS'a karşı.** Test yılında uydurulan ETAS (E4) da J1'in gerisinde: tüm yılda +0.051
[+0.030, +0.094], ilk günde +0.047 [+0.001, +0.085]. Kahramanmaraş'ta tüm yıl farkı kâhine karşı
belirsizdi, burada sıfırı dışlıyor.

## Kahramanmaraş'tan farkı

Japonya'da ETAS'ın elinde büyük diziler var: eğitim döneminde 25 tane M ≥ 7, Tōhoku dahil. Buna
rağmen sonuç aynı yönde, ama mekanizmanın bir kısmı değişiyor:

- **Yalnız Japonya modeli (J0) de ETAS'ı geçiyor.** Tüm yılda E5'e karşı +0.056, ilk günde +0.148.
  Türkiye'de yalnız Türkiye modeli ETAS'ın gerisindeydi. Japonya kataloğu büyük dizileri içerdiği
  için model bunları kendi verisinden öğrenebiliyor.
- **Ek katalogların katkısı küçülüyor.** J1 − J0 tüm yılda +0.016 (Türkiye'de T1 − T0 +0.087). İlk
  günde +0.042 [+0.016, +0.062], 7 günde +0.039 [+0.020, +0.047]. Yani diğer kataloglar burada en
  çok büyük dizinin ilk günlerinde işe yarıyor.
- **Japonya'yı eğitim hedefi olarak görmeyen model (J2)** J0'ın biraz gerisinde (−0.007), ama ETAS'ı
  yine geçiyor (E5'e karşı +0.050). İlk günde J0'dan iyi (+0.023).
- **ETAS'ın üretkenlik katsayısı.** Japonya'da a = 1.13–1.25. Türkiye'deki 2023 öncesi ETAS'ta ≈ 1.0
  idi. Kâhinde a = 1.65, Türkiye kâhininde 2.70. Yani Japon ETAS'ı büyük dizinin üretkenliğini daha
  iyi biliyor, açık daha küçük. Bu, beklentiyle tutarlı.
- **Eksik kayıt.** Japonya'da algılama parametreleri 2024 öncesi veriden uydurulabildi (E7: G = 5.94,
  H = 0.42). Türkiye'de bu mümkün olmamıştı. Ama E7 testte eksik kayıtsız havuzlu ETAS'tan (E5)
  daha zayıf: 2.584'e karşı 2.593. Kâhinde (E8) uydurma algılama kaybını sıfırladı. E8 ile E4 aynı
  sonucu veriyor (2.6152). Japonya'da M ≥ 3.0'da eksik kayıt belirleyici değil.

## Sonuçlar

Olay başına zamansal log-olabilirlik (nat, gün birimi). Modeller 3 tohum ortalaması.

| | Tüm yıl (4 362) | Noto ilk gün (972) | Noto ilk 7 gün (1 444) | Noto kutusu 30 g (1 610) | 30 g sonrası (2 556) | Noto kutusu dışı (2 221) | Hyuganada ilk gün (34) |
|---|---:|---:|---:|---:|---:|---:|---:|
| E0 kısıtsız | 2.573 | 5.985 | 5.174 | 4.763 | 1.207 | 1.109 | 2.654 |
| E1 kesik Omori | 2.572 | 5.968 | 5.161 | 4.751 | 1.211 | 1.113 | 2.659 |
| **E5 havuz + kesik** | **2.593** | 6.083 | 5.242 | 4.823 | 1.203 | 1.096 | 2.645 |
| E7 eksik kayıt (uydurulmuş) | 2.584 | 6.029 | 5.204 | 4.791 | 1.207 | 1.108 | 2.615 |
| E4 kâhin | 2.615 | 6.226 | 5.338 | 4.915 | 1.181 | 1.064 | 1.463 |
| E8 kâhin + eksik kayıt | 2.615 | 6.226 | 5.338 | 4.915 | 1.181 | 1.064 | 1.463 |
| J0 yalnız Japonya | 2.650 | 6.231 | 5.325 | 4.897 | 1.252 | 1.131 | 2.507 |
| **J1 Japonya + diğerleri** | **2.666** | **6.274** | **5.363** | **4.936** | **1.254** | **1.132** | 2.603 |
| J2 yalnız diğerleri | 2.643 | 6.254 | 5.340 | 4.915 | 1.229 | 1.104 | 2.602 |

J1 − ETAS:

| | Tüm yıl (7 g GA) | Noto ilk gün (1 sa GA) | 30 g sonrası (7 g GA) | Noto kutusu dışı (7 g GA) | Hyuganada ilk gün (1 sa GA) |
|---|---|---|---|---|---|
| − E5 | +0.073 [+0.034, +0.096] | +0.191 [+0.110, +0.242] | +0.051 [+0.031, +0.075] | +0.036 [+0.026, +0.047] | −0.042 [−0.127, +0.092] |
| − E7 | +0.082 [+0.022, +0.119] | +0.245 [+0.126, +0.315] | +0.047 [+0.020, +0.082] | +0.024 [+0.015, +0.035] | −0.012 [−0.138, +0.190] |
| − E1 | +0.094 [+0.018, +0.144] | +0.306 [+0.199, +0.370] | +0.043 [+0.014, +0.084] | +0.018 [+0.009, +0.028] | −0.056 [−0.138, +0.067] |
| − E4 kâhin | +0.051 [+0.030, +0.094] | +0.047 [+0.001, +0.085] | +0.073 [+0.042, +0.115] | +0.068 [+0.035, +0.116] | +1.140 [+0.356, +2.055] |

Kaynak: `sonuclar/c7_tablolar.md`, `sonuclar/c7_ozet.json` (`kod/analiz7.py`). Şekiller:
`sekiller/c7_sekil1_etas_varyantlari`, `sekiller/c7_sekil2_kumulatif` (PNG + PDF).

### Kazanç nereden geliyor

J1'in E5'e göre toplam kazancı 317 nat:
- **Noto'nun ilk günü:** 185 nat (972 olay, olay başına +0.19).
- **26 Kasım 2024'teki M6.6 (Noto'nun batı kıyısı):** 46 nat. Bu depremin ilk gününde 141 artçı var;
  J1 bunlarda E5'i olay başına +0.32, kâhini +0.15 geçiyor. Şekil 2'de yıl sonundaki dik çıkış bu.
- **Geri kalan:** 86 nat, yıla yayılmış. Sakin dönemde ve Noto kutusu dışında da J1 her ETAS'ın önünde.

Tek bir olayda J1 ile E5 arasındaki en büyük fark yaklaşık 2 nat. Kazanç tek tük olaylardan değil,
dizilerin bütününden geliyor.

**Hyuganada (M7.1, Ağustos 2024) farklı.** İlk günde yalnızca 34 olay var ve J1, E5'in biraz gerisinde
(−0.042, GA sıfırı içeriyor). Bu, Japonya'nın büyük ama az artçılı bir dalma-batma depremi. Model
burada üstünlük göstermiyor. Kâhin ise çok kötü (1.46): test yılının bütününe uydurulan yüksek
üretkenlik, bu az artçılı dizide çok fazla olay bekliyor.

## Ön kayıttan sapmalar

- **E2 (alt kritik) tamamlanmadı.** İki saatte üç başlangıcın birincisini bile bitiremedi, durduruldu.
  Türkiye'de en güçlü geçerli ETAS buydu. Japonya'da kısıtsız E0'ın testteki dallanma oranı 1.76,
  kesik E1'inki 0.94. E2'nin E5'i geçip geçmeyeceği bilinmiyor. Sonucu değiştirmesi için 2.666'ya
  (J1) yaklaşması gerekirdi. Bu, diğer bütün geçerli varyantlardan (2.57–2.59) çok yüksek ve kâhinin
  (2.615) bile üstünde olurdu.
- **E6 (literatür sabitli eksik kayıt) tamamlanmadı.** İlk denemede GPU belleği yetmediği için çöktü.
  Hesap daha küçük parçalara bölünüp yeniden başlatıldı. Bir saatte bir başlangıç bitti (uydurma TLL
  2.129, E7'nin 2.210'unun altında; E7, G ve H serbest bırakıldığı için E6'yı kapsıyor). Durduruldu.
- Karar bu yüzden E1, E5 ve E7 arasından seçilen en güçlü ETAS'a göre verildi.
- E1, E0 ve E4, E2 GPU 0'ı meşgul ettiği için GPU 3'e taşındı. Sonucu etkilemiyor.

## Dikkat

- **Tek ülke, tek yıl.** Japonya'nın 2024'ü üç dizi içeriyor (Noto, Hyuganada, Kasım M6.6), ama hepsi
  aynı katalogdan. Türkiye ile birlikte iki ileriye dönük test oldu.
- **Konum yok.** Bütün Japonya tek bir zaman dizisi olarak modelleniyor. Noto'nun artçılarıyla
  binlerce kilometre uzaktaki depremler aynı dizide.
- **J1 − J0'ın tüm yıl GA'sı sıfıra değiyor.** Çok katalog eğitiminin Japonya'daki genel katkısı
  küçük. Asıl katkısı büyük dizilerin ilk günlerinde.
- **Hyuganada'da üstünlük yok.** Az artçılı büyük depremlerde modelin avantajı görülmüyor.

## Bunun anlamı

1. **İki ileriye dönük testte de model, denenen bütün ETAS'ları geçti:** Kahramanmaraş 2023 ve Noto
   2024. İlk günde fark büyük (+0.15 ile +0.19), yıl ortalamasında orta (+0.05 ile +0.07).
2. **Çok katalog eğitiminin değeri, bölgenin kendi geçmişine bağlı.** Büyük dizi görmemiş bir bölgede
   (Türkiye) belirleyici; zengin geçmişi olan bir bölgede (Japonya) küçük ama ilk günlerde hâlâ
   anlamlı.
3. **Makale için ana iddia güçlendi.** Bulgu tek diziye özgü değil.

## Sunucu

İşler GPU 0, 1 ve 3'te çalıştı, her GPU'da tek süreç vardı. Bütün sonuçlar Mac'e alındı. Sunucudaki 44
dosya Mac'tekilerle SHA-256 ile karşılaştırıldı, hepsi aynıydı. Kullanıcının isteğiyle sunucudaki proje klasörü
bu kez silinmedi; kullanıcı "bitti" deyince silinecek.

## Sonraki adımlar (öneri, yapılmadı)

1. **Mimari:** konum girdisi, katalog gömmesi, ETAS simülasyonlarıyla ön eğitim. Ön kayıtlı bir testle.
2. **Operasyonel çıktı:** "24 saatte M ≥ 5 olasılığı" türünden tahminler ve kalibrasyonu.
3. **Üçüncü bir ileriye dönük dizi:** Hualien 2024 (Tayvan); yeni katalog ve indirme onayı gerekir.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_7.md` | Ön kayıt |
| `kod/hazirla_jp.py` | `veri/japonya.npz`, `veri/ek_jp.npz`, `sonuclar/jp_veri_ozeti.json` |
| `kod/analiz7.py` | Tablolar, karar, şekiller |
| `kod/etas_eksik.py` | Parça boyu 512'ye indirildi (Japonya'da bellek) |
| `kod/c7_g0.cmd`, `c7_g1.cmd`, `c7_g1b.cmd`, `c7_g3.cmd`, `c7_g3b.cmd` | Sunucu işleri |
| `sonuclar/c7_J{0,1,2}_t{1,2,3}/` | Model koşuları |
| `sonuclar/etas7_{E0,E1,E4,E5,E7,E8}/` | ETAS uydurmaları |
| `sonuclar/c7_ozet.json`, `sonuclar/c7_tablolar.md` | Sonuç özeti |
| `kayitlar/c7_g*.log` | Günlükler |
