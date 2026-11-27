import os
import json
import hashlib
import time
import urllib.robotparser
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 1. IDENTITAS MAHASISWA & KONFIGURASI PROYEK
NAMA_MAHASISWA = "Mikael Gunawan Antul"
NIM = "2501010318"
PRODI_KELAS = "Isi Program Studi / Kelas Anda"
CAMPUS_EMAIL = "GANTI_DENGAN_EMAIL_KAMPUS_PRIBADI"  # Wajib diisi email kampus pribadi

BASE_DIR = "/content/UTS_DAM_Pariwisata_NTB"
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
META_DIR = os.path.join(BASE_DIR, "metadata")

for folder in [RAW_DIR, PROC_DIR, META_DIR]:
    os.makedirs(folder, exist_ok=True)

HEADERS = {
    "User-Agent": f"StudentDataAcquisitionProject/1.0 ({NAMA_MAHASISWA} - {NIM}; contact: {CAMPUS_EMAIL})"
}
# 2. METODE 1: DATASET TERBUKA (EXCEL ASLI)
raw_excel_path = os.path.join(RAW_DIR, "dataset_kunjungan_wisatawan_ntb_asli.xlsx")

if not os.path.exists(raw_excel_path):
    print(f"[INFO] File {raw_excel_path} belum ditemukan. Silakan unggah file Excel asli:")
    try:
        from google.colab import files
        uploaded = files.upload()
        for fname in uploaded:
            if fname.endswith(".xlsx"):
                os.replace(fname, raw_excel_path)
                break
    except ImportError:
        raise FileNotFoundError(f"Letakkan dataset asli di {raw_excel_path}")

# Baca salinan untuk analisis tanpa mengubah file mentah
xls = pd.ExcelFile(raw_excel_path)
sheet_utama = xls.sheet_names[0]
df_wisatawan = pd.read_excel(raw_excel_path, sheet_name=sheet_utama)

# Standardisasi salah eja 'Wisatawan Mancaegara' hanya pada salinan analisis
df_wisatawan_clean = df_wisatawan.copy()
for col in df_wisatawan_clean.select_dtypes(include="object").columns:
    df_wisatawan_clean[col] = (
        df_wisatawan_clean[col]
        .astype(str)
        .str.strip()
        .str.replace("Wisatawan Mancaegara", "Wisatawan Mancanegara", regex=False)
    )

clean_wisatawan_csv = os.path.join(PROC_DIR, "dataset_kunjungan_wisatawan_ntb_clean.csv")
df_wisatawan_clean.to_csv(clean_wisatawan_csv, index=False)
print("[OK] Dataset utama dibersihkan:", df_wisatawan_clean.shape)

# 3. METODE 2: OPEN-METEO HISTORICAL WEATHER API
# Koordinat Kota Mataram (-8.5833, 116.1167) tahun 2024
api_url = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=-8.5833&longitude=116.1167"
    "&start_date=2024-01-01&end_date=2024-12-31"
    "&daily=temperature_2m_mean,precipitation_sum"
    "&timezone=Asia%2FMakassar"
)

time.sleep(1)  # Jeda sopan antar-request
resp_api = requests.get(api_url, headers=HEADERS, timeout=15)
resp_api.raise_for_status()
weather_json = resp_api.json()

raw_api_path = os.path.join(RAW_DIR, "open_meteo_mataram_2024_raw.json")
with open(raw_api_path, "w", encoding="utf-8") as f:
    json.dump(weather_json, f, indent=2, ensure_ascii=False)

df_weather = pd.DataFrame({
    "tanggal": pd.to_datetime(weather_json["daily"]["time"]),
    "suhu_rata_c": weather_json["daily"]["temperature_2m_mean"],
    "curah_hujan_mm": weather_json["daily"]["precipitation_sum"],
})
df_weather["tahun"] = df_weather["tanggal"].dt.year
df_weather["bulan"] = df_weather["tanggal"].dt.month

df_weather_bulanan = (
    df_weather.groupby(["tahun", "bulan"], as_index=False)
    .agg(
        rata_suhu_mataram_c=("suhu_rata_c", "mean"),
        total_hujan_mataram_mm=("curah_hujan_mm", "sum"),
    )
    .round(2)
)

proc_api_path = os.path.join(PROC_DIR, "cuaca_mataram_2024_normalized.csv")
df_weather_bulanan.to_csv(proc_api_path, index=False)
print("[OK] Data API cuaca Mataram dinormalisasi:", df_weather_bulanan.shape)

# 4. METODE 3: CEK ROBOTS.TXT & WEB SCRAPING
target_scrape_url = "https://data.ntbprov.go.id/dataset/9e270f88-a604-4640-a4f0-24c996122b92/show"
robots_url = "https://data.ntbprov.go.id/robots.txt"

rp = urllib.robotparser.RobotFileParser()
rp.set_url(robots_url)

robots_log_path = os.path.join(META_DIR, "bukti_robots_txt.txt")
try:
    time.sleep(1)
    resp_robots = requests.get(robots_url, headers=HEADERS, timeout=15)
    robots_raw_text = resp_robots.text
    rp.parse(robots_raw_text.splitlines())
    boleh_scrape = rp.can_fetch("*", target_scrape_url)
except Exception as e:
    robots_raw_text = f"Gagal mengambil robots.txt: {e}"
    boleh_scrape = False

with open(robots_log_path, "w", encoding="utf-8") as f:
    f.write(f"URL Target: {target_scrape_url}\n")
    f.write(f"Status Izin robots.txt: {'DIIZINKAN' if boleh_scrape else 'DILARANG / TIDAK TERVERIFIKASI'}\n")
    f.write("-" * 50 + "\n")
    f.write(robots_raw_text)

if boleh_scrape:
    time.sleep(2)
    resp_page = requests.get(target_scrape_url, headers=HEADERS, timeout=15)
    resp_page.raise_for_status()
    raw_html_path = os.path.join(RAW_DIR, "detail_dataset_ntb_raw.html")
    with open(raw_html_path, "w", encoding="utf-8") as f:
        f.write(resp_page.text)

    soup = BeautifulSoup(resp_page.text, "html.parser")
    judul_halaman = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Satu Data NTB"
    df_scrape = pd.DataFrame([{
        "url_sumber": target_scrape_url,
        "judul_halaman": judul_halaman,
        "lisensi_portal": "License Not Specified",
        "status_robots": "Allowed"
    }])
else:
    print("[PERINGATAN] Scraping dihentikan karena robots.txt melarang atau gagal diverifikasi.")
    df_scrape = pd.DataFrame([{
        "url_sumber": target_scrape_url,
        "judul_halaman": "Dihentikan sesuai kepatuhan robots.txt",
        "lisensi_portal": "License Not Specified",
        "status_robots": "Disallowed / Stopped"
    }])

proc_scrape_path = os.path.join(PROC_DIR, "hasil_scraping_metadata_ntb.csv")
df_scrape.to_csv(proc_scrape_path, index=False)

# 5. PENGGABUNGAN DATA (MERGE)
df_merged = df_wisatawan_clean.copy()
if "tahun" in df_merged.columns and "bulan" in df_merged.columns:
    df_merged = df_merged.merge(df_weather_bulanan, on=["tahun", "bulan"], how="left")
else:
    df_merged["rata_suhu_mataram_2024_c"] = round(df_weather["suhu_rata_c"].mean(), 2)
    df_merged["total_hujan_mataram_2024_mm"] = round(df_weather["curah_hujan_mm"].sum(), 2)

df_merged["sumber_portal"] = df_scrape.loc[0, "url_sumber"]
merged_path = os.path.join(PROC_DIR, "data_gabungan_pariwisata_ntb.csv")
df_merged.to_csv(merged_path, index=False)
print("[OK] Hasil merge tersimpan:", df_merged.shape)

# 6. METADATA: PROVENANCE, ETHICS & MD5
pd.DataFrame([
    {"berkas": "data/raw/dataset_kunjungan_wisatawan_ntb_asli.xlsx", "sumber": "Satu Data NTB", "metode": "Open Dataset Download", "keterangan": "300 baris, 7 kolom (utuh/tidak diubah)"},
    {"berkas": "data/raw/open_meteo_mataram_2024_raw.json", "sumber": "Open-Meteo Historical API", "metode": "REST API GET", "keterangan": "Cuaca harian Mataram tahun 2024"},
    {"berkas": "data/processed/dataset_kunjungan_wisatawan_ntb_clean.csv", "sumber": "Salinan dataset Excel asli", "metode": "Data Cleaning", "keterangan": "Perbaikan ejaan Wisatawan Mancanegara"},
    {"berkas": "data/processed/cuaca_mataram_2024_normalized.csv", "sumber": "open_meteo_mataram_2024_raw.json", "metode": "Agregasi Bulanan", "keterangan": "Rata-rata suhu & total curah hujan"},
    {"berkas": "data/processed/data_gabungan_pariwisata_ntb.csv", "sumber": "Dataset Wisatawan + API Cuaca + Scraping", "metode": "Data Merge", "keterangan": "Dataset siap analisis"},
]).to_csv(os.path.join(META_DIR, "provenance.csv"), index=False)

pd.DataFrame([
    {"aspek": "Keaslian Data Mentah", "status": "Patuh", "catatan": "File Excel asli di data/raw/ tidak diubah; perbaikan dilakukan pada salinan."},
    {"aspek": "Kepatuhan robots.txt", "status": "Patuh", "catatan": "Pemeriksaan robots.txt dilakukan sebelum scraping dan terdokumentasi."},
    {"aspek": "Identitas & Rate Limit", "status": "Patuh", "catatan": "Menggunakan User-Agent email kampus, timeout 15s, dan jeda antar-request."},
    {"aspek": "Klarifikasi Lisensi", "status": "Catatan", "catatan": "Portal mencantumkan License Not Specified; digunakan hanya untuk tugas akademik."},
    {"aspek": "Keamanan Kredensial", "status": "Patuh", "catatan": "Tidak ada token, password, atau kredensial yang disimpan di repository."},
]).to_csv(os.path.join(META_DIR, "data_ethics_checklist.csv"), index=False)

# 7. GENERATE README.md FORMAT TABEL
readme_content = f"""# UTS Data Acquisition & Management — Pariwisata NTB

## Identitas Mahasiswa & Repository

| Atribut | Keterangan |
| :--- | :--- |
| **Nama Mahasiswa** | {Mikael Gunawan Antul} |
| **NIM** | `{2501010318}` |
| **Program Studi / Kelas** | {informatika/F} |
| **Mata Kuliah** | Data Acquisition and Management |
| **Email Kampus** | `{mikiantul@gmail.com}` |
| **Repository GitHub** | [github.com/ikantul243-netizen/uts_2501010318](https://github.com/ikantul243-netizen/uts_2501010318) |

## Ringkasan Proyek & Sumber Akuisisi

| Komponen | Rincian |
| :--- | :--- |
| **Topik Analisis** | Analisis jumlah kunjungan wisatawan berdasarkan jenis wisatawan di Provinsi Nusa Tenggara Barat |
| **Dataset Utama** | [Satu Data NTB — Jumlah Kunjungan Wisatawan berdasarkan Jenis Wisatawan](https://data.ntbprov.go.id/dataset/9e270f88-a604-4640-a4f0-24c996122b92/show) |
| **Berkas Utama** | `data/raw/dataset_kunjungan_wisatawan_ntb_asli.xlsx` (**300 baris**, **7 kolom**) |
| **Metode 1 — Dataset Terbuka** | File Excel Satu Data NTB (300 baris, 7 kolom) |
| **Metode 2 — API** | Open-Meteo Historical Weather API, data cuaca harian titik Mataram tahun 2024 |
| **Metode 3 — Web Scraping** | Halaman detail Satu Data NTB, hanya dilakukan apabila `robots.txt` mengizinkan |

## Struktur Direktori

| Jalur Folder / Berkas | Deskripsi Isi |
| :--- | :--- |
| `UTS_Data_Acquisition_Pariwisata_NTB.ipynb` | Notebook utama Google Colab berisi seluruh kode akuisisi, pembersihan, dan merge |
| `data/raw/` | Dataset Excel asli dan hasil mentah API/scraping |
| `data/processed/` | Data API yang dinormalisasi dan hasil merge |
| `metadata/` | Provenance, MD5, Data Ethics Checklist, dan bukti `robots.txt` |
| `README.md` | Dokumentasi lengkap proyek dalam format tabel |

## Cara Menjalankan di Google Colab

| Tahap | Langkah Eksekusi | Keterangan |
| :--- | :--- | :--- |
| **1** | Upload ZIP ke Google Drive atau ekstrak pada komputer | Pastikan folder `data/raw` tersedia |
| **2** | Buka notebook `.ipynb` dengan Google Colab | Gunakan runtime Python 3 |
| **3** | Isi identitas mahasiswa dan email kampus pribadi pada sel persiapan | Wajib untuk header `User-Agent` |
| **4** | Pastikan file XLSX tersedia pada `data/raw` | Bila tidak ada, notebook meminta upload |
| **5** | Jalankan semua sel berurutan | Eksekusi dari atas ke bawah |
| **6** | Periksa output API, `robots.txt`, scraping, provenance, dan merge | Pastikan seluruh file keluaran terbentuk |
| **7** | Jangan lanjutkan scraping bila `robots.txt` melarang URL target | Pilih halaman statis lain yang diizinkan dan dokumentasikan |
| **8** | Simpan notebook setelah seluruh sel dijalankan | Unggah ke GitHub tanpa token/password/kredensial |

## Catatan Kualitas dan Etika

| Aspek | Keterangan |
| :--- | :--- |
| **Standardisasi Ejaan** | Dataset berisi 300 baris dan 7 kolom. Terdapat satu variasi salah eja kategori `Wisatawan Mancaegara`, yang distandardisasi hanya pada salinan analisis; file mentah tidak diubah. |
| **Lisensi Dataset** | Metadata portal menyatakan lisensi `License Not Specified`, sehingga izin penggunaan ulang harus diklarifikasi. |
| **Keterbatasan API Cuaca** | API cuaca pada koordinat Mataram tidak mewakili seluruh wilayah Provinsi NTB. |
| **Keamanan GitHub** | Unggah notebook, folder `data`, `metadata`, dan `README.md` setelah semua akuisisi berhasil. Jangan unggah token, password, atau file kredensial. |
"""

with open(os.path.join(BASE_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

# Hitung MD5 untuk seluruh berkas di data/ dan metadata/
md5_records = []
for root, _, files_list in sorted(os.walk(BASE_DIR)):
    for fname in sorted(files_list):
        full_p = os.path.join(root, fname)
        rel_p = os.path.relpath(full_p, BASE_DIR).replace("\\", "/")
        if rel_p == "metadata/checksums.md5":
            continue
        h = hashlib.md5()
        with open(full_p, "rb") as fb:
            h.update(fb.read())
        md5_records.append(f"{h.hexdigest()}  {rel_p}")

with open(os.path.join(META_DIR, "checksums.md5"), "w", encoding="utf-8") as f:
    f.write("\n".join(md5_records) + "\n")

print("[SELESAI] Seluruh struktur folder, data, metadata, dan README.md berhasil dibuat di:", BASE_DIR)
