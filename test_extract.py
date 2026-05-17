import unittest
from unittest.mock import patch, MagicMock
from utils.extract import extract_data

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_extract_data_success(self, mock_get):
        # Menyusun HTML palsu yang mirip dengan struktur web Fashion Studio
        mock_html = """
        <html>
            <div class="card">
                <h5 class="card-title">Kaos Polos</h5>
                <p class="card-text">Rp 100.000</p>
                <span class="badge">T-shirt</span>
            </div>
            <div class="card">
                <h5 class="card-title">Celana Jeans</h5>
                <p class="card-text">Rp 200.000</p>
                <span class="badge">Pants</span>
            </div>
        </html>
        """
        
        # Konfigurasi mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        # Jalankan fungsi
        url = "https://fashion-studio.dicoding.dev/"
        result = extract_data(url)

        # Assertions (Memastikan data yang diekstrak benar)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['product_name'], 'Kaos Polos')
        self.assertEqual(result[1]['category'], 'Pants')
        mock_get.assert_called_once_with(url)

    @patch('utils.extract.requests.get')
    def test_extract_data_failure(self, mock_get):
        # Simulasi jika website down (error 404)
        mock_get.side_effect = Exception("Connection Error")
        
        result = extract_data("https://salah-url.com")
        
        # Harus mengembalikan list kosong jika terjadi error
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
