import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time


def fetching_content(url, session=None):
    """
    Fungsi untuk mengambil konten HTML mentah dari URL tertentu.
    Dibungkus terpisah agar mudah dilakukan Mock Testing.
    """
    if session is None:
        session = requests.Session()

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None

def scrape_main(base_url, start_page=1, end_page=50, save_raw_csv=False):
    """
    Fungsi utama untuk melakukan iterasi dari halaman 1 sampai 50,
    mengekstrak data mentah secara universal, dan menambahkan kolom timestamp.
    """
    products = []
    session = requests.Session()

    try:
        # Standardisasi domain agar bersih dari slash di ujungnya
        clean_base = base_url.rstrip("/")

        for page in range(start_page, end_page + 1):
            # FIX PATTERN URL: Mengikuti format asli website target (/page2, /page3, dst.)
            if page == 1:
                url = f"{clean_base}/"
            else:
                url = f"{clean_base}/page{page}"

            html_content = fetching_content(url, session)
            if html_content is None:
                print(f"Skipping page {page} due to connection error.")
                continue

            soup = BeautifulSoup(html_content, "html.parser")
            cards = soup.find_all(class_="collection-card")

            if not cards:
                print(
                    f"[!] No product cards found on page {page}, continuing to next page."
                )
                time.sleep(1)
                continue

            for card in cards:
                # 1. Ambil Title secara Universal berdasarkan nama Class langsung
                title_tag = card.find(class_="product-title")
                title = title_tag.get_text(strip=True) if title_tag else None

                # 2. Ambil Price secara Universal berdasarkan nama Class langsung
                price_tag = card.find(class_="price")
                price = price_tag.get_text(strip=True) if price_tag else None

                # 3. Mencari informasi tambahan di dalam tag p biasa
                rating, colors, size, gender = None, None, None, None
                p_tags = card.find_all("p")

                for p in p_tags:
                    text = p.get_text(strip=True)
                    if "rating" in text.lower() or "rated" in text.lower():
                        rating = text
                    elif "colors" in text.lower():
                        colors = text
                    elif "size:" in text.lower():
                        size = text
                    elif "gender:" in text.lower():
                        gender = text

                timestamp = datetime.now().isoformat()

                products.append(
                    {
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "Timestamp": timestamp,
                    }
                )

            print(f"[+] Successfully scraped page {page}")
            time.sleep(1)  # Jeda aman 1 detik anti-rate limit

        df_raw = pd.DataFrame(products)

        if save_raw_csv and not df_raw.empty:
            try:
                df_raw.to_csv("products_raw.csv", index=False)
                print(
                    f"[+] Saved raw scraped data to products_raw.csv ({len(df_raw)} rows)"
                )
            except Exception as e:
                print(f"Warning: failed to save raw CSV: {e}")

        return df_raw

    except Exception as e:
        print(f"An error occurred in scrape_main: {e}")
        return pd.DataFrame()
