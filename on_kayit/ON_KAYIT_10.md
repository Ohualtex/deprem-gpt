# Ön kayıt 10: konum çıktısı (hiçbir model ya da uzaysal ETAS uydurulmadan yazıldı, 22 Kasım 2026)

Soru: Model, bir sonraki depremin zamanı ve büyüklüğünün yanında **yerini** de tahmin edebilir mi? Bu
konum tahmini, uzaysal ETAS'ın aynı türden tahmininden iyi mi? Konum çıktısı eklemek zaman tahminini
bozuyor mu?

## Model S (`kod/egit3.py`, bayrak `--konum_cikti`)
- **Girdi:** mimari testindeki A2 ile aynı. Zaman ve büyüklüğe ek olarak katalog merkezine göre konum
  (x, y, 1000 km birimi), önceki olaya uzaklığın logaritması ve konum bayrağı.
- **Yeni çıkış:** bir sonraki olayın konumu için 16 bileşenli iki boyutlu Gauss karışımı. Ortalamalar
  **son olayın konumuna göre** öteleme olarak üretiliyor (bf16 hassasiyeti nedeniyle). Standart
  sapmalar 0.5 km ile 2 000 km arasında sınırlı.
- **Kayıp:** −(TLL + MLL + SLL). SLL olay başına uzaysal log-olabilirlik.
- **Erken durdurma:** doğrulama döneminde TLL + SLL.
- **Diğer ayarlar:** T1/J1 ile aynı (küçük model, L = 512, ek kataloglar). Her testte 3 tohum.

## Uzaysal ETAS (`kod/etas_uzay.py`)
- **Zaman bileşeni** sabit: Türkiye E2, Japonya E5.
- **Uzay çekirdeği** (Ogata 1998 / Mizrahi vd. 2021 biçimi), r km cinsinden:

      f(r | m) = (ρ/π) · D(m)^ρ / (r² + D(m))^(1+ρ),   D(m) = d · e^(γ m)

- **Arka plan u(x):** eğitim dönemi olaylarının izotropik Gauss çekirdek yoğunluğu, bant genişliği h km.
- **Koşullu uzaysal yoğunluk:** olay zamanı t_i verildiğinde

      p(x_i | t_i) = [μ u(x_i) + Σ_j g_j(t_i) f(x_i − x_j | m_j)] / [μ + Σ_j g_j(t_i)]

  Burada g_j, sabit zamansal ETAS'ın tetikleme terimi. Böylece ETAS'ın toplam log-olabilirliği
  TLL + SLL olarak ayrılıyor.
- **Uydurma:** d, γ, ρ ve h, eğitim döneminden rastgele seçilen 5 000 olayda (sabit tohum) en büyük
  olabilirlikle uyduruluyor. Bu olayların bütün geçmişi hesaba giriyor. Değerlendirme bütün test
  olaylarında.

## Ölçüt
- **Birincil:** olay başına SLL (km² başına yoğunluğun logaritması), model S − uzaysal ETAS. Test yılının
  tamamında, 7 günlük blok GA.
- **İkincil:**
  - ana şoktan sonraki ilk gün (1 saatlik blok GA)
  - toplam TLL + SLL
  - S'nin TLL'si, aynı testteki A0'a (mimari testi tabanı) göre
  - yalnız arka plan (u(x)) tabanına göre SLL

## Karar kuralı
- **Konum tahmini daha iyi:** iki testte de S − uzaysal ETAS SLL farkı > 0 ve GA sıfırı dışlıyor.
- **Daha kötü:** iki testte de < 0 ve GA sıfırı dışlıyor.
- Arası "karışık".
- **Ayrıca:** S'nin tüm yıl TLL'si A0'dan 0.01'den fazla düşükse "konum çıktısı zaman tahminini
  bozuyor" diye raporlanır.

## İkincil çıktı (karara katılmaz)
Model senaryolarına konum örneklemesi eklenir. Ana şoktan 12 saat sonra yayınlanan tahminde, önümüzdeki
24 saat için deprem yoğunluğu haritası çıkarılır ve gerçekleşen depremler üzerine çizilir. Bu, haritalı
artçı tahmini örneği.
