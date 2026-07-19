import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Daftar kategori target di Periplus.com untuk mendapatkan dataset yang representatif
CATEGORIES = {
    "Fiction & Literature": "https://www.periplus.com/c/1_32/fiction-and-amp-literature",
    "Business & Self-Help": "https://www.periplus.com/c/1_13/business-and-self-help",
    "Children's Books": "https://www.periplus.com/c/1_14/children-s-books",
    "Computer & IT": "https://www.periplus.com/c/1_15/computer-and-amp-it",
    "Biographies & Memoirs": "https://www.periplus.com/c/1_12/biographies-and-amp-memoirs"
}

def scrape_periplus():
    books_data = []
    
    # Header user-agent realistis agar tidak diblokir oleh web server
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
        "Referer": "https://www.periplus.com/"
    }

    print("=== Memulai Scraping Periplus.com ===")
    
    for category_name, base_url in CATEGORIES.items():
        print(f"\nScraping Kategori: {category_name}...")
        
        # Kita scrape 5 halaman per kategori untuk mendapatkan total data sekitar 500-600 baris
        for page in range(1, 6):
            url = f"{base_url}?page={page}"
            
            # Tambahkan retry mechanism untuk mengatasi timeout
            max_retries = 3
            response = None
            for attempt in range(1, max_retries + 1):
                print(f"Mengakses Halaman {page} (Percobaan {attempt}/{max_retries}): {url}")
                try:
                    response = requests.get(url, headers=headers, timeout=20)
                    if response.status_code == 200:
                        break
                    else:
                        print(f"Status code {response.status_code} pada percobaan {attempt}")
                except Exception as e:
                    print(f"Error pada percobaan {attempt}: {e}")
                
                if attempt < max_retries:
                    sleep_time = attempt * 5  # Backoff: 5s, 10s
                    print(f"Menunggu {sleep_time} detik sebelum mencoba lagi...")
                    time.sleep(sleep_time)
            
            if response is None or response.status_code != 200:
                print(f"Gagal mengakses {url} setelah {max_retries} percobaan. Lanjut ke kategori berikutnya.")
                break
            
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                products = soup.find_all('div', class_='single-product')
                
                if not products:
                    print("Tidak ada produk ditemukan di halaman ini. Selesai untuk kategori ini.")
                    break
                
                print(f"Menemukan {len(products)} produk di Halaman {page}.")
                
                for product in products:
                    # 1. Ekstraksi Judul & Link Produk
                    title_tag = product.find('div', class_='product-content')
                    title = ""
                    product_url = ""
                    if title_tag and title_tag.h3 and title_tag.h3.a:
                        title = title_tag.h3.a.text.strip()
                        product_url = title_tag.h3.a.get('href', '').strip()
                    
                    # 2. Ekstraksi Penulis
                    author_tag = product.find('div', class_='product-author')
                    author = ""
                    if author_tag:
                        author = author_tag.text.strip()
                    
                    # 3. Ekstraksi Format Buku (Paperback/Hardcover)
                    binding_tag = product.find('div', class_='product-binding')
                    binding = ""
                    if binding_tag:
                        binding = binding_tag.text.strip()
                    
                    # 4. Ekstraksi Harga & Diskon
                    price_container = product.find('div', class_='product-price')
                    raw_price = ""
                    original_price = ""
                    discount_pct = ""
                    
                    if price_container:
                        price_divs = price_container.find_all('div')
                        if len(price_divs) == 1:
                            # Harga normal (tidak diskon)
                            raw_price = price_divs[0].text.strip()
                        elif len(price_divs) > 1:
                            # Harga diskon
                            for div in price_divs:
                                style = div.get('style', '')
                                if 'line-through' in style:
                                    original_price = div.text.strip()
                                else:
                                    raw_price = div.text.strip()
                            
                            discount_span = price_container.find('span')
                            if discount_span:
                                discount_pct = discount_span.text.strip()
                    
                    # 5. Ekstraksi Status Ketersediaan Stok
                    unavailable_tag = product.find('div', class_='currently-unavailable')
                    in_stock = 0 if unavailable_tag else 1
                    
                    # Simpan data mentah
                    books_data.append({
                        "title": title,
                        "author": author,
                        "binding": binding,
                        "raw_price": raw_price,
                        "original_price": original_price,
                        "discount_pct": discount_pct,
                        "in_stock": in_stock,
                        "category": category_name,
                        "product_url": product_url
                    })
                
                # Delay sopan agar tidak membebani server target
                time.sleep(random.uniform(1.0, 2.5))
                
            except Exception as e:
                print(f"Error saat memproses halaman {page}: {e}")
                # Jangan break agar tidak menghentikan seluruh kategori jika satu halaman gagal diolah
                continue
                
    # Simpan ke CSV
    if books_data:
        import os
        os.makedirs("data", exist_ok=True)
        df = pd.DataFrame(books_data)
        output_file = "data/periplus_books_raw.csv"
        df.to_csv(output_file, index=False)
        print(f"\nScraping Selesai! Berhasil mengumpulkan {len(df)} data buku.")
        print(f"Data mentah berhasil disimpan di file: '{output_file}'")
    else:
        print("\nGagal mengumpulkan data buku.")

if __name__ == "__main__":
    scrape_periplus()
