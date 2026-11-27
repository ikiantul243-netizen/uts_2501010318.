# Laporan UTS Data Acquisition & Management
## Analisis Data Pariwisata Nusa Tenggara Barat

### 1. Pendahuluan
Proyek ini mengkaji data jumlah kunjungan wisatawan berdasarkan jenis wisatawan di Provinsi Nusa Tenggara Barat. Akuisisi dirancang melalui dataset terbuka, API cuaca, dan web scraping yang mematuhi robots.txt.

### 2. Dataset utama dan pemeriksaan
Berkas Excel yang diterima berisi 300 baris dan 7 kolom. Kolom mencakup kode/nama provinsi, kategori wisatawan, jumlah orang, tahun, dan bulan. File mentah disimpan tanpa perubahan. Pada salinan analisis, jumlah dikonversi dari teks dengan pemisah ribuan menjadi numerik, dan satu variasi salah ketik kategori `Wisatawan Mancaegara` distandardisasi menjadi `Wisatawan Mancanegara`.

### 3. Etika dan lisensi
Metadata portal untuk dataset utama menampilkan `License Not Specified`. Oleh karena itu, proyek ini tidak mengklaim dataset utama berlisensi terbuka tertentu. Data yang terlihat bersifat agregat dan tidak memuat identitas langsung individu pada kolom yang diperiksa. Checklist terperinci tersedia di `metadata/data_ethics_checklist.md`.

### 4. Akuisisi API
Notebook mengambil data cuaca harian 2024 untuk titik Mataram (-8.5833, 116.1167) menggunakan Open-Meteo Historical Weather API. Variabel yang diminta adalah suhu rata-rata, curah hujan, dan kecepatan angin maksimum. API diharapkan menghasilkan lebih dari 30 baris harian. Atribusi Open-Meteo dan CC BY 4.0 dicantumkan.

### 5. Web scraping
Notebook memeriksa `https://data.ntbprov.go.id/robots.txt` sebelum mengakses katalog. Jika robots.txt tidak dapat diakses/diverifikasi atau melarang target, proses dihentikan. Hasil scraping hanya dinyatakan berhasil jika file keluaran terbentuk setelah notebook dijalankan.

### 6. Penggabungan data
Data kunjungan tahun 2024 digabung dengan ringkasan cuaca per bulan berdasarkan kunci tahun dan bulan. Karena terdapat beberapa kategori wisatawan per bulan dan satu baris cuaca per bulan, relasi merge menggunakan `validate='many_to_one'`. Pemeriksaan jumlah baris, indikator merge, dan duplikasi dilakukan di notebook.

### 7. Kesimpulan sementara
Dataset utama memenuhi batas minimal 100 baris. Data mentah, hasil pembersihan, provenance, dan checksum awal telah disiapkan. Hasil API, scraping, dan merge perlu dikonfirmasi dengan menjalankan seluruh sel notebook di Google Colab.
