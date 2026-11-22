# Literatür notları (değerlendirme ayrıntıları)

21 Kasım 2026. Kaynaklar web sayfalarından okundu; "[özet]" işaretli yerler makalenin
birebir metninden değil, sayfanın otomatik özetinden geliyor, doğrulanmadı.

## EarthquakeNPP (Stockman, Lawson, Werner; arXiv 2410.08226v3, TMLR 2026)

- Kod: github.com/ss15859/EarthquakeNPP (MIT). Katalog depoda: `Datasets/ComCat/ComCat_catalog.csv`
  (sütunlar id, time, longitude, latitude, magnitude, x, y).
- ComCat_25: tüm California poligonu, Mc = 2.5. Yardımcı (yalnız geçmiş) 1971-01-01,
  eğitim 1981-01-01, doğrulama 1998-01-01, test 2007-01-01 → 2020-01-17.
- ETAS: Mizrahi `etas` paketi. `invert_etas.py` eğitim+doğrulama dönemine (1981–2007) uyduruyor,
  `predict_etas.py` → `ETASLikelihoodCalculation.evaluate()`.
- Ölçüt (etas/evaluation.py, birebir okundu): test penceresindeki her olay için
  `TLL_i = log λ*(t_i) − ∫_{t_{i-1}}^{t_i} λ*(s) ds`, λ* bölgeye integre edilmiş yoğunluk,
  birim **gün**. Rapor edilen `tll` bunların test olayları üzerinden ortalaması (olay başına).
  Geçmiş 1971'den itibaren tüm olayları içeriyor. Büyüklük log-olabilirliği hesaplanmıyor.
- ComCat_25 ETAS sonucu (`output_data_ComCat_25/ll_scores.json`): tll = 1.4343, Poisson tll = 0.5126.
  Olay başına değerler `augmented_catalog.csv` içindeki `TLL` sütununda (21 889 test olayı).
  Depo README'si test için 23 059 olay diyor; ETAS dosyasındaki sayı 21 889. Farkın nedeni
  bulunamadı (büyük olasılıkla 0.1'e yuvarlama ve poligon süzgeci). Biz ETAS dosyasındaki olay
  kümesini kullanıyoruz, böylece karşılaştırma olay olay eşleşik.
- Sinir ağı modelleri (NSTPP, DeepSTPP, AutoSTPP, DSTPP, SMASH) 3 tohumla. Son 20 olaylık pencere
  [özet]. Makalenin metnine göre ETAS zamansal log-olabilirlikte hep en iyi [özet].
- Büyük deprem dönemleri ayrı bir tabloda verilmiyor. Ek E.1'de kümülatif bilgi kazancı
  grafikleri var; en büyük düşüşler 2010 El Mayor-Cucapah M7.2 ve 2019 Ridgecrest M7.1
  dizilerinde (birebir alıntı okundu).

## Fusion (Xiong ve ark., arXiv 2608.18791v2, Kasım 2026)

"Scaling-law-informed neural point processes for earthquake sequence forecasting".
- Veri: AVN 2016–2017 (İtalya) ve EarthquakeNPP'nin beş kataloğu.
- Hedef eşik M_d = 3.0; girdi eşiği M_cut ayrıca değiştiriliyor (ComCat'te en düşük 2.5).
- Zamansal LL: `(1/N_d) Σ [log λ − Λ]`, olay başına. Büyüklük LL ayrı. Konum yok.
- Bağlam: son L = 20 olay (LSTM).
- **Eşik uyuşmazlığı:** kıyas tablosunda Fusion'ın düşük M_cut sonucu, ETAS'ın M_cut = 3.0
  sonucuyla yan yana konuyor. Aynı M_cut = 3.0'da Fusion ComCat, SCEDC ve Campotosto'da ETAS'ın
  altında. ComCat: ETAS (3.0) −2.4091, Fusion (2.5) −2.3538 ± 0.0118, Fusion (3.0) −2.4385 ± 0.0642
  [tablo değerleri özet ve gövde metninden; makaleyle teyit edilmeli].
  Bu sayılar bizim tll ile doğrudan kıyaslanamaz (farklı hedef eşik ve muhtemelen farklı zaman birimi).
- Büyüklük: Gutenberg–Richter ötesinde tutarlı kazanç yok (yazarların kendi sonucu).
- Ana şoktan sonraki dönem için ayrı olabilirlik değerlendirmesi yok (Ek A yalnız Omori betimlemesi).

## Tian, Stockman, Zhang, Werner (2026), Earth's Future 14(8) e2025EF007318

"Can Domain-Informed Design Improve Neural Spatio-Temporal Point Processes for Earthquake
Forecasting?" DOI 10.1029/2025EF007318.
- Yalnız Crossref özeti okunabildi (Wiley sayfası HTTP 403). Çin Deprem Ağları kataloğu,
  DeepSTPP; büyüklüğü girdi yapmak, yardımcı eğitim dönemi, daha uzun geçmiş, farklı eşikler.
- Özet: yardımcı dönem özellikle hemen sonraki artçılarda yardımcı oluyor; kısa bellek ve
  "dikkat seyrelmesi" büyüklük ve uzun geçmişin yararını sınırlıyor; uzay-zaman toplamında ETAS'ın
  altında, düşük eşiklerde zamansal tahminde ETAS'ı geçiyor.
- Eşik değerleri, bölünmeler ve sayılar okunamadı. Zenodo paketi: 10.5281/zenodo.16745818 (açılmadı).
- Bizim için ders: uzun geçmişin yararı "dikkat seyrelmesi" yüzünden kaybolabilir; bu testte
  tam olarak bunu ölçüyoruz.
