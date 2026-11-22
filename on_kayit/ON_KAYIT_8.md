# Ön kayıt 8: mimari testi (hiçbir varyant eğitilmeden yazıldı, 21 Kasım 2026)

Soru: Model büyütme ve bağlam uzatma işe yaramamıştı (testler 1 ve 2). Bu testte boyut değil, yapı
değişiyor. Üç yapısal değişiklik, iki ileriye dönük testin (Kahramanmaraş 2023, Noto 2024) birincil
modellerini (T1, J1) iyileştiriyor mu?

## Varyantlar (`kod/egit2.py`; bayraklar kapalıyken `kod/egit.py` ile aynı model)
| Kod | Değişiklik |
|---|---|
| A0 | Taban: T1 / J1'in aynısı, yeni kodla yeniden (denetim: üçüncü ve yedinci testteki sonuçlarla aynı çıkmalı) |
| A1 | **Katalog gömmesi:** her olayın jetonuna, hangi katalogdan geldiğini gösteren öğrenilmiş bir vektör eklenir (Türkiye, Japonya, California, İtalya, Yeni Zelanda, sentetik) |
| A2 | **Konum girdisi:** olayın katalog merkezine göre konumu (x, y, 1000 km biriminde), bir önceki olaya uzaklığın logaritması ve "konum var" bayrağı. Çıktı yine yalnızca zaman ve büyüklük |
| A3 | **Sentetik ön eğitim:** önce ETAS benzetimiyle üretilmiş kataloglarda 3000 adım, sonra gerçek veriyle A0'daki gibi eğitim |
| A4 | A1 + A2 + A3 birlikte |

**A3 için sentetik veri (`kod/sentetik_etas.py`).**
- **Katalog:** 400 benzetim kataloğu, toplam yaklaşık 1 milyon olay.
- **Parametreler (her katalogda ayrı çekilir):**
  - b ∈ [0.85, 1.2], a ∈ [0.9, 2.5], p ∈ [1.02, 1.35]
  - c ∈ [0.002, 0.1] gün (log-düzgün), μ ∈ [0.05, 3] olay/gün (log-düzgün)
  - dallanma oranı ∈ [0.6, 1.0]
- **Büyük şok:** katalogların %70'ine M − Mc ∈ [3.5, 5.5] büyüklüğünde bir büyük şok eklenir.
- **Eksik kayıt:** katalogların yarısında Helmstetter tipi algılama kaybı uygulanır
  (G ∈ [4, 6], H ∈ [0.3, 1.0], σ = 0.2). Algılanmayan olaylar tetiklemeye katılır ama kataloğa girmez.
- **Kaynak:** benzetim yalnızca ETAS'a dayanıyor; hiçbir gerçek test verisi kullanılmıyor.

**Ortak ayarlar.** Her varyant iki testte, 3 tohumla koşar (toplam 30 koşu). Bütün eğitim verisi ve
erken durdurma ilgili testin kesim tarihinden önce. Diğer ayarlar üçüncü ve yedinci testlerdeki
gibi (küçük model, L = 512).

## Ölçüt
Her varyant için A0'a göre tohum eşleşik fark. Testler:
- Türkiye: tüm test yılı ve Kahramanmaraş sonrası ilk gün
- Japonya: tüm test yılı ve Noto sonrası ilk gün

GA'lar tüm yıl için 7 günlük blok, ilk gün için 1 saatlik blok.

## Karar kuralı (her varyant için ayrı)
- **Yararlı:** iki testin ikisinde de tüm yıl farkı ≥ +0.01. En az birinde GA sıfırı dışlıyor. 6 tohum
  eşleşik farkın (2 test × 3 tohum) en az 5'i pozitif.
- **Yararsız:** iki testte de tüm yıl farkı ≤ 0.
- Arası "belirsiz".
- İkincil: ilk gün farkları, doğrulama dönemi TLL'leri.

## Önemli uyarı
Bu iki test seti artık birçok kez kullanıldı. Burada seçilen bir mimari, makalede ileri sürülmeden önce
yeni bir ileriye dönük dizide (örneğin Hualien 2024) yeniden sınanmalı. Bu yüzden doğrulama
dönemindeki TLL'ler de raporlanacak. Doğrulama ile test çelişirse bu açıkça yazılacak.
