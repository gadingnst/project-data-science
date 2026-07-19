"""
Script untuk membersihkan data dan melakukan feature engineering
Input: data/periplus_books_raw.csv
Output: data/periplus_books_clean.csv
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime

def extract_year_from_date(date_str):
    """
    Ekstrak tahun dari berbagai format tanggal
    Examples: "04 July 2023", "2023", "July 2023"
    """
    if pd.isna(date_str):
        return None
    
    # Try to find 4-digit year
    year_match = re.search(r'(19|20)\d{2}', str(date_str))
    if year_match:
        return int(year_match.group())
    
    return None

def clean_data():
    """
    Main cleaning function
    """
    print("=" * 80)
    print("🧹 Starting Data Cleaning Process")
    print("=" * 80)
    
    # Load raw data
    input_file = "data/periplus_books_raw.csv"
    print(f"\n📂 Loading: {input_file}")
    
    try:
        df = pd.read_csv(input_file)
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found!")
        print("Please run 'python scrapers/scrape_periplus.py' first.")
        return
    
    print(f"\n{'='*80}")
    print("📊 Initial Data Info:")
    print(f"{'='*80}")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"\nColumns: {', '.join(df.columns.tolist())}")
    
    # Check missing values
    print(f"\n{'='*80}")
    print("🔍 Missing Values Check:")
    print(f"{'='*80}")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    for col in df.columns:
        if missing[col] > 0:
            print(f"{col:25s}: {missing[col]:4d} ({missing_pct[col]:5.1f}%)")
    
    # === DATA CLEANING ===
    
    print(f"\n{'='*80}")
    print("🧹 Step 1: Handling Missing Values")
    print(f"{'='*80}")
    
    # 1. Fill missing author
    df['author'] = df['author'].fillna('Unknown Author')
    print("✅ Filled missing 'author' with 'Unknown Author'")
    
    # 2. Fill missing binding
    df['binding'] = df['binding'].fillna('Unknown')
    print("✅ Filled missing 'binding' with 'Unknown'")
    
    # 3. Fill missing language
    df['language'] = df['language'].fillna('Unknown')
    print("✅ Filled missing 'language' with 'Unknown'")
    
    # 4. Fill missing publisher
    df['publisher'] = df['publisher'].fillna('Unknown Publisher')
    print("✅ Filled missing 'publisher' with 'Unknown Publisher'")
    
    # 5. Fill missing review_count with 0
    df['review_count'] = df['review_count'].fillna(0).astype(int)
    print("✅ Filled missing 'review_count' with 0")
    
    # 6. Handle missing pages, weight - will be used in feature engineering
    print("ℹ️  Keeping missing 'pages' and 'weight' as NaN (will handle in feature engineering)")
    
    print(f"\n{'='*80}")
    print("🔧 Step 2: Data Type Conversion")
    print(f"{'='*80}")
    
    # Ensure numeric types
    df['price_idr'] = pd.to_numeric(df['price_idr'], errors='coerce')
    df['original_price_idr'] = pd.to_numeric(df['original_price_idr'], errors='coerce')
    df['discount_percent'] = pd.to_numeric(df['discount_percent'], errors='coerce')
    df['pages'] = pd.to_numeric(df['pages'], errors='coerce')
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
    df['in_stock'] = df['in_stock'].astype(int)
    
    print("✅ Converted numeric columns to proper types")
    
    # === FEATURE ENGINEERING ===
    
    print(f"\n{'='*80}")
    print("🛠️  Step 3: Feature Engineering")
    print(f"{'='*80}")
    
    # 1. Extract publication year
    print("\n📅 Feature 1: publication_year")
    df['publication_year'] = df['publication_date'].apply(extract_year_from_date)
    year_extracted = df['publication_year'].notna().sum()
    print(f"   ✅ Extracted year for {year_extracted}/{len(df)} rows ({year_extracted/len(df)*100:.1f}%)")
    
    # 2. Calculate book age
    print("\n📆 Feature 2: book_age")
    current_year = datetime.now().year
    df['book_age'] = current_year - df['publication_year']
    df['book_age'] = df['book_age'].fillna(-1)  # -1 for unknown age
    df.loc[df['book_age'] < 0, 'book_age'] = -1
    age_calculated = (df['book_age'] > 0).sum()
    print(f"   ✅ Calculated age for {age_calculated}/{len(df)} rows ({age_calculated/len(df)*100:.1f}%)")
    print(f"   ℹ️  Book age range: {df[df['book_age'] > 0]['book_age'].min():.0f} - {df[df['book_age'] > 0]['book_age'].max():.0f} years")
    
    # 3. Price per page
    print("\n💰 Feature 3: price_per_page")
    df['price_per_page'] = df['price_idr'] / df['pages']
    df['price_per_page'] = df['price_per_page'].replace([np.inf, -np.inf], np.nan)
    ppp_calculated = df['price_per_page'].notna().sum()
    print(f"   ✅ Calculated for {ppp_calculated}/{len(df)} rows ({ppp_calculated/len(df)*100:.1f}%)")
    if ppp_calculated > 0:
        print(f"   ℹ️  Price per page range: Rp {df['price_per_page'].min():.0f} - Rp {df['price_per_page'].max():.0f}")
    
    # 4. Popularity score
    print("\n⭐ Feature 4: popularity_score")
    # Formula: review_count × (1 + discount_bonus)
    # Books with more reviews and discounts are more popular
    df['popularity_score'] = df['review_count'] * (1 + df['discount_percent'] / 100)
    print(f"   ✅ Calculated popularity score for all rows")
    print(f"   ℹ️  Popularity score range: {df['popularity_score'].min():.2f} - {df['popularity_score'].max():.2f}")
    
    # 5. Is new release flag
    print("\n🆕 Feature 5: is_new_release")
    df['is_new_release'] = (df['publication_year'] >= 2024).astype(int)
    df.loc[df['publication_year'].isna(), 'is_new_release'] = 0
    new_releases = df['is_new_release'].sum()
    print(f"   ✅ Flagged {new_releases}/{len(df)} books as new releases ({new_releases/len(df)*100:.1f}%)")
    
    # 6. Price category
    print("\n🏷️  Feature 6: price_category")
    df['price_category'] = pd.cut(
        df['price_idr'],
        bins=[0, 150000, 250000, 400000, float('inf')],
        labels=['Budget', 'Mid-range', 'Premium', 'Luxury']
    )
    print(f"   ✅ Categorized books into price ranges:")
    print(df['price_category'].value_counts().to_string())
    
    # 7. Has discount flag
    print("\n🎁 Feature 7: has_discount")
    df['has_discount'] = (df['discount_percent'] > 0).astype(int)
    discounted = df['has_discount'].sum()
    print(f"   ✅ {discounted}/{len(df)} books have discount ({discounted/len(df)*100:.1f}%)")
    
    # === DATA QUALITY CHECKS ===
    
    print(f"\n{'='*80}")
    print("🔍 Step 4: Data Quality Checks")
    print(f"{'='*80}")
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['title', 'author', 'isbn'], keep='first').sum()
    if duplicates > 0:
        print(f"⚠️  Found {duplicates} duplicate books (by title, author, ISBN)")
        df = df.drop_duplicates(subset=['title', 'author', 'isbn'], keep='first')
        print(f"✅ Removed duplicates. New row count: {len(df)}")
    else:
        print("✅ No duplicates found")
    
    # Check for invalid prices
    invalid_prices = (df['price_idr'] <= 0).sum()
    if invalid_prices > 0:
        print(f"⚠️  Found {invalid_prices} rows with invalid prices (≤0)")
        df = df[df['price_idr'] > 0]
        print(f"✅ Removed invalid rows. New row count: {len(df)}")
    else:
        print("✅ All prices are valid")
    
    # === SAVE CLEANED DATA ===
    
    print(f"\n{'='*80}")
    print("💾 Step 5: Saving Cleaned Data")
    print(f"{'='*80}")
    
    output_file = "data/periplus_books_clean.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ SUCCESS!")
    print(f"📁 File saved: {output_file}")
    print(f"📊 Final dataset: {len(df)} rows × {len(df.columns)} columns")
    
    # Final summary
    print(f"\n{'='*80}")
    print("📈 Final Dataset Summary:")
    print(f"{'='*80}")
    print(f"Total books: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"\nNew features added:")
    print("  1. publication_year")
    print("  2. book_age")
    print("  3. price_per_page")
    print("  4. popularity_score")
    print("  5. is_new_release")
    print("  6. price_category")
    print("  7. has_discount")
    
    print(f"\nData Quality:")
    print(f"  ✅ In stock: {df['in_stock'].sum()} ({df['in_stock'].sum()/len(df)*100:.1f}%)")
    print(f"  ✅ With discount: {df['has_discount'].sum()} ({df['has_discount'].sum()/len(df)*100:.1f}%)")
    print(f"  ✅ New releases: {df['is_new_release'].sum()} ({df['is_new_release'].sum()/len(df)*100:.1f}%)")
    print(f"  ✅ With ISBN: {df['isbn'].notna().sum()} ({df['isbn'].notna().sum()/len(df)*100:.1f}%)")
    print(f"  ✅ With pages: {df['pages'].notna().sum()} ({df['pages'].notna().sum()/len(df)*100:.1f}%)")
    print(f"  ✅ With reviews: {(df['review_count'] > 0).sum()} ({(df['review_count'] > 0).sum()/len(df)*100:.1f}%)")
    
    print(f"\n{'='*80}")
    print("🎉 Data Cleaning Completed!")
    print(f"{'='*80}")
    
    # Save summary statistics
    summary_file = "data/data_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("DATA SUMMARY - Periplus Books Dataset\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Records: {len(df)}\n")
        f.write(f"Total Columns: {len(df.columns)}\n\n")
        f.write("="*80 + "\n")
        f.write("DESCRIPTIVE STATISTICS\n")
        f.write("="*80 + "\n\n")
        f.write(df.describe(include='all').to_string())
        f.write("\n\n")
        f.write("="*80 + "\n")
        f.write("MISSING VALUES\n")
        f.write("="*80 + "\n\n")
        missing_summary = pd.DataFrame({
            'Missing Count': df.isnull().sum(),
            'Missing Percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        f.write(missing_summary.to_string())
    
    print(f"\n📄 Summary statistics saved to: {summary_file}")

if __name__ == "__main__":
    clean_data()
