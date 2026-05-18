import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql, load_main

class TestLoad(unittest.TestCase):

    def setUp(self):
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
        mock_exists.return_value = True
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value.values.return_value.clear.return_value.execute.return_value = {}
        mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {"updatedCells": 10}

        result = load_to_google_sheets(self.df_dummy, spreadsheet_id="fake_id")
        self.assertTrue(result)

    def test_load_to_google_sheets_missing_id(self):
        """Menguji handling ketika spreadsheet_id kosong"""
        result = load_to_google_sheets(self.df_dummy, spreadsheet_id=None)
        self.assertFalse(result)

    @patch("utils.load.os.path.exists")
    def test_load_to_google_sheets_missing_credentials_file(self, mock_exists):
        """Menguji handling ketika file json kredensial tidak ditemukan"""
        mock_exists.return_value = False
        result = load_to_google_sheets(self.df_dummy, spreadsheet_id="fake_id", credentials_path="wrong_path.json")
        self.assertFalse(result)

    @patch("utils.load.create_engine")
    @patch("pandas.DataFrame.to_sql")
    def test_load_to_postgresql_success(self, mock_to_sql, mock_create_engine):
        result = load_to_postgresql(self.df_dummy, db_url="postgresql://fake", table_name="fake_table")
        self.assertTrue(result)
        mock_to_sql.assert_called_once()

    @patch("utils.load.load_to_csv")
    @patch("utils.load.load_to_google_sheets")
    @patch("utils.load.load_to_postgresql")
    def test_load_main_orchestration(self, mock_pg, mock_gs, mock_csv):
        """Menguji apakah load_main memanggil ketiga fungsi penyimpanan dengan benar"""
        load_main(self.df_dummy, spreadsheet_id="fake_id", db_url="postgresql://fake")
        mock_csv.assert_called_once()
        mock_gs.assert_called_once()
        mock_pg.assert_called_once()

    def test_load_main_empty_dataframe(self):
        """Menguji load_main ketika menerima dataframe kosong"""
        # Tidak akan mengeksekusi penyimpanan dan hanya memunculkan warning log
        load_main(pd.DataFrame())

if __name__ == "__main__":
    unittest.main()