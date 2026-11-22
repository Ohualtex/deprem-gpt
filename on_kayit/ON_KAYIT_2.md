# Ön kayıt 2: çok katalog testi (eğitimden önce yazıldı, 21 Kasım 2026)

Soru: Aynı küçük modeli California'nın yanında Japonya, İtalya ve Yeni Zelanda kataloglarıyla da
eğitmek, California test döneminde zamansal tahmini iyileştiriyor mu? İlk testte darboğazın veri
olduğu görüldü (model birkaç yüz adımda aşırı öğreniyor). Bu test onu sınıyor.

Bu dosya ek kataloglar hazırlandıktan (olay sayıları ve tamlık eşikleri bilinirken), ama hiçbir
model bu verilerle eğitilmeden ve sonuç görülmeden yazıldı.

## Ek veri (`kod/hazirla_cok.py`, `sonuclar/ek_veri_ozeti.json`)
| Katalog | Dönem | Bölge | Eşik | Olay |
|---|---|---|---|---:|
| Japonya, JMA (yalnız J kayıtları, F/N bayrakları hariç) | 2000–2024 | 30–46°K, 128–148°D | M ≥ 3.0 | 108 699 |
| İtalya, INGV (yalnız "earthquake") | 2005–2025 | 35–48°K, 6–19°D | M ≥ 2.8 | 8 871 |
| Yeni Zelanda, GeoNet (yalnız "earthquake") | 2012–2025 | 48–34°G, 165–179°D | M ≥ 3.3 | 8 524 |

- Derinlik ≤ 70 km. Büyüklük 0.1'e yuvarlandı ve katalog eşiğine göre göreli verildi (M − Mc).
  California'da bu zaten M − 2.5 idi.
- Eşik kuralı: ön seçilen eşik (Japonya 3.0, İtalya 2.5, Yeni Zelanda 3.0) ile her yılın en büyük
  eğrilik + 0.2 değerinin büyüğü. İtalya ve Yeni Zelanda verisi zaten 2.5 ve 3.0'dan kesilerek
  indirildiği için bu denetim orada gerçek tamlığı ölçemiyor, yalnızca eşiği 0.3 yükseltiyor.
  Bu muhafazakâr sonuç olduğu gibi bırakıldı.
- Hiçbir ek katalog California bölgesiyle örtüşmüyor. Ek kataloglar California test dönemini
  (2007–2020) zaman olarak kapsıyor. Bu, California hakkında bilgi sızdırmaz ama ileriye dönük bir
  tahmin düzeninde olmayacak bir şeydir. Bunun için katı varyant (M5) var.

## Koşular (hepsi 3 tohum; California doğrulama 1998–2007 ile erken durdurma; test aynı)
| Kod | Veri | Model | L |
|---|---|---|---:|
| M0 | Yalnız California (ilk testin L = 512 ayarı, yeni kodla yeniden) | küçük (0.83 M) | 512 |
| **M1 (birincil)** | California + 3 katalog | küçük | 512 |
| M2 | California + 3 katalog | büyük (d = 256, 6 katman, 8 baş) | 512 |
| M3 | Yalnız California | büyük | 512 |
| M4 | California + 3 katalog | küçük | 4096 |
| M5 | California + yalnız 2007 öncesi ek veri (katı) | küçük | 512 |

Eğitim pencereleri tüm kataloglardan olay sayısıyla orantılı çekilir, pencereler katalog sınırını
aşmaz. California eğitim hedefleri yine 1981–1998. Diğer ayarlar ilk testtekiyle aynı.

## Ölçüt ve belirsizlik
İlk testteki gibi: California test olaylarında olay başına zamansal log-olabilirlik (gün), ETAS ile
olay olay eşleşik. 30 günlük blok bootstrap %95 GA, tohum eşleşik farklar.

## Karar kuralı
- **Devam:** M1 − M0 ≥ 0.03 nat/olay (tüm test), GA sıfırı dışlıyor ve üç tohum eşleşik farkın
  üçü de pozitif; **ve** M1 ya da M2, tüm testte ETAS'ı GA'sı sıfırı dışlayarak geçiyor.
- **Dur:** M1 − M0 < 0.01 ya da GA sıfırı içeriyor; **ve** M2 − M3 < 0.01.
- Arası "belirsiz".
- İkincil: büyük deprem sonrası 30 gün (ilk testteki tanım), M5'in M1'e göre durumu, M4 − M1.
