# Deprem GPT, sekizinci adım: mimari testi

21–22 Kasım 2026. Bu testin ön kaydı `ON_KAYIT_8.md`, hiçbir varyant eğitilmeden yazıldı. Önceki
testlerde model büyütme ve bağlam uzatma işe yaramamıştı. Burada boyut değil, yapı değişti.

## Karar: dört varyant da BELİRSİZ

Ön kayıtlı kurala göre "yararlı" sayılabilmek için bir varyantın iki testte de tüm yıl TLL'sini en az
+0.01 artırması gerekiyordu. Hiçbiri bunu sağlamadı. Ama sonuçlar aynı yönde belirsiz değil: üç
varyant çok farklı davranıyor.

| Varyant | Kahramanmaraş, yıl | Kahramanmaraş, ilk gün | Noto, yıl | Noto, ilk gün |
|---|---|---|---|---|
| A1 katalog gömmesi | **−0.020** [−0.037, −0.011] | +0.006 [−0.012, +0.025] | +0.003 [−0.002, +0.006] | +0.010 [−0.020, +0.038] |
| A2 konum girdisi | +0.003 [+0.001, +0.008] | −0.003 [−0.016, +0.011] | +0.002 [−0.003, +0.005] | +0.014 [−0.002, +0.029] |
| A3 sentetik ETAS ön eğitimi | +0.001 [−0.002, +0.004] | +0.003 [−0.007, +0.012] | **+0.016** [+0.003, +0.026] | **+0.045** [+0.019, +0.071] |
| A4 üçü birlikte | −0.016 [−0.027, +0.002] | **−0.078** [−0.129, −0.027] | +0.011 [+0.005, +0.015] | +0.020 [−0.010, +0.052] |

Değerler A0'a (taban) göre olay başına TLL farkı, 3 tohum ortalaması. GA'lar yıl için 7 günlük,
ilk gün için 1 saatlik blok bootstrap. Kaynak: `sonuclar/c8_tablolar.md`, `sonuclar/c8_ozet.json`
(`kod/analiz8.py`). Şekil: `sekiller/c8_sekil1_mimari` (PNG + PDF).

## Önce bir denetim bulgusu: GPU eğitimi tekrarlanabilir değil

A0 (bütün bayraklar kapalı) ile üçüncü ve yedinci testlerdeki T1 ve J1'in birebir aynı çıkmasını
bekliyordum. Ortalamalar çok yakın çıktı:
- Türkiye: A0 2.742, T1 2.743
- Japonya: A0 2.663, J1 2.666

Ama olay bazında farklar var (en büyüğü 0.37–1.7 nat). Sebebini ayırmak için eski eğitim kodunu
(`egit.py`) aynı tohumla iki kez daha çalıştırdım. İki çalıştırma kendi aralarında da farklı çıktı:
ortalama 2.742 ve 2.739, olay bazında en büyük fark 0.76 nat. Fark daha ilk değerlendirmelerden
(100–200. adım) başlıyor.

Yani sorun kodda değil: GPU'daki eğitim bit düzeyinde tekrarlanabilir değil. Muhtemel kaynak dikkat
katmanındaki paralel toplamaların sırası. Sonuç olarak aynı tohumla koşudan koşuya yaklaşık ±0.003
nat/olay gürültü var. Bu, önceki raporlarda üç tohumun yayılımına zaten dahildi, ama bu testin
yorumu için önemli. ±0.003 civarındaki farklar (A2 gibi) bu gürültünün içinde.

Kaynak: `sonuclar/c8_tekrar_egit_T1_t1`, `sonuclar/c8_tekrar_egit_T1_t1b`, `kayitlar/c8_tekrar.log`.

## Ne öğrendik

**1. Katalog gömmesi Türkiye'ye zarar veriyor (A1).** Modele "bu olay hangi katalogdan" bilgisi
verilince Türkiye testi tüm yılda 0.020 kötüleşiyor. Üç tohumun üçünde de kötüleşme var ve GA sıfırı
dışlıyor. Japonya'da etki yok.

Makul açıklama şu: çok katalog eğitiminin Türkiye'deki yararı, diğer katalogların büyük dizilerinden
öğrenileni Türkiye'ye taşımaktan geliyordu (`RAPOR_6.md`). Katalog kimliği verilince model Türkiye
için ayrı bir yol öğrenebiliyor. Bu yolda büyük dizi deneyimi yok, sonuç yalnız Türkiye modeline
yaklaşıyor. Japonya'nın kendi verisi bol olduğu için orada fark etmiyor. Bu açıklama sınanmadı.

**2. Konum girdisi bu kurulumda pek bir şey katmıyor (A2).** İki testte de +0.002 ile +0.003, yani
koşudan koşuya gürültü düzeyinde. Noto'nun ilk gününde +0.014 ama GA sıfıra değiyor. Çıktı hâlâ
yalnızca zaman olduğu için konum ancak dolaylı yardım edebiliyor. Asıl değeri, model "nerede"
sorusunu da tahmin etmeye başladığında görülür.

**3. Sentetik ETAS ön eğitimi Japonya'da işe yarıyor, Türkiye'de yaramıyor (A3).** Noto testinde:
- tüm yıl +0.016, üç tohum +0.014 ile +0.017;
- Noto'nun ilk günü +0.045, üç tohum +0.038 ile +0.053.

Bu, koşu gürültüsünün beş katı. Türkiye'de ise etki yok (+0.001).

Neden böyle olduğu belli değil. Bir olasılık şu: Türkiye modeli büyük dizi bilgisini zaten gerçek
kataloglardan (Japonya dahil) alıyor; Japonya modelinin ek kataloglarında ise Tōhoku büyüklüğünde bir
dizi yok, sentetik büyük şoklar bu boşluğu dolduruyor olabilir. Sınanmadı.

Bir ayrıntı daha: ön eğitim yalnızca sentetik veriyle 250 adım sürdüğünde gerçek doğrulama TLL'si
−0.38'e düşüyor (duman testi), yani sentetik katalog gerçek katalogdan epey farklı. Gerçek veriyle
eğitimde bu kapanıyor.

**4. Üçü birlikte Türkiye'de ilk gün için zararlı (A4).** Kahramanmaraş'ın ilk günü −0.078,
üç tohumun üçünde de negatif. Bu büyük olasılıkla katalog gömmesinin etkisi (bkz. 1).

**5. Doğrulama dönemleri testle aynı şeyi söylemiyor.** Bütün varyantlar doğrulama TLL'sini biraz
artırıyor. Türkiye'de A1 +0.006, A4 +0.013. Oysa A1 ve A4 Türkiye testinde zararlı. Türkiye'nin
doğrulama dönemi (2021–2023) büyük dizi içermiyor. Bu yüzden büyük dizi davranışını bozan bir
değişikliği yakalayamıyor. Mimari seçimi için doğrulama setinde de büyük bir dizi olması gerekiyor.

## Bunun anlamı

- **Mimari tarafında şimdilik sağlam bir kazanç yok.** Ön kayıtlı kurala göre hiçbir varyant
  benimsenmiyor. Ana model taban (A0) olarak kalıyor.
- **Sentetik ön eğitim umut verici ama tek testte.** Bir sonraki ileriye dönük dizide (örneğin
  Hualien 2024) ayrıca sınanmalı. Bu iki test seti artık çok kullanıldı.
- **Katalog gömmesi kaçınılması gereken bir şey olarak öğrenildi.** Bu bilgi değerli: çok katalog
  eğitiminin yararı paylaşılan, kataloğa özgü olmayan temsilden geliyor.
- **Konum, ancak çıktıya da eklenirse anlamlı olur.** Yani modelin "nerede" sorusunu da tahmin
  etmesi gerekir. Bu ayrı ve büyük bir iş.

## Ön kayıttan sapmalar

- **Sentetik veri miktarı.** Ön kayıtta "yaklaşık 1 milyon olay" yazıyordu. Benzetim 400 katalogda
  2.76 milyon olay üretti, katalog boyları beklenenden büyük çıktı. Kurallar değiştirilmedi.
- **A0 denetimi.** "Eski sonuçlarla aynı çıkmalı" beklentisi bit düzeyinde tutmadı. Sebebi GPU
  belirlenimsizliği, yukarıda ayrıntısı var.

## Sunucu

İşler GPU 0, 1 ve 3'te çalıştı, her GPU'da tek süreç vardı:
- 30 koşu: 5 varyant × 2 test × 3 tohum.
- Bir duman testi.
- Belirlenimcilik denetimi için 2 koşu.

Sunucudaki 148 dosya Mac'tekilerle SHA-256 ile karşılaştırıldı, hepsi aynıydı. sunucudaki proje klasörü
kullanıcının isteğiyle duruyor.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_8.md` | Ön kayıt |
| `kod/egit2.py` | Varyant bayraklarıyla eğitim kodu |
| `kod/hazirla_konum.py` | `veri/konum.npz` (bütün katalogların konumları, eski sıralamayla hizalı) |
| `kod/sentetik_etas.py` | `veri/sentetik.npz`, `sonuclar/sentetik_ozeti.json` |
| `kod/analiz8.py` | Tablolar, karar, şekil |
| `kod/c8_g0.cmd`, `c8_g1.cmd`, `c8_g3.cmd`, `c8_duman.cmd`, `c8_tekrar.cmd` | Sunucu işleri |
| `sonuclar/c8_{TR,JP}_A{0..4}_t{1,2,3}/` | Koşular |
| `sonuclar/c8_tekrar_egit_T1_t1{,b}/` | Belirlenimcilik denetimi |
| `sonuclar/c8_ozet.json`, `sonuclar/c8_tablolar.md` | Sonuç özeti |
| `kayitlar/c8_*.log` | Günlükler |
