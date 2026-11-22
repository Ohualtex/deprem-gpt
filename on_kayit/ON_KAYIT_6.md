# Ön kayıt 6: eksik kaydı modelleyen ETAS'a karşı (uydurmadan önce yazıldı, 21 Kasım 2026)

Soru: Çok katalog modelinin (T1) Kahramanmaraş ana şokundan sonraki ilk gündeki üstünlüğü
(+0.157, alt kritik ETAS E2'ye karşı; `RAPOR_4.md`), ana şok sonrası eksik kaydı açıkça modelleyen bir
ETAS'a karşı da duruyor mu? `RAPOR_5.md` bu üstünlüğün bir kısmının kataloğun kayıt davranışından
öğrenilmiş olabileceğini gösterdi. Model koşuları değişmiyor, yalnızca rakip değişiyor.

## Model (`kod/etas_eksik.py`)
Tam süreç alt kritik ETAS (E2 ile aynı biçim: Omori, p > 1, dallanma ≤ 0.99). Kaydedilen olayların
yoğunluğu:

    λ_kayıt(t) = P(t) · λ(t)

Algılanma olasılığı P(t), Ogata-Katsura tipi yumuşak bir algılama eşiği μ_d(t) ile hesaplanıyor.
Bunun için Gutenberg-Richter dağılımı (b sabit, Türkiye eğitim döneminden, 1.139) normal dağılım
birikimli fonksiyonu Φ((m − μ_d)/σ) ile çarpılıp Mc = 3.0 üstünde integrali alınıyor (kapalı biçim).

Algılama eşiği, Helmstetter vd. (2006) biçiminde:

    μ_d(t) = en büyük_j [ M_j − G − H log10(t − t_j) ]    (t_j < t, M_j ≥ 5.0, gün birimi)

Bunun alt sınırı Mc − 2, yani olağan dönemde P ≈ 1. Algılanmayan olayların tetiklemesi hesaba
katılmıyor; bu yaklaşımda yaygın bir basitleştirme. İntegral, eksik aralıklarda Gauss-Legendre
kareleme (32 düğüm, log-zaman), tam aralıklarda kapalı biçimle alınıyor.

| Kod | Algılama parametreleri | ETAS uydurma dönemi |
|---|---|---|
| E6 | Literatür: G = 4.5, H = 0.75 (Helmstetter vd. 2006, California), σ = 0.2 | Türkiye 2008 – 2023-02-06 |
| E7 | G ve H Türkiye 2008 – 2023-02-06 verisinde ETAS'la birlikte uydurulur, σ = 0.2 | aynı |
| E8 | Kâhin: G, H ve ETAS test yılında uydurulur, dallanma kısıtı yok | 2023-02-06 – 2024-02-06 |

Denetim: algılama kapatıldığında (G = 100) kod E2'nin test TLL'sini (2.692) yeniden üretmeli.

## Karar kuralı
"Eksik kayıtlı en güçlü ETAS" = E6 ve E7 içinde test TLL'si en yüksek olan. Seçimin test üzerinde
yapılması ETAS'ın lehine.

**Birincil:** ana şoktan sonraki ilk gün (594 olay), T1 − en güçlü eksik kayıtlı ETAS. GA 1 saatlik
blok bootstrap ile.
- **Kalıyor:** fark ≥ 0.05 ve üç tohumun üçünde de pozitif.
- **Kapanıyor:** fark ≤ 0.02.
- Arası "kısmen".

**İkincil:**
- tüm test yılı (7 günlük blok GA); en güçlü geçerli ETAS seçimi bu kez E1, E2, E5, E6, E7 arasından
- 1–3 gün
- kâhin E8'e karşı ilk gün
- büyüklük: ilk günde T1 − zamana bağlı GR (E6 ve E7'nin algılama eşiğiyle). Önceki adımdaki sabit
  GR'ye karşı +0.4 ile +2.0 nat arasındaki kazancın ne kadarının kaldığı
