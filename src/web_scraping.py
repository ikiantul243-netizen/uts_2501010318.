"""Scrape katalog Satu Data NTB hanya bila robots.txt mengizinkan."""
from pathlib import Path
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
import time, requests, pandas as pd
from bs4 import BeautifulSoup
EMAIL="GANTI_DENGAN_EMAIL_KAMPUS_PRIBADI"
if "@" not in EMAIL or EMAIL.startswith("GANTI_"): raise ValueError("Isi EMAIL kampus")
url="https://data.ntbprov.go.id/index.php/dataset?publisher=18"
robots="https://data.ntbprov.go.id/robots.txt"
headers={"User-Agent":f"UTS-DAM-Student-Project ({EMAIL})"}
r=requests.get(robots,headers=headers,timeout=20); r.raise_for_status()
p=RobotFileParser(); p.parse(r.text.splitlines())
if not p.can_fetch(headers["User-Agent"],url): raise PermissionError("robots.txt tidak mengizinkan target; scraping dihentikan")
time.sleep(2); page=requests.get(url,headers=headers,timeout=30); page.raise_for_status()
soup=BeautifulSoup(page.text,"html.parser")
rows=[]
for a in soup.select("a[href]"):
    name=a.get_text(" ",strip=True); href=a.get("href")
    if name and href: rows.append({"teks_tautan":name,"url":urljoin(url,href)})
df=pd.DataFrame(rows).drop_duplicates()
out=Path("data/raw"); out.mkdir(parents=True,exist_ok=True); df.to_csv(out/"hasil_scraping_satu_data_ntb.csv",index=False)
print("Baris tautan:",len(df))
