import os
import json
import hashlib
import time
import urllib.robotparser
import requests
import pandas as pd
from bs4 import BeautifulSoup
 
## Proyek UTS - Data Acquisition & Management (DAM)
Repositori ini disusun untuk memenuhi Ujian Tengah Semester (UTS) mata kuliah Data Acquisition & Management (DAM). Proyek ini mencakup proses akuisisi data dari tiga sumber berbeda (Download CSV/Excel, REST API, dan Web Scraping), verifikasi etika pengambilan data (robots.txt), pembersihan data (data cleaning), hingga penggabungan data ke dalam format tabel terstruktur. 

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
