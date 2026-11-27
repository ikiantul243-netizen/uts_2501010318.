# Data Ethics Checklist — Pariwisata NTB

| No. | Aspek | Pemeriksaan | Status awal | Bukti/catatan |
|---|---|---|---|---|
| 1 | Sumber dan tujuan | Dataset berasal dari portal Satu Data NTB dan dipakai untuk tugas akademik | Sesuai | URL dicatat pada provenance.csv |
| 2 | Lisensi | Metadata dataset utama menunjukkan License Not Specified | Perlu klarifikasi | Jangan menyatakan CC-BY/open license tanpa bukti |
| 3 | PII langsung | Kolom yang diperiksa tidak berisi nama/alamat/telepon individu | Tidak teridentifikasi | Dataset agregat wisatawan |
| 4 | Quasi-identifier | Wilayah, tahun, bulan, kategori adalah atribut agregat | Risiko rendah | Tidak mengidentifikasi individu secara langsung |
| 5 | Minimisasi | Analisis memakai kolom yang relevan | Sesuai | File mentah dipisahkan dari hasil olahan |
| 6 | Keamanan | Tidak menyimpan token/API key | Sesuai | Open-Meteo endpoint publik tanpa token untuk penggunaan ini |
| 7 | Transparansi | URL, tanggal akses, lisensi, nama file, MD5 dicatat | Sebagian | API/scraping dilengkapi otomatis setelah notebook dijalankan |
| 8 | Kepatuhan API/scraping | Timeout, User-Agent email kampus, jeda, status HTTP, robots.txt | Bersyarat | Scraping hanya berjalan jika robots.txt mengizinkan |
| 9 | Penyimpanan/publikasi | Raw dipertahankan, data turunan diberi sumber, rahasia tidak diunggah | Sesuai | Periksa isi folder sebelum publikasi |

Status ini adalah pemeriksaan awal dan harus diperbarui berdasarkan hasil nyata saat notebook dijalankan.
