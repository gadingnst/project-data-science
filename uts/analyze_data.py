import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style visualisasi
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def load_data():
    file_path = "data/periplus_books_clean.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset bersih '{file_path}' tidak ditemukan. Jalankan scraper dan cleaner terlebih dahulu.")
    return pd.read_csv(file_path)

def calculate_statistics(df):
    print("=== KALKULASI STATISTIKA DESKRIPTIF (HARGA JUAL - price_idr) ===")
    
    prices = df['price_idr']
    
    # 1. Ukuran Pemusatan Data
    mean_val = prices.mean()
    median_val = prices.median()
    mode_val = prices.mode()[0] if not prices.mode().empty else None
    
    # 2. Ukuran Penyebaran Data
    std_val = prices.std()
    var_val = prices.var()
    min_val = prices.min()
    max_val = prices.max()
    range_val = max_val - min_val
    
    # Kuartil & IQR
    q1 = prices.quantile(0.25)
    q3 = prices.quantile(0.75)
    iqr = q3 - q1
    
    # 3. Deteksi Outlier (Pencilan)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(prices < lower_bound) | (prices > upper_bound)]
    
    # Tampilkan hasil ke terminal
    print(f"Mean (Rata-rata)     : Rp {mean_val:,.2f}")
    print(f"Median (Nilai Tengah): Rp {median_val:,.2f}")
    print(f"Mode (Modus)         : Rp {mode_val:,.2f}")
    print(f"Standar Deviasi      : Rp {std_val:,.2f}")
    print(f"Varians              : {var_val:,.2f} (Rp²)")
    print(f"Rentang (Min - Max)  : Rp {min_val:,.2f} - Rp {max_val:,.2f} (Range: Rp {range_val:,.2f})")
    print(f"Kuartil 1 (Q1)       : Rp {q1:,.2f}")
    print(f"Kuartil 3 (Q3)       : Rp {q3:,.2f}")
    print(f"IQR                  : Rp {iqr:,.2f}")
    print(f"Batas Bawah Outlier  : Rp {lower_bound:,.2f}")
    print(f"Batas Atas Outlier   : Rp {upper_bound:,.2f}")
    print(f"Jumlah Outliers      : {len(outliers)} produk")
    
    # Tulis ringkasan ke file teks
    os.makedirs("data", exist_ok=True)
    with open("data/descriptive_statistics.txt", "w") as f:
        f.write("=== RINGKASAN STATISTIKA DESKRIPTIF HARGA ===\n")
        f.write(f"Mean (Rata-rata)     : Rp {mean_val:,.2f}\n")
        f.write(f"Median (Nilai Tengah): Rp {median_val:,.2f}\n")
        f.write(f"Mode (Modus)         : Rp {mode_val:,.2f}\n")
        f.write(f"Standar Deviasi      : Rp {std_val:,.2f}\n")
        f.write(f"Varians              : {var_val:,.2f} (Rp²)\n")
        f.write(f"Rentang (Min - Max)  : Rp {min_val:,.2f} - Rp {max_val:,.2f} (Range: Rp {range_val:,.2f})\n")
        f.write(f"Kuartil 1 (Q1)       : Rp {q1:,.2f}\n")
        f.write(f"Kuartil 3 (Q3)       : Rp {q3:,.2f}\n")
        f.write(f"IQR                  : Rp {iqr:,.2f}\n")
        f.write(f"Batas Bawah Outlier  : Rp {lower_bound:,.2f}\n")
        f.write(f"Batas Atas Outlier   : Rp {upper_bound:,.2f}\n")
        f.write(f"Jumlah Outliers      : {len(outliers)} produk\n\n")
        
        f.write("=== STATISTIKA PER KATEGORI ===\n")
        category_stats = df.groupby('category')['price_idr'].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
        f.write(category_stats.to_string())
        
    print("\n[INFO] Ringkasan statistik berhasil disimpan di 'data/descriptive_statistics.txt'")

def generate_plots(df):
    print("\n=== MEMBUAT VISUALISASI DATA ===")
    os.makedirs("plots", exist_ok=True)
    
    # 1. Histogram Distribusi Harga
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price_idr'], kde=True, color='skyblue', bins=30)
    plt.title('Distribusi Harga Buku Impor di Periplus.com', fontsize=14, fontweight='bold')
    plt.xlabel('Harga (Rupiah)', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x:,.0f}'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/price_distribution.png', dpi=300)
    plt.close()
    print("- Saved: plots/price_distribution.png")
    
    # 2. Boxplot Harga Buku (Deteksi Outlier)
    plt.figure(figsize=(10, 4))
    sns.boxplot(x=df['price_idr'], color='lightcoral')
    plt.title('Boxplot Harga Buku Impor (Deteksi Outlier)', fontsize=14, fontweight='bold')
    plt.xlabel('Harga (Rupiah)', fontsize=12)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x:,.0f}'))
    plt.tight_layout()
    plt.savefig('plots/price_boxplot.png', dpi=300)
    plt.close()
    print("- Saved: plots/price_boxplot.png")
    
    # 3. Bar Chart Jumlah Buku per Kategori
    plt.figure(figsize=(10, 6))
    category_counts = df['category'].value_counts()
    sns.barplot(x=category_counts.values, y=category_counts.index, palette='viridis')
    plt.title('Jumlah Buku per Kategori dalam Dataset', fontsize=14, fontweight='bold')
    plt.xlabel('Jumlah Buku', fontsize=12)
    plt.ylabel('Kategori', fontsize=12)
    plt.tight_layout()
    plt.savefig('plots/category_distribution.png', dpi=300)
    plt.close()
    print("- Saved: plots/category_distribution.png")
    
    # 4. Boxplot Harga Buku per Kategori
    plt.figure(figsize=(12, 7))
    sns.boxplot(x='price_idr', y='category', data=df, palette='Set2')
    plt.title('Perbandingan Sebaran Harga Buku per Kategori', fontsize=14, fontweight='bold')
    plt.xlabel('Harga (Rupiah)', fontsize=12)
    plt.ylabel('Kategori', fontsize=12)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x:,.0f}'))
    plt.tight_layout()
    plt.savefig('plots/category_price_boxplot.png', dpi=300)
    plt.close()
    print("- Saved: plots/category_price_boxplot.png")
    
    print("[INFO] Semua visualisasi berhasil disimpan di folder 'plots/'")

if __name__ == "__main__":
    try:
        df = load_data()
        calculate_statistics(df)
        generate_plots(df)
    except Exception as e:
        print(f"Error: {e}")
