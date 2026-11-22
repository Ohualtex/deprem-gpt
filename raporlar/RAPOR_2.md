# Deprem GPT, ikinci test: çok katalogla eğitim

21 Kasım 2026. Önceki test: `RAPOR.md` (uzun bağlam için "dur"). Bu testin ön kaydı: `ON_KAYIT_2.md`
(ek kataloglar hazırlandıktan sonra, eğitimden önce yazıldı).

## Sonradan eklenen düzeltme: daha güçlü bir ETAS'a karşı (21 Kasım 2026, Kahramanmaraş testi hazırlanırken)

Kahramanmaraş testi için kendi zamansal ETAS kodumu yazdım (`kod/etas_zaman.py`, Ogata 1988,
doğrudan zamansal olabilirliği en büyükleyen uydurma). Kodu sınamak için California'da EarthquakeNPP
ile aynı dönemde (1981–2007) uydurdum. Bu ETAS California testinde **1.465** veriyor.
EarthquakeNPP'nin ETAS'ı ise 1.434 veriyordu, yani fark +0.031. Fark büyük depremlerden sonra
büyüyor: M≥6 sonrası ilk günde +0.28. Aşağıdaki "ETAS'ı geçiyor" sonuçları EarthquakeNPP'nin
ETAS'ına göre. Daha güçlü ETAS'a karşı tablo şöyle (30 günlük blok GA; diziler için 1 günlük blok):

| | Tüm test | M≥6 sonrası 30 g | M≥6 sonrası 1 g | Sakin dönem | Ridgecrest |
|---|---|---|---|---|---|
| M1 − ETAS (bizim) | **+0.031** [+0.024, +0.038] | +0.040 [+0.008, +0.052] | +0.087 [+0.050, +0.113] | +0.028 [+0.022, +0.035] | +0.043 [−0.030, +0.073] |
| M0 − ETAS (bizim) | −0.021 [−0.079, +0.018] | −0.115 [−0.249, +0.026] | −0.271 [−0.452, +0.039] | +0.012 [+0.006, +0.018] | −0.287 [−0.415, −0.001] |
| M5 − ETAS (bizim) | −0.002 [−0.046, +0.027] | −0.073 [−0.167, +0.039] | −0.165 [−0.297, +0.071] | +0.022 [+0.016, +0.029] | −0.195 [−0.276, +0.004] |

Kaynak: `sonuclar/c2_etas_zaman_kiyas.json` (`kod/etas_kiyas_ca.py`), ETAS uydurması
`sonuclar/etas_ca_dogrulama/etas.json`.

Bunun anlamı:
- Birincil model M1, daha güçlü ETAS'ı da GA'sı sıfırı dışlayarak geçiyor, ama kazanç +0.062'den
  +0.031'e iniyor.
- Yalnızca California'yla eğitilen model (M0) ve yalnızca 2007 öncesi ek veriyle eğitilen katı
  varyant (M5) bu ETAS'ı geçmiyor.
- Ön kayıtlı karar kuralı EarthquakeNPP'nin ETAS'ına göre yazılmıştı, karar o kurala göre DEVAM
  olarak kalıyor. Ama "ETAS'ı geçiyor" sonucu artık yalnızca test dönemini kapsayan ek veriyle
  eğitilen modeller için geçerli. Bu yüzden Kahramanmaraş testi (`RAPOR_3.md`) asıl sınav oluyor.

## Karar: DEVAM

Ön kayıtlı kuralın iki koşulu da sağlandı.

1. Aynı küçük modeli California'ya ek olarak Japonya, İtalya ve Yeni Zelanda kataloglarıyla eğitmek
   (M1) California test döneminde zamansal log-olabilirliği **+0.052 nat/olay** artırıyor
   (%95 GA [+0.014, +0.110]). Üç tohumun üçünde de kazanç pozitif: +0.049, +0.038, +0.069.
   Eşik 0.03 idi.
2. M1 tüm testte ETAS'ı **+0.062 nat/olay** geçiyor (%95 GA [+0.016, +0.104]). İlk testte hiçbir
   ana koşu ETAS'ı GA'sı sıfırı dışlayarak geçememişti.

Kazancın çoğu büyük depremden hemen sonra geliyor. Ana şoktan sonraki ilk günde M1, ETAS'ı
+0.36 nat/olay geçiyor. Ridgecrest 2019'da California'yla eğitilen model ETAS'ın 0.13 altındaydı,
çok katalogla eğitilen model 0.20 üstünde. Model büyütmenin (M2, M3) ve bağlamı 4096'ya
çıkarmanın (M4) bir yararı yok. Fark yaratan şey veri.

Aşağıdaki "Dikkat" bölümünde bu sonucun neden henüz kesin sayılmaması gerektiği yazılı. En önemlisi
şu: ek kataloglar California test dönemini (2007–2020) de kapsıyor. Bu dönemi dışlayan katı
varyantta kazanç üçte bire iniyor.

## Veri

Kullanıcı onayıyla indirildi (21 Kasım 2026): JMA `h2000.zip`–`h2024.zip` (128.8 MB),
INGV FDSN 2005–2025 M ≥ 2.5 (2.9 MB), GeoNet FDSN 2012–2025 M ≥ 3.0 (6.2 MB).
Hazırlık `kod/hazirla_cok.py`, özet `sonuclar/ek_veri_ozeti.json`.

| Katalog | Dönem | Bölge, derinlik | Eşik | Olay | M ≥ 6 |
|---|---|---|---|---:|---:|
| Japonya, JMA | 2000–2024 | 30–46°K, 128–148°D, ≤ 70 km | 3.0 | 108 699 | 302 |
| İtalya, INGV | 2005–2025 | 35–48°K, 6–19°D, ≤ 70 km | 2.8 | 8 871 | 4 |
| Yeni Zelanda, GeoNet | 2012–2025 | 48–34°G, 165–179°D, ≤ 70 km | 3.3 | 8 524 | 19 |

- Büyüklük her katalogda eşiğe göre göreli (M − Mc). California'da bu M − 2.5.
- Eşik kuralı (ön seçilen eşik ile yıllık en büyük eğrilik + 0.2 değerinin büyüğü) İtalya ve
  Yeni Zelanda'da eşiği 0.3 yükseltti. Bu iki katalog zaten 2.5 ve 3.0'dan kesilerek indirildiği
  için denetim orada gerçek tamlığı ölçemiyor. Sonuç muhafazakâr kaldı (daha az veri).
- Ek veri toplam 126 094 olay. California eğitim hedefleri 40 701, yani yaklaşık üç kat.
- INGV'den gelen dosyalarda küresel olaylar, GeoNet'ten gelenlerde "ağ ilgisi dışında" olaylar da
  vardı. Bölge kutusu ve olay türü süzgeci bunları ayıkladı.
- Hiçbir ek katalog California bölgesine dokunmuyor. California doğrulama ve test olayları değişmedi.

## Sonuçlar

### Tablo 1. California test zamansal log-olabilirliği (nat/olay, gün birimi; 3 tohum ortalama ± ss)

| Koşu | Tüm test (21 889) | M ≥ 6 sonrası 30 gün (5 634) | M ≥ 6 sonrası 1 gün (2 321) | Dizi dışı (16 255) | El Mayor 2010 M7.2, 30 gün | Ridgecrest 2019 M7.1, 30 gün |
|---|---:|---:|---:|---:|---:|---:|
| ETAS | 1.434 | 4.073 | 5.588 | 0.520 | 3.950 | 4.755 |
| M0 California, küçük | 1.444 ± 0.015 | 4.100 ± 0.047 | 5.592 ± 0.128 | 0.524 ± 0.006 | 4.110 ± 0.001 | 4.625 ± 0.108 |
| **M1 Çok katalog, küçük** | **1.496 ± 0.002** | **4.255 ± 0.009** | **5.950 ± 0.014** | **0.540 ± 0.001** | 4.132 ± 0.007 | 4.955 ± 0.012 |
| M2 Çok katalog, büyük | 1.488 ± 0.005 | 4.239 ± 0.017 | 5.921 ± 0.041 | 0.535 ± 0.001 | 4.126 ± 0.015 | 4.933 ± 0.046 |
| M3 California, büyük | 1.437 ± 0.011 | 4.102 ± 0.031 | 5.600 ± 0.073 | 0.514 ± 0.006 | 4.108 ± 0.008 | 4.629 ± 0.064 |
| M4 Çok katalog, küçük, L = 4096 | 1.486 ± 0.008 | 4.220 ± 0.021 | 5.874 ± 0.048 | 0.539 ± 0.005 | 4.126 ± 0.005 | 4.880 ± 0.050 |
| M5 Katı (yalnız 2007 öncesi ek veri) | 1.463 ± 0.004 | 4.142 ± 0.010 | 5.698 ± 0.022 | 0.534 ± 0.002 | 4.113 ± 0.003 | 4.717 ± 0.023 |

Küçük model 0.83 M parametre, büyük model 4.85 M. Bağlam L = 512 (M4 hariç).
Kaynak: `sonuclar/c2_ozet.json`, `sonuclar/c2_tablolar.md`. ETAS: ilk testteki gibi
`veri/earthquakenpp/Experiments/ETAS/output_data_ComCat_25/augmented_catalog.csv`.

### Tablo 2. Karar için farklar (nat/olay; 30 günlük blok bootstrap %95 GA; tohum eşleşik farklar)

| Fark | Tüm test | M ≥ 6 sonrası 30 gün | Dizi dışı | Tohum eşleşik (tüm test) |
|---|---|---|---|---|
| **M1 − M0** (veri etkisi, küçük model) | **+0.052 [+0.014, +0.110]** | +0.155 [+0.022, +0.290] | +0.016 [+0.011, +0.021] | +0.049, +0.038, +0.069 |
| M2 − M3 (veri etkisi, büyük model) | +0.051 [+0.017, +0.105] | +0.137 [+0.005, +0.261] | +0.021 [+0.015, +0.026] | +0.053, +0.039, +0.060 |
| M3 − M0 (model büyütme, yalnız California) | −0.007 [−0.011, −0.003] | +0.002 [−0.006, +0.007] | −0.010 [−0.013, −0.007] | −0.008, −0.009, −0.003 |
| M4 − M1 (bağlam 4096, çok katalog) | −0.010 [−0.023, −0.001] | −0.035 [−0.064, −0.006] | −0.002 [−0.003, +0.000] | −0.021, −0.002, −0.008 |
| M5 − M0 (katı ek veri) | +0.018 [+0.007, +0.034] | +0.042 [−0.003, +0.081] | +0.010 [+0.007, +0.013] | +0.019, +0.005, +0.032 |
| M1 − M5 | +0.034 [+0.005, +0.077] | +0.113 [+0.011, +0.211] | +0.006 [+0.003, +0.010] | +0.030, +0.033, +0.037 |
| **M1 − ETAS** | **+0.062 [+0.016, +0.104]** | +0.182 [+0.008, +0.217] | +0.020 [+0.011, +0.030] | – |
| M2 − ETAS | +0.054 [+0.010, +0.093] | +0.167 [−0.007, +0.204] | +0.015 [+0.006, +0.025] | – |

Yoğun dönem GA'ları yalnız 10 bloğa dayanıyor, kaba okunmalı. Tek dizi satırları için 1 günlük blok
GA'ları `sonuclar/c2_tablolar.md` içinde. Şekiller: `sekiller/c2_sekil1_etas_farki.png` (ETAS'a göre
farklar), `sekiller/c2_sekil2_kumulatif.png` (kümülatif kazanç), `sekiller/c2_sekil3_dogrulama.png`
(doğrulama eğrileri).

### Gözlemler
- **Aşırı öğrenme gecikti.** Doğrulamada en iyi adım M0'da 200–300, M1'de 400–600. Büyük model
  California'yla tek başına 200. adımdan sonra hızla bozuluyor (M3), çok katalogla bozulmuyor (M2).
  Kaynak: `sonuclar/c2_M*_t*/kayit.json`.
- **Tohumlar arası değişkenlik azaldı.** Tüm testte ss M0'da 0.015, M1'de 0.002.
- **Kazancın yeri.** M1'in ETAS'a göre toplam kazancı 1 358 nat (tohum ortalaması, olay farklarının
  toplamı). Bunun 544'ü Ridgecrest'in 30 gününden, 474'ü El Mayor-Cucapah'ın 30 gününden, 10'u
  diğer M ≥ 6 dizilerinden, 330'u dizi dışı dönemden geliyor. El Mayor'daki kazancın çoğu M0'da da
  vardı. M0'dan farkı asıl Ridgecrest yaratıyor.
- **Büyüklük.** Büyüklük log-olabilirliği M0'da −2.5610, M1'de −2.5535 (GR −2.5834). Küçük bir
  iyileşme. İlk testte yazılan kayıt eksikliği uyarısı burada da geçerli.
- **Tekrarlanabilirlik.** M0, ilk testteki L = 512 ayarının yeni kodla yeniden koşusu. Ortalama
  1.444 ± 0.015, ilk testte 1.446 ± 0.011. GPU belirsizliği ve yeni pencere örnekleme yolu yüzünden
  sayılar birebir aynı değil, ama aynı aralıkta.

## Dikkat: sonucu zayıflatabilecek noktalar

- **Zaman örtüşmesi.** Ek kataloglar California test dönemini (2007–2020) kapsıyor. Tōhoku 2011,
  Kumamoto 2016, Kaikōura 2016 ve Amatrice–Norcia 2016 dizileri eğitimde var. Bu California
  hakkında bilgi sızdırmıyor (farklı bölgeler), ama gerçek bir ileriye dönük tahminde model bu
  dizileri henüz görmemiş olurdu. Yalnız 2007 öncesi ek veriyle (M5, 23 832 olay) kazanç +0.018'e
  iniyor. Bu düşüşün ne kadarı daha az veriden, ne kadarı test dönemindeki büyük dizilerden
  geliyor, bu deneyle ayrılamaz. Bugünden ileriye bakan bir model için bu sorun yok: bugüne kadarki
  tüm veri zaten kullanılabilir.
- **İki büyük dizi.** Test döneminde yalnız iki M7 dizisi var ve kazancın büyük kısmı onlardan
  geliyor. Bir dizinin davranışı sonucu çok değiştirebilir.
- **ETAS yalnız California'yla uydurulmuş.** Karşılaştırılan ETAS, EarthquakeNPP'nin kendi çıktısı.
  Diğer bölgelerden bilgi alan bir ETAS (ör. ortak parametre önsel dağılımları) bu farkı
  daraltabilir. Bu denenmedi.
- **Yalnız zaman.** Konum yok. ETAS'ın uzaysal gücüyle bir karşılaştırma yapılmadı.
- **Büyüklük ölçekleri farklı.** JMA (Mj/Mv), INGV (çoğu ML) ve GeoNet büyüklükleri aynı ölçek
  değil. Eşiğe göre göreli büyüklük bunu kısmen dengeliyor.

## Başarısız ya da sapan şeyler
- İtalya ve Yeni Zelanda eşikleri ön seçilen değerin 0.3 üstünde kaldı (yukarıda açıklandı).
- Ön kayıttan sapma yok. Ön kayıtta olmayan tek ek inceleme, kazancın diziler arasındaki dökümü.
- Duman testi (`duman_c2`, 40 adım) yalnız kodu denemek içindi ve silindi.

## Sunucu
Hesaplar H100 makinesinde GPU 0, 1 ve 3'te yapıldı (her GPU'da tek süreç, 18 koşu, her biri
0.5–3.5 dakika). Sonuçlar tek arşivle Mac'e alındı (166 208 000 bayt, SHA-256 karşılaştırıldı,
57 dosya). Sunucudaki kod ve veri Mac'teki kopyalarla aynıydı. Sonra sunucudaki proje klasörü silindi.
Tek kopya Mac'te.

## Sonraki adımlar (test geçti)
1. **Zaman örtüşmesini kapatan test.** Modeli yalnız belirli bir tarihten önceki tüm katalog
   verisiyle eğitip, o tarihten sonraki bir dönemde sınamak. Örnek: tüm kataloglar 2019 öncesi,
   test Ridgecrest dahil 2019–2020 California. Ya da daha temiz olanı: hiç görülmemiş bir bölgede
   sınamak.
2. **Türkiye, Kahramanmaraş 2023.** Türkiye'yi hiç görmemiş, 6 Şubat 2023 öncesi verilerle
   eğitilmiş model. Zamansal kısım bugünkü modelle hemen sınanabilir: M7.8'den sonraki 9 saatte
   olay hızını ETAS'tan iyi tahmin ediyor mu? AFAD ya da KOERI kataloğu gerekir (indirmeden önce
   onay). Başka bir fay kolundaki M7.5 sorusu için konum gerekiyor.
3. **Konum ve fay bilgisi.** Jetona konum ve GEM Global Active Faults bilgisini eklemek. Bu,
   ETAS'la uzay-zaman toplamında karşılaştırmayı da mümkün kılar.
4. **Daha çok katalog.** Ek veri arttıkça kazancın sürüp sürmediğine bakmak (ör. Japonya'yı daha
   düşük eşikle, SCEDC'nin 2007 öncesini, Türkiye'yi eklemek). Model büyütme bu ölçekte yararsız
   çıktı, önce veri artırılmalı.

## Dosyalar
| Dosya | İçerik |
|---|---|
| `ON_KAYIT_2.md` | Bu testin ön kaydı |
| `kod/hazirla_cok.py` | JMA, INGV, GeoNet → `veri/ek_kataloglar.npz` (`--kati` ile `ek_kataloglar_kati.npz`) |
| `kod/egit.py` | `--ek` seçeneğiyle ek katalog desteği (California indeksleri değişmez) |
| `kod/analiz2.py` | Tablolar, karar, şekiller |
| `kod/c2_g*.cmd` | H100 iş dosyaları |
| `veri/jma/`, `veri/ingv/`, `veri/geonet/` | İndirilen ham kataloglar |
| `sonuclar/c2_M*_t*/` | Koşu başına `kayit.json`, `test.npz`, `en_iyi.pt` |
| `sonuclar/c2_ozet.json`, `sonuclar/c2_tablolar.md` | Bu rapordaki tüm sayılar |
| `kayitlar/c2_g*.log` | Sunucu günlükleri |

Kaynak gösterimi: JMA Birleşik Hiposantr Kataloğu (Japonya Meteoroloji Ajansı, Public Data License
1.0); INGV deprem kataloğu (CC BY 4.0); GeoNet (GNS Science, CC BY 3.0 NZ); EarthquakeNPP
(Stockman ve ark., MIT).
