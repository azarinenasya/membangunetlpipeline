
import pandas as pd

def transform_data(raw_data):
    if not raw_data:
        return pd.DataFrame()

    # Assuming raw_data is a list of product dictionaries
    df = pd.DataFrame(raw_data)

    # Example transformations:
    # Rename columns for consistency
    df = df.rename(columns={'product_id': 'id', 'product_name': 'name', 'product_price': 'price'})

    # Convert price to numeric, handling missing values
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Fill missing prices with 0 or a sensible default
    df['price'] = df['price'].fillna(0)

    # Add a 'currency' column if not present
    if 'currency' not in df.columns:
        df['currency'] = 'IDR' # Example default currency

    return df
