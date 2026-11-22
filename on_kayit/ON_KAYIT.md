# Ön kayıt (eğitimden önce yazıldı, 21 Kasım 2026)

Bu dosya model eğitilmeden ve test sonucu görülmeden yazıldı. Sonradan değiştirilirse
değişiklik ve nedeni RAPOR.md'de yazılacak.

## Veri
- Olay kümesi: EarthquakeNPP ETAS çıktısındaki `augmented_catalog.csv` (ComCat, M ≥ 2.5,
  büyüklük 0.1'e yuvarlı, California poligonu). 92 263 olay.
- Yardımcı (yalnız geçmiş) < 1981-01-01; eğitim hedefleri 1981–1998; doğrulama 1998–2007;
  test 2007-01-01 → 2020-01-17 (21 889 olay). Bu, kıyas setindeki sinir ağı protokolüyle aynı.
  ETAS ise 1981–2007'ye uydurulmuş (doğrulama dönemini de görmüş).

## Ölçüt
- Birincil: olay başına zamansal log-olabilirlik, gün biriminde,
  `TLL_i = log p(Δt_i | geçmiş)`. Bu, ETAS'taki `log λ*(t_i) − ∫ λ*` ile aynı nicelik.
  Her test olayı için bağlam tam olarak önceki L olay (L = 20, 512, 4096).
- Karşılaştırma olay olay eşleşik: fark_i = TLL_i(model) − TLL_i(ETAS).
- Belirsizlik: 3 tohum (ortalama ± standart sapma) ve olay farklarının 30 günlük bloklarla
  blok bootstrap %95 güven aralığı (2000 yeniden örnekleme).
- İkincil: büyüklük log-olabilirliği, 0.1'lik bölmelerde, ETAS'ın β = 2.147 değeriyle
  Gutenberg–Richter'e karşı.

## Büyük deprem sonrası yoğun dönem (birincil tanım)
Test penceresindeki her M ≥ 6.0 olaydan sonraki 30 gün (ana şokun kendisi hariç, birleşim):
2010-01-10 M6.5 (açık deniz, Eureka), 2010-04-04 M7.2 (El Mayor-Cucapah), 2014-03-10 M6.8
(açık deniz), 2014-08-24 M6.0 (Napa), 2019-07-04 M6.4 ve 2019-07-06 M7.1 (Ridgecrest).
Ek kırılımlar: yalnız M ≥ 7 dizileri; ana şoktan sonraki ilk 1 gün ve ilk 7 gün; dizi dizi.

## Karar kuralı
- **Devam:** (a) tüm testte TLL(4096) − TLL(20) ≥ 0.05 nat/olay ve %95 GA sıfırı dışlıyor;
  ve (b) yoğun dönemde ETAS ile aradaki açık L = 20'den L = 4096'ya en az yarı yarıya kapanıyor
  ya da model ETAS'ı geçiyor.
- **Dur:** tüm testte |TLL(4096) − TLL(20)| < 0.02 ya da GA sıfırı içeriyor.
- Arada kalan durumlar "belirsiz" diye raporlanacak.
- Ölçek için: ETAS'ın Poisson'a göre kazancı 1.434 − 0.513 = 0.92 nat/olay.

## Model (sabit, üç bağlamda aynı)
Decoder-only transformer, d = 128, 4 katman, 4 baş, MLP 4×, dropout 0.1, pre-LN.
Girdi jetonu: (log10 Δt, M − 2.5). Konum: başın yarısında olay sırasıyla, yarısında olay
zamanıyla döndürme (RoPE). Çıktı: log Δt için 16 bileşenli Gauss karışımı (log-normal karışım),
büyüklük için 0.1'lik bölmelerde kategorik dağılım. Adım başına 16 384 hedef jeton, en çok
4000 adım, doğrulama zamansal LL'sine göre erken durdurma.
