# Folder Scrapers

Folder ini berisi script untuk pengumpulan data dari Periplus.com dan pembersihan data.

## 📄 Files

### 1. `scrape_periplus.py`
Script utama untuk scraping data buku dari Periplus.com.

**Features:**
- Scraping dari 8 kategori buku
- Target: 1500+ rows
- 16 fields per book (basic + extended info)
- Retry mechanism untuk handling network errors
- Random delay untuk menghindari rate limiting

**Fields yang di-scrape:**
- **Basic:** title, author, binding, category, price, discount, in_stock, url
- **Extended:** isbn, publisher, publication_date, pages, language, weight, review_count

**Usage:**
```bash
python scrapers/scrape_periplus.py
```

**Output:** `data/periplus_books_raw.csv`

**Estimasi waktu:** 30-45 menit (tergantung koneksi internet)

---

### 2. `clean_data.py`
Script untuk membersihkan data dan melakukan feature engineering.

**Cleaning steps:**
1. Handling missing values
2. Data type conversion
3. Duplicate removal
4. Invalid data removal

**Feature Engineering:**
1. `publication_year` - Ekstrak tahun dari publication_date
2. `book_age` - Umur buku (current_year - publication_year)
3. `price_per_page` - Harga per halaman
4. `popularity_score` - Skor popularitas (review_count × discount_bonus)
5. `is_new_release` - Flag buku baru (2024+)
6. `price_category` - Kategori harga (Budget/Mid-range/Premium/Luxury)
7. `has_discount` - Flag diskon

**Usage:**
```bash
python scrapers/clean_data.py
```

**Input:** `data/periplus_books_raw.csv`  
**Output:** 
- `data/periplus_books_clean.csv` - Dataset bersih
- `data/data_summary.txt` - Summary statistics

---

## 🚀 Workflow

1. **Step 1:** Run scraper
   ```bash
   python scrapers/scrape_periplus.py
   ```

2. **Step 2:** Clean data
   ```bash
   python scrapers/clean_data.py
   ```

3. **Step 3:** Analyze data (use notebooks)
   ```bash
   jupyter notebook notebooks/analysis.ipynb
   ```

---

## ⚙️ Configuration

### Kategori yang di-scrape:
- Fiction & Literature
- Business & Self-Help
- Children's Books
- Computer & IT
- Biographies & Memoirs
- Arts & Photography
- Cooking & Food
- Health & Fitness

### Scraping parameters:
- Pages per category: 8
- Expected products per page: ~20-25
- Total expected: ~1280-1600 rows
- Delay between products: 0.5-1.5 seconds
- Delay between pages: 2-4 seconds

---

## 🔧 Troubleshooting

### Problem: "No products found"
- **Cause:** Website structure changed atau network error
- **Solution:** Check website HTML structure, adjust selectors

### Problem: "Timeout errors"
- **Cause:** Slow internet connection
- **Solution:** Increase timeout value in `requests.get(timeout=20)`

### Problem: "Rate limited / Blocked"
- **Cause:** Too many requests too fast
- **Solution:** Increase delay values (currently safe at 2-4s per page)

### Problem: "Missing data in clean dataset"
- **Cause:** Website tidak punya field tertentu (misal: pages, weight)
- **Solution:** This is expected, cleaning script handles missing values properly

---

## 📝 Notes

- Script menggunakan `BeautifulSoup` untuk parsing HTML
- User-Agent header digunakan untuk menghindari blocking
- Data di-scrape dari halaman publik (legal & ethical)
- Hasil scraping dapat berbeda tergantung waktu (produk baru, diskon berubah)
