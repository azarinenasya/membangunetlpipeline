import pandas as pd
import re

def transform_data(raw_data):
    if not raw_data:
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)
    
    # Fungsi membersihkan harga: "Rp 150.000" -> 150000
    def clean_price(price_str):
        clean_str = re.sub(r'[^\d]', '', price_str)
        return int(clean_str) if clean_str else 0

    df['price'] = df['price'].apply(clean_price)
    
    # Menghapus duplikat jika ada
    df = df.drop_duplicates()
    
    # Tambahkan kolom timestamp untuk audit data
    df['extracted_at'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return df
