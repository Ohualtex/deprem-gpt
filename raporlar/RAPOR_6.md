# Deprem GPT, altıncı adım: eksik kaydı modelleyen ETAS'a karşı

21 Kasım 2026. Önceki adım: `RAPOR_5.md` (ilk saatlerdeki kazancın kaynağı, keşif). Bu adımın ön kaydı
`ON_KAYIT_6.md`, ETAS varyantları uydurulmadan yazıldı. Model koşuları üçüncü testin aynısı.

## Karar: KALIYOR

Eksik kaydı modelleyen ETAS'lardan (E6, E7) testte en güçlüsü **E7** oldu. Çok katalog modeli (T1),
ana şoktan sonraki ilk günde onu **+0.151 nat/olay** geçiyor. 1 saatlik blok %95 GA [+0.123, +0.178],
üç tohum: +0.151, +0.141, +0.160. Ön kayıtlı "kalıyor" eşiği 0.05 idi.

Tüm test yılında E7, şimdiye kadarki geçerli ETAS'ların en güçlüsü (2.6930; E2 2.6920). T1 onu
+0.050 [+0.023, +0.067] geçiyor.

Ama bu sonucun nasıl okunacağı önemli. Aşağıda yazdığım gibi, eksik kayıt eklenince ETAS iyileşmedi.
Sorunun asıl kaynağı başka yerde.

## Ne yapıldı

Kaydedilen olay yoğunluğu, tam ETAS yoğunluğunun algılanma olasılığıyla çarpımı olarak modellendi:
λ_kayıt = P(t) λ(t).
- **Algılama:** Ogata-Katsura tipi yumuşak bir eşik (σ = 0.2). Eşik, Helmstetter vd. (2006)
  biçiminde büyük depremden sonra yükseliyor ve zamanla düşüyor:
  μ_d(t) = M − G − H log10(t − t_ana).
- **Tam süreç:** E2 gibi alt kritik ETAS (dallanma ≤ 0.99) (`kod/etas_eksik.py`).

| Kod | Algılama | ETAS uydurma dönemi | Test TLL |
|---|---|---|---:|
| E2 (karşılaştırma) | yok | 2008 – 2023-02-06 | 2.6920 |
| E6 | Literatür, California: G = 4.5, H = 0.75 | aynı | 2.5195 |
| **E7** | G, H Türkiye 2023 öncesinde uyduruldu → G = 9.0 (sınır), H = 1.96 | aynı | **2.6930** |
| E8 | Kâhin: G, H ve ETAS test yılında → G = 4.52, H = 0.57, a = 2.70 | test yılı | 2.7209 |
| E9 (ön kayıt dışı, keşif) | Kâhinin G, H değerleri sabit | 2008 – 2023-02-06 | 2.5571 |
| *T1* | | | *2.743* |

**Denetim.** Algılama kapatıldığında (G = 100) kod E2'nin test TLL'sini aynen verdi (2.6920). Olay
başına en büyük fark 1.1e−4. Bu fark, Nelder-Mead'in farklı başlangıç noktalarıyla çok az farklı bir
noktada durmasından geliyor.

Kaynak: `sonuclar/c6_tablolar.md`, `sonuclar/c6_ozet.json`, `sonuclar/etas6_*/etas.json`.

## Bulgular

**1. Geçerli bir ETAS, eksik kaydı 2023 öncesi Türkiye verisinden öğrenemiyor.** E7'de G üst sınıra
dayandı. Uydurma, algılama kaybını fiilen kapattı. 2023'ten önce Türkiye'de M 3.0 eşiğinde kaydı
belirgin biçimde bozacak büyüklükte bir deprem yok (en büyüğü Van 2011, M 7.2). Bu yüzden E7 pratikte
E2'nin aynısı.

**2. Literatür sabitleri KOERI için fazla sert.** E6, ana şoktan 30 dakika sonra algılama eşiğini
M 4.6 buluyor. Veride ilk saatin tamlık eşiği 3.8 civarında (`RAPOR_5.md`). E6 ilk saatlerde çok az
olay bekliyor: ortalama Λ ilk saatte 0.02, oysa doğru modelde 1 olmalı. Test TLL'si 2.52'ye düşüyor.

**3. Eksik kaydı bilmek tek başına ETAS'ı iyileştirmiyor, kötüleştiriyor.** E9, kâhinin algılama
parametrelerini kullanıyor ama ETAS'ı 2023 öncesinde uyduruyor. Test TLL'si 2.557, E2'den kötü.
Sebep şu: 2023 öncesi Türkiye verisinden öğrenilen üretkenlik katsayısı (a ≈ 1.0) M7.8 için zaten çok
az artçı öngörüyor. Algılama kaybı eklenince beklenen kayıtlı olay sayısı daha da düşüyor (ilk 9 saatte
Λ 0.03–0.15). Kâhin ETAS ancak üretkenliği de yeniden uydurunca (a = 2.70) iyi çalışıyor.

**4. ETAS'ın asıl sorunu eksik kayıt değil, üretkenliğin taşınması.** Küçük ve orta depremlerden
öğrenilen büyüklük-üretkenlik ilişkisi M7.8'e uzatılınca artçı sayısı ciddi biçimde az tahmin ediliyor.
Kâhin bunu test verisini görerek düzeltiyor; dallanma oranı da 2.4 çıkıyor, yani üst kritik. T1 ise
bunu diğer katalogların büyük dizilerinden öğrenmiş görünüyor.

**5. Kâhine karşı bile ilk gün üstünlüğü sürüyor.** T1 − E8 ilk günde +0.142 [+0.112, +0.172].
Saat saat bakılınca:
- **İlk saat:** fark +0.02'ye iniyor. Kâhin ilk saati iyi yakalıyor.
- **1–9 saat:** +0.158.
- **9–24 saat:** +0.140.

Tüm yılda kâhine karşı fark +0.022 [−0.013, +0.046], yani belirsiz.

**6. Büyüklükte de kazancın bir kısmı kalıyor.** Kâhin algılamalı GR'ye (E8) karşı:

| Dönem | T1 − sabit GR | T1 − kâhin algılamalı GR | Not |
|---|---:|---:|---|
| İlk saat | +2.04 | +0.17 | Kazancın çoğu eksik kayıttan |
| İlk gün | +0.68 | +0.23 [+0.07, +0.38] | Büyük kısmı eksik kayıt, bir kısmı kalıyor |
| 9–12 saat | | −0.19 | Kâhin M7.6 sonrasında daha iyi |

Sonuç: ilk saatteki büyüklük kazancı büyük ölçüde eksik kaydın etkisiydi, ama ilk günün tamamında
bir kısmı kalıyor.

## Zaman aralıklarına göre özet (T1 − ETAS, nat/olay)

| Kıyas | İlk gün | 0–1 saat | 1–9 saat | 9–24 saat | 1–3 gün | Tüm test |
|---|---|---:|---:|---:|---:|---|
| − E2 | +0.157 [+0.130, +0.184] | +0.153 | +0.196 | +0.130 | +0.066 | +0.051 [+0.022, +0.069] |
| − E7 | +0.151 [+0.123, +0.178] | +0.092 | +0.192 | +0.126 | +0.064 | +0.050 [+0.023, +0.067] |
| − E8 kâhin | +0.142 [+0.112, +0.172] | +0.019 | +0.158 | +0.140 | +0.054 | +0.022 [−0.013, +0.046] |

Türkiye'yi eğitimde hiç görmeyen T2, E7'yi ilk günde +0.123 [+0.095, +0.153] geçiyor.

Yalnız Türkiye modeli T0 ilk günde E7 ile eşit: +0.020 [−0.036, +0.075]. Tüm yılda E7'nin gerisinde.

## Bunun anlamı

1. **Makalenin ana iddiası artık savunulabilir.** Birden çok katalogla eğitilen küçük bir Transformer,
   daha önce görülmemiş büyüklükteki bir depremin ardından ilk günü bütün geçerli ETAS
   varyantlarından iyi tahmin ediyor. Bunlara eksik kaydı modelleyen ETAS da dahil. Test yılının
   verisiyle kurulmuş kâhin ETAS'ı da geçiyor.
2. **Mekanizma.** Üstünlük büyük ölçüde, dev bir dizinin ne kadar artçı üreteceğini ve bu artçıların
   kayıtta nasıl görüneceğini diğer katalogların büyük dizilerinden öğrenmekten geliyor. Tek bölgeye
   uydurulan ETAS bunu yapamıyor, çünkü o bölgenin geçmişinde böyle bir dizi yok. Bu, çok katalog
   eğitiminin neden işe yaradığının somut bir açıklaması.
3. **Sınır.** Bütün bunlar tek bir diziye dayanıyor. Bulgunun genelleşip genelleşmediğini başka
   ileriye dönük diziler gösterecek.

## Dikkat

- **Algılama modelinde basitleştirmeler.** Algılanmayan olayların tetiklemesi hesaba katılmadı.
  Algılama bütün Türkiye kutusuna uygulandı, oysa gerçekte yalnızca dizinin çevresinde etkili. İlk
  günlerde olayların neredeyse tamamı dizide olduğu için bunun etkisi küçük olmalı. Denenmedi.
- **İki küçük tutarsızlık.** Zaman modelinde P(t) Mc = 3.0'dan, büyüklük karşılaştırmasında sürekli
  GR Mc − 0.05'ten başlıyor (0.05'lik fark). b-değeri (1.139) eğitim döneminden sabit alındı.
- **G sınırda.** E7'de G üst sınıra (9) dayandı. Sınır daha geniş olsaydı da sonuç değişmezdi, çünkü
  G büyüdükçe algılama kaybı zaten sıfıra iniyor.
- **E9 ön kayıtta yoktu.** Keşif amacıyla sonradan eklendi, karara katılmadı.
- **Büyüklük karşılaştırmasında düzeltme.** İlk sürüm GR bölme olasılıklarını "yoğunluk × 0.1"
  diye yaklaşıkladı. Bu GR lehine yaklaşık 0.13 nat kayma yarattı. Tam bölme integraline geçildi,
  tablolardaki değerler düzeltilmiş hâliyle.

## Sonraki adımlar (öneri, yapılmadı)

1. **Başka ileriye dönük diziler.** Noto 2024 (JMA), Hualien 2024 (Tayvan), 2023–2025'in diğer büyük
   dizileri. Her birinde eğitim o dizinin öncesinde kesilir, aynı ETAS varyantları kullanılır.
2. **Büyük-dizi üretkenliği bilgisi verilmiş ETAS.** ETAS'ın a katsayısını dünya genelindeki büyük
   dizilerden (örneğin havuzlu, yalnızca M ≥ 6.5 ana şoklar) kestirmek. Modelin ilk gün üstünlüğünün
   ne kadarının yalnızca bu bilgiyle kapanacağını gösterir.
3. **Operasyonel çıktı.** "Önümüzdeki 24 saatte M ≥ 5 olasılığı" türünden tahminlerin kalibrasyonu.

## Sunucu

İşler GPU 0, 1 ve 3'te çalıştı, her GPU'da tek süreç vardı:
- GPU 0: denetim, E6 ve E9
- GPU 1: E7
- GPU 3: E8

Denetim koşusunun ilk denemesi sınır denetimindeki bir hata yüzünden çöktü. Hata düzeltildi, koşu
yeniden yapıldı. Sunucudaki 15 dosya Mac'tekilerle SHA-256 ile karşılaştırıldı, hepsi aynıydı.
sunucudaki proje klasörü silindi.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_6.md` | Ön kayıt |
| `kod/etas_eksik.py` | Eksik kaydı modelleyen ETAS |
| `kod/analiz6.py` | Tablolar, karar, şekil |
| `kod/c6_g0.cmd`, `c6_g0b.cmd`, `c6_g0c.cmd`, `c6_g1.cmd`, `c6_g3.cmd` | Sunucu işleri |
| `sonuclar/etas6_{E6,E7,E8,E9,kapali}/` | Uydurmalar ve olay başına bileşenler |
| `sonuclar/c6_ozet.json`, `sonuclar/c6_tablolar.md` | Sonuç özeti |
| `sekiller/c6_sekil1_eksik_kayit.{png,pdf}` | (a) ilk 72 saatte T1'in birikimli kazancı, (b) büyüklük kazancı |
| `kayitlar/c6_g*.log` | Günlükler |
