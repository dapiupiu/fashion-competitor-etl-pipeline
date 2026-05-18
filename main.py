import sys
from utils.extract import scrape_main
from utils.transform import transform_main
from utils.load import load_main

# Konfigurasi Global
BASE_URL = "https://fashion-studio.dicoding.dev"

# Spreadsheet ID Google Sheets
SPREADSHEET_ID = "17dn82H4jhKFNG24ea2wfeUIdAhDYra0Jz66yeY1dsBk"

# URL Database PostgreSQL
DB_URL = "postgresql://kakadavidharmawan:kakadavidharmawan@localhost:5432/fashion_retail_competitor"

def run_pipeline():
    print("=========================================")
    print("STARTING ETL PIPELINE - FASHION STUDIO")
    print("=========================================\n")
    
    # EXTRACT STAGE
    print("[1/3] Executing Extract Stage...")
    # Menjalankan scraping dari halaman 1 sampai 50
    df_raw = scrape_main(BASE_URL, start_page=1, end_page=50)
    
    if df_raw.empty:
        print("[-] Extract Stage Failed: No data scraped. Terminating pipeline.")
        sys.exit(1)
        
    print(f"[+] Extract Stage Success: Captured {len(df_raw)} raw data rows.\n")
    
    # TRANSFORM STAGE
    print("[2/3] Executing Transform Stage...")
    df_cleaned = transform_main(df_raw)
    
    if df_cleaned.empty:
        print("[-] Transform Stage Failed: Dataframe is empty after cleaning. Terminating pipeline.")
        sys.exit(1)
        
    print(f"[+] Transform Stage Success: Filtered down to {len(df_cleaned)} clean data rows.\n")
    
    # LOAD STAGE
    print("[3/3] Executing Load Stage...")
    # Menyimpan ke 3 repositori sekaligus: CSV, Google Sheets, dan PostgreSQL
    load_main(df_cleaned, spreadsheet_id=SPREADSHEET_ID, db_url=DB_URL)
    
    print("\n=========================================")
    print("ETL PIPELINE EXECUTED SUCCESSFULLY!")
    print("=========================================")

if __name__ == "__main__":
    run_pipeline()