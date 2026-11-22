# Deprem GPT, dördüncü test: güçlendirilmiş ETAS'a karşı

21 Kasım 2026. Önceki test: `RAPOR_3.md` (Kahramanmaraş, "devam"). Bu testin ön kaydı `ON_KAYIT_4.md`,
ETAS varyantları uydurulmadan yazıldı. Model koşuları üçüncü testtekilerin aynısı, yalnızca rakip
güçlendirildi.

## Karar: SAĞLAM

Ön kayıtlı kurala göre en güçlü geçerli ETAS **E2** çıktı: alt kritik, dallanma oranı ≤ 0.99, test
TLL'si 2.692. Çok katalog modeli (T1) onu tüm test yılında **+0.051 nat/olay** geçiyor. 7 günlük blok
%95 GA [+0.022, +0.069], üç tohum: +0.051, +0.047, +0.055. Üçüncü testteki +0.065'lik kazancın yaklaşık
dörtte üçü güçlendirilmiş ETAS'a karşı da duruyor.

**Kâhin ETAS'a karşı.** Test yılının kendisinde uydurulmuş ETAS (E4) geçerli bir tahmin değil. Gelecekteki
veriyi görüyor ve bu testte ETAS ailesinin tavanını gösteriyor. Model onu da geçiyor (+0.027), ama GA
sıfırı içine alıyor [−0.004, +0.048]. Kazancın iki parçası burada ayrışıyor:

- **İlk gün:** model, kâhin ETAS'ı da +0.134 geçiyor (üç tohum +0.125 ile +0.143 arası). Ana şoktan
  sonraki ilk saatlerde modelin üstünlüğü ETAS'ın parametre seçiminden bağımsız görünüyor.
- **30 gün sonrası:** kâhine karşı fark sıfır (+0.002 [−0.006, +0.012]). Üçüncü testte bu dönemde
  görülen +0.070'lik kazanç büyük ölçüde ETAS'ın uzun kuyruğunun kötü kurulmasından geliyordu.
  Parametreleri doğru olan bir ETAS bu dönemde modelle eşit. Geçerli ETAS'lar içinde en iyisi (E2)
  bu dönemde farkı +0.046'ya, havuzlu E5 ise +0.036'ya indiriyor.

**Veri avantajı ETAS'a verilince ne oluyor.** Havuzlu ETAS (E5), tetikleme parametrelerini modelin
gördüğü beş kataloğun hepsinden öğreniyor. Bu, yalnız Türkiye'yle kurulan ETAS'tan pek iyi değil:
2.683'e karşı 2.678. Diğer katalogların verisi Transformer'ın işine yarıyor, ETAS'ın beş
parametresine pek bir şey katmıyor.

## ETAS varyantları (Türkiye, test yılı)

| Kod | Tanım | Test TLL | İlk gün | Dizi kutusu 30 g | 30 g sonrası | a | c (gün) | p | τ (gün) | Dallanma |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E0 | Üçüncü testteki ETAS (yeni kodla) | 2.678 | 5.343 | 4.037 | 0.737 | 0.955 | 0.025 | 1.110 | – | 1.36 |
| E1 | Kesik Omori | 2.668 | 5.344 | 4.035 | 0.715 | 1.023 | 0.017 | 1.050 | 1 176 | 0.99 |
| **E2** | **Alt kritik (n ≤ 0.99)** | **2.692** | 5.356 | 4.044 | 0.761 | 0.986 | 0.036 | 1.189 | – | 0.99 |
| E3 | Havuz | tamamlanmadı | | | | | | | | |
| E5 | Havuz + kesik Omori | 2.683 | 5.328 | 4.023 | 0.771 | 1.113 | 0.011 | 1.083 | 1 346 | 0.91 |
| E4 | Kâhin (test yılında uydurulmuş) | 2.716 | 5.379 | 4.056 | 0.805 | 1.740 | 0.218 | 1.165 | – | 1.38 |
| | *T1 (karşılaştırma için)* | *2.743* | *5.513* | *4.102* | *0.807* | | | | | |

Her varyantta üç başlangıç noktası kullanıldı. E0, E1, E2 ve E4'te üçü de aynı uydurma olabilirliğine
yakınsadı. E5'te iki başlangıç aynı noktaya geldi, üçüncüsü biraz aşağıda kaldı (1.65121'e karşı
1.65138). Kaynak: `sonuclar/c4_tablolar.md`, `sonuclar/c4_ozet.json`, `sonuclar/etas4_*/etas.json`.

## T1 − ETAS (Türkiye)

| | Tüm test (7 g GA) | İlk gün (tohumlar) | Dizi kutusu 30 g (1 g GA) | 30 g sonrası (7 g GA) | Dizi dışı (7 g GA) |
|---|---|---|---|---|---|
| − E0 | +0.065 [+0.039, +0.081] | +0.170 (+0.171, +0.161, +0.179) | +0.065 [+0.011, +0.108] | +0.071 [+0.055, +0.089] | +0.048 [+0.025, +0.076] |
| − E1 | +0.075 [+0.051, +0.094] | +0.169 (+0.169, +0.159, +0.178) | +0.067 [+0.013, +0.109] | +0.092 [+0.073, +0.114] | +0.062 [+0.035, +0.095] |
| **− E2** | **+0.051 [+0.022, +0.069]** | +0.157 (+0.157, +0.148, +0.166) | +0.058 [+0.005, +0.098] | +0.046 [+0.032, +0.062] | +0.035 [+0.014, +0.058] |
| − E5 | +0.060 [+0.018, +0.090] | +0.185 (+0.185, +0.175, +0.194) | +0.079 [+0.018, +0.121] | +0.036 [+0.023, +0.053] | +0.038 [+0.015, +0.062] |
| − E4 (kâhin) | +0.027 [−0.004, +0.048] | +0.134 (+0.135, +0.125, +0.143) | +0.046 [−0.003, +0.083] | +0.002 [−0.006, +0.012] | +0.014 [−0.007, +0.035] |

Türkiye'yi eğitimde hiç görmeyen model (T2), en güçlü geçerli ETAS'ı (E2) +0.038 [+0.014, +0.054]
geçiyor. Kâhine karşı +0.014 [−0.012, +0.032]. Yalnızca Türkiye'yle eğitilen T0, E2'nin gerisinde
(−0.037 [−0.070, −0.016]).

Şekil: `sekiller/c4_sekil1_etas_varyantlari` (PNG + PDF).

## California (ikincil)

| ETAS | Test TLL |
|---|---:|
| EarthquakeNPP | 1.434 |
| C0: bizim taban ETAS | 1.465 |
| C2: alt kritik | 1.462 |
| C1: kesik Omori | tamamlanmadı |

İkinci testin birincil modeli M1 bunların hepsini geçiyor: C2'ye karşı +0.034 [+0.028, +0.040], M≥6
sonrası ilk günde +0.080. Yalnız California modeli M0 ve katı varyant M5 güçlü ETAS'ları geçemiyor.
Bu, `RAPOR_2.md`'nin başındaki düzeltmeyle aynı tablo.

## Ön kayıttan sapmalar

**E3 ve C1 tamamlanmadı.** E3 (kesik olmayan havuzlu ETAS) iki saatte, C1 (California, kesik Omori)
bir saat elli dakikada üç başlangıcın birincisini bile bitiremedi. 30 dakikalık ek süreden sonra ikisi
de durduruldu, sonuç yok.

E3'ün eksikliği kararı büyük olasılıkla değiştirmiyor. E5, E3'ün τ serbest bırakılmış hâli: τ sonsuza
gittiğinde E3'e dönüşüyor, yani uydurma olabilirliği E3'ünkünden düşük olamaz. Ama test TLL'si
uydurma olabilirliğiyle aynı sırayı izlemek zorunda değil (E1 ile E0 bunun örneği). Bu yüzden
"E3 daha güçlü olamazdı" demek kesin değil.

**E5'in `etas.json` dosyası günlükten kuruldu.** Havuzlu koşuda kodun ilk sürümü sonuç JSON'unu
yazarken çöktü (numpy int64 JSON'a yazılamadı). Test TLL'leri (`etas_test.npz`) bundan önce
kaydedilmişti. Parametreler, koşunun günlüğündeki üç başlangıç satırından `kod/etas_json_onar.py` ile
kuruldu. Hata kodda düzeltildi.

**E0 yeni kodla.** Test TLL'si eski kodunkiyle aynı (2.678). Olay başına en büyük fark 0.0097. Yeni
kodun EM'si daha iyi yakınsıyor ve arka plan oranını sıfıra götürüyor. Eski kod μ = 0.0045'te
durmuştu. Uydurma olabilirliği farkı 4e−6.

## Başarısız ya da sapan şeyler

- **İlk EM sürümü çok yavaştı.** Her değerlendirmede 2000 yinelemeye kadar dönüyordu. İşler
  durduruldu, EM sıcak başlangıç ve olabilirliğe göre durdurmayla yeniden yazıldı, işler yeniden
  başlatıldı.
- **Havuzlu ETAS'lar beklenenden yavaş.** Tanı (`kayitlar/tani4.log`) tek değerlendirmenin 1.3 saniye
  sürdüğünü gösterdi. Yavaşlık, arka planın sıfıra gittiği bölgelerde EM'nin ağırlaşmasından ve
  Nelder-Mead'in çok sayıda değerlendirme yapmasından geliyor. E5 18 dakikada bitti, E3 bitmedi.
- **SSH tüneli** birkaç kez koptu. İşler etkilenmedi, yalnızca izleme gecikti.

## Bunun anlamı

1. **Ana şoktan sonraki ilk saatler sağlam görünüyor.** Çok katalog modeli, bu testte denenen her
   ETAS'ı geçiyor; kâhin ETAS da buna dahil. Asıl yararlı bulgu bu, ve artçı tahmininin en çok
   işe yaradığı an da bu.
2. **Tüm yıl ortalamasında kazanç gerçek ama mütevazı.** En güçlü geçerli ETAS'a karşı +0.05 nat/olay.
   Kâhin ETAS'a karşı aralık sıfıra değiyor.
3. **Üçüncü testteki 30 gün sonrası kazancı büyük ölçüde rakibin zayıflığından geliyordu.** Bunu
   `RAPOR_3.md`'de "denenmedi" diye yazmıştım, şimdi doğrulandı.
4. **Çok katalog verisi ETAS'a yaramıyor, Transformer'a yarıyor.** Bu, makale için temiz bir karşıtlık.

## Sonraki adımlar (öneri, yapılmadı)

1. **İlk saatlerin ayrıntılı analizi.** Kazanç ilk saatlerde nereden geliyor? Model kısa süreli eksik
   kaydı mı öğreniyor, yoksa ikinci büyük şoka (M7.6) mı daha iyi hazırlanıyor? Saat saat kıyas
   bunu ayırabilir.
2. **Başka ileriye dönük diziler** (Noto 2024, Hualien 2024). Aynı ETAS varyantlarıyla.
3. **Eksik kaydı modelleyen ETAS.** Örneğin Helmstetter tipi, zamana bağlı Mc. İlk saatlerdeki
   kazancın bir kısmı buna karşı kapanabilir.
4. **E3 ve C1'i bitirmek** gerekiyorsa: daha hızlı iç optimizasyon (μ ve K için Newton) ya da
   başlangıçları ayrı GPU'larda paralel koşturmak.

## Sunucu

İşler GPU 0, 1 ve 3'te çalıştı, her GPU'da tek süreç vardı:
- C2 ve tanı betiği GPU 3'te, E5 bittikten sonra çalıştı.
- GPU 0'daki iş sırası, C2 iki kez koşmasın diye C1 sırasında durduruldu.

Bitince sunucudaki 17 dosya Mac'tekilerle SHA-256 ile karşılaştırıldı: 16'sı aynıydı. Farklı olan tek
dosya E5'in çöküşte yarım kalmış `etas.json` dosyası (283 bayt), Mac'teki sürüm günlükten kuruldu.
sunucudaki proje klasörü silindi.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ON_KAYIT_4.md` | Ön kayıt |
| `kod/etas_guclu.py` | ETAS varyantları (kesik, n_max, havuz) |
| `kod/etas_json_onar.py` | E5'in etas.json dosyasını günlükten kuran betik |
| `kod/analiz4.py` | Tablolar, karar, şekil |
| `kod/c4_g0.cmd`, `c4_g1.cmd`, `c4_g3.cmd`, `c4_g3b.cmd` | Sunucu işleri |
| `sonuclar/etas4_{E0,E1,E2,E4,E5,C2}/` | Uydurmalar ve test TLL'leri |
| `sonuclar/c4_ozet.json`, `sonuclar/c4_tablolar.md` | Sonuç özeti |
| `sekiller/c4_sekil1_etas_varyantlari.{png,pdf}` | Şekil |
| `kayitlar/c4_g*.log`, `kayitlar/tani4.log` | Günlükler |
