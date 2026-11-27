"""Contoh normalisasi dataset kunjungan NTB dan ekspor CSV."""
from pathlib import Path
import pandas as pd
raw=Path("data/raw/dataset_kunjungan_wisatawan_ntb_asli.xlsx")
out=Path("data/processed"); out.mkdir(parents=True,exist_ok=True)
df=pd.read_excel(raw,sheet_name="Worksheet",dtype={"Kode provinsi":"string","Jumlah (Orang)":"string"})
df.columns=["nomor","kode_provinsi","nama_provinsi","kategori_wisatawan","jumlah_teks","tahun","bulan"]
df["jumlah"]=pd.to_numeric(df["jumlah_teks"].str.replace(",","",regex=False),errors="coerce")
df["kategori_wisatawan"]=df["kategori_wisatawan"].replace({"Wisatawan Mancaegara":"Wisatawan Mancanegara"})
df.to_csv(out/"kunjungan_wisatawan_ntb_bersih.csv",index=False)
print(df.shape, "duplikat:",df.duplicated().sum())
