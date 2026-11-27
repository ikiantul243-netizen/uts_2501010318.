"""Ambil data cuaca historis Open-Meteo; isi email kampus sebelum menjalankan."""
import json, time
from pathlib import Path
import requests, pandas as pd

EMAIL = "GANTI_DENGAN_EMAIL_KAMPUS_PRIBADI"
OUT = Path("data/raw"); OUT.mkdir(parents=True, exist_ok=True)
if "@" not in EMAIL or EMAIL.startswith("GANTI_"): raise ValueError("Isi EMAIL dengan email kampus pribadi")
url="https://archive-api.open-meteo.com/v1/archive"
params={"latitude":-8.5833,"longitude":116.1167,"start_date":"2024-01-01","end_date":"2024-12-31","daily":"temperature_2m_mean,precipitation_sum,wind_speed_10m_max","timezone":"Asia/Makassar"}
headers={"User-Agent":f"UTS-DAM-Student-Project ({EMAIL})"}
for attempt in range(3):
    try:
        time.sleep(1); r=requests.get(url,params=params,headers=headers,timeout=30)
        if r.status_code==200: break
        if r.status_code not in (429,500,502,503,504): r.raise_for_status()
    except requests.RequestException:
        if attempt==2: raise
    time.sleep(2*(attempt+1))
r.raise_for_status(); data=r.json()
(OUT/"open_meteo_mataram_2024_raw.json").write_text(json.dumps(data,indent=2),encoding="utf-8")
print("Data harian:",len(data.get("daily",{}).get("time",[])))
