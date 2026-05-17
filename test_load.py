import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv, load_to_google_sheets

class TestLoad(unittest.TestCase):

    def setUp(self):
        # Menyiapkan data dummy dalam bentuk DataFrame
        self.df_dummy = pd.DataFrame({
            'product_name': ['Kaos'],
            'price': [100000],
            'category': ['T-shirt']
        })

    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv(self, mock_to_csv):
        # Menjalankan fungsi load ke csv
        file_name = "test_products.csv"
        load_to_csv(self.df_dummy, file_name)

        # Memastikan fungsi to_csv dipanggil dengan argumen yang benar
        mock_to_csv.assert_called_once_with(file_name, index=False)

    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    @patch('utils.load.gspread.authorize')
    def test_load_to_google_sheets(self, mock_authorize, mock_creds):
        # Mocking gspread client dan spreadsheet
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_sheet = MagicMock()
        
        mock_authorize.return_value = mock_client
        mock_client.open_by_url.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_sheet

        # Jalankan fungsi
        gsheet_url = "https://docs.google.com/spreadsheets/d/dummy"
        json_key = "dummy.json"
        load_to_google_sheets(self.df_dummy, gsheet_url, json_key)

        # Assertions
        # Memastikan kredensial dipanggil
        mock_creds.assert_called_once()
        # Memastikan sheet dikosongkan sebelum diisi
        mock_sheet.clear.assert_called_once()
        # Memastikan update dipanggil (upload data)
        mock_sheet.update.assert_called_once()

if __name__ == '__main__':
    unittest.main()
