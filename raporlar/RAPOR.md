# Deprem GPT: ilk gün devam/dur testi

21 Kasım 2026. Hesaplar H100 makinesinde
sunucudaki proje klasöründe yapıldı. İş bitince 98 dosyanın tamamı (107 822 137 bayt) Mac'e alındı,
SHA-256 özetleri karşılaştırıldı (hepsi aynı) ve sunucudaki klasör silindi. Tek kopya Mac'te.

## Karar: DUR (uzun bağlam hipotezi için)

Ön kayıtlı kurala göre (`ON_KAYIT.md`, eğitimden önce yazıldı) sonuç **dur**.

- Bağlamı 20 depremden 4096 depreme çıkarmak tüm test döneminde yalnızca **+0.018 nat/olay**
  kazandırıyor. Bu, kuraldaki 0.02'lik "fark yok" sınırının altında ve 0.05'lik "devam" eşiğinin
  çok altında. Olaylar üzerinden blok bootstrap GA'sı sıfırı dışlıyor [+0.009, +0.026], ama
  tohumlar arası değişkenlik farkla aynı büyüklükte (tohum tohum farklar: +0.002, +0.029, +0.024).
- Kazancın tamamı 20 → 512 arasında. 512 → 4096 hiçbir ayarda bir şey eklemiyor
  (ek denemelerde 4096, 512'nin biraz altında).
- Büyük deprem sonrası 30 günde model ETAS'tan zaten +0.02 ile +0.03 nat/olay yukarıda, ama
  bu L = 20'de de böyle. Uzun bağlam bu dönemde açığı kapatmıyor, çünkü kapatılacak ortalama
  bir açık yok. Asıl tablo iki dizinin zıt yönde çekmesi: El Mayor-Cucapah 2010'da her model
  ETAS'ı yaklaşık 0.13–0.17 nat/olay geçiyor, Ridgecrest 2019'da her model ETAS'ın
  0.09–0.14 nat/olay altında kalıyor. Bağlam uzunluğu ikisini de değiştirmiyor.
- Sonuç iki ek denemede de aynı kaldı: daha güçlü düzenlileştirme ve ETAS ile aynı veriyle
  (eğitim + doğrulama) yeniden eğitim. Bu ikisinde fark +0.020 ve +0.025 çıktı, yani kuralın
  "belirsiz" bölgesinde. "Devam" ölçütüne hiçbirinde yaklaşılamadı.

Kısaca: küçük bir transformer, yalnız zaman ve büyüklükle, ETAS'a eşit düzeyde (genel ortalamada
+0.014, GA sıfırı içeriyor) zamansal tahmin yapabiliyor. Bu da EarthquakeNPP'deki sinir ağlarından
iyi bir sonuç. Ama bunu sağlayan şey uzun bağlam değil. "Son 20 depremden çok daha uzun bellek
gerekir" fikri bu veriyle desteklenmedi.

## Ne yapıldı

### Veri ve ETAS karşılaştırması (aynı eşik)
- EarthquakeNPP ComCat_25 kataloğu (California, M ≥ 2.5). Kullanıcı onayıyla ~37 MB indirildi
  (`veri/earthquakenpp/`, `veri/etas_kaynak/`).
- Olay kümesi olarak ETAS'ın kendi değerlendirme çıktısı kullanıldı
  (`Experiments/ETAS/output_data_ComCat_25/augmented_catalog.csv`, 92 263 olay, 21 889 test olayı).
  Bu dosyada ETAS'ın **olay başına** zamansal log-olabilirliği (`TLL`) var. Böylece model ile ETAS
  aynı eşikte (2.5) ve aynı olaylarda, olay olay eşleşik karşılaştırıldı. Dosyadaki ortalama
  1.4343, `ll_scores.json`'daki değerle birebir aynı (`kod/hazirla.py` bunu denetliyor).
- Ölçüt: `TLL_i = log p(Δt_i | geçmiş)`, gün biriminde. ETAS'taki
  `log λ*(t_i) − ∫_{t_{i−1}}^{t_i} λ*` ile matematiksel olarak aynı nicelik (`etas/evaluation.py`
  okunarak doğrulandı).
- Bölünme kıyas setindeki sinir ağlarıyla aynı: geçmiş 1971–1981 (yalnız bağlam), eğitim 1981–1998
  (40 701 hedef), doğrulama 1998–2007 (14 741), test 2007-01-01 → 2020-01-17. ETAS ise 1981–2007'ye
  uydurulmuş. Bu farkı kapatmak için ek deneme B yapıldı.
- Her test olayı tam olarak önceki L olayla tahmin edildi (ilk test olayı katalogda 70 374'üncü sırada,
  yani 4096'lık bağlam her zaman dolu).

### Model (`kod/egit.py`)
Decoder-only transformer, 0.83 M parametre (d = 128, 4 katman, 4 baş). Her deprem bir jeton:
(log10 Δt, M − 2.5) ve büyüklük gömmesi. Konum: baş boyutunun yarısı olay sırasıyla, yarısı olay
zamanıyla döndürülüyor (RoPE; zaman ölçekleri 10⁻⁴–10⁴ gün). Çıktı: ln Δt için 16 bileşenli
Gauss karışımı (log-normal karışım yoğunluğu) ve büyüklük için 0.1'lik 60 sınıf. Adım başına
16 384 hedef jeton (L = 20'de 819 pencere, 512'de 32, 4096'da 4), AdamW, doğrulama zamansal
LL'sine göre erken durdurma. Üç bağlam × üç tohum, GPU 0, 1 ve 3'te (her GPU'da tek süreç).
Koşu süreleri 0.5–2.5 dakika.

## Sonuçlar

### Tablo 1. Test zamansal log-olabilirliği (nat/olay, gün birimi), ana deney

Değerler 3 tohumun ortalaması ± standart sapması.

| Küme | n | Poisson | ETAS | L = 20 | L = 512 | L = 4096 | 4096 − 20 [%95 GA] |
|---|---:|---:|---:|---:|---:|---:|---|
| Tüm test | 21 889 | 0.513 | 1.434 | 1.430 ± 0.005 | 1.446 ± 0.011 | 1.448 ± 0.010 | +0.018 [+0.009, +0.026] |
| M ≥ 6 sonrası 30 gün (birincil yoğun dönem) | 5 634 | – | 4.073 | 4.092 ± 0.003 | 4.098 ± 0.033 | 4.104 ± 0.021 | +0.012 [−0.012, +0.054] |
| M ≥ 7 sonrası 30 gün | 4 854 | – | 4.323 | 4.338 ± 0.005 | 4.346 ± 0.035 | 4.351 ± 0.023 | +0.013 [−0.015, +0.065] |
| M ≥ 6 sonrası 1 gün | 2 321 | – | 5.588 | 5.611 ± 0.009 | 5.578 ± 0.087 | 5.592 ± 0.047 | −0.020 [−0.041, +0.058] |
| Dizi dışı (sakin) | 16 255 | – | 0.520 | 0.508 ± 0.008 | 0.526 ± 0.004 | 0.528 ± 0.006 | +0.020 [+0.016, +0.024] |

GA: olay başına farkların (tohum ortalaması) 30 günlük bloklarla blok bootstrap'ı, 2000 örnek.
Bu GA yalnız olay örneklemesini yansıtıyor, tohum değişkenliğini içermiyor. Tohum eşleşik
4096 − 20 farkları tüm testte +0.002, +0.029, +0.024 (ortalama 0.018, ss 0.014; t dağılımıyla
%95 GA kabaca [−0.018, +0.054], sıfırı içeriyor).
Kaynak: `sonuclar/ozet.json`, `sonuclar/tablolar.md`. ETAS ve Poisson:
`veri/earthquakenpp/Experiments/ETAS/output_data_ComCat_25/ll_scores.json` ve `augmented_catalog.csv`.

### Tablo 2. Model − ETAS farkı (nat/olay), ana deney

| Küme | L = 20 | L = 512 | L = 4096 |
|---|---|---|---|
| Tüm test | −0.004 [−0.037, +0.037] | +0.011 [−0.026, +0.055] | +0.014 [−0.025, +0.061] |
| M ≥ 6 sonrası 30 gün | +0.019 [−0.085, +0.162] | +0.026 [−0.095, +0.177] | +0.032 [−0.095, +0.192] |
| Dizi dışı | −0.012 [−0.022, −0.002] | +0.006 [−0.002, +0.014] | +0.008 [+0.000, +0.015] |
| El Mayor-Cucapah 2010 M7.2, 30 gün (n = 2 604) | +0.133 | +0.156 | +0.169 [+0.069, +0.236]* |
| Ridgecrest 2019 M6.4, 30 gün (n = 2 543) | −0.089 | −0.103 | −0.104 [−0.177, +0.054]* |
| Ridgecrest 2019 M7.1, 30 gün (n = 2 250) | −0.122 | −0.133 | −0.138 [−0.192, −0.016]* |

\* Tek bir dizi en çok iki 30 günlük bloğa düşüyor, o yüzden 30 günlük blok GA'sı anlamsız.
Dizi satırlarında 1 günlük blok GA'sı verildi. Bu, ön kayıttan sapma (aşağıda).
Kaynak: `sonuclar/tablolar.md` (ikinci tablo), `sekiller/sekil1_etas_farki.png`,
`sekiller/sekil2_kumulatif.png`.

Şekil 2 (kümülatif kazanç) durumu açıkça gösteriyor. Tüm test ortalamasını iki olay belirliyor:
El Mayor-Cucapah'ta +400 nat civarı bir sıçrama, Ridgecrest'te −300 nat civarı bir düşüş.
L = 20 sakin dönemlerde (özellikle 2015–2019) ETAS'ın gerisine yavaşça düşüyor, 512 ve 4096
düşmüyor. Uzun bağlamın tek tutarlı katkısı bu: arka plan hızındaki yavaş değişimi izlemek.

Neden El Mayor'da iyi, Ridgecrest'te kötü olduğunu bu deneyle bilemiyoruz. ETAS iki dizide de
artçı sayısını eksik tahmin ediyor (ilk 30 günde El Mayor: 2 605 gözlenen, 1 438 beklenen;
Ridgecrest: 2 543 gözlenen, 1 491 beklenen; `augmented_catalog.csv` `int_lambd` toplamı). Yani
bu basit bir bölge sınırı etkisi değil. Ridgecrest'te öncü M6.4'ten 34 saat sonra M7.1 geldi.
Modeller bu ikinci sıçramayı ETAS'tan daha kötü karşılıyor olabilir, ama bu doğrulanmadı.

### Tablo 3. Büyüklük log-olabilirliği (nat/olay, 0.1'lik bölmeler)

| Küme | Gutenberg–Richter (ETAS β = 2.147) | L = 20 | L = 512 | L = 4096 |
|---|---:|---:|---:|---:|
| Tüm test | −2.5834 | −2.5616 | −2.5601 | −2.5612 |
| M ≥ 6 sonrası 30 gün | −2.7055 | −2.6438 | −2.6447 | −2.6416 |
| Dizi dışı | −2.5411 | −2.5330 | −2.5307 | −2.5333 |

Modeller GR'yi az farkla geçiyor (+0.02 nat/olay; yoğun dönemde +0.06). Bağlam uzunluğu fark
yaratmıyor. Yoğun dönemdeki kazanç büyük olasılıkla büyük depremden hemen sonraki kayıt
eksikliğinden (küçük olaylar kaçırılınca görünen büyüklük dağılımı kayıyor). Bu, fiziksel bir
büyüklük öngörüsü sayılmamalı. Kaynak: `sonuclar/tablolar.md` (üçüncü tablo).

## Ek denemeler (sonradan eklendi, ön kayıtta yok)

Ana deneyde her koşu 200–300. adımda doğrulamada zirve yaptı, sonra eğitim kaybı 2.07'den
0.27'ye inerken doğrulama düştü (`sekiller/sekil3_dogrulama.png`, `sonuclar/L*_t*/kayit.json`).
Model 40 bin olayı birkaç yüz adımda ezberliyor. "Dur" kararının bu aşırı öğrenmeden
kaynaklanıp kaynaklanmadığını görmek için iki deneme daha yapıldı. Sonuç ikisinde de değişmedi.

| Deneme | L = 20 | L = 512 | L = 4096 | 4096 − 20 [%95 GA] | 4096 − ETAS, yoğun 30 g |
|---|---:|---:|---:|---|---|
| Ana | 1.430 ± 0.005 | 1.446 ± 0.011 | 1.448 ± 0.010 | +0.018 [+0.009, +0.026] | +0.032 |
| A. Düzenlileştirme (dropout 0.3, wd 0.1, lr 2e-4, 25 adımda bir doğrulama) | 1.437 ± 0.002 | 1.462 ± 0.003 | 1.457 ± 0.007 | +0.020 [+0.016, +0.025] | +0.045 |
| B. ETAS ile aynı veri (eğitim + doğrulama, ana koşunun en iyi adım sayısı kadar) | 1.431 ± 0.003 | 1.465 ± 0.015 | 1.456 ± 0.005 | +0.025 [+0.021, +0.029] | +0.034 |

ETAS = 1.434. Kaynak: `sonuclar/duzen_ozet.json`, `sonuclar/duzen_tablolar.md`,
`sonuclar/tam_ozet.json`, `sonuclar/tam_tablolar.md`; şekiller `sekiller/duzen_*`, `sekiller/tam_*`.
A'da en iyi adım 375–600'e kaydı ama aşırı öğrenme yine erken. Ek denemelerde göze çarpan
bir şey var: L = 512, Ridgecrest'teki kaybın çoğunu kapatıyor (B'de M7.1 sonrası 30 günde
ETAS'a göre −0.032, L = 4096'da −0.122; A'da −0.052 ve −0.106; kaynak `sonuclar/tam_tablolar.md`,
`sonuclar/duzen_tablolar.md`). Yani bu dizide daha uzun bağlam daha kötü sonuç veriyor. Bu,
Tian ve ark.'nın "dikkat seyrelmesi" yorumuyla uyumlu, ama ana deneyde görülmediği için yalnız
bir ipucu sayılmalı. B'de L = 512 tüm testte
ETAS'ı +0.030 [+0.005, +0.065] geçiyor. Bu, testteki tek GA'sı sıfırı dışlayan "ETAS'tan iyi"
sonucu, ama sonradan eklenmiş bir denemede ve tek bir karşılaştırmada çıktı.

## Başarısız, yarıda kalan ya da sapan şeyler

- **İlk başlatma bozuk çalıştı.** İş dosyalarını üreten kabuk komutu `kod\egit.py` içindeki `\e`
  dizisini kaçış karakterine çevirdi. Üç iş de dosya bulunamadı hatasıyla anında bitti
  (`kayitlar/ana_g*.log` ilk sürümü, sonra üzerine yazıldı). Düzeltilip yeniden başlatıldı.
  Sonuçlara etkisi yok.
- **SSH tüneli bir kez düştü**. İşler sunucuda bağımsız çalıştığı için etkilenmedi.
- **Duman testi** (`duman_L4096`, `duman_L20`, 60 adım) yalnız kodu denemek için yapıldı ve silindi.
- **Olay sayısı uyuşmazlığı.** EarthquakeNPP README'si ComCat testi için 23 059 olay diyor,
  ETAS çıktısında 21 889 var. Nedeni bulunamadı. ETAS ile eşleşik olmak için 21 889 kullanıldı.
- **Δt = 0 olayları.** Testte 4 olayın önceki olayla zamanı aynı. Modelde Δt 10⁻⁶ güne çekildi.
  Ortalamaya etkisi 0.0003 nat/olaydan küçük.
- **Ön kayıttan sapmalar.** (1) Tek dizi satırlarında 30 günlük yerine 1 günlük blok GA'sı.
  (2) Ek denemeler A ve B. (3) `egit.py`'ye ek denemeler için `--wd` seçeneği eklendi ve
  `--sabit_adim` kipinde öğrenme hızı planı 4000 adıma sabitlendi. Varsayılan ayarlarda davranış
  ana koşulardakiyle aynı.
- **Literatürde okunamayanlar.** EarthquakeNPP'nin veri kümesi başına sonuç sayıları yalnız
  şekillerde (görüntü), metin olarak okunamadı. Tian ve ark. (2026) makalesinin yalnız özeti
  okunabildi (Wiley HTTP 403). Notlar `LITERATUR_NOTLARI.md`'de.

## Sınırlılıklar

- Tek katalog, tek eşik (M 2.5), tek model boyutu. Model küçük ve veri az. Aşırı öğrenme her
  ayarda birkaç yüz adımda başlıyor. Daha çok katalogla eğitilen bir model uzun bağlamdan
  yararlanabilir. Bu test o soruyu yanıtlamıyor.
- Konum yok. ETAS'ın gücünün önemli bir kısmı uzaydan geliyor. Burada yalnız zamansal kısım
  karşılaştırıldı.
- Test döneminde yalnız iki büyük dizi var ve ikisi zıt sonuç veriyor. Yoğun dönem için GA'lar
  bu yüzden çok geniş. "Büyük deprem sonrası ETAS'ı geçiyor mu" sorusuna bu veriyle sağlam
  bir yanıt verilemez.
- Doğrulama dönemi (1998–2007) testten daha sakin. Erken durdurma bu yüzden yoğun dönemlere
  göre ayarlanmamış olabilir.

## Sonraki adımlar için öneri

**Güncelleme (21 Kasım 2026):** Aşağıdaki birinci öneri yapıldı ve ön kayıtlı kurala göre "devam" çıktı.
Ayrıntı `RAPOR_2.md`'de.

Görev tanımındaki sonraki adımlar (Japonya, İtalya, Yeni Zelanda katalogları; GEM aktif fay
bilgisi; Kahramanmaraş 2023 dizisinde Türkiye'yi görmemiş modelin denenmesi) testin geçmesine
bağlanmıştı. Test **uzun bağlam** için geçmedi. Ama model ETAS düzeyinde ve sınırlayıcı etken
açıkça veri miktarı (aşırı öğrenme). Bu yüzden önerim şu:

1. "Uzun bağlam" yerine "çok katalog" hipotezini sınamak: aynı modeli L = 512 ile, birkaç
   katalogla birlikte eğitip California testinde ETAS'a karşı ölçmek. Bu, görev tanımındaki
   ilk sonraki adımın daha dar bir sürümü. Ön kayıtla ve aynı karar kuralıyla yapılmalı.
2. Bu geçerse fay bilgisi ve Kahramanmaraş testi. Kahramanmaraş için asıl soru
   (M7.8'den sonraki 9 saatte, başka bir fay kolundaki M7.5'e ETAS'tan yüksek olasılık) konum
   gerektiriyor. Yalnız zaman ve büyüklükle çalışan bu model o soruyu yanıtlayamaz.
3. Ridgecrest'teki kaybın nedenine bakmak (öncü + ana şok yapısı). Bu, iki dizinin neden zıt
   davrandığını anlamak için gerekli.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT.md` | Eğitimden önce yazılan yöntem ve karar kuralı |
| `LITERATUR_NOTLARI.md` | EarthquakeNPP, Fusion, Tian ve ark. değerlendirme ayrıntıları |
| `kod/hazirla.py` | ETAS olay kümesinden `veri/olaylar.npz`, `sonuclar/veri_ozeti.json` |
| `kod/egit.py` | Model, eğitim, test değerlendirmesi |
| `kod/analiz.py` | Tablolar, bootstrap, şekiller (`python3 kod/analiz.py [duzen_|tam_]`) |
| `kod/*.cmd`, `kod/arka.ps1` | H100'de iş başlatma (GPU 0, 1, 3; `CUDA_DEVICE_ORDER=PCI_BUS_ID`). Yeniden çalıştırmak için `kod/`, `veri/olaylar.npz` sunucuda sunucudaki proje klasörü altına kopyalanmalı |
| `sonuclar/<deneme>L<L>_t<tohum>/` | `kayit.json` (doğrulama eğrisi, en iyi adım, süre), `test.npz` (olay başına TLL ve büyüklük LL), `en_iyi.pt` (model ağırlıkları, 27 koşunun hepsinde) |
| `sonuclar/*ozet.json`, `sonuclar/*tablolar.md` | Bu rapordaki tüm sayılar |
| `sekiller/` | 300 dpi PNG + PDF |
| `kayitlar/` | Sunucu günlükleri |

Kahramanmaraş testi: `RAPOR_3.md`.
