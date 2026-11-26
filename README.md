# UTS Data Acquisition & Management — Pariwisata NTB

## Topik
Analisis Jumlah Kunjungan Wisatawan berdasarkan Jenis Wisatawan di Provinsi Nusa Tenggara Barat (NTB), dengan data cuaca Mataram sebagai variabel pendukung.

## Sumber
1. Dataset utama: [Satu Data NTB — Jumlah Kunjungan Wisatawan berdasarkan Jenis Wisatawan](https://data.ntbprov.go.id/dataset/9e270f88-a604-4640-a4f0-24c996122b92/show)
2. API: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
3. Scraping: [Katalog dataset Satu Data NTB, publisher Dinas Pariwisata](https://data.ntbprov.go.id/index.php/dataset?publisher=18), hanya dijalankan jika robots.txt mengizinkan.

## Cara menjalankan di Google Colab
1. Upload folder/repository ini ke Google Drive atau buka file `.ipynb` di Colab.
2. Isi nama, NIM, kelas, dan email kampus pribadi pada bagian identitas.
3. Jalankan sel secara berurutan.
4. Saat diminta, unggah CSV asli yang diunduh melalui tombol Download CSV di halaman dataset utama.
5. Pastikan `CAMPUS_EMAIL` diisi email kampus pribadi sebelum request API/scraping.
6. Periksa hasil pemeriksaan robots.txt. Jika tidak diizinkan, jangan lanjutkan scraping; ganti halaman statis lain yang diizinkan dan dokumentasikan alasannya.
7. Periksa hasil merge dan file pada `data/processed` serta `metadata`.

## Struktur
- `data/raw/`: file mentah asli (tidak diedit).
- `data/processed/`: hasil normalisasi dan penggabungan.
- `metadata/`: provenance dan Data Ethics Checklist.
- `UTS_Data_Acquisition_Mikael.ipynb`: notebook utama.

## Catatan etika dan batasan
Metadata dataset utama menampilkan `License Not Specified`; jangan menyatakan dataset memiliki lisensi terbuka tanpa konfirmasi. Data cuaca diambil untuk titik Mataram, sehingga tidak mewakili seluruh NTB. Semua request web memakai timeout, User-Agent dengan email kampus, jeda, serta pemeriksaan robots.txt untuk scraping.

## Identitas
Lengkapi nama, NIM, kelas, dan email kampus pada notebook sebelum dikumpulkan.
