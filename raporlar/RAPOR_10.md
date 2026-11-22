# Deprem GPT, onuncu adım: konum çıktısı

22 Kasım 2026. Bu adımın ön kaydı `ON_KAYIT_10.md`, hiçbir model ya da uzaysal ETAS uydurulmadan yazıldı.
Model artık bir sonraki depremin zamanı ve büyüklüğünün yanında yerini de tahmin ediyor.

## Karar (ön kayıtlı model S): DAHA KÖTÜ

Ön kayıtlı model S, konumu son depremin çevresinde 16 bileşenli bir Gauss karışımıyla tahmin ediyordu.
Uzaysal ETAS'ın iki testte de belirgin biçimde gerisinde kaldı.

| | Türkiye | Japonya |
|---|---|---|
| SLL, S − uzaysal ETAS, tüm yıl (7 g GA) | −1.88 [−2.10, −1.75] | −1.79 [−2.01, −1.40] |
| SLL, S − uzaysal ETAS, ilk gün (1 sa GA) | −1.23 [−1.44, −1.00] | −2.07 [−2.22, −1.91] |
| S'nin zaman TLL'si − A0 (tüm yıl) | −0.006 | +0.010 |

SLL olay başına km² cinsinden konum log-olabilirliği. Konum çıktısı zaman tahminini bozmadı: iki farkın
mutlak değeri de 0.01'in altında ya da çevresinde.

Kaynak: `sonuclar/c10_tablolar.md`, `sonuclar/c10_ozet.json` (`kod/analiz10.py`).

## Neden kaybetti: iki keşif denemesi (ön kayıt dışı)

Bu iki deneme ön kayıtlı karara katılmıyor. Sonuçları yalnızca yön gösterici.

**1. Daha uzun eğitim (S, 12 000 adım, tek tohum).** S'nin bütün koşularında en iyi adım üst sınırdaydı
(4 000), yani eğitim yarıda kalmıştı. Uzun eğitim farkı pek değiştirmedi: tüm yılda Türkiye'de −1.63,
Japonya'da −1.61. Sorun eğitim süresi değil.

**2. İşaretçi başlık (S2, 12 000 adım, 3 tohum).** S, konum dağılımını yalnızca son depremin etrafında
kuruyordu. ETAS ise geçmişteki her depremin çevresine artçı koyabiliyor. S2 bunun Transformer karşılığı:
dikkat mekanizmasıyla bağlamdaki 512 depremden birini seçip onun çevresine bir Gauss koyuyor, ayrıca bir
arka plan bileşeni var.

| | Türkiye | Japonya |
|---|---|---|
| SLL, S2 − uzaysal ETAS, tüm yıl | −0.26 [−0.41, −0.17] | −0.06 [−0.18, +0.01] |
| SLL, S2 − uzaysal ETAS, ilk gün | **+0.19** [+0.10, +0.28] | +0.04 [−0.10, +0.17] |
| (TLL + SLL), S2 − ETAS, tüm yıl | −0.23 [−0.39, −0.12] | +0.01 [−0.14, +0.09] |
| (TLL + SLL), S2 − ETAS, ilk gün | **+0.32** [+0.23, +0.42] | **+0.21** [+0.06, +0.32] |
| S2'nin zaman TLL'si − A0 | −0.020 | −0.001 |

- **Açık neredeyse kapanıyor.** S2, S'ye göre 1.6–1.7 nat kazanıyor.
- **Tüm yılda** uzaysal ETAS konum tahmininde hâlâ biraz önde: Türkiye'de anlamlı, Japonya'da sınırda.
- **İlk gün:** zaman ve konum birlikte değerlendirildiğinde S2 iki testte de ETAS'ı geçiyor.
- **Bedel:** S2'nin zaman tahmini Türkiye'de 0.020 düşüyor.

S2 ön kayıtta yoktu ve aynı iki test setinde geliştirildi. Bu yüzden onun lehine bir sonuç ancak yeni bir
ileriye dönük dizide doğrulanırsa ileri sürülebilir.

## Uzaysal ETAS

Zaman bileşeni sabit (Türkiye E2, Japonya E5). Çekirdek
f(r | m) = (ρ/π) D^ρ / (r² + D)^(1+ρ), D = d·e^(γm).
Arka plan, eğitim olaylarının Gauss çekirdek yoğunluğu (bant h). Dört parametre, eğitim döneminden
5 000 olayda uyduruldu; üç başlangıç noktası da aynı çözüme yakınsadı.

| | d (km²) | γ | ρ | h (km) |
|---|---:|---:|---:|---:|
| Türkiye | 3.68 | **−0.26** | 0.41 | 3.3 |
| Japonya | 1.51 | 0.62 | 0.36 | 1.0 |

**Türkiye'de γ negatif çıktı.** Büyük depremlerin artçı alanı küçük depremlerinkinden dar çıkıyor; fiziksel
olarak beklenenin tersi. Türkiye'nin eğitim döneminde büyük dizi olmadığı için büyük depremin artçı alanı
bu veriden öğrenilemiyor. Zaman tarafındaki üretkenlik sorununun aynısı. Bu, en büyük olabilirlik çözümü;
değiştirilmedi.

**Arka planın bant genişlikleri çok küçük (1–3 km).** Kataloglardaki depremler aynı noktalarda tekrar
tekrar kümeleniyor.

**Yalnız arka plan tabanı:** Türkiye −16.0, Japonya −27.7. Japonya'daki çok düşük değerin sebebi: bant
genişliği küçük olduğu için Noto gibi daha önce sakin bölgelerde yoğunluk çok küçük kalıyor. Bu taban
sunucuda float32 taşması yüzünden −∞ çıkmıştı, Mac'te logaritma uzayında yeniden hesaplandı.

## Haritalı artçı tahmini (ikincil)

Ana şoktan 12 saat sonra yayınlanmış, önümüzdeki 24 saat için beklenen deprem sayısı haritası (10 km
hücre), S2 modeli ve uzaysal ETAS. Model için 900 senaryo (3 tohum × 300), ETAS için 900 senaryo.
Şekil: `sekiller/c10_sekil1_harita`. Kod: `kod/harita_model.py`, `kod/harita_etas.py`, `kod/harita_ciz.py`.

| | Gözlenen (kutu içi) | Model beklenen | ETAS beklenen | Hücre Poisson LL, model | Hücre Poisson LL, ETAS |
|---|---:|---:|---:|---:|---:|
| Kahramanmaraş | 453 | 834 | 225 | −303.8 | **−246.7** |
| Noto | 240 | **239** | 214 | **243.2** | 153.0 |

- **İki yöntem de kırılmanın şeklini yakalıyor.** Kahramanmaraş'ta iki fay kolu, Noto'da yarımada
  boyunca uzanan kuşak.
- **Noto'da model daha keskin ve sayıyı tutturuyor.**
- **Kahramanmaraş'ta model sayıyı yaklaşık iki kat abartıyor.** Olasılığı da fazla geniş bir alana
  dağıtıyor. ETAS sayıyı yarıya yakın az buluyor ama yeri daha isabetli.
- **S2 ile T1 arasındaki fark.** S2'nin Kahramanmaraş için 24 saatlik sayı tahmini (834), yalnız zaman
  modeli T1'inkinden (12. saatte 327, `RAPOR_9.md`) çok yüksek. Konum eklenen modelin kendi ürettiği
  artçılarla daha kolay "patladığını" gösteriyor. Tohumlar arasında da fark büyük: senaryo başına
  572–1 224 olay.

Bu hücre skorları tek bir yayın anına dayanıyor. Yalnızca örnek olarak verildi, istatistiksel bir
karşılaştırma değil.

## Bunun anlamı

1. **Model artık yer de tahmin edebiliyor.** Haritalı artçı tahmini üretilebiliyor.
2. **Konum tahmininde tasarım belirleyici.** "Son depremin çevresi" tasarımı ETAS'ın çok gerisinde. "Geçmiş
   depremlerden birinin çevresi" tasarımı (işaretçi başlık) açığı neredeyse kapatıyor ve büyük depremin
   ilk gününde ETAS'ı geçiyor.
3. **Ama ön kayıtlı sonuç olumsuz.** İşaretçi başlık sonradan, aynı test setlerinde bulundu. Yeni bir
   dizide sınanmadan bir iddiaya dönüşemez.
4. **Senaryo sayılarında kararsızlık.** Konumlu model, Kahramanmaraş'ta kendi senaryolarında artçı sayısını
   abartıyor ve tohumlar arasında büyük fark var. Operasyonel kullanım için bu düzeltilmeli.

## Sunucu

İşler GPU 0, 1 ve 3'te çalıştı, her GPU'da tek süreç vardı. Sunucudaki 215 dosya Mac'tekilerle SHA-256
ile karşılaştırıldı, hepsi aynıydı. sunucudaki proje klasörü kullanıcının isteğiyle duruyor.

## Sonraki adımlar (öneri, yapılmadı)

1. **Yeni bir ileriye dönük dizi (Hualien 2024).** S2 ve sentetik ön eğitim burada ön kayıtla sınanabilir.
   Tayvan kataloğu (CWA) için indirme onayı gerekir.
2. **Senaryo kararlılığı:** konumlu modelin kendi ürettiği artçılarla patlamasını önlemek. Örneğin daha
   çok tohumun ortalamasını almak ya da S2'yi zaman açısından T1 ile birleştirmek: zamanı T1'den, yeri
   S2'den almak.
3. **Hızlandırma:** KV önbelleği.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_10.md` | Ön kayıt |
| `kod/egit3.py` | Konum çıktılı eğitim (`--konum_cikti`, keşif: `--uzay_isaretci`) |
| `kod/etas_uzay.py` | Uzaysal ETAS uydurma ve değerlendirme (sunucu) |
| `kod/analiz10.py` | Tablolar ve karar |
| `kod/harita_model.py`, `kod/harita_etas.py`, `kod/harita_ciz.py` | Haritalı tahmin |
| `kod/c10_g*.cmd`, `kod/c10k_g*.cmd`, `kod/c10h_g3.cmd` | Sunucu işleri |
| `sonuclar/c10_{TR,JP}_{S,S2}_t{1,2,3}/`, `sonuclar/c10_{TR,JP}_Suzun_t1/` | Koşular |
| `sonuclar/etas10_{TR,JP}/` | Uzaysal ETAS |
| `sonuclar/c10_{TR,JP}_harita/` | Harita senaryoları |
| `sonuclar/c10_ozet.json`, `c10_tablolar.md`, `c10_harita_ozet.json` | Özetler |
| `sekiller/c10_sekil1_harita.{png,pdf}` | Harita |
| `kayitlar/c10*.log` | Günlükler |
