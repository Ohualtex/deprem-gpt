# Ön kayıt 4: güçlendirilmiş ETAS'a karşı (ETAS varyantları uydurulmadan yazıldı, 21 Kasım 2026)

Soru: Kahramanmaraş testinde çok katalog modelinin (T1) ETAS'a karşı kazancı (+0.065 nat/olay), daha
iyi kurulmuş ETAS'lara karşı da duruyor mu? Model koşuları değişmiyor. Üçüncü testin
`sonuclar/c3_T*_t*` çıktıları olduğu gibi kullanılıyor. Yalnızca rakip güçleniyor.

Gerekçe: üçüncü testte uydurulan ETAS'ın dallanma oranı yaklaşık 1.36 (üst kritik). Kazancın %44'ü
dizi söndükten sonraki aylardan geliyor. Bu, ETAS'ın uzun kuyruğundaki bir kusurdan kaynaklanıyor
olabilir. Modelin ek kataloglardan aldığı veri avantajını ETAS'a da vermek ayrıca adil olur.

## Varyantlar (`kod/etas_guclu.py`, hepsi zamansal, aynı TLL tanımı)
| Kod | Tanım |
|---|---|
| E0 | Üçüncü testteki ETAS, yeni kodla yeniden (eşdeğerlik denetimi: test TLL 2.678 çıkmalı) |
| E1 | Kesik Omori: çekirdek (t + c)^(−p), t < τ için. τ serbest, p > 0 serbest |
| E2 | Alt kritik: dallanma oranı n ≤ 0.99 kısıtı (p > 1) |
| E3 | Havuz: tetikleme parametreleri (K, a, c, p) Türkiye + California + JMA + INGV + GeoNet (hepsi 2023-02-06 öncesi) üzerinde ortak, arka plan μ her katalog için ayrı. Modele verilen ek verinin aynısı |
| E5 | E3 + kesik Omori |
| E4 | Kâhin: test yılının kendisinde uydurulmuş ETAS. Geçerli bir tahmin değil, yalnızca ETAS ailesinin bu testte ulaşabileceği tavan |

Uydurma dönemi E0, E1, E2, E3 ve E5 için Türkiye 2008–2023-02-06. Hepsinde üç başlangıç noktası
kullanılıyor ve en yüksek uydurma olabilirliği seçiliyor.
İkincil: California'da C1 (kesik) ve C2 (n ≤ 0.99), 1981–2007 uydurması, ikinci testin modellerine
karşı.

## Karar kuralı
"En güçlü geçerli ETAS" = E1, E2, E3, E5 içinde **test** TLL'si en yüksek olan. Seçimin test
üzerinde yapılması ETAS'ın lehine, modelin aleyhine.
- **Sağlam:** T1 − en güçlü ETAS > 0 ve 7 günlük blok %95 GA sıfırı dışlıyor (tüm test yılı).
- **Zayıfladı:** ortalama > 0 ama GA sıfırı içeriyor.
- **Çöktü:** ortalama ≤ 0.
- İkincil: aynı kıyas ilk gün, dizi kutusunun ilk 30 günü ve 30 gün sonrası için; T2 için; kâhin E4'e
  karşı.
