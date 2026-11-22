# Ön kayıt 11: Hualien 2024 testi (veri indirilirken, hiçbir model ya da ETAS uydurulmadan yazıldı, 22 Kasım 2026)

Üçüncü bağımsız ileriye dönük test. Kahramanmaraş ve Noto'dan sonra ana iddianın üçüncü bir dizide
tekrarlanıp tekrarlanmadığına bakılıyor. Önceki adımlarda aynı iki test setinde bulunan iki bulgu da
burada ilk kez temiz biçimde sınanıyor:
- sentetik ETAS ön eğitiminin yararı (`RAPOR_8.md`, yalnızca Noto'da görülmüştü),
- işaretçi konum başlığının ilk gündeki üstünlüğü (`RAPOR_10.md`, keşif).

## Veri (`kod/hazirla_tw.py`)
- **Kaynak:** ISC katalog aramasından Tayvan resmi ağının (CWA, ISC kodu TAP) depremleri. Büyüklük TAP ML.
  21–26°K, 119–123°D, derinlik ≤ 70 km, 0.1'e yuvarlı.
- **Mc:** 2007–2023 yıllarının her biri için en büyük eğrilik + 0.2 hesaplanıyor, en büyüğü alınıyor.
  Test dönemine bakılmıyor.
- **Bölümler:**

  | Bölüm | Dönem |
  |---|---|
  | Geçmiş (yalnızca bağlam) | 2005–2006 |
  | Eğitim | 2007–2020 |
  | Doğrulama | 2021-01-01 – 2024-04-02 00:00 (2022 Chishang M6.8 dizisini içerir) |
  | Test | 2024-04-02 00:00 – 2025-01-01 (yaklaşık 9 ay; TAP verisi ISC'de 2024 sonunda bitiyor) |

- **Ana şok:** Hualien, 2024-04-02 23:58 UTC, TAP ML 7.2.
- **Kümeler:** ana şoktan sonraki ilk gün, ilk 7 gün, ilk 30 gün; tüm test dönemi.
- **Ek kataloglar,** hepsi 2024-04-02 öncesi:
  - California, JMA, INGV, GeoNet,
  - Türkiye KOERI (Kahramanmaraş dahil).

## Modeller (küçük model, L = 512, 3 tohum, Tayvan doğrulamasıyla erken durdurma)
| Kod | Tanım | Kod dosyası |
|---|---|---|
| H0 | Yalnızca Tayvan | `egit.py` |
| **H1 (birincil)** | Tayvan + ek kataloglar | `egit.py` |
| H2 | Yalnızca ek kataloglar (Tayvan yalnızca bağlam ve erken durdurma) | `egit.py` |
| H3 | H1 + sentetik ETAS ön eğitimi (3 000 adım, `veri/sentetik.npz`) | `egit2.py --on_egitim` |
| HS2 | H1 + işaretçi konum başlığı (12 000 adım) | `egit3.py --uzay_isaretci` |

## ETAS (Tayvan 2007 – 2024-04-02 uydurması, 2005–2006 geçmiş)
| Kod | Tanım |
|---|---|
| E0 | Kısıtsız |
| E1 | Kesik Omori |
| E2 | Alt kritik |
| E5 | Havuz + kesik |
| E7 | Alt kritik + eksik kayıt, algılama parametreleri uydurulur |
| E4 | Kâhin, test döneminde uydurulur; yalnızca tavan olarak |

- **Uzaysal ETAS** (`etas_uzay.py`): zaman bileşeni, geçerli varyantlar içinde test TLL'si en yüksek olan
  (ETAS lehine seçim).
- **Süre sınırı:** 120 dakikada bitmeyen bir ETAS varyantı durdurulur, "tamamlanmadı" olarak raporlanır ve
  karara katılmaz. Önceki iki testte bazı varyantlar saatlerce bitmedi; bu sınır önceden konuyor.

## Karar kuralları
"En güçlü geçerli ETAS" = E1, E2, E5, E7 içinde tamamlanan ve test TLL'si en yüksek olan.

**Birincil (ana iddia):**
- **Tekrarlandı:** üç koşul birlikte sağlanıyor:
  - H1 − en güçlü geçerli ETAS, tüm test döneminde > 0 ve 7 günlük blok GA sıfırı dışlıyor;
  - Hualien'den sonraki ilk günde > 0 ve 1 saatlik blok GA sıfırı dışlıyor;
  - H1 − H0 > 0, üç tohumun üçünde de pozitif.
- **Tekrarlanmadı:** H1 − en güçlü geçerli ETAS hem tüm dönemde hem ilk günde ≤ 0.
- Arası "kısmen".

**İkincil 1 (sentetik ön eğitim):**
- Tekrarlandı: H3 − H1 tüm dönemde ≥ +0.01, GA sıfırı dışlıyor, üç tohumun üçünde de pozitif.
- Aksi halde tekrarlanmadı.

**İkincil 2 (konum):**
- Tekrarlandı: HS2 − uzaysal ETAS, ilk günde zaman + konum toplamında (TLL + SLL) > 0 ve GA sıfırı
  dışlıyor.
- Tüm dönemdeki SLL farkı ayrıca raporlanır.

## Not
Bu test seti hiçbir önceki adımda kullanılmadı. Burada yalnızca önceden belirlenmiş modeller ve kurallar
uygulanır. Hiçbir ayar bu test sonuçlarına bakılarak değiştirilmez.

## Veri hazırlandıktan sonra eklendi (eğitimden önce, `sonuclar/tw_veri_ozeti.json`)
- ISC'den 225 087 satır (TAP ML ≥ 2.0). İlk denemede ISC dört eşzamanlı isteğe "meşgul" yanıtı verdi ve
  129 ay boş kaydedildi. Bu dosyalar silindi, betiğe ret denetimi eklendi, iki kolla yeniden indirildi.
  Son veride ret yanıtı yok. Bölünen üç parçada yarıların toplamı bütünle aynı (kesilme yok).
- Olay türleri ke, se, fe, de (hepsi deprem). Kural gereği Mc = 2.7. 65 094 olay: geçmiş 6 387, eğitim
  36 935, doğrulama 16 048, test 5 724.
- Ana şok 2024-04-02 23:58:11 UTC, ML 7.2. Eğitim dönemindeki en büyük olay ML 6.9, doğrulamada ML 6.8.
