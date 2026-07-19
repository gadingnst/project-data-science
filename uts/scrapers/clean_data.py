import pandas as pd
import re

def clean_price(price_str):
    if pd.isna(price_str) or not isinstance(price_str, str):
        return None
    # Hapus "Rp", spasi, titik ribuan, dan karakter non-angka lainnya
    cleaned = re.sub(r'[^\d]', '', price_str)
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None

def clean_discount(discount_str):
    if pd.isna(discount_str) or not isinstance(discount_str, str):
        return 0.0
    # Ambil angka saja (misal "-5%" -> 5.0)
    cleaned = re.sub(r'[^\d.]', '', discount_str)
    try:
        return float(cleaned) if cleaned else 0.0
    except ValueError:
        return 0.0

def process_cleaning():
    import os
    os.makedirs("data", exist_ok=True)
    input_file = "data/periplus_books_raw.csv"
    output_file = "data/periplus_books_clean.csv"
    
    print(f"=== Memulai Pembersihan Data: '{input_file}' ===")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' tidak ditemukan. Silakan jalankan 'scrape_periplus.py' terlebih dahulu.")
        return
        
    print(f"Data awal terisi: {len(df)} baris.")
    
    # 1. Bersihkan Kolom Harga
    df['price_idr'] = df['raw_price'].apply(clean_price)
    df['original_price_idr'] = df['original_price'].apply(clean_price)
    
    # Jika original_price_idr kosong (karena tidak diskon), isi dengan price_idr
    df['original_price_idr'] = df['original_price_idr'].fillna(df['price_idr'])
    
    # 2. Bersihkan Kolom Diskon
    df['discount_percent'] = df['discount_pct'].apply(clean_discount)
    
    # 3. Handling Missing Values pada kolom kritis
    # Hapus baris yang tidak memiliki harga jual
    df = df.dropna(subset=['price_idr'])
    
    # Isi author kosong dengan "Unknown Author"
    df['author'] = df['author'].fillna("Unknown Author")
    
    # Isi binding kosong dengan "Unknown Binding"
    df['binding'] = df['binding'].fillna("Unknown Binding")
    
    # 4. Drop kolom mentah yang sudah tidak diperlukan
    df_clean = df.drop(columns=['raw_price', 'original_price', 'discount_pct'])
    
    # Simpan hasil pembersihan
    df_clean.to_csv(output_file, index=False)
    print(f"Pembersihan selesai! Data bersih disimpan di: '{output_file}'")
    print(f"Jumlah baris setelah dibersihkan: {len(df_clean)} baris.")
    print("\nContoh data bersih:")
    print(df_clean[['title', 'author', 'price_idr', 'discount_percent', 'category']].head())

if __name__ == "__main__":
    process_cleaning()
