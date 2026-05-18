import unittest
import pandas as pd
from utils.transform import transform_main

class TestTransform(unittest.TestCase):

    def test_transform_complete_pipeline(self):
        # Membuat data kotor buatan (mock raw data)
        raw_data = {
            "Title": ["T-shirt 2", "Unknown Product", "Pants 4"],
            "Price": ["$100.00", "Price Unavailable", "$50.00"],
            "Rating": ["Rating: \u2b50 4.0 / 5", "Invalid Rating", "Rating: \u2b50 3.5 / 5"],
            "Colors": ["3 Colors", "5 Colors", "1 Colors"],
            "Size": ["Size: M", "Size: L", "Size: XL"],
            "Gender": ["Gender: Women", "Gender: Unisex", "Gender: Men"],
            "Timestamp": ["2026-05-19T00:00:00", "2026-05-19T00:00:00", "2026-05-19T00:00:00"]
        }
        df_raw = pd.DataFrame(raw_data)

        # Eksekusi fungsi transformasi utama
        df_cleaned = transform_main(df_raw)

        # Verifikasi hasil akhir harus bersih dari data 'Unknown Product' / 'Price Unavailable'
        # Baris ke-2 akan terbuang karena dropna() pada nilai invalid, menyisakan 2 baris.
        self.assertEqual(len(df_cleaned), 2)
        
        # Cek apakah konversi kurs $100.00 * 16000 = 1600000.0 bekerja dengan benar
        self.assertEqual(df_cleaned.iloc[0]["Price"], 1600000.0)
        
        # Cek pembersihan string prefix
        self.assertEqual(df_cleaned.iloc[0]["Size"], "M")
        self.assertEqual(df_cleaned.iloc[0]["Gender"], "Women")
        self.assertEqual(df_cleaned.iloc[0]["Colors"], 3)
        self.assertEqual(df_cleaned.iloc[0]["Rating"], 4.0)

        # Pastikan tipe data mutlak sesuai ekspektasi Dicoding
        self.assertEqual(df_cleaned["Price"].dtype, "float64")
        self.assertEqual(df_cleaned["Rating"].dtype, "float64")
        self.assertEqual(df_cleaned["Colors"].dtype, "int64")

if __name__ == "__main__":
    unittest.main()