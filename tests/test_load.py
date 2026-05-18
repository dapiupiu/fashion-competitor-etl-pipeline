import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

class TestLoad(unittest.TestCase):

    def setUp(self):
        # Menyiapkan dataframe tiruan ringkas untuk pengujian
        self.df_dummy = pd.DataFrame([{
            "Title": "Kaos", "Price": 160000.0, "Rating": 4.5, 
            "Colors": 2, "Size": "L", "Gender": "Men", "Timestamp": "2026"
        }])

    @patch("pandas.DataFrame.to_csv")
    def test_load_to_csv_success(self, mock_to_csv):
        result = load_to_csv(self.df_dummy, filename="fake_products.csv")
        self.assertTrue(result)
        mock_to_csv.assert_called_once()

    @patch("utils.load.os.path.exists")
    @patch("utils.load.service_account.Credentials.from_service_account_file")
    @patch("utils.load.build")
    def test_load_to_google_sheets_success(self, mock_build, mock_creds, mock_exists):
        # Mengelabui pengecekan file json agar dianggap ada
        mock_exists.return_value = True
        
        # Mocking Google API client internal call chain
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value.values.return_value.clear.return_value.execute.return_value = {}
        mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {"updatedCells": 10}

        result = load_to_google_sheets(self.df_dummy, spreadsheet_id="fake_id")
        self.assertTrue(result)

    @patch("utils.load.create_engine")
    @patch("pandas.DataFrame.to_sql")
    def test_load_to_postgresql_success(self, mock_to_sql, mock_create_engine):
        result = load_to_postgresql(self.df_dummy, db_url="postgresql://fake", table_name="fake_table")
        self.assertTrue(result)
        mock_to_sql.assert_called_once()

if __name__ == "__main__":
    unittest.main()