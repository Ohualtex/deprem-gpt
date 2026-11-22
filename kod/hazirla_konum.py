"""Mimari testi (ON_KAYIT_8.md) için her kataloğun olay konumları: veri/konum.npz.

Her katalog için önceki hazırlık betikleriyle birebir aynı süzme ve sıralama yeniden yapılır.
Zamanların daha önce kullanılan dosyalardakiyle tam aynı olduğu doğrulanır. Ek katalog dosyaları
(ek_tr.npz, ek_jp.npz) bu tam katalogların zamana göre kesilmiş önekleri olduğundan egit2.py
konumları önekten alır.
Çıktı anahtarları: <ad>_t, <ad>_enlem, <ad>_boylam
(ad: California_ComCat, Japonya_JMA, Italya_INGV, YeniZelanda_GeoNet, Turkiye_KOERI)
Mac'te: /usr/bin/python3 kod/hazirla_konum.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parent.parent
out = {}

# California: hazirla.py ile aynı okuma ve sıralama
A = KOK / "veri/earthquakenpp/Experiments/ETAS/output_data_ComCat_25/augmented_catalog.csv"
df = pd.read_csv(A, parse_dates=["time"]).sort_values("time").reset_index(drop=True)
t0 = np.datetime64("1971-01-01T00:00:00")
t = (df.time.values.astype("datetime64[us]") - t0).astype("timedelta64[us]").astype(np.float64) / 86400e6
assert np.array_equal(t, np.load(KOK / "veri/olaylar.npz")["t_gun"])
out.update(California_ComCat_t=t, California_ComCat_enlem=df.latitude.values, California_ComCat_boylam=df.longitude.values)

# JMA, INGV, GeoNet: hazirla_cok.py'deki fonksiyonlar ve süzme (dosya yazan kısım çalıştırılmaz)
sys.argv = ["hazirla_cok.py"]
kaynak = (KOK / "kod/hazirla_cok.py").read_text(encoding="utf-8").split('t0 = pd.Timestamp("1971-01-01")')[0]
ad_alani = {"__file__": str(KOK / "kod/hazirla_cok.py")}
exec(kaynak, ad_alani)                                                    # noqa: S102
e = np.load(KOK / "veri/ek_kataloglar.npz")
T0 = pd.Timestamp("1971-01-01")
for k, (ad, c) in enumerate(ad_alani["KATALOG"].items()):
    d = c["oku"]()
    if c["bolge"]:
        a, b, ee, f = c["bolge"]
        d = d[d.lat.between(a, b) & d.lon.between(ee, f)]
    d = d[d.derin <= ad_alani["DERIN_MAX"]].copy()
    d["m"] = ad_alani["yuvarla"](d.m)
    yil_mc = d[d.m >= 1.0].groupby(d.zaman.dt.year).m.apply(lambda x: ad_alani["mc_maxc"](x.values))
    mc = max(c["mc"], float(yil_mc.max())) if len(yil_mc) else c["mc"]
    d = d[d.m >= mc - 1e-9].sort_values("zaman")
    tt = (d.zaman - T0).dt.total_seconds().values / 86400.0
    i = list(e["seg_ad"]).index(ad)
    assert np.array_equal(tt, e["t_gun"][e["seg_bas"][i]:e["seg_son"][i]]), ad
    out.update({f"{ad}_t": tt, f"{ad}_enlem": d.lat.values.astype(float), f"{ad}_boylam": d.lon.values.astype(float)})

vt = np.load(KOK / "veri/turkiye.npz")
out.update(Turkiye_KOERI_t=vt["t_gun"], Turkiye_KOERI_enlem=vt["enlem"], Turkiye_KOERI_boylam=vt["boylam"])
vj = np.load(KOK / "veri/japonya.npz")
n_j = len(vj["t_gun"])                                                     # japonya.npz, JMA'nın 2025 öncesi öneki
assert np.array_equal(vj["t_gun"], out["Japonya_JMA_t"][:n_j]) and np.allclose(vj["enlem"], out["Japonya_JMA_enlem"][:n_j])
np.savez(KOK / "veri/konum.npz", **out)
for k in out:
    if k.endswith("_t"):
        print(k[:-2], len(out[k]))
