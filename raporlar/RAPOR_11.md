# Deprem GPT, on birinci adım: Hualien 2024 testi

22 Kasım 2026. Bu testin ön kaydı `ON_KAYIT_11.md`. Veri indirilirken, hiçbir model ya da ETAS
uydurulmadan yazıldı. Bu test seti hiçbir önceki adımda kullanılmadı ve yalnızca bir kez çalıştırıldı.

## Kararlar (ön kayıtlı)

| | Karar |
|---|---|
| **Birincil (ana iddia)** | **KISMEN** |
| İkincil 1: sentetik ETAS ön eğitimi | **TEKRARLANDI** |
| İkincil 2: işaretçi konum başlığı | **TEKRARLANDI** |

En güçlü geçerli ETAS: **E7** (alt kritik + eksik kayıt, test TLL 3.346). Algılama parametreleri
sınıra dayandığı için E7 pratikte E2 ile aynı (3.345). Havuzlu ETAS (E5) süre sınırını aştı ve karara
katılmadı (bkz. Eklenti).

### Birincil karar neden "kısmen"

Ön kayıtlı üç koşul:

| Koşul | Sonuç | Sağlandı mı |
|---|---|---|
| H1 − en güçlü ETAS, tüm test dönemi (7 g GA sıfırı dışlıyor) | **+0.107** [+0.073, +0.181] | evet |
| H1 − en güçlü ETAS, ilk gün (1 sa GA sıfırı dışlıyor) | +0.036 [−0.009, +0.076] | **hayır** |
| H1 − H0 > 0, üç tohumda da | −0.009 (tohumlar −0.042, −0.000, +0.015) | **hayır** |

- **Tüm dönem:** model ETAS'ı açıkça geçiyor.
- **İlk gün:** Kahramanmaraş ve Noto'daki büyük üstünlük Hualien'de görülmüyor.
- **Çok katalog eğitimi:** yalnız Tayvan modelini geçmiyor.

### İkincil kararlar

- **Sentetik ön eğitim:** H3 − H1 = **+0.032** [+0.023, +0.045], üç tohumda da pozitif (+0.086, +0.004,
  +0.007). Noto'daki bulgu (`RAPOR_8.md`) yeni bir dizide doğrulandı.
- **Konum (işaretçi başlık HS2) − uzaysal ETAS:**

  | | Konum (SLL) | Zaman + konum |
  |---|---|---|
  | İlk gün | **+0.084** [+0.046, +0.118] | **+0.080** [+0.019, +0.135] |
  | Tüm dönem | −0.019 [−0.125, +0.030] | +0.102 [+0.008, +0.177] |

  `RAPOR_10.md`'deki keşif bulgusu yeni bir dizide ön kayıtla doğrulandı.

## Veri

- **Kaynak:** ISC, Tayvan resmi ağı (CWA, TAP), ML ≥ 2.0, 2005–2024. 225 087 satır.
- **Süzme:** kutu, derinlik ≤ 70 km ve Mc = 2.7 sonrası 65 094 olay.

  | Bölüm | Olay |
  |---|---:|
  | Geçmiş | 6 387 |
  | Eğitim (2007–2020) | 36 935 |
  | Doğrulama (2021 – 2024-04-02) | 16 048 |
  | Test (2024-04-02 – 2024-12-31) | 5 724 |

- **Ana şok:** 2024-04-02 23:58:11 UTC, ML 7.2. Eğitim dönemindeki en büyük olay ML 6.9, doğrulamada ML 6.8
  (2022 Chishang).
- **Mc kuralı:** Mc, 2022'nin MAXC + 0.2 değeriyle belirlendi. Önceki yıllarda bu değer 2.2 idi.
- **İndirme sorunu:** ilk indirmede ISC dört eşzamanlı isteğe "meşgul" yanıtı verdi ve 129 ay boş
  kaydedildi. Ayrıştırma sonrası denetimde yakalandı. Dosyalar silindi, ret denetimi eklendi, iki kolla
  yeniden indirildi. Son veride sorun yok.

Kaynak: `sonuclar/tw_veri_ozeti.json`.

## Sonuçlar

Olay başına zamansal log-olabilirlik (nat, gün). Modeller 3 tohum ortalaması.

| | Tüm test | İlk gün | İlk 7 gün | 30 gün sonrası |
|---|---:|---:|---:|---:|
| ETAS E0 kısıtsız (dallanma 5 647, patlayan) | 3.296 | 5.834 | 5.111 | 1.038 |
| ETAS E1 kesik Omori | 3.260 | 5.830 | 5.107 | 1.042 |
| ETAS E2 alt kritik | 3.345 | 5.832 | 5.110 | 1.048 |
| **ETAS E7 eksik kayıtlı (en güçlü geçerli)** | **3.346** | 5.841 | 5.116 | 1.071 |
| ETAS E4 kâhin | 3.428 | 5.884 | 5.202 | 0.568 |
| H0 yalnız Tayvan | 3.462 | 5.851 | 5.167 | |
| **H1 Tayvan + ek kataloglar** | **3.453** | 5.877 | 5.169 | |
| H2 yalnız ek kataloglar | 3.373 | 5.797 | 5.050 | |
| H3 H1 + sentetik ön eğitim | 3.485 | 5.875 | 5.195 | |
| HS2 H1 + işaretçi konum başlığı | 3.467 | 5.837 | 5.163 | |

Farklar (7 g GA tüm dönem ve 30 g sonrası, 1 sa GA ilk gün):

| Fark | Tüm test | İlk gün | 30 g sonrası |
|---|---|---|---|
| H1 − E7 | +0.107 [+0.073, +0.181] | +0.036 [−0.009, +0.076] | +0.120 [+0.064, +0.194] |
| H1 − E4 (kâhin) | +0.025 [−0.007, +0.100] | −0.007 [−0.057, +0.033] | +0.100 [+0.061, +0.137] |
| H0 − E7 | +0.116 [+0.063, +0.200] | +0.010 [−0.043, +0.072] | |
| H2 − E7 | +0.027 [−0.020, +0.132] | | |
| H1 − H0 | −0.009 [−0.056, +0.034] | +0.026 [−0.054, +0.093] | |

Kaynak: `sonuclar/c11_tablolar.md`, `sonuclar/c11_ozet.json` (`kod/analiz11.py`).

## Yorum

**Bölgesel ETAS üretkenliği az tahmin etmiyor.** Tayvan ETAS'ının (E7) a katsayısı 1.07, kâhinin 0.57. Yani
Tayvan'da bölgesel ETAS üretkenliğin büyüklükle artışını kâhinden daha **büyük** buluyor. Türkiye'de
0.99'a karşı 1.74, Japonya'da 1.13'e karşı 1.65 idi; orada bölgesel ETAS büyük ana şokun üretkenliğini
az tahmin ediyordu. Kahramanmaraş ve Noto'da modelin ilk günde ETAS'ı geçmesini sağlayan "taşınamayan
bilgi" Hualien'de yoktu. (Bu raporun ilk sürümünde kâhin için yanlış sütundan 1.22 okunmuştu; o değer
p idi, düzeltildi.)

**Tayvan kataloğu zengin.** 2005–2024 arasında Mc 2.7 üstünde 65 bin olay var. Eğitimde ML 6.9'a kadar,
doğrulamada 2022 Chishang M6.8 dizisi var. Yalnız Tayvan modeli (H0) çok katalog modeli kadar iyi.

**Model yine de ETAS'tan iyi.** Hem H0 hem H1 tüm dönemde ETAS'ı yaklaşık 0.11 geçiyor. Kazanç 30 gün
sonrasında da sürüyor ve kâhine karşı da duruyor (+0.10). Yani Tayvan'da modelin üstünlüğü ETAS'ın
kuyruk hatasından değil, sakin dönemi daha iyi modellemekten geliyor. Bu Kahramanmaraş'tan farklı.

**Ana iddianın yeni biçimi.** Çok katalog eğitiminin değeri koşullu. Bölgenin kataloğu büyük dizilerden
yoksunsa ve ETAS üretkenliği taşıyamıyorsa belirleyici; zengin kataloglarda küçük ya da sıfır. Model,
tek kataloglu olsa bile, üç dizinin üçünde de tüm test döneminde ETAS'tan iyi.

## Ön kayıttan sapmalar ve işletim notları

- **E5 (havuzlu ETAS):** ilk denemede GPU belleği yetmediği için çöktü. Yöntem değiştirilmeden daha
  küçük parçalarla (`--parca 512`) yeniden başlatıldı. Süre sınırı yine 120 dakika.
- **E0 iki kez koştu:** GPU 0'daki sırayı beklememek için GPU 3'te de başlatıldı; iki kopya da aynı
  sonucu yazdı (3.2963).
- **Uzaysal ETAS:** zaman bileşeni o an en güçlü geçerli olan E7 ile çalıştırıldı. E5 daha güçlü
  çıkarsa ön kayıt gereği E5 ile yeniden çalıştırılacak.

## Eklenti: E5

Havuzlu ETAS (E5) 120 dakikalık süre sınırını aştı (`SURE_ASIMI: tamamlanmadi`). Ön kayıt gereği karara
katılmadı. En güçlü geçerli ETAS E7 olarak kesinleşti. Uzaysal ETAS zaten E7 ile çalıştırılmıştı,
yeniden çalıştırma gerekmedi. Yukarıdaki kararlar son halleri.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_11.md` | Ön kayıt |
| `kod/indir_isc_tayvan.py`, `kod/hazirla_tw.py` | Veri |
| `kod/analiz11.py` | Analiz ve karar |
| `kod/c11_*.cmd` | Sunucu işleri |
| `veri/tayvan/`, `veri/tayvan.npz`, `veri/ek_tw.npz` | Katalog |
| `sonuclar/c11_*`, `sonuclar/etas11_*` | Koşular ve ETAS'lar |
| `sonuclar/c11_ozet.json`, `sonuclar/c11_tablolar.md` | Özet |
