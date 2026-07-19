# Tugas Data Science - Semester Genap 2025/2026

Repositori ini digunakan untuk pengerjaan **Tugas** mata kuliah **Data Science** (Kelas IF404) Program Studi PJJ Informatika S1.

---

## 👥 Anggota Kelompok
1. Sutan Gading Fadhillah Nasution (250401020159)
2. Rina Mardiana (250401020151)

## 📖 Studi Kasus Proyek
**Analisis E-Commerce: Sistem Rekomendasi dan Analisis Harga Buku Periplus.com**

Proyek ini mencakup 7 analisis utama:
1. ✅ Manajemen Data
2. ✅ Asosiasi Data
3. ✅ Korelasi Data
4. ✅ Analisis Regresi
5. ✅ Klasifikasi Data
6. ✅ Clustering Data
7. ✅ Big Data dan Perkembangannya

---

## 📂 Struktur Repositori
* `README.md` - Informasi umum proyek dan panduan penggunaan
* `SOAL.md` - Detail soal tugas dan requirements
* `scrapers/` - Script untuk scraping dan cleaning data
  * `scrape_periplus.py` - Scraper utama dengan field lengkap
  * `clean_data.py` - Script pembersihan dan feature engineering
* `data/` - Dataset hasil scraping (raw dan clean)
* `notebooks/` - Jupyter notebooks untuk analisis
* `plots/` - Visualisasi hasil analisis
* `models/` - Model machine learning yang terlatih
* `requirements.txt` - Dependencies Python

---

## 🛠️ Panduan Menjalankan Proyek

### 1. Setup Virtual Environment

#### A. Membuat Virtual Environment
```bash
python3 -m venv env
```

#### B. Aktivasi Virtual Environment
**macOS / Linux:**
```bash
source env/bin/activate
```

**Windows (Command Prompt):**
```cmd
env\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.\env\Scripts\Activate.ps1
```

#### C. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 2. Scraping Data

#### A. Scraping Data Mentah (Target: 1500 rows)
Script ini akan scrape data dengan field lengkap:
- Basic info: title, author, binding, category, price, discount
- Extended info: pages, publisher, publication_date, isbn, review_count, weight, language

```bash
python scrapers/scrape_periplus.py
```

Output: `data/periplus_books_raw.csv`

*Note: Proses ini memakan waktu ~30-45 menit karena scraping detail setiap produk dengan delay untuk safety.*

#### B. Cleaning & Feature Engineering
```bash
python scrapers/clean_data.py
```

Output: `data/periplus_books_clean.csv`

Features tambahan yang di-generate:
- `book_age` - Umur buku (tahun)
- `price_per_page` - Harga per halaman
- `popularity_score` - Skor popularitas berdasarkan review count
- `is_new_release` - Flag untuk buku baru (2024+)

---

### 3. Analisis Data

Gunakan Jupyter Notebook untuk analisis interaktif:

```bash
jupyter notebook
```

Atau buka `notebooks/analysis.ipynb` di VS Code dengan ekstensi Jupyter.

---

## 📊 Dataset Structure

### Raw Dataset Fields:
| Field | Type | Description |
|-------|------|-------------|
| title | string | Judul buku |
| author | string | Nama penulis |
| binding | string | Jenis cover (Paperback/Hardcover) |
| in_stock | int | Ketersediaan (1=ada, 0=habis) |
| category | string | Kategori buku |
| product_url | string | URL produk |
| price_idr | float | Harga saat ini (IDR) |
| original_price_idr | float | Harga asli (IDR) |
| discount_percent | float | Persentase diskon |
| **isbn** | string | ISBN-13 (unique identifier) |
| **publisher** | string | Nama penerbit |
| **publication_date** | string | Tanggal terbit |
| **pages** | int | Jumlah halaman |
| **language** | string | Bahasa buku |
| **weight** | float | Berat buku (kg) |
| **review_count** | int | Jumlah customer review |

### Cleaned Dataset (Additional Features):
- `book_age` - 2026 - publication_year
- `price_per_page` - price_idr / pages
- `popularity_score` - Computed metric
- `is_new_release` - Boolean flag

---

## 🎯 Target & Goals

- **Dataset Size:** 1500+ rows
- **Categories:** 8-10 kategori berbeda
- **Data Quality:** <5% missing values
- **Use Cases:**
  - Price prediction model
  - Book recommendation system
  - Publisher & category analysis
  - Customer behavior insights

---

## 📝 Notes

- Script menggunakan random delay (1-3 detik) untuk menghindari rate limiting
- Data di-scrape dari halaman publik Periplus.com
- Untuk troubleshooting, cek log output di terminal
