import pandas as pd
import os

def load_data(df, file_name='products.csv'):
    try:
        # Simpan ke CSV
        df.to_csv(file_name, index=False)
        print(f"Berhasil menyimpan data ke {file_name}")
        return True
    except Exception as e:
        print(f"Gagal menyimpan data: {e}")
        return False
