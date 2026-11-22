"""KOERI (Kandilli) deprem kataloğunu aylık parçalarla indirir ve ayrıştırır.

Kaynak: http://www.koeri.boun.edu.tr/sismo/zeqdb/submitRecSearchT.asp (sitenin kendi arama formu)
Kapsam: 2006-01-01 .. 2024-03-31, enlem 35-43, boylam 25-45, M >= 2.0, Tip=Deprem
Çıktı:  veri/koeri/ham/<bas>_<son>.html   (ham yanıtlar)
        veri/koeri/koeri_2006_2024.csv     (ayrıştırılmış, tekrarsız)
Bir parçada ayrıştırılan satır sayısı "Bulunan" ile tutmazsa ya da 4000'i aşarsa parça ikiye bölünür.
"""
import csv
import datetime as dt
import re
import sys
import time
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HAM = KOK / "veri/koeri/ham"
HAM.mkdir(parents=True, exist_ok=True)
URL = ("http://www.koeri.boun.edu.tr/sismo/zeqdb/submitRecSearchT.asp?"
       "bYear={a.year}&bMont={a.month:02d}&bDay={a.day:02d}&eYear={b.year}&eMont={b.month:02d}&eDay={b.day:02d}"
       "&EnMin=35&EnMax=43&BoyMin=25&BoyMax=45&MAGMin=2.0&MAGMax=9.0&DerMin=0&DerMax=500&Tip=Deprem"
       "&ofName=deprem_gpt_{a:%Y%m%d}.txt")
SUTUN = ["kod", "tarih", "saat", "enlem", "boylam", "derinlik", "xM", "MD", "ML", "Mw", "Ms", "Mb", "tip", "yer"]
SINIR = 4000


def ayristir(h):
    t = re.sub(r"<[^>]*>", "\t", h)
    hucre = [x.strip() for x in t.split("\t") if x.strip()]
    out = []
    for i, x in enumerate(hucre):
        if re.fullmatch(r"\d{14}", x) and i + 13 < len(hucre) and re.fullmatch(r"\d{4}\.\d\d\.\d\d", hucre[i + 1]):
            out.append(hucre[i:i + 14])
    m = re.search(r"Bulunan:\s*(\d+)", h)
    return out, (int(m.group(1)) if m else None)


def getir(a, b):
    yol = HAM / f"{a:%Y%m%d}_{b:%Y%m%d}.html"
    if yol.exists():
        h = yol.read_text(encoding="utf-8")
    else:
        for deneme in range(4):
            try:
                req = urllib.request.Request(URL.format(a=a, b=b), headers={"User-Agent": "deprem-arastirma"})
                h = urllib.request.urlopen(req, timeout=180).read().decode("utf-8", "replace")
                break
            except Exception as e:  # noqa: BLE001
                print("hata", a, b, e, flush=True)
                time.sleep(10 * (deneme + 1))
        else:
            raise SystemExit(f"indirilemedi {a} {b}")
        time.sleep(1.0)
    s, bulunan = ayristir(h)
    if (bulunan is None or len(s) != bulunan or len(s) >= SINIR) and a < b:
        orta = a + (b - a) // 2
        print(f"böl {a}..{b} satir={len(s)} bulunan={bulunan}", flush=True)
        if yol.exists():
            yol.unlink()
        return getir(a, orta) + getir(orta + dt.timedelta(days=1), b)
    if not yol.exists():
        yol.write_text(h, encoding="utf-8")
    if bulunan is None or len(s) != bulunan:
        print(f"UYARI {a}..{b} satir={len(s)} bulunan={bulunan}", flush=True)
    return s


tum = []
a = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2006, 1, 1)   # paralel ikinci süreç için
while a <= dt.date(2024, 3, 31):
    b = (a.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    s = getir(a, b)
    tum += s
    print(a, len(s), flush=True)
    a = b + dt.timedelta(days=1)

if len(sys.argv) > 1:
    sys.exit(0)          # yalnızca ham dosyaları indiren yardımcı süreç; CSV ana süreçte yazılır
gor, tekil = set(), []
for r in tum:
    k = (r[0], r[2], r[3], r[4])
    if k not in gor:
        gor.add(k)
        tekil.append(r)
tekil.sort(key=lambda r: (r[1], r[2]))
with open(KOK / "veri/koeri/koeri_2006_2024.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(SUTUN)
    w.writerows(tekil)
print("toplam", len(tum), "tekil", len(tekil), file=sys.stderr)
