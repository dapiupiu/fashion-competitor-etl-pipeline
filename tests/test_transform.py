import unittest
import pandas as pd
from utils.transform import transform_main, clean_title_column

class TestTransform(unittest.TestCase):

    def test_transform_complete_pipeline(self):
        # Data kotor buatan (mock raw data)
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

        # Eksekusi transformasi
        df_cleaned = transform_main(df_raw)

        self.assertEqual(len(df_cleaned), 2)
        self.assertEqual(df_cleaned.iloc[0]["Price"], 1600000.0)
        self.assertEqual(df_cleaned.iloc[0]["Size"], "M")
        self.assertEqual(df_cleaned.iloc[0]["Gender"], "Women")
        self.assertEqual(df_cleaned.iloc[0]["Colors"], 3)
        self.assertEqual(df_cleaned.iloc[0]["Rating"], 4.0)

    def test_transform_main_empty_dataframe(self):
        """Menguji skenario ketika dataframe yang masuk kosong"""
        df_empty = pd.DataFrame()
        result = transform_main(df_empty)
        self.assertTrue(result.empty)

    def test_clean_column_exception_handling(self):
        """Memicu blok 'except' dengan sengaja dengan melempar objek Non-DataFrame"""
        # Mengirimkan None akan memicu AttributeError di dalam fungsi dan mengeksekusi blok 'except'
        result = clean_title_column(None)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()