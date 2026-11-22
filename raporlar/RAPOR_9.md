# Deprem GPT, dokuzuncu adım: olasılık çıktısı

22 Kasım 2026. Bu adımın ön kaydı `ON_KAYIT_9.md`, benzetimlerden önce yazıldı. Model artık "önümüzdeki
24 saatte bölgede en az bir M ≥ X deprem olma olasılığı %Y" türünden operasyonel tahminler veriyor.
Bu tahminler iki test yılında (Türkiye 2023–2024, Japonya 2024) her gün yayınlanmış gibi üretilip
gerçekleşenlerle karşılaştırıldı.

## Nasıl çalışıyor

Her yayın anında modele o ana kadarki son 512 deprem veriliyor. Model bir sonraki depremin zamanını ve
büyüklüğünü kendi dağılımından çekiyor, bu depremi bağlama ekliyor ve 24 saat dolana kadar böyle
devam ediyor. Bu, bir dil modelinin metin üretmesiyle aynı mantık. Her yayında 1 200 senaryo üretiliyor
(3 tohum × 400). Olasılık, M ≥ X içeren senaryoların oranı. Aynı senaryolardan "beklenen deprem sayısı"
ve %5–95 aralığı da çıkıyor.

ETAS (Türkiye'de alt kritik E2, Japonya'da havuz + kesik Omori E5) aynı yayın zamanlarında 2 000
senaryoyla ileri benzetildi. Kod: `kod/olasilik_model.py` (sunucu), `kod/olasilik_etas.py` (Mac).

## Karar: KARIŞIK

Ön kayıtlı kuralda "daha iyi" için dört hedefin en az üçünde logaritmik skor farkının GA'sının sıfırın
üstünde olması gerekiyordu. İkisinde öyle. Hiçbir hedefte model ETAS'tan anlamlı olarak kötü değil.

| Hedef | Gün | Gözlenen oran | Model ort. olasılık | ETAS ort. olasılık | Log skor: model − ETAS (7 g GA) | Brier: model − ETAS (GA) |
|---|---:|---:|---:|---:|---|---|
| Türkiye, M ≥ 4 | 364 | 0.500 | 0.465 | 0.386 | **+0.033** [+0.013, +0.053] | −0.014 [−0.024, −0.006] |
| Türkiye, M ≥ 5 | 364 | 0.066 | 0.091 | 0.052 | −0.001 [−0.015, +0.015] | −0.000 [−0.003, +0.002] |
| Japonya, M ≥ 4 | 365 | 0.671 | 0.611 | 0.708 | +0.016 [−0.018, +0.052] | −0.000 [−0.012, +0.010] |
| Japonya, M ≥ 5 | 365 | 0.115 | 0.103 | 0.247 | **+0.064** [+0.026, +0.101] | −0.023 [−0.036, −0.010] |

Brier skorunda negatif fark modelin lehine. Kaynak: `sonuclar/c9_tablolar.md`, `sonuclar/c9_ozet.json`
(`kod/analiz9.py`).

**İklim tabanına karşı.** "Her gün aynı olasılık" tahmini de karşılaştırıldı. Bu tabanın olasılığı test
yılının kendi gözlenen oranından alındı, yani taban bu bakımdan kâhin. Logaritmik skor:

| | Model | ETAS | İklim |
|---|---:|---:|---:|
| Türkiye, M ≥ 4 | −0.597 | −0.630 | −0.693 |
| Türkiye, M ≥ 5 | −0.205 | −0.204 | −0.243 |
| Japonya, M ≥ 4 | −0.640 | −0.655 | −0.633 |
| Japonya, M ≥ 5 | −0.343 | −0.407 | −0.357 |

- Model Japonya M ≥ 4 dışında iklim tabanını geçiyor; orada çok az geride.
- ETAS Japonya'nın iki hedefinde de iklim tabanının gerisinde.

## Kalibrasyon: model olasılıkları gerçekçi

**Yıl ortalaması.** Modelin öngördüğü ortalama olasılık gözlenen orana yakın. Öngörülen/gözlenen oranı:

| | Model | ETAS |
|---|---:|---:|
| Türkiye, M ≥ 4 | 0.93 | 0.77 |
| Türkiye, M ≥ 5 | 1.38 | |
| Japonya, M ≥ 4 | 0.91 | |
| Japonya, M ≥ 5 | 0.89 | **2.15** |

ETAS Japonya'da günlük M ≥ 5 olasılığını iki kattan fazla abartıyor. Ön kayıttaki "kalibre değil"
ölçütüne (yarısından az ya da iki katından fazla) model hiçbir hedefte girmiyor.

**Dilimlere göre.** Şekil 1'de görülüyor:
- Model çizgisi köşegene ETAS'tan genellikle daha yakın.
- Türkiye M ≥ 5'te yüksek olasılıklı günlerde (≥ 0.4) model biraz fazla iddialı: 11 günde ortalama 0.6
  olasılık verdi, gözlenen 0.45.
- Yüksek olasılık dilimlerinde gün sayısı çok az (1–11). Bu noktalar gürültülü.

Şekil: `sekiller/c9_sekil1_kalibrasyon`.

## Ana şoktan sonraki ilk üç gün (ikincil, karara katılmadı)

Ana şoktan 1 dakika sonra başlayıp 3 saatte bir yayınlanan tahminler, önümüzdeki 24 saat için. Şekil:
`sekiller/c9_sekil2_artci_tahmini`.

**Kahramanmaraş.**
- **İlk 9 saat:** iki yöntem de ciddi biçimde az deprem bekliyor. Ana şoktan 1 dakika sonra model 100,
  ETAS 59 deprem beklerken 595 oldu. Bu, beşinci adımdaki bulguyla aynı: dev bir dizinin ilk
  saatleri, henüz artçılar görülmeden tahmin edilemiyor.
- **12. saatten sonra:** model gözleneni tutturuyor (24. saatte 310'a karşı 343, 48. saatte 226'ya
  karşı 222). ETAS üç gün boyunca sistematik olarak az bekliyor.
- **Belirsizlik aralıkları:** gözlenen sayı modelin %5–95 aralığına 25 yayının 21'inde (%84) düşüyor.
  ETAS'ın aralığına hiçbirinde düşmüyor (%0). ETAS'ın aralıkları gerçekçi olmayacak kadar dar.
- **P(M ≥ 5):** model ilk iki gün 0.82–1.00 verdi ve her seferinde M ≥ 5 oldu. ETAS 0.25–0.72 verdi.

**Noto.**
- **Model:** 3. saatte fazla bekledi (1 146'ya karşı 595), 6. saatten sonra gözleneni tutturdu.
- **ETAS:** ilk 6 saatte az bekledi, sonra o da tutturdu.
- **Kapsama:** model %96, ETAS %92.
- **P(M ≥ 5):** 12. saatten sonra model 0.4–0.6'ya indi ama M ≥ 5 depremler sürdü. ETAS'ın 0.9–1.0
  tahmini burada daha iyiydi. Modelin büyüklük tahmini Noto dizisinin ikinci ve üçüncü gününde
  M ≥ 5 olasılığını düşük tutuyor.

## Dikkat

- **Taşan senaryolar.** Japonya'nın ikinci tohumunda 13 senaryo (yaklaşık 470 bin içinden) adım sınırına
  (24 saatte 4 000 olay) ulaştı. Model kendi ürettiği artçılarla patlayan bir dizi üretmiş. Oran çok
  küçük, olasılıkları pratikte etkilemiyor. Ama otoregresif benzetimin kendi hatalarını büyütebileceğini
  gösteriyor.
- **Konum yok.** Olasılıklar bütün bölge için. Operasyonel bir ürün "nerede" sorusunu da cevaplamalı.
- **Aynı iki test seti.** Bu test setleri önceki adımlarda da kullanıldı. Ancak bu adımda model ve ETAS
  yeniden eğitilmedi, yalnızca yeni bir çıktı biçimi sınandı.
- **İlk saatler.** Dev bir ana şoktan hemen sonra yayınlanan tahminler iki yöntemde de güvenilir değil.
  Operasyonel kullanımda ilk birkaç saat tahminlerin sık güncellenmesi gerekir. Bu, USGS'nin
  uygulamasıyla da uyumlu.

## Bunun anlamı

1. **Model artık kullanılabilir bir çıktı veriyor.** "24 saatte M ≥ 5 olasılığı", beklenen deprem sayısı
   ve belirsizlik aralığı.
2. **Olasılıkları iyi kalibre.** Yıl ortalamasında gözlenene yakın. ETAS'tan genellikle daha iyi;
   Japonya M ≥ 5'te ve Türkiye M ≥ 4'te anlamlı olarak.
3. **En değerli farkı belirsizlik aralıkları.** Kahramanmaraş'ta ETAS'ın aralıkları gözleneni hiç
   kapsamadı, modelinkiler %84 kapsadı.
4. **Ön kayıtlı kurala göre "açıkça daha iyi" denemiyor.** Dört hedefin ikisinde fark anlamlı değil.

## Sunucu

Model benzetimleri GPU 0 (Türkiye) ve GPU 1'de (Japonya) çalıştı; tohum başına 11–23 dakika. ETAS
benzetimleri Mac'te birkaç saniye sürdü. Sunucudaki 159 dosya Mac'tekilerle SHA-256 ile
karşılaştırıldı, hepsi aynıydı. sunucudaki proje klasörü kullanıcının isteğiyle duruyor.

## Sonraki adımlar (öneri, yapılmadı)

1. **Konum:** modelin olayın yerini de tahmin etmesi, haritalı olasılık.
2. **Hızlandırma:** benzetimde dikkat önbelleği (KV cache). Şu an her adım 512 olayı yeniden işliyor;
   operasyonel kullanımda dakikalar yerine saniyeler gerekir.
3. **Üçüncü bir ileriye dönük dizi** (Hualien 2024).

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_9.md` | Ön kayıt |
| `kod/olasilik_model.py` | Modelden otoregresif Monte Carlo (sunucu) |
| `kod/olasilik_etas.py` | ETAS ileri benzetimi (Mac) |
| `kod/analiz9.py` | Skorlar, kalibrasyon, karar, şekiller |
| `kod/c9_TR.cmd`, `kod/c9_JP.cmd` | Sunucu işleri |
| `sonuclar/c9_{TR,JP}_model/senaryo_t{1,2,3}.npz` | Model senaryoları |
| `sonuclar/c9_{TR,JP}_etas/` | ETAS senaryoları ve parametreler |
| `sonuclar/c9_ozet.json`, `sonuclar/c9_tablolar.md` | Sonuç özeti |
| `sekiller/c9_sekil1_kalibrasyon.{png,pdf}`, `sekiller/c9_sekil2_artci_tahmini.{png,pdf}` | Şekiller |
| `kayitlar/c9_TR.log`, `kayitlar/c9_JP.log` | Günlükler |
