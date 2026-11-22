"""ISC katalog aramasından Tayvan (CWA, ISC kodu TAP) depremlerini aylık indirir ve ayrıştırır.

Kaynak: https://www.isc.ac.uk/cgi-bin/web-db-run (CATCSV), büyüklük TAP ML >= 2.0, 21–26°K, 119–123°D,
2005-01 .. 2024-12 (TAP verisi ISC'de 2024 sonunda bitiyor).
Çıktı: veri/tayvan/ham/<bas>_<son>.html, veri/tayvan/isc_tap_2005_2024.csv
Bir parçada 3 000'den çok olay varsa parça ikiye bölünür ve yarıların toplamı tümüyle karşılaştırılır
(kesilme denetimi). Sorgular arasında 2 saniye beklenir.
"""
import csv
import datetime as dt
import re
import sys
import time
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HAM = KOK / "veri/tayvan/ham"
HAM.mkdir(parents=True, exist_ok=True)
URL = ("https://www.isc.ac.uk/cgi-bin/web-db-run?request=COMPREHENSIVE&out_format=CATCSV&searchshape=RECT"
       "&bot_lat=21&top_lat=26&left_lon=119&right_lon=123&ctr_lat=&ctr_lon=&radius=&max_dist_units=deg&srn=&grn="
       "&start_year={a.year}&start_month={a.month}&start_day={a.day}&start_time=00%3A00%3A00"
       "&end_year={b.year}&end_month={b.month}&end_day={b.day}&end_time=23%3A59%3A59"
       "&min_dep=&max_dep=&min_mag=2.0&max_mag=&req_mag_type=ML&req_mag_agcy=TAP&include_links=off")
SUTUN = ["eventid", "tur", "yazar", "tarih", "saat", "enlem", "boylam", "derinlik", "ml"]


def ayristir(h):
    out = []
    for satir in re.sub(r"<[^>]*>", "\n", h).splitlines():
        p = [x.strip() for x in satir.split(",")]
        if len(p) < 12 or not p[0].isdigit() or not re.fullmatch(r"\d{4}-\d\d-\d\d", p[3]):
            continue
        ml = None
        for k in range(9, len(p) - 2, 3):
            if p[k] == "TAP" and p[k + 1] == "ML" and p[k + 2]:
                ml = p[k + 2]
                break
        if ml is None:
            continue
        out.append([p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], ml])
    return out


def getir(a, b):
    yol = HAM / f"{a:%Y%m%d}_{b:%Y%m%d}.html"
    if yol.exists():
        h = yol.read_text(encoding="utf-8")
    else:
        for deneme in range(8):
            try:
                req = urllib.request.Request(URL.format(a=a, b=b), headers={"User-Agent": "deprem-arastirma"})
                h = urllib.request.urlopen(req, timeout=600).read().decode("utf-8", "replace")
                if "ISC: Event catalogue" not in h:
                    raise ValueError("beklenmeyen yanıt")
                if "cannot be processed" in h:                  # ISC yük nedeniyle reddetti: kaydetme, bekle, yeniden dene
                    raise ValueError("ISC meşgul")
                break
            except Exception as e:  # noqa: BLE001
                print("hata", a, b, e, flush=True)
                time.sleep(60 * (deneme + 1))
        else:
            raise SystemExit(f"indirilemedi {a} {b}")
        yol.write_text(h, encoding="utf-8")
        time.sleep(2.0)
    s = ayristir(h)
    if len(s) >= 3000 and a < b:
        orta = a + (b - a) // 2
        s1, s2 = getir(a, orta), getir(orta + dt.timedelta(days=1), b)
        print(f"böl {a}..{b}: tümü {len(s)}, yarılar {len(s1)} + {len(s2)}", flush=True)
        return s1 + s2 if len(s1) + len(s2) >= len(s) else s
    return s


tum = []
a = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2005, 1, 1)   # paralel yardımcı süreç için
while a <= dt.date(2024, 12, 31):
    b = (a.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    s = getir(a, b)
    tum += s
    print(a, len(s), flush=True)
    a = b + dt.timedelta(days=1)
if len(sys.argv) > 1:
    sys.exit(0)          # yardımcı süreç yalnızca ham dosyaları indirir; CSV ana süreçte yazılır
gor, tekil = set(), []
for r in tum:
    if r[0] not in gor:
        gor.add(r[0])
        tekil.append(r)
tekil.sort(key=lambda r: (r[3], r[4]))
with open(KOK / "veri/tayvan/isc_tap_2005_2024.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(SUTUN)
    w.writerows(tekil)
print("toplam", len(tum), "tekil", len(tekil), file=sys.stderr)
