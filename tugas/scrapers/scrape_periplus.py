"""
Scraper untuk mengambil data buku dari Periplus.com
Target: 1500+ rows dengan field lengkap untuk analisis data science

Field yang di-scrape:
- Basic  : title, author, binding, in_stock, category, product_url,
           price_idr, original_price_idr, discount_percent
- Extended: isbn, publisher, publication_date, pages, language, weight, review_count
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
from datetime import datetime

# ---------------------------------------------------------------------------
# Kategori target (8 kategori × ~8 halaman × ~24 produk ≈ 1500 rows)
# ---------------------------------------------------------------------------
CATEGORIES = {
    "Fiction & Literature":   "https://www.periplus.com/c/1_32/fiction-and-amp-literature",
    "Business & Self-Help":   "https://www.periplus.com/c/1_13/business-and-self-help",
    "Children's Books":       "https://www.periplus.com/c/1_14/children-s-books",
    "Computer & IT":          "https://www.periplus.com/c/1_15/computer-and-amp-it",
    "Biographies & Memoirs":  "https://www.periplus.com/c/1_12/biographies-and-amp-memoirs",
    "Arts & Photography":     "https://www.periplus.com/c/1_11/arts-and-amp-photography",
    "Cooking & Food":         "https://www.periplus.com/c/1_17/cooking-and-amp-food",
    "Health & Fitness":       "https://www.periplus.com/c/1_22/health-and-amp-fitness",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
    "Referer":         "https://www.periplus.com/",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_price(text: str) -> float | None:
    """Ekstrak angka dari string harga Periplus (contoh: 'Rp 258,000' → 258000.0)"""
    if not text:
        return None
    cleaned = re.sub(r"[^\d]", "", text)
    return float(cleaned) if cleaned else None


def extract_review_count(soup: BeautifulSoup) -> int:
    """
    Cari jumlah review dari halaman detail.
    Format di website: '4 customer reviews | Write a review'
    """
    # Cari teks yang mengandung 'customer review'
    for tag in soup.find_all(string=re.compile(r"\d+\s+customer\s+review", re.I)):
        m = re.search(r"(\d+)\s+customer\s+review", tag, re.I)
        if m:
            return int(m.group(1))
    return 0


def extract_detail_fields(soup: BeautifulSoup) -> dict:
    """
    Parse field detail dari halaman produk.
    Struktur aktual website:
      <label>ISBN-13</label><span>9781786583239</span>  (atau variasi lain)
    Kadang juga muncul sebagai pasangan teks di dalam div .description-right, dll.
    Kita pakai pendekatan robust: cari semua <li> dan <div> yang punya label keyword.
    """
    detail = {
        "isbn":             None,
        "publisher":        None,
        "publication_date": None,
        "pages":            None,
        "language":         None,
        "weight":           None,
        "review_count":     0,
    }

    detail["review_count"] = extract_review_count(soup)

    # --- Strategi 1: cari pasangan <label>/<span> atau <b>/<span> ---
    # Website Periplus menyimpan info di blok seperti:
    #   ISBN-13\n9781786583239\nPublisher\nBonnier Books Ltd\n...
    # Kita cari semua text node di area product detail lalu parse secara sekuensial.

    # Cari container detail (biasanya ada di div dengan class tertentu, atau table)
    # Berdasarkan fetch HTML: info muncul langsung sebagai text biasa berurutan
    # → kita ambil semua teks dari seluruh halaman lalu regex
    full_text = soup.get_text(separator="\n")

    def extract_after_label(label_pattern: str, text: str) -> str | None:
        m = re.search(
            rf"{label_pattern}\s*\n\s*(.+?)(?:\n|$)",
            text,
            re.IGNORECASE
        )
        return m.group(1).strip() if m else None

    raw_isbn   = extract_after_label(r"ISBN-13",          full_text)
    raw_pub    = extract_after_label(r"Publisher",        full_text)
    raw_date   = extract_after_label(r"Publication\s+Date", full_text)
    raw_pages  = extract_after_label(r"Pages",            full_text)
    raw_lang   = extract_after_label(r"Language",         full_text)
    raw_weight = extract_after_label(r"Shipping\s+Weight", full_text)

    if raw_isbn:
        detail["isbn"] = re.sub(r"[^\d]", "", raw_isbn) or None

    if raw_pub:
        detail["publisher"] = raw_pub

    if raw_date:
        detail["publication_date"] = raw_date

    if raw_pages:
        m = re.search(r"(\d+)", raw_pages)
        detail["pages"] = int(m.group(1)) if m else None

    if raw_lang:
        detail["language"] = raw_lang

    if raw_weight:
        m = re.search(r"([\d.]+)", raw_weight)
        detail["weight"] = float(m.group(1)) if m else None

    return detail


# ---------------------------------------------------------------------------
# Scrape satu halaman kategori → list of product dicts (basic fields only)
# ---------------------------------------------------------------------------

def scrape_category_page(url: str, category_name: str, page_num: int) -> list[dict]:
    """
    Parse halaman listing kategori.
    Struktur aktual Periplus list page:
      - Setiap produk ada di dalam <div class="col-..."> yang berisi <h3><a>
      - Author ada di <div> atau <span> setelah h3
      - Harga: format '-31% Rp 358,000 Rp 248,000' atau 'Rp 258,000'
      - "Fast Delivery" badge → in_stock = 1
    """
    products = []

    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            print(f"    ❌ HTTP {resp.status_code} for {url}")
            return products

        soup = BeautifulSoup(resp.text, "html.parser")

        # Setiap produk di list page ada di dalam container yang memiliki <h3> berisi link
        # Coba beberapa kemungkinan selector container
        items = soup.select("div.single-product")
        if not items:
            # Fallback: cari semua h3 > a yang linknya ke /p/
            items = [a.find_parent() for a in soup.select("h3 > a[href*='/p/']") if a.find_parent()]

        if not items:
            print(f"    ℹ️  Tidak ada produk ditemukan di page {page_num}")
            return products

        print(f"    📦 Ditemukan {len(items)} produk di page {page_num}")

        for item in items:
            try:
                # --- Title & URL ---
                # Image link: <a href='/p/...'><img></a>  -> text kosong, skip
                # Title link: <a href='/p/...'>Judul Buku</a> -> ambil ini
                all_links = item.find_all('a', href=re.compile(r'/p/\d+/'))
                a_tag = None
                for lnk in all_links:
                    if lnk.get_text(strip=True):
                        a_tag = lnk
                        break

                if not a_tag:
                    continue

                title = a_tag.get_text(strip=True)
                product_url = a_tag["href"].strip()
                if not product_url.startswith("http"):
                    product_url = "https://www.periplus.com" + product_url

                if not title:
                    continue

                # --- Full text dari item untuk parse lainnya ---
                item_text = item.get_text(separator=" | ", strip=True)

                # --- Author ---
                # item_text format: "Fast Delivery | Title | Author | Binding | Rp ..."
                # Author ada di antara title dan binding keyword
                author = "Unknown Author"
                binding_kws = "Paperback|Hardcover|Board Book|Spiral|Loose Leaf|Hardback"
                title_esc = re.escape(title)
                author_m = re.search(
                    title_esc + r"\s*\|?\s*(.+?)\s*\|?\s*(?:" + binding_kws + ")",
                    item_text, re.IGNORECASE
                )
                if author_m:
                    candidate = author_m.group(1).strip().strip('|').strip()
                    if candidate and "Rp" not in candidate and len(candidate) < 80:
                        author = candidate

                # --- Binding ---
                binding = "Unknown"
                for kw in ("Paperback", "Hardcover", "Board Book", "Spiral", "Loose Leaf"):
                    if kw.lower() in item_text.lower():
                        binding = kw
                        break

                # --- In Stock ---
                in_stock = 1 if "fast delivery" in item_text.lower() or "in stock" in item_text.lower() else 0

                # --- Prices ---
                # Format dengan diskon : "-31% Rp 358,000 Rp 248,000"
                # Format tanpa diskon  : "Rp 258,000"
                price_idr          = None
                original_price_idr = None
                discount_percent   = 0.0

                # Cari semua angka harga (setelah "Rp")
                prices_found = re.findall(r"Rp\s*([\d.,]+)", item_text)
                discount_m   = re.search(r"-(\d+)%", item_text)

                if discount_m:
                    discount_percent = float(discount_m.group(1))

                if len(prices_found) >= 2:
                    p1 = clean_price(prices_found[0])
                    p2 = clean_price(prices_found[1])
                    if p1 and p2:
                        original_price_idr = max(p1, p2)
                        price_idr          = min(p1, p2)
                elif len(prices_found) == 1:
                    p1 = clean_price(prices_found[0])
                    price_idr          = p1
                    original_price_idr = p1

                products.append({
                    "title":              title,
                    "author":             author,
                    "binding":            binding,
                    "in_stock":           in_stock,
                    "category":           category_name,
                    "product_url":        product_url,
                    "price_idr":          price_idr,
                    "original_price_idr": original_price_idr,
                    "discount_percent":   discount_percent,
                })

            except Exception as e:
                print(f"    ⚠️  Error parse item: {e}")
                continue

    except Exception as e:
        print(f"    ❌ Error scraping page: {e}")

    return products


# ---------------------------------------------------------------------------
# Scrape detail page → extended fields
# ---------------------------------------------------------------------------

def scrape_product_detail(url: str) -> dict:
    detail = {
        "isbn":             None,
        "publisher":        None,
        "publication_date": None,
        "pages":            None,
        "language":         None,
        "weight":           None,
        "review_count":     0,
    }
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            print(f"      ⚠️  Detail HTTP {resp.status_code}: {url}")
            return detail
        soup = BeautifulSoup(resp.text, "html.parser")
        detail = extract_detail_fields(soup)
    except Exception as e:
        print(f"      ⚠️  Detail error: {e}")
    return detail


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def scrape_periplus():
    all_books = []

    print("=" * 80)
    print("🚀 Periplus.com Scraper — Enhanced v2")
    print("=" * 80)
    print(f"📊 Target   : 1500+ rows")
    print(f"📁 Kategori : {len(CATEGORIES)}")
    print(f"📄 Max pages: 8 per kategori")
    print("=" * 80)

    for cat_name, base_url in CATEGORIES.items():
        print(f"\n{'='*80}")
        print(f"📚 Kategori: {cat_name}")
        print(f"{'='*80}")

        for page in range(1, 9):
            page_url = f"{base_url}?page={page}"
            print(f"\n  🔍 Page {page}/8  →  {page_url}")

            # --- Retry scrape category page ---
            products = []
            for attempt in range(1, 4):
                try:
                    products = scrape_category_page(page_url, cat_name, page)
                    if products:
                        break
                except Exception as e:
                    print(f"  ⚠️  Attempt {attempt}/3 failed: {e}")
                    time.sleep(attempt * 5)

            if not products:
                print(f"  ❌ Skip page {page} (tidak ada produk)")
                continue

            # --- Scrape detail page untuk setiap produk ---
            for idx, prod in enumerate(products, 1):
                url = prod["product_url"]
                print(f"    📖 [{idx}/{len(products)}] {prod['title'][:55]}...")
                detail = scrape_product_detail(url)
                prod.update(detail)
                time.sleep(random.uniform(0.4, 1.2))

            all_books.extend(products)
            total = len(all_books)
            print(f"  ✅ +{len(products)} produk  |  Total: {total}")

            time.sleep(random.uniform(2.0, 3.5))

        cat_count = sum(1 for b in all_books if b["category"] == cat_name)
        print(f"\n✅ '{cat_name}' selesai → {cat_count} buku")

    # --- Save ---
    print("\n" + "=" * 80)
    print("💾 Menyimpan data...")
    print("=" * 80)

    if not all_books:
        print("❌ Tidak ada data yang berhasil di-scrape!")
        return

    df = pd.DataFrame(all_books)
    output_file = "data/periplus_books_raw.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")

    # --- Summary ---
    print(f"\n✅ SUKSES!")
    print(f"📁 File   : {output_file}")
    print(f"📊 Rows   : {len(df)}")
    print(f"📋 Kolom  : {len(df.columns)}  →  {', '.join(df.columns)}")
    print(f"\n{'='*80}")
    print("📈 Summary Statistics:")
    print(f"{'='*80}")
    print(f"Total rows         : {len(df)}")
    print(f"Kategori           : {df['category'].nunique()}")
    print(f"Judul unik         : {df['title'].nunique()}")
    print(f"In stock           : {df['in_stock'].sum()} ({df['in_stock'].mean()*100:.1f}%)")
    print(f"Ada diskon         : {(df['discount_percent'] > 0).sum()} ({(df['discount_percent'] > 0).mean()*100:.1f}%)")
    print(f"Ada ISBN           : {df['isbn'].notna().sum()} ({df['isbn'].notna().mean()*100:.1f}%)")
    print(f"Ada pages          : {df['pages'].notna().sum()} ({df['pages'].notna().mean()*100:.1f}%)")
    print(f"Ada review_count>0 : {(df['review_count'] > 0).sum()} ({(df['review_count'] > 0).mean()*100:.1f}%)")
    print(f"Ada publisher      : {df['publisher'].notna().sum()} ({df['publisher'].notna().mean()*100:.1f}%)")
    print(f"\n{'='*80}")
    print("🎉 Scraping selesai!")
    print("=" * 80)


if __name__ == "__main__":
    scrape_periplus()
