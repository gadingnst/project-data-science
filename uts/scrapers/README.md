# Scrapers - Pengumpulan & Pembersihan Data

Folder ini berisi script Python yang digunakan untuk mengumpulkan data dari e-commerce target dan membersihkannya.

## Daftar Script
* `scrape_periplus.py` - Mengambil data buku impor dari Periplus.com secara otomatis lintas 5 kategori utama. Hasil output disimpan di `data/periplus_books_raw.csv`.
* `clean_data.py` - Melakukan pembersihan data (*data cleaning*) terhadap dataset mentah. Hasil output disimpan di `data/periplus_books_clean.csv`.

## Cara Menjalankan
Pastikan Anda berada di root directory proyek ini, lalu jalankan:

```bash
# 1. Scraping data mentah
python scrapers/scrape_periplus.py

# 2. Membersihkan data
python scrapers/clean_data.py
```
