import pandas as pd
import re

def transform_data(raw_data):
    if not raw_data:
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)
    
    # Fungsi untuk membersihkan harga (contoh: "Rp 150.000" -> 150000)
    def clean_price(price_str):
        if not price_str:
            return 0
        # Hapus 'Rp', titik, dan spasi
        clean_str = re.sub(r'[^\d]', '', price_str)
        return int(clean_str) if clean_str else 0

    df['price'] = df['price'].apply(clean_price)
    
    # Membersihkan nama produk (opsional)
    df['product_name'] = df['product_name'].str.title()
    
    # Menghapus duplikat
    df = df.drop_duplicates()
    
    return df
