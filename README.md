# UTS Data Acquisition & Management
## Analisis Data Pariwisata Nusa Tenggara Barat (NTB)

### Identitas Mahasiswa
| Keterangan | Data |
|---|---|
| Nama | Mikael Gunawan Antul |
| NIM | 2501010318 |
| Kelas | F |
| Program Studi | Informatika |
| Perguruan Tinggi | INSTIKI |
| Mata Kuliah | Data Acquisition & Management |
| Tahun | 2026 |

## Deskripsi
Proyek ini mengakuisisi dan mengolah data kunjungan wisatawan Provinsi Nusa Tenggara Barat. Tiga metode yang dirancang adalah unduh dataset terbuka, API cuaca Open-Meteo, dan web scraping halaman katalog statis yang hanya dilakukan jika diizinkan robots.txt.

## Dataset utama
- Nama: Jumlah Kunjungan Wisatawan berdasarkan Jenis Wisatawan
- Sumber: [Satu Data NTB](https://data.ntbprov.go.id/dataset/9e270f88-a604-4640-a4f0-24c996122b92/show)
- File asli: `data/raw/dataset_kunjungan_wisatawan_ntb_asli.xlsx`
- Ukuran: 300 baris × 7 kolom (berdasarkan file yang diterima)
- Lisensi: metadata portal menunjukkan **License Not Specified**; konfirmasi ke pengelola sebelum redistribusi.

## Metode
1. Membaca dan memeriksa Excel dengan Pandas.
2. Mengambil data cuaca harian Mataram tahun 2024 melalui Open-Meteo Historical Weather API. Data API harus diambil ketika notebook dijalankan.
3. Memeriksa `robots.txt` sebelum scraping katalog Satu Data NTB. Jika robots tidak dapat diperiksa atau melarang target, scraping dihentikan.
4. Merangkum cuaca per bulan dan menggabungkan dengan data kunjungan tahun 2024 memakai `validate='many_to_one'`.

## Struktur folder
```text
notebooks/   notebook utama
data/raw/    sumber mentah tanpa perubahan
data/processed/ data hasil pembersihan dan penggabungan
metadata/    provenance, checksum, checklist etika
src/         skrip akuisisi dan pengolahan
docs/        laporan proyek
```

## Cara menjalankan
1. Buka notebook `notebooks/UTS_Data_Acquisition_Pariwisata_NTB.ipynb` di Google Colab.
2. Isi nama, NIM, dan email kampus pribadi pada sel identitas/User-Agent.
3. Jalankan semua sel dari atas ke bawah.
4. Pastikan API berhasil, status robots.txt tercatat, dan scraping hanya berjalan bila diizinkan.
5. Periksa hasil di `data/raw`, `data/processed`, dan `metadata`.

## Atribusi
Data cuaca: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), data ditawarkan di bawah CC BY 4.0 dan memerlukan atribusi: [Open-Meteo](https://open-meteo.com/).

## Status hasil
File Excel asli dan hasil pembersihan lokal disertakan. File API, scraping, dan merge dibuat oleh notebook saat dijalankan; jangan menganggap akuisisi tersebut selesai sebelum sel notebook sukses dan file keluarannya tersedia.
