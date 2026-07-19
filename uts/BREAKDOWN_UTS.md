# Breakdown Pengerjaan UTS Data Science (IF404)
**Studi Kasus: Analisis Harga dan Kategori Buku Impor pada E-Commerce Periplus.com**

Dokumen ini memuat rencana kerja (roadmap) dan monitoring progress untuk menyelesaikan UTS Data Science sebelum deadline tanggal **14 Juni 2026**.

---

## 📅 Monitoring Progress & Checklist Tugas

### Fase 1: Data Acquisition & Preprocessing
* [x] **1. Pembuatan Scraper Periplus.com (`scrapers/scrape_periplus.py`)**
  * Menggunakan `requests` dan `BeautifulSoup` untuk mengekstrak data dari halaman kategori Periplus.
  * Mengambil data dari 5 kategori berbeda dengan total target $\approx 500$ baris data.
  * Menyimpan dataset mentah ke `data/periplus_books_raw.csv`.
* [x] **2. Pembersihan Data (`scrapers/clean_data.py`)**
  * Membersihkan string harga (menghapus format "Rp", titik ribuan, spasi) dan konversi ke tipe data numerik (`float`).
  * Menangani data kosong (*missing values*) dan menyaring data yang tidak memiliki harga jual.
  * Menyimpan dataset bersih ke `data/periplus_books_clean.csv`.

### Fase 2: Analisis Statistik & Visualisasi
* [x] **1. Kalkulasi Statistika Deskriptif (`analyze_data.py`)**
  * Menghitung nilai pemusatan data: *Mean*, *Median*, *Mode*.
  * Menghitung nilai penyebaran data: *Standard Deviation*, *Variance*, *Range* (Min-Max), *Kuartil 1 (Q1)*, *Kuartil 3 (Q3)*, dan *Interquartile Range (IQR)*.
  * Melakukan deteksi pencilan (*outliers*) menggunakan metode IQR.
  * Menyimpan ringkasan statistik ke `data/descriptive_statistics.txt`.
* [x] **2. Pembuatan Visualisasi Data (Folder `/plots/`)**
  * [x] **Histogram:** Distribusi harga buku impor keseluruhan (`plots/price_distribution.png`).
  * [x] **Boxplot:** Deteksi outlier harga secara visual (`plots/price_boxplot.png`).
  * [x] **Bar Chart:** Sebaran jumlah buku per kategori (`plots/category_distribution.png`).
  * [x] **Boxplot per Kategori:** Membandingkan sebaran harga buku antar kategori (`plots/category_price_boxplot.png`).

### Fase 3: Dokumentasi & Penyusunan Laporan
* [x] **1. Pembuatan Jupyter Notebook (`project_data_science.ipynb`)**
  * Mengintegrasikan proses loading data, cleaning, kalkulasi statistik, visualisasi, dan rekomendasi bisnis ke dalam notebook interaktif.
* [x] **2. Penyusunan Makalah (`makalah_data_science.md`)**
  * Menyusun naskah akademis sesuai format soal UTS:
    * **BAB I: Pengantar Data Science** (Definisi & peran di e-commerce).
    * **BAB II: Teknik Pengumpulan Data** (Penjelasan scraper Periplus).
    * **BAB III: Eksplorasi & Kualitas Data** (Proses cleaning & kualitas data).
    * **BAB IV: Konsep Dasar Statistika & Peringkasan Data** (Tabel hasil kalkulasi statistik).
    * **BAB V: Penyajian & Visualisasi Data** (Penjelasan grafik hist/boxplot/bar).
    * **BAB VI: Studi Kasus & Manfaat bagi Pengguna** (Rekomendasi bisnis berbasis data untuk e-commerce/Periplus).

### Fase 4: Finalisasi & Submission (Target: 14 Juni 2026)
* [x] **1. Konversi Laporan ke PDF**
  * Mengonversi `makalah_data_science.md` ke format PDF dengan nama file sesuai instruksi: `DS_IF404_GadingNasution.pdf`.
* [ ] **2. Upload Google Drive & LMS**
  * Mengunggah dataset (CSV), notebook (IPYNB), dan PDF Makalah ke Google Drive.
  * Menyematkan link folder Google Drive di dalam makalah.
  * Mengumpulkan file PDF makalah di LMS Edlink.
