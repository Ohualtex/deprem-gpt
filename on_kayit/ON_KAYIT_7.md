# Ön kayıt 7: Noto 2024 testi (eğitimden ve ETAS uydurmasından önce yazıldı, 21 Kasım 2026)

Soru: Kahramanmaraş testindeki bulgu ikinci bir ileriye dönük dizide tekrarlanıyor mu? Kahramanmaraş'tan
farklı olarak Japonya'nın geçmişinde büyük diziler bol: eğitim döneminde 25 tane M ≥ 7 var, Tōhoku
(M 9.0) dahil. Japon ETAS'ı büyük dizilerin üretkenliğini kendi verisinden öğrenebilir. Bu yüzden
modelin "büyük dizileri başka kataloglardan öğrenme" avantajının burada küçülmesi beklenebilir. Daha
zor bir sınav.

Veri hazırlandı (`kod/hazirla_jp.py`, `sonuclar/jp_veri_ozeti.json`). Hiçbir model ya da ETAS bu
düzenle henüz eğitilmedi.

## Veri
- **Katalog:** JMA, ikinci testteki hazırlığın aynısı (J kayıtları, F/N hariç, 30–46°K, 128–148°D,
  derinlik ≤ 70 km), Mc = 3.0. İkinci testten beri JMA için kullanılan eşik; yıllık MAXC + 0.2
  değerleri 2002–2023 boyunca bunun altında.
- **Bölümler:**

  | Bölüm | Dönem | Olay |
  |---|---|---:|
  | Geçmiş (yalnızca bağlam) | 2000–2001 | 9 316 |
  | Eğitim | 2002–2020 | 85 530 |
  | Doğrulama | 2021 – 2024-01-01 | 9 491 |
  | Test | 2024-01-01 – 2025-01-01 | 4 362 |

- **Noto ana şoku:** 2024-01-01 07:10:22 UTC, M 7.6. Noto kutusu 36.5–38.0°K, 136.0–138.0°D.
- **Kümeler:** Noto'dan sonraki ilk gün 972 olay, ilk 30 günde kutu içinde 1 610 olay. Kutu dışında
  2 221 olay.
- **Hyuganada:** 2024-08-08, M 7.1. İkincil küme olarak değerlendiriliyor.
- **Ek kataloglar (`veri/ek_jp.npz`), hepsi 2024-01-01 öncesi:** California, INGV, GeoNet ve Türkiye
  (KOERI, M ≥ 3.0). Türkiye kataloğu Kahramanmaraş dizisini de içeriyor.

## Koşular (hepsi küçük model, L = 512, 3 tohum, Japonya doğrulamasıyla erken durdurma)
| Kod | Eğitim hedefleri |
|---|---|
| J0 | Yalnızca Japonya 2002–2020 |
| **J1 (birincil)** | Japonya 2002–2020 + ek kataloglar |
| J2 | Yalnızca ek kataloglar. Japonya yalnızca bağlam ve erken durdurma için |

## ETAS varyantları (Japonya 2002 – 2024-01-01 uydurması, 2000–2001 geçmiş)
| Kod | Tanım | Kod dosyası |
|---|---|---|
| E0 | Kısıtsız Omori | `etas_guclu.py` |
| E1 | Kesik Omori | `etas_guclu.py` |
| E2 | Alt kritik (n ≤ 0.99) | `etas_guclu.py` |
| E5 | Havuz + kesik: Japonya + ek kataloglar | `etas_guclu.py` |
| E6 | Alt kritik + algılama, literatür G = 4.5, H = 0.75 | `etas_eksik.py` |
| E7 | Alt kritik + algılama, G ve H uydurulur | `etas_eksik.py` |
| E4 | Kâhin, test yılında uydurulur | `etas_guclu.py` |
| E8 | Kâhin + algılama, test yılında uydurulur | `etas_eksik.py` |

## Karar kuralı
"En güçlü geçerli ETAS" = E1, E2, E5, E6, E7 içinde **test** TLL'si en yüksek olan (ETAS lehine seçim).
- **Tekrarlandı:** üç koşul birlikte sağlanıyor:
  - J1 − en güçlü geçerli ETAS tüm test yılında > 0, 7 günlük blok %95 GA sıfırı dışlıyor;
  - Noto'dan sonraki ilk günde J1 − en güçlü geçerli ETAS > 0, 1 saatlik blok GA sıfırı dışlıyor;
  - J1 − J0 > 0, üç tohumun üçünde de pozitif.
- **Tekrarlanmadı:** J1 − en güçlü geçerli ETAS tüm test yılında ≤ 0 **ve** ilk günde ≤ 0.
- Arası "kısmen".
- İkincil:
  - J2 (Japonya'yı eğitim hedefi olarak görmeyen model)
  - kâhin E4 ve E8'e karşı farklar
  - Hyuganada'dan sonraki ilk gün
  - Noto kutusu dışı
  - üretkenlik katsayısı a: Japonya ETAS'ında Türkiye'dekinden (≈ 1.0) büyük mü?
