import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.extract import fetching_content, scrape_main

class TestExtract(unittest.TestCase):

    @patch("utils.extract.requests.Session")
    def test_fetching_content_success(self, mock_session_cls):
        # Membuat mock untuk response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body><div class='collection-card'></div></body></html>"
        
        # Mengatur agar session.get() mengembalikan mock_response
        mock_session_obj = mock_session_cls.return_value
        mock_session_obj.get.return_value = mock_response

        result = fetching_content("https://example.com", session=mock_session_obj)
        self.assertIsNotNone(result)
        self.assertIn(b"collection-card", result or b"")

    @patch("utils.extract.requests.Session")
    def test_fetching_content_failure(self, mock_session_cls):
        mock_session_obj = mock_session_cls.return_value
        # Mensimulasikan error koneksi
        mock_session_obj.get.side_effect = Exception("Connection Timeout")

        result = fetching_content("https://example.com", session=mock_session_obj)
        self.assertIsNone(result)

    @patch("utils.extract.fetching_content")
    def test_scrape_main_success(self, mock_fetching):
        # Simulasi HTML tiruan dengan 1 kartu produk kotor untuk dites
        html_dummy = """
        <html>
            <div class="collection-card">
                <h3 class="product-title">T-shirt 2</h3>
                <div class="price-container">
                    <span class="price">$102.15</span>
                </div>
                <p>Rating: ⭐ 3.9 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Women</p>
            </div>
        </html>
        """.encode("utf-8")
        mock_fetching.return_value = html_dummy

        # Menjalankan scrape tiruan untuk 1 halaman saja agar cepat
        df = scrape_main("https://fake-url.com", start_page=1, end_page=1)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]["Title"], "T-shirt 2")
        self.assertEqual(df.iloc[0]["Price"], "$102.15")

if __name__ == "__main__":
    unittest.main()