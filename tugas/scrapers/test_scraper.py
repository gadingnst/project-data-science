"""
Test script untuk memvalidasi scraper sebelum full run.
Scrape 3 produk saja: 1 dari category page + detail page-nya.

Run: python scrapers/test_scraper.py
"""

import requests
from bs4 import BeautifulSoup
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
    "Referer": "https://www.periplus.com/"
}

TEST_CATEGORY_URL = "https://www.periplus.com/c/1_32/fiction-and-amp-literature?page=1"
MAX_TEST_PRODUCTS = 3


def extract_number(text):
    if not text:
        return None
    cleaned = text.replace(',', '').replace('.', '')
    match = re.search(r'\d+', cleaned)
    return float(match.group()) if match else None


def test_category_page():
    print("=" * 70)
    print("🔍 TEST 1: Category Page Parsing")
    print("=" * 70)
    print(f"URL: {TEST_CATEGORY_URL}\n")

    response = requests.get(TEST_CATEGORY_URL, headers=HEADERS, timeout=20)
    print(f"HTTP Status: {response.status_code}")
    assert response.status_code == 200, "❌ Failed to fetch category page!"

    soup = BeautifulSoup(response.text, 'html.parser')

    # --- Find product links ---
    product_links = soup.find_all('a', href=re.compile(r'/p/\d+/'))
    # Deduplicate
    seen = set()
    unique_links = []
    for a in product_links:
        href = a.get('href', '').strip()
        if href not in seen:
            seen.add(href)
            unique_links.append(a)

    print(f"✅ Product links found: {len(unique_links)}")
    assert len(unique_links) > 0, "❌ No product links found! Selector mungkin salah."

    # Kumpulkan unique containers (div.single-product)
    containers = soup.find_all('div', class_='single-product')
    if not containers:
        # fallback: parent dari title link
        containers = []
        for a in unique_links:
            p = a.find_parent('div')
            if p and p not in containers:
                containers.append(p)

    products_raw = []
    for item in containers[:MAX_TEST_PRODUCTS]:
        # --- Title & URL ---
        all_links = item.find_all('a', href=re.compile(r'/p/\d+/'))
        a_tag = None
        for lnk in all_links:
            if lnk.get_text(strip=True):
                a_tag = lnk
                break
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        href = a_tag['href'].strip()
        if not href.startswith('http'):
            href = 'https://www.periplus.com' + href

        item_text = item.get_text(separator=' | ', strip=True)

        # --- Author ---
        binding_kws = 'Paperback|Hardcover|Board Book|Spiral|Loose Leaf|Hardback'
        title_esc = re.escape(title)
        author = 'Unknown'
        author_m = re.search(
            title_esc + r'\s*\|?\s*(.+?)\s*\|?\s*(?:' + binding_kws + ')',
            item_text, re.IGNORECASE
        )
        if author_m:
            candidate = author_m.group(1).strip().strip('|').strip()
            if candidate and 'Rp' not in candidate and len(candidate) < 80:
                author = candidate

        # --- Binding ---
        binding_match = re.search(r'(Paperback|Hardcover|Hardback|Spiral|Board Book)', item_text, re.IGNORECASE)
        binding = binding_match.group(1) if binding_match else 'Unknown'

        # --- In Stock ---
        in_stock = 1 if re.search(r'fast delivery|in stock', item_text, re.IGNORECASE) else 0

        # --- Prices ---
        prices = re.findall(r'Rp\s*([\d.,]+)', item_text)
        prices_clean = [extract_number(p) for p in prices if extract_number(p)]
        original_price = max(prices_clean) if prices_clean else None
        current_price = min(prices_clean) if prices_clean else None
        discount_match = re.search(r'-(\d+)%', item_text)
        discount_percent = float(discount_match.group(1)) if discount_match else 0.0
        if not discount_percent:
            current_price = original_price

        products_raw.append({
            'title': title,
            'author': author,
            'binding': binding,
            'in_stock': in_stock,
            'product_url': href,
            'price_idr': current_price,
            'original_price_idr': original_price,
            'discount_percent': discount_percent
        })

    print(f"\n📦 Sample products from category page ({MAX_TEST_PRODUCTS}):")
    for i, p in enumerate(products_raw, 1):
        print(f"\n  [{i}] {p['title'][:60]}")
        print(f"      Author   : {p['author']}")
        print(f"      Binding  : {p['binding']}")
        print(f"      In Stock : {p['in_stock']}")
        print(f"      Price    : Rp {p['price_idr']:,.0f}" if p['price_idr'] else "      Price    : N/A")
        print(f"      Ori Price: Rp {p['original_price_idr']:,.0f}" if p['original_price_idr'] else "      Ori Price: N/A")
        print(f"      Discount : {p['discount_percent']}%")
        print(f"      URL      : {p['product_url'][:70]}")

    return products_raw


def test_detail_page(product_url):
    print("\n" + "=" * 70)
    print("🔍 TEST 2: Detail Page Parsing")
    print("=" * 70)
    print(f"URL: {product_url}\n")

    response = requests.get(product_url, headers=HEADERS, timeout=20)
    print(f"HTTP Status: {response.status_code}")
    assert response.status_code == 200, "❌ Failed to fetch detail page!"

    soup = BeautifulSoup(response.text, 'html.parser')
    full_text = soup.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in full_text.splitlines() if l.strip()]

    detail = {
        'isbn': None,
        'publisher': None,
        'publication_date': None,
        'pages': None,
        'language': None,
        'weight': None,
        'review_count': 0
    }

    # Parse label → next line = value
    label_map = {
        'isbn-13': 'isbn',
        'isbn': 'isbn',
        'publisher': 'publisher',
        'publication date': 'publication_date',
        'pages': 'pages',
        'language': 'language',
        'shipping weight': 'weight',
        'weight': 'weight',
    }

    for i, line in enumerate(lines):
        lower = line.lower().strip(':').strip()
        if lower in label_map and i + 1 < len(lines):
            field = label_map[lower]
            value = lines[i + 1].strip()
            if field == 'pages':
                num = extract_number(value)
                detail[field] = int(num) if num else None
            elif field == 'weight':
                num = extract_number(value)
                detail[field] = num
            else:
                detail[field] = value

    # Review count
    review_match = re.search(r'(\d+)\s*customer\s*review', full_text, re.IGNORECASE)
    detail['review_count'] = int(review_match.group(1)) if review_match else 0

    print("📋 Detail fields parsed:")
    for k, v in detail.items():
        status = "✅" if v is not None and v != 0 else "⚠️ "
        print(f"  {status} {k:20s}: {v}")

    return detail


def test_raw_html_snippet():
    """Dump raw text sekitar produk pertama untuk debugging manual"""
    print("\n" + "=" * 70)
    print("🔍 TEST 3: Raw HTML Structure (First Product Container)")
    print("=" * 70)

    response = requests.get(TEST_CATEGORY_URL, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari link produk pertama
    first_link = soup.find('a', href=re.compile(r'/p/\d+/'))
    if not first_link:
        print("❌ Tidak ada link produk ditemukan!")
        return

    print(f"\nFirst product link: {first_link.get('href')}")
    print(f"Link text: {first_link.get_text(strip=True)[:80]}")

    # Dump parent containers (3 levels up)
    parent = first_link.parent
    for level in range(1, 4):
        if parent:
            text = parent.get_text(separator=" | ", strip=True)[:300]
            print(f"\n  Parent level {level} ({parent.name}.{' '.join(parent.get('class', []))}):")
            print(f"  {text}")
            parent = parent.parent


def run_all_tests():
    print("\n" + "=" * 70)
    print("🧪 PERIPLUS SCRAPER - TEST SUITE")
    print("=" * 70)

    try:
        # Test 1: Category page
        products = test_category_page()

        # Test 2: Detail page (pake produk pertama)
        if products:
            first_url = products[0]['product_url']
            detail = test_detail_page(first_url)

            print("\n" + "=" * 70)
            print("✅ COMBINED RESULT (product[0] + detail):")
            print("=" * 70)
            combined = {**products[0], **detail}
            for k, v in combined.items():
                print(f"  {k:25s}: {v}")

        # Test 3: Raw HTML dump
        test_raw_html_snippet()

        print("\n" + "=" * 70)
        print("🎉 All tests completed!")
        print("=" * 70)

        # Final verdict
        print("\n📊 VERDICT:")
        has_title = bool(products and products[0].get('title'))
        has_price = bool(products and products[0].get('price_idr'))
        has_detail = bool(detail.get('isbn') or detail.get('pages') or detail.get('publisher'))
        has_review = bool(detail.get('review_count') is not None)

        print(f"  {'✅' if has_title  else '❌'} Title parsing     : {'OK' if has_title  else 'FAILED'}")
        print(f"  {'✅' if has_price  else '❌'} Price parsing     : {'OK' if has_price  else 'FAILED'}")
        print(f"  {'✅' if has_detail else '❌'} Detail fields     : {'OK' if has_detail else 'FAILED - cek HTML structure'}")
        print(f"  {'✅' if has_review else '❌'} Review count      : {'OK' if has_review else 'FAILED'}")

        if has_title and has_price and has_detail:
            print("\n  🟢 SCRAPER READY - Aman untuk full run!")
        else:
            print("\n  🔴 ADA MASALAH - Cek output di atas sebelum full run!")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
