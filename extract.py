import requests
from bs4 import BeautifulSoup

def extract_data(url):
    print(f"Mengambil data dari {https://fashion-studio.dicoding.dev/}")
    try:
        response = requests.get(https://fashion-studio.dicoding.dev/)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        # Mencari container produk (sesuai struktur umum Dicoding Fashion Studio)
        items = soup.find_all('div', class_='card')
        
        for item in items:
            name = item.find('h5', class_='card-title').text.strip() if item.find('h5', class_='card-title') else None
            price = item.find('p', class_='card-text').text.strip() if item.find('p', class_='card-text') else None
            # Mencari kategori melalui tag tertentu atau teks
            category = item.find('span', class_='badge').text.strip() if item.find('span', class_='badge') else "Uncategorized"
            
            if name and price:
                products.append({
                    'product_name': name,
                    'price': price,
                    'category': category
                })
        
        return products
    except Exception as e:
        print(f"Error saat extract: {e}")
        return []
