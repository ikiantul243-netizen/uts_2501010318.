
# UTS DATA ACQUISITION & MANAGEMENT
## Analisis Data Pariwisata Nusa Tenggara Barat (NTB)

## 1. Identitas Mahasiswa

| Keterangan | Data Mahasiswa |
|---|---|
| Nama | Mikael Gunawan Antul |
| NIM | 2501010318 |
| Kelas | F |
| Program Studi | Informatika |
| Mata Kuliah | Data Acquisition & Management |
| Perguruan Tinggi | INSTIKI |
| Tahun Akademik | 2026 |

## 2. Deskripsi Proyek

Proyek ini dibuat untuk memenuhi tugas Ujian Tengah Semester (UTS)
mata kuliah Data Acquisition & Management.

Topik yang dipilih adalah **Analisis Data Pariwisata Nusa Tenggara Barat (NTB)**.
Proyek ini bertujuan mengumpulkan, mengolah, dan menggabungkan data
kunjungan wisatawan dengan informasi pendukung melalui tiga metode
akuisisi data, yaitu dataset terbuka, API, dan web scraping.

## 3. Tujuan Proyek

1. Mengumpulkan data kunjungan wisatawan di Provinsi NTB.
2. Memahami proses akuisisi data dari berbagai sumber.
3. Mengambil data tambahan menggunakan API.
4. Melakukan web scraping pada halaman yang diizinkan.
5. Membersihkan dan menggabungkan data menggunakan Python.
6. Mendokumentasikan sumber, lisensi, dan proses pengambilan data.

## 4. Sumber Data

| No. | Metode Akuisisi | Sumber | Keterangan |
|---|---|---|---|
| 1 | Dataset terbuka | Satu Data NTB | Data kunjungan wisatawan NTB |
| 2 | API | Open-Meteo | Data cuaca wilayah NTB |
| 3 | Web Scraping | Halaman statis yang diizinkan | Informasi pendukung pariwisata NTB |

**Sumber dataset utama:**

https://data.ntbprov.go.id/dataset/9e270f88-a604-4640-a4f0-24c996122b92/show

## 5. Metode Pengerjaan

Proyek ini menggunakan beberapa tahapan:

1. Mengunduh dataset Excel dari portal Satu Data NTB.
2. Memeriksa jumlah baris, kolom, dan tipe data.
3. Mengambil data cuaca melalui API Open-Meteo.
4. Memeriksa robots.txt sebelum melakukan web scraping.
5. Mengambil informasi dari halaman web statis yang diizinkan.
6. Membersihkan dan menormalisasi data.
7. Menggabungkan minimal dua sumber data menggunakan Pandas.
8. Memeriksa duplikasi dan kesesuaian hasil penggabungan.
9. Menyimpan hasil dan dokumentasi proyek.

## 6. Struktur Folder Proyek

```text
UTS-DAM-Pariwisata-NTB/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   └── UTS_Data_Acquisition_Pariwisata_NTB.ipynb
│
├── data/
│   ├── raw/
│   │   ├── dataset_kunjungan_wisatawan_ntb_asli.xlsx
│   │   ├── api_cuaca_ntb_raw.json
│   │   └── hasil_scraping_ntb_raw.csv
│   │
│   └── processed/
│       └── dataset_gabungan_pariwisata_ntb.csv
│
├── metadata/
│   ├── provenance.csv
│   ├── md5_checksum.txt
│   └── data_ethics_checklist.md
│
├── src/
│   ├── acquisition_api.py
│   ├── web_scraping.py
│   └── data_processing.py
│
└── docs/
    └── laporan_uts.md
```

## 7. Tools dan Teknologi

| No. | Tools | Kegunaan |
|---|---|---|
| 1 | Python | Bahasa pemrograman |
| 2 | Google Colab | Menjalankan notebook |
| 3 | Pandas | Pengolahan data |
| 4 | Requests | Mengakses API dan halaman web |
| 5 | BeautifulSoup | Web scraping |
| 6 | OpenPyXL | Membaca file Excel |
| 7 | GitHub | Penyimpanan dan dokumentasi proyek |

## 8. Hasil yang Diharapkan

Hasil akhir proyek ini meliputi:

- Dataset mentah kunjungan wisatawan NTB.
- Dataset hasil pengambilan melalui API.
- Dataset hasil web scraping yang diizinkan.
- Dataset gabungan dari minimal dua sumber.
- Notebook Python yang dapat dijalankan.
- Dokumentasi provenance dan checksum MD5.
- Checklist etika akuisisi data.

## 9. Etika dan Penggunaan Data

Pengumpulan data dilakukan dengan memperhatikan ketentuan berikut:

- Menggunakan sumber data yang dapat diakses secara sah.
- Memeriksa ketentuan lisensi dan penggunaan data.
- Memeriksa robots.txt sebelum melakukan scraping.
- Menggunakan User-Agent yang sesuai.
- Menggunakan timeout dan jeda antar-request.
- Tidak mengambil data pribadi yang tidak diperlukan.
- Tidak menyimpan API key atau token rahasia di repository.

## 10. Kesimpulan

Proyek ini diharapkan dapat memberikan pemahaman mengenai
proses Data Acquisition & Management melalui pengumpulan data
dari berbagai sumber, pengolahan menggunakan Python, serta
penggabungan data untuk mendukung analisis sektor pariwisata
di Provinsi Nusa Tenggara Barat.
