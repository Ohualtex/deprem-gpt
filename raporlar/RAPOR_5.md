# Deprem GPT, beşinci adım: ilk saatlerdeki kazanç nereden geliyor

21 Kasım 2026. Önceki adım: `RAPOR_4.md`. Orada çok katalog modelinin (T1) ana şoktan sonraki ilk günde
kâhin ETAS'ı da geçtiği görülmüştü (+0.134 nat/olay). Bu adım keşif amaçlı. Yeni model eğitilmedi,
devam/dur kuralı yok. Üçüncü testin modelleri ve dördüncü testin ETAS'ları ayrıştırıldı.

## Kısa cevap

Kazanç ne M7.6'yı önceden sezmekten ne de ETAS'ın eksik kayıt yüzünden fazla olay beklemesinden
geliyor. Kaynağı, dev bir dizinin **gözlenen** artçı oranını saat saat daha iyi tutturmak:

- **Türkiye'ye uydurulmuş ETAS ilk saatlerde az olay bekliyor.** Katalog eksik olduğu halde böyle.
  Ana şoktan sonraki 48 saatte 935 deprem gözlendi; alt kritik ETAS (E2) 780 bekliyordu, T1 860.
  ETAS'ın büyüklük-üretkenlik ilişkisi Türkiye'nin küçük ve orta depremlerinden öğreniliyor ve M7.8'e
  taşınınca artçı sayısını az buluyor. Yalnızca Türkiye'yle eğitilen model (T0) da aynı biçimde az
  bekliyor (600). Bu büyüklükte bir diziyi hiç görmedi.
- **Kâhin ETAS toplam sayıyı tutturuyor, zamana dağılımını tutturamıyor.** Test yılında uydurulan
  ETAS 48 saatte 945 bekliyor, gözlenene çok yakın. Ama ilk saatte fazla (Λ = 1.19), 1–9 saatte az
  (0.80–0.81), M7.6'dan sonraki üç saatte yine fazla (1.52) bekliyor. Tek bir Omori eğrisi ve tek bir
  üretkenlik katsayısı, eksik kaydın biçimlendirdiği gözlenen oranı izleyemiyor.
- **T1 neredeyse her aralıkta 1'e yakın.** 0.86–1.04 arası; tek istisna 1–3 saat aralığında 0.76.
  Diğer katalogların büyük dizilerinden (JMA'da Tōhoku ve diğerleri) büyük bir dizinin kayıtta nasıl
  göründüğünü öğrenmiş görünüyor.
- **Büyüklük tahmininde de aynı iz var.** İlk saatte kaydedilen depremlerin hepsi M ≥ 3.5. T1
  bunları sabit bir Gutenberg-Richter dağılımından olay başına **+2.04 nat** daha iyi tahmin ediyor,
  T0 +1.28. Model, büyük bir şoktan hemen sonra kayda giren depremlerin büyük olacağını öngörüyor.
  Eksik kaydın beklenen izi bu.
- **M7.6'nın kendisi fark yaratmıyor.** M7.6 anında T1 ile alt kritik ETAS arasındaki fark +0.2 nat.
  Diğer büyük olaylarda da fark ±0.2 içinde. Kazanç tek tek büyük şoklarda değil, yüzlerce artçıya
  yayılmış.

## Yöntem

Olay başına zamansal log-olabilirlik iki parçaya ayrılabilir:

    TLL_i = log λ(t_i) − Λ_i,    Λ_i = ∫_{t_(i−1)}^{t_i} λ(s) ds

- **ETAS için** bu ayrıştırma doğrudan yapılabiliyor (`kod/etas_ayristir.py`, Mac). Saklanan TLL ile
  en büyük fark 4e−13.
- **Model için** bir sonraki olaya kadar geçen sürenin dağılımı kullanılıyor. Tehlike oranı
  h = p / S, birikimli tehlike H = −log S, burada S hayatta kalma olasılığı. Böylece
  TLL_i = log h(Δt_i) − H(Δt_i) (`kod/model_ayristir.py`, sunucuda GPU 0). Saklanan TLL ile en büyük
  fark 1e−6 (bf16 kaynaklı).
- **Λ_i'nin yorumu:** Λ_i zaman yeniden ölçekleme kalıntısı. Doğru bir modelde ortalaması 1. 1'den
  büyükse model o aralıkta gözlenenden fazla, küçükse az olay bekliyor.
- **Tamlık:** ham KOERI (M ≥ 2.0) verisinden, dizi kutusunda, zaman aralıklarına göre en büyük
  eğrilikle (MAXC) ölçüldü.

## Tamlık: ilk saatlerde katalog ne kadar eksik

| Ana şoktan sonra | Olay (M ≥ 3.0) | Ort. M | Ham M ≥ 2 | MAXC | M ≥ 3 içinde 3.0–3.4 oranı |
|---|---:|---:|---:|---:|---:|
| 0–1 saat | 27 | 4.56 | 25 | 3.8 | 0.00 |
| 1–3 saat | 74 | 3.94 | 73 | 3.7 | 0.11 |
| 3–9 saat | 160 | 3.66 | 189 | 3.4 | 0.43 |
| 9–12 saat (M7.6 sonrası) | 69 | 4.35 | 68 | 3.9 | 0.06 |
| 12–24 saat | 264 | 3.76 | 298 | 3.3 | 0.34 |
| 1–3 gün | 565 | 3.52 | 1 117 | 2.9 | 0.54 |
| 3–30 gün | 1 392 | 3.47 | 7 013 | 2.0 | 0.62 |
| 30 gün sonrası | 1 711 | 3.44 | 10 273 | 2.0 | 0.67 |

Tam bir katalogda M ≥ 3 depremlerin yaklaşık üçte ikisi 3.0–3.4 arasında (son satır). İlk saatte bu
oran sıfır. Katalog ancak üçüncü günden sonra M 3.0'ın altında tam.

## Oran kalibrasyonu: ortalama Λ

| Ana şoktan sonra | E2 (alt kritik ETAS) | E4 (kâhin ETAS) | T0 | T1 | T2 |
|---|---:|---:|---:|---:|---:|
| 0–1 saat | 0.68 | 1.19 | 0.63 | 0.94 | 0.96 |
| 1–3 saat | 0.56 | 0.81 | 0.64 | 0.76 | 0.93 |
| 3–9 saat | 0.66 | 0.80 | 0.65 | 0.86 | 0.97 |
| 9–12 saat | 1.06 | 1.52 | 0.62 | 0.99 | 1.06 |
| 12–24 saat | 0.89 | 1.11 | 0.61 | 0.91 | 1.02 |
| 1–3 gün | 0.89 | 0.96 | 0.72 | 0.99 | 1.15 |
| 3–30 gün | 1.05 | 0.98 | 0.88 | 0.99 | 1.10 |
| 30 gün sonrası | 1.26 | 1.01 | 0.73 | 1.04 | 1.03 |

Türkiye'yi eğitimde hiç görmeyen T2 de ilk saatlerde iyi kalibre (0.93–0.97). Bu, büyük dizi
davranışının diğer kataloglardan geldiğini destekliyor.

## T1 − ETAS farkının ayrışması (nat/olay)

| Ana şoktan sonra | −E2: log λ | −E2: −Λ | −E2: TLL | −E4: log λ | −E4: −Λ | −E4: TLL |
|---|---:|---:|---:|---:|---:|---:|
| 0–1 saat | +0.411 | −0.258 | +0.153 | −0.162 | +0.251 | +0.089 |
| 1–3 saat | +0.433 | −0.200 | +0.233 | +0.068 | +0.042 | +0.110 |
| 3–9 saat | +0.375 | −0.197 | +0.178 | +0.176 | −0.055 | +0.121 |
| 9–12 saat | +0.029 | +0.075 | +0.104 | −0.338 | +0.534 | +0.196 |
| 12–24 saat | +0.151 | −0.014 | +0.137 | −0.065 | +0.202 | +0.137 |
| 1–3 gün | +0.166 | −0.100 | +0.066 | +0.091 | −0.035 | +0.056 |
| 3–30 gün | −0.055 | +0.061 | +0.006 | +0.010 | −0.010 | +0.000 |
| 30 gün sonrası | −0.173 | +0.219 | +0.046 | +0.031 | −0.029 | +0.002 |

**Alt kritik ETAS'a (E2) karşı ilk 9 saat.** Kazanç, depremlerin geldiği anlarda daha yüksek yoğunluk
vermekten geliyor (log λ +0.4). Model daha çok olay beklediği için integral cezası artıyor (−0.2), ama
net kazanç pozitif.

**Kâhin ETAS'a (E4) karşı.** Kazancın biçimi değişiyor:
- **İlk saat ve M7.6 sonrası:** kâhin fazla olay beklediği için integral cezası yiyor (+0.25 ve +0.53
  T1 lehine).
- **1–9 saat:** iki yönden de biraz önde.

**30 gün sonrası.** E2'ye karşı kazanç, E2'nin fazla olay beklemesinden geliyor (Λ = 1.26). Kâhine
karşı sıfır. Bu, dördüncü adımdaki bulguyla aynı.

## Büyük olayların kendisi

| Olay | Ana şoktan sonra | Önceki olaydan bu yana | TLL E2 | TLL E4 | TLL T1 (3 tohum) |
|---|---:|---:|---:|---:|---|
| M7.8 | 0 | 61.5 dk | +1.22 | +0.60 | +1.08 (+1.05, +1.19, +1.02) |
| M6.6 | 0.18 saat | 1.4 dk | +5.52 | +5.87 | +5.65 |
| M7.6 | 9.12 saat | 3.2 dk | +5.06 | +5.11 | +5.28 |
| M6.0 | 10.74 saat | 3.6 dk | +4.90 | +4.63 | +5.46 |
| M6.4 | 14.7 gün | 13.7 dk | +3.25 | +3.30 | +3.12 |

Ana şokun kendisinde model önceden bir işaret görmüyor. 61.5 dakikalık sessizlikten sonra gelmesine ETAS
ile aynı düzeyde, hatta biraz daha düşük olasılık veriyor. M7.6'yı da "sezmiyor". Fark küçük ve tek
yönlü değil.

## Büyüklük tahmini (sabit Gutenberg-Richter'e göre, nat/olay)

Taban: Türkiye eğitim döneminden (2008–2020) kestirilen b = 1.14 ile sabit bir Gutenberg-Richter
dağılımı.

| Ana şoktan sonra | GR | T0 − GR | T1 − GR | T2 − GR |
|---|---:|---:|---:|---:|
| 0–1 saat | −5.557 | +1.277 | +2.040 | +1.906 |
| 1–3 saat | −3.930 | +0.797 | +0.857 | +0.835 |
| 3–9 saat | −3.204 | +0.236 | +0.321 | +0.312 |
| 9–12 saat | −4.998 | +1.253 | +1.479 | +1.453 |
| 12–24 saat | −3.468 | +0.419 | +0.496 | +0.484 |
| 1–3 gün | −2.824 | +0.071 | +0.103 | +0.097 |
| 3–30 gün | −2.708 | +0.042 | +0.069 | +0.067 |
| 30 gün sonrası | −2.619 | +0.026 | +0.042 | +0.038 |

Bu karşılaştırma modeller lehine eğik. Sabit GR, eksik kaydı hesaba katmayan en basit taban.
Zamana bağlı tamlık eşiğiyle düzeltilmiş bir GR (Helmstetter tipi) çok daha güçlü bir rakip olurdu.
Bu denenmedi. Sonuç olarak şu söylenebilir: modeller büyük şokların hemen ardından büyüklük
dağılımının yukarı kaydığını öğrenmiş. Bu sabit GR'ye karşı bir kazanç; eksik kaydı modelleyen
bir ETAS'a karşı üstünlük olduğu henüz gösterilmiş değil.

## Bunun anlamı

1. **Makale için bulgu.** Çok katalogla eğitilen Transformer, dev bir dizinin ilk saatlerinde gözlenen
   oranı (eksik kayıt dahil) tek bölgeye uydurulmuş ETAS'tan da, kâhin ETAS'tan da daha iyi izliyor.
   Üstünlük, ETAS'ın tek Omori eğrisi ve tek üretkenlik katsayısıyla tutturamadığı zamansal biçimden
   geliyor.
2. **Dürüst sınır.** Bu üstünlüğün bir kısmı depremin fiziğinden değil, kataloğun kayıt davranışından
   öğreniliyor olabilir. Gerçek bir operasyonel tahminde bu yine işe yarar, çünkü tahmin edilen şey
   kataloğa girecek depremlerdir. Ama "model artçı fiziğini daha iyi biliyor" demek için eksik kaydı
   modelleyen bir ETAS'a karşı sınamak gerekiyor.
3. **Önceden sezme yok.** Model ana şoku ya da M7.6'yı öngörmüyor. Artçı tahmini yapıyor, deprem
   kehaneti değil.

## Sonraki adımlar (öneri, yapılmadı)

1. **Eksik kaydı modelleyen ETAS.** Helmstetter tipi zamana bağlı Mc(t) ile inceltilmiş bir ETAS ve
   GR. Katsayılar Türkiye'nin 2023 öncesi büyük dizilerinden (Van 2011, Elazığ 2020, Sisam 2020)
   kestirilir. İlk saatlerdeki kazancın ne kadarının kaldığını gösterir.
2. **Daha yüksek eşikte değerlendirme.** Örneğin M ≥ 4.0, ilk saatlerde de büyük ölçüde tam. Modeller
   M ≥ 3.0 ile eğitildi, bu yüzden bağlam ve hedef kaymasıyla ilgili dikkatli bir kurulum gerekir.
3. **Başka ileriye dönük diziler** (Noto 2024, Hualien 2024). Bu bulgunun tek diziye özgü olup
   olmadığını gösterir.

## Sunucu

Model ayrıştırması GPU 0'da tek süreçle çalıştı (yaklaşık 2 dakika). Sunucudaki 20 dosya Mac'tekilerle
SHA-256 ile karşılaştırıldı, hepsi aynıydı. Bunlar Mac'ten gönderilen model ağırlıkları, kod ve veri,
bir de sonuç dosyası ile günlük. sunucudaki proje klasörü silindi.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `kod/etas_ayristir.py` | ETAS'ın olay başına log λ ve Λ ayrıştırması (Mac) |
| `kod/model_ayristir.py` | Modellerin tehlike oranı, birikimli tehlike, PIT, medyan (sunucu) |
| `kod/analiz5.py` | Tablolar ve şekil |
| `kod/c5_g0.cmd` | Sunucu işi |
| `sonuclar/c5_etas_ayristirma.npz`, `sonuclar/c5_model_ayristirma.npz` | Ayrıştırmalar |
| `sonuclar/c5_ozet.json`, `sonuclar/c5_tablolar.md` | Özet |
| `sekiller/c5_sekil1_ilk_saatler.{png,pdf}` | (a) gözlenen ve beklenen olay sayısı, (b) Λ kalibrasyonu, (c) büyüklük tahmini |
| `kayitlar/c5_g0.log` | Günlük |
