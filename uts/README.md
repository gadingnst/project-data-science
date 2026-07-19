# UTS Data Science - Semester Genap 2025/2026

Repositori ini digunakan untuk pengerjaan proyek Ujian Tengah Semester (UTS) mata kuliah **Data Science** (Kelas IF404) Program Studi PJJ Informatika S1.

---

## 👥 Anggota Kelompok
1. Sutan Gading Fadhillah Nasution (250401020159)
2. Rina Mardiana (250401020151)

## 📖 Studi Kasus Proyek
**Analisis Harga dan Kategori Buku Impor pada E-Commerce Periplus.com**

## 📂 Struktur Repositori
* `README.md` - Informasi umum proyek dan soal UTS.
* `BREAKDOWN_UTS.md` - Rencana kerja dan breakdown tugas UTS.
* `scrapers/` - Folder berisi script untuk pengumpulan dan pembersihan data.
  * `scrape_periplus.py` - Script scraper untuk mengambil data buku dari Periplus.com.
  * `clean_data.py` - Script untuk pembersihan data mentah hasil scraping.
* `analyze_data.py` - Script untuk melakukan analisis statistika deskriptif dan menghasilkan visualisasi data.
* `project_data_science.ipynb` - Jupyter Notebook interaktif untuk analisis eksploratif data (EDA), visualisasi, dan rekomendasi bisnis.
* `data/` - Folder berisi dataset hasil scraping (raw dan clean) serta ringkasan statistik.
* `plots/` - Folder berisi file gambar visualisasi data hasil analisis.
* `requirements.txt` - File daftar dependencies Python yang dibutuhkan.

---

## 🛠️ Panduan Menjalankan Proyek

### 1. Prasyarat & Setup Virtual Environment (venv)
Sangat disarankan menggunakan virtual environment agar dependencies tidak menimpa package Python global kita.

#### Langkah A: Membuat Virtual Environment
Jalankan perintah berikut di root directory proyek:

```bash
# Membuat venv dengan nama 'env' (atau nama lain bebas)
python3 -m venv env
```

#### Langkah B: Mengaktifkan Virtual Environment
* **macOS / Linux:**
  ```bash
  source env/bin/activate
  ```
* **Windows (Command Prompt):**
  ```cmd
  env\Scripts\activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .\env\Scripts\Activate.ps1
  ```

#### Langkah C: Menginstal Dependencies
Setelah virtual environment aktif (ditandai dengan tulisan `(env)` di terminal), instal library yang diperlukan menggunakan `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Cara Menjalankan Scraper
Pastikan virtual environment kita **tetap aktif** dan jalankan semua perintah dari **root directory** repositori ini.

#### Langkah A: Scraping Data Mentah
Jalankan script scraper untuk mengambil data dari Periplus.com. Script ini akan mengambil sekitar 500-600 baris data dari 5 kategori berbeda dan menyimpannya sebagai `data/periplus_books_raw.csv`.

```bash
python scrapers/scrape_periplus.py
```

*Catatan: Script ini menggunakan delay acak (1.0 s.d 2.5 detik) di setiap halaman agar proses scraping berjalan aman dan tidak membebani server target.*

#### Langkah B: Pembersihan Data
Setelah proses scraping selesai dan file `data/periplus_books_raw.csv` terbentuk, jalankan script pembersihan untuk merapikan format harga, menghitung diskon, menangani missing values, dan menghasilkan dataset bersih `data/periplus_books_clean.csv`.

```bash
python scrapers/clean_data.py
```

#### Langkah C: Analisis dan Visualisasi Data
Setelah dataset bersih `data/periplus_books_clean.csv` terbentuk, jalankan script analisis untuk melakukan kalkulasi statistika deskriptif dan menghasilkan visualisasi data ke dalam folder `plots/`.

```bash
python analyze_data.py
```

Hasil dari langkah ini:
* File `data/descriptive_statistics.txt` yang berisi ringkasan statistik deskriptif data.
* Folder `plots/` yang berisi 4 file visualisasi grafik (distribusi harga, boxplot outlier, bar chart kategori, dan perbandingan harga per kategori).

---

### 3. Eksplorasi Interaktif dengan Jupyter Notebook (.ipynb)

Untuk melakukan analisis secara interaktif dan melihat visualisasi beserta penjelasan lengkap langkah demi langkah, kita dapat menggunakan Jupyter Notebook yang telah disediakan (`project_data_science.ipynb`).

#### Opsi A: Menggunakan VS Code (Rekomendasi)
1. Pastikan kita telah menginstal ekstensi **Jupyter** di VS Code.
2. Pastikan virtual environment `env` telah aktif.
3. Buka file `project_data_science.ipynb` di VS Code.
4. Pilih kernel Python dari virtual environment (`env/bin/python`).
5. Klik **Run All** atau jalankan setiap cell secara berurutan.

#### Opsi B: Menggunakan Jupyter Notebook Server di Browser
1. Pastikan virtual environment kita telah aktif.
2. Instal Jupyter Notebook di venv kita (jika belum terinstal):
   ```bash
   pip install notebook
   ```
3. Jalankan server Jupyter:
   ```bash
   jupyter notebook
   ```
4. Browser akan otomatis terbuka dan menampilkan dashboard Jupyter. Buka file `project_data_science.ipynb` dan jalankan cell yang ada.
