import pandas as pd

def clean_title_column(df):
    """
    Fungsi pembantu untuk memvalidasi kolom Title.
    Dibungkus tersendiri untuk keperluan Unit Testing.
    """
    try:
        if df is None:
            return None
        return df[df['Title'] != 'Unknown Product']
    except Exception as e:
        print(f"Error in clean_title_column: {e}")
        return None

def transform_main(df_raw):
    """
    Fungsi utama tahap Transform.
    Membersihkan data kotor pada kolom Title, Price, dan Rating tanpa over-dropping.
    Target output: Tepat 867 baris data bersih dari 1000 data unik halaman 1-50.
    """
    if df_raw.empty:
        print("[-] Transform Stage: Input DataFrame is empty.")
        return pd.DataFrame()

    try:
        df = df_raw.copy()

        # 1. Eliminasi data kotor (Title & Price exact match)
        df = df[df['Title'] != 'Unknown Product']
        df = df[df['Price'] != 'Price Unavailable']
        
        # Eliminasi data kotor pada kolom Rating
        df = df[~df['Rating'].str.contains('Invalid Rating', case=False, na=False)]

        # Kita hanya membuang baris jika Title atau Price-nya yang hilang secara mutlak
        df = df.dropna(subset=['Title', 'Price'])

        # 2. Transformasi kolom Price ($102.15 -> Angka Float * 16000 Rupiah)
        df['Price'] = df['Price'].str.extract(r'(\d+\.\d+|\d+)').astype(float) * 16000

        # 3. Transformasi kolom Rating (Rating: ⭐ 3.9 / 5 -> 3.9)
        # Produk berstatus "Not Rated" hasil extract-nya NaN, otomatis diisi 0.0 (Data tetap aman terjaga)
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+|\d+)').astype(float).fillna(0.0)

        # 4. Transformasi kolom Colors (3 Colors -> 3)
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').fillna(0).astype(int)

        # 5. Transformasi kolom Size (Size: M -> M)
        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False).str.strip()

        # 6. Transformasi kolom Gender (Gender: Women -> Women)
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False).str.strip()
        
        print(f"[+] Transform Stage Success: Filtered down to {len(df)} clean data rows.")
        return df

    except Exception as e:
        print(f"An error occurred in transform_main: {e}")
        return pd.DataFrame()