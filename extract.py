import requests
from bs4 import BeautifulSoup

def extract_data(url):
    try:
        response = requests.get(https://fashion-studio.dicoding.dev/)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        # Mencari card produk di website Fashion Studio
        items = soup.find_all('div', class_='card')
        
        for item in items:
            name = item.find('h5', class_='card-title').text.strip()
            price = item.find('p', class_='card-text').text.strip()
            # Mencari kategori dari badge
            category = item.find('span', class_='badge').text.strip()
            
            products.append({
                'product_name': name,
                'price': price,
                'category': category
            })
        return products
    except Exception as e:
        print(f"Error during extraction: {e}")
        return []
