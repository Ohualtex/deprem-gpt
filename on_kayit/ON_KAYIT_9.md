# Ön kayıt 9: olasılık çıktısı ve kalibrasyonu (benzetimlerden önce yazıldı, 22 Kasım 2026)

Soru: Model, "önümüzdeki 24 saatte bölgede en az bir M ≥ X deprem olma olasılığı" türünden operasyonel
tahminler üretebilir mi? Bu olasılıklar gerçekleşenlerle tutarlı mı (kalibre mi), ve ETAS'ın aynı
türden tahminlerinden daha iyi mi?

## Tahmin
- **Yayın zamanları:** her test yılında her gün 00:00 UTC.
  - Türkiye: 2023-02-06'dan başlayarak 365 tahmin. İlk tahmin ana şoktan 1 saat 17 dakika önce
    yayınlanıyor.
  - Japonya: 2024-01-01'den başlayarak 366 tahmin.
- **Hedefler (Mc = 3.0 kataloglarında, bütün bölge):** önümüzdeki 24 saatte en az bir M ≥ 4.0
  olayı, en az bir M ≥ 5.0 olayı.
- **Model (`kod/olasilik_model.py`):** üçüncü ve yedinci testin birincil modelleri (T1 ve J1, 3 tohum).
  - Her yayın zamanında, o ana kadarki son 512 olay bağlam olarak giriyor.
  - Model kendi örnekleriyle adım adım ileri yürütülüyor (otoregresif Monte Carlo): her adımda bir
    sonraki olayın zamanı karışım dağılımından, büyüklüğü sınıf dağılımından çekiliyor.
  - İlk adımda son olaydan yayın zamanına kadar olay olmadığı bilgisi kullanılıyor (dağılım
    t0 − t_son'dan kesiliyor).
  - Her tohumda 400, toplam 1 200 senaryo. Olasılık, M ≥ X içeren senaryoların oranı.
- **ETAS (`kod/olasilik_etas.py`):** en güçlü geçerli ETAS'lar, parametreler sabit.
  - Türkiye için E2 (alt kritik).
  - Japonya için E5 (havuz + kesik Omori, Japonya arka planı).
  - Geçmiş olayların tetiklemesi, arka plan ve kademeli artçılarla ileri benzetim yapılıyor. Her
    yayında 2 000 senaryo.
  - Büyüklükler Gutenberg-Richter'den (b ilgili ülkenin eğitim döneminden, üst sınır M 9.0) çekiliyor.

## Skorlar
- **Logaritmik skor:** olay başına ortalama log olasılık (gerçekleşen sonuca verilen olasılığın
  logaritması). Olasılıklar [1e−4, 1 − 1e−4] aralığına kırpılıyor. Yüksek olan daha iyi.
- **Brier skoru:** düşük olan daha iyi.
- **Kalibrasyon:** olasılık dilimlerine göre öngörülen ve gözlenen sıklık; yıl ortalamasında
  öngörülen ve gözlenen oran.
- **Belirsizlik:** model − ETAS farkları için 7 günlük blok bootstrap %95 GA.

## Karar kuralı
- **Daha iyi:** dört hedefte (2 ülke × 2 eşik) logaritmik skor farkı (model − ETAS) en az üçünde
  pozitif ve GA sıfırı dışlıyor; hiçbirinde GA sıfırın tamamen altında değil.
- **Daha kötü:** en az ikisinde GA sıfırın altında.
- Arası "karışık".
- Ayrıca kalibrasyon raporlanır. Model kalibre değilse (yıl ortalamasında öngörülen oran gözlenenin
  yarısından az ya da iki katından fazla) bu açıkça yazılır.

## İkincil (karara katılmaz)
Ana şoklardan sonraki 3 gün boyunca 3 saatte bir yayınlanan tahminler (önümüzdeki 24 saatte M ≥ 5),
gözlenenle birlikte çizilir. USGS tipi artçı tahmini örneği.
