import os
import importlib

# Install necessary packages for the utils modules if not already installed.
# These packages are used by utils/extract.py and utils/transform.py
try:
    import requests
    import bs4 # For BeautifulSoup
    import pandas
except ImportError:
    print("Installing required packages: requests, beautifulsoup4, pandas...")
    !pip install requests beautifulsoup4 pandas --quiet
    print("Packages installed.")

# --- Start of utils module creation for self-containment ---

# Ensure 'utils' directory exists
if not os.path.exists('utils'):
    os.makedirs('utils')
    print("Created directory: utils/")
else:
    print("Directory 'utils/' already exists.")

# Create utils/extract.py
# (This code is taken from cell DRPEvu6dsttz in the notebook history)
extract_code = """
import requests
from bs4 import BeautifulSoup
import json

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for HTTP errors

        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response.headers.get('Content-Type')}")
        print(f"Response text (first 500 chars): {response.text[:500]}")

        soup = BeautifulSoup(response.text, 'html.parser')
        products_data = []

        # --- REFINING SELECTORS FOR CONTAINERS ---
        # Broader search for product containers, looking for common patterns.
        # This current setup found 41 containers, so the issue is likely within the container.
        product_containers = soup.find_all(
            lambda tag: tag.name in ['div', 'article', 'section'] and
                        tag.has_attr('class') and
                        any(cls in x.lower() for x in tag['class'] for cls in ['product', 'item', 'card', 'col-md-'])
        )

        if not product_containers:
            print("No specific product containers found with common class patterns.")
            # Fallback to finding all divs/articles/sections if no specific product containers were found
            product_containers = soup.find_all(['div', 'article', 'section'])
            if not product_containers:
                print("No general div/article/section tags found either. Cannot proceed with extraction.")
                return []

        print(f"Found {len(product_containers)} potential product containers.")

        for i, container in enumerate(product_containers):
            product_name = 'N/A'
            product_price = 0.0

            # --- REFINING SELECTORS FOR NAME AND PRICE WITHIN CONTAINER ---

            # Search for product name: Try h tags (h1-h6), then strong tag within the container.
            # Prioritize elements that contain 'name' in their class, but fall back to any h-tag or strong.
            name_tag = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong'],
                                      class_=lambda x: x and 'name' in x.lower())
            if not name_tag:
                name_tag = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong'])

            if name_tag:
                product_name = name_tag.get_text(strip=True)
                if not product_name: # If text is empty after stripping, consider it not found
                    product_name = 'N/A'

            # Search for product price: Try p/span with 'price' in class, then p/span with digits, then any p/span.
            price_tag = container.find(['p', 'span'],
                                       class_=lambda x: x and 'price' in x.lower())
            if not price_tag:
                 price_tag = container.find(['p', 'span'],
                                            string=lambda text: text and any(char.isdigit() for char in text))
            if not price_tag:
                price_tag = container.find(['p', 'span']) # Last resort: any p or span tag

            if price_tag:
                product_price_str = price_tag.get_text(strip=True)

                # Robust cleaning of price string: extract digits and a single decimal point
                cleaned_chars = []
                has_decimal = False
                for char in product_price_str:
                    if char.isdigit():
                        cleaned_chars.append(char)
                    elif char == '.' and not has_decimal: # Allow only one decimal point
                        cleaned_chars.append(char)
                        has_decimal = True
                    # Ignore other characters like currency symbols, commas, spaces

                product_price_str_cleaned = ''.join(cleaned_chars)

                try:
                    product_price = float(product_price_str_cleaned) if product_price_str_cleaned else 0.0
                except ValueError:
                    product_price = 0.0 # Default if conversion fails

            # Only add to products_data if both name is found and price is positive (not 0 from parsing failure)
            if product_name != 'N/A' and product_price > 0.0:
                 products_data.append({
                    'product_name': product_name,
                    'product_price': product_price
                })

        print(f"Extracted {len(products_data)} products.")
        return products_data

    except requests.exceptions.RequestException as e:
        print(f"Error during data extraction: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e} - Type: {type(e)}")
        return None
"""

with open('utils/extract.py', 'w') as f:
    f.write(extract_code)
print("Updated utils/extract.py with web scraping logic")

# Create utils/transform.py
# (This code is taken from cell 5505e9c6 in the notebook history)
transform_code = """
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
"""

with open('utils/transform.py', 'w') as f:
    f.write(transform_code)
print("Created utils/transform.py")

# Reload the modules to apply changes, in case they were already loaded in the session
# This ensures that the subsequent imports use the newly defined files.
if 'utils.extract' in importlib.sys.modules:
    importlib.reload(importlib.sys.modules['utils.extract'])
if 'utils.transform' in importlib.sys.modules:
    importlib.reload(importlib.sys.modules['utils.transform'])

# --- End of utils module creation for self-containment ---

from utils.extract import extract_data
from utils.transform import transform_data
# load_to_csv and load_to_google_sheets are defined in cell hMD1GahJruuU, so no need to import them from utils.load
# from utils.load import load_to_csv, load_to_google_sheets

def main():
    URL = "https://fashion-studio.dicoding.dev/"
    # Ganti dengan URL Google Sheets Anda
    GSHEET_URL = "https://docs.google.com/spreadsheets/d/your-id-here/edit"
    JSON_KEY = "google-sheets-api.json"

    print("--- Starting ETL Pipeline ---")

    # Extract
    raw_data = extract_data(URL)

    if raw_data:
        # Transform
        df_cleaned = transform_data(raw_data)

        # Load
        # The functions `load_to_csv` and `load_to_google_sheets` are defined in another cell (`hMD1GahJruuU`).
        # For the purpose of fixing the immediate `ModuleNotFoundError: No module named 'utils'`,
        # these definitions are not included here, assuming cell `hMD1GahJruuU` is run beforehand.
        load_to_csv(df_cleaned)

        # Load to Google Sheets (pastikan file json sudah ada)
        # load_to_google_sheets(df_cleaned, GSHEET_URL, JSON_KEY)

        print("--- ETL Pipeline Completed Successfully ---")
    else:
        print("No data extracted. Pipeline stopped.")

if __name__ == "__main__":
    main()

# Create the 'utils' directory if it doesn't exist
import os
if not os.path.exists('utils'):
    os.makedirs('utils')
    print("Created directory: utils/")
else:
    print("Directory 'utils/' already exists.")



# Create utils/extract.py
extract_code = """
import requests
import json

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for HTTP errors

        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response.headers.get('Content-Type')}")
        print(f"Response text (first 500 chars): {response.text[:500]}")

        # Attempt to parse as JSON
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during data extraction: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print(f"Response text that caused error: {response.text}")
        return None
"""

with open('utils/extract.py', 'w') as f:
    f.write(extract_code)
print("Updated utils/extract.py for debugging")

import importlib
import utils.extract
importlib.reload(utils.extract)
print("Reloaded utils.extract module")

# Create utils/transform.py
transform_code = """
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
"""

with open('utils/transform.py', 'w') as f:
    f.write(transform_code)
print("Created utils/transform.py")

# Install BeautifulSoup for web scraping
!pip install beautifulsoup4

# Update utils/extract.py to use web scraping
extract_code_for_scraping = """
import requests
from bs4 import BeautifulSoup
import json

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for HTTP errors

        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response.headers.get('Content-Type')}")
        print(f"Response text (first 500 chars): {response.text[:500]}")

        soup = BeautifulSoup(response.text, 'html.parser')
        products_data = []

        # --- REFINING SELECTORS FOR CONTAINERS ---
        # Broader search for product containers, looking for common patterns.
        # This current setup found 41 containers, so the issue is likely within the container.
        product_containers = soup.find_all(
            lambda tag: tag.name in ['div', 'article', 'section'] and
                        tag.has_attr('class') and
                        any(cls in x.lower() for x in tag['class'] for cls in ['product', 'item', 'card', 'col-md-'])
        )

        if not product_containers:
            print("No specific product containers found with common class patterns.")
            # Fallback to finding all divs/articles/sections if no specific product containers were found
            product_containers = soup.find_all(['div', 'article', 'section'])
            if not product_containers:
                print("No general div/article/section tags found either. Cannot proceed with extraction.")
                return []

        print(f"Found {len(product_containers)} potential product containers.")

        for i, container in enumerate(product_containers):
            product_name = 'N/A'
            product_price = 0.0

            # --- REFINING SELECTORS FOR NAME AND PRICE WITHIN CONTAINER ---

            # Search for product name: Try h tags (h1-h6), then strong tag within the container.
            # Prioritize elements that contain 'name' in their class, but fall back to any h-tag or strong.
            name_tag = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong'],
                                      class_=lambda x: x and 'name' in x.lower())
            if not name_tag:
                name_tag = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong'])

            if name_tag:
                product_name = name_tag.get_text(strip=True)
                if not product_name: # If text is empty after stripping, consider it not found
                    product_name = 'N/A'

            # Search for product price: Try p/span with 'price' in class, then p/span with digits, then any p/span.
            price_tag = container.find(['p', 'span'],
                                       class_=lambda x: x and 'price' in x.lower())
            if not price_tag:
                 price_tag = container.find(['p', 'span'],
                                            string=lambda text: text and any(char.isdigit() for char in text))
            if not price_tag:
                price_tag = container.find(['p', 'span']) # Last resort: any p or span tag

            if price_tag:
                product_price_str = price_tag.get_text(strip=True)

                # Robust cleaning of price string: extract digits and a single decimal point
                cleaned_chars = []
                has_decimal = False
                for char in product_price_str:
                    if char.isdigit():
                        cleaned_chars.append(char)
                    elif char == '.' and not has_decimal: # Allow only one decimal point
                        cleaned_chars.append(char)
                        has_decimal = True
                    # Ignore other characters like currency symbols, commas, spaces

                product_price_str_cleaned = ''.join(cleaned_chars)

                try:
                    product_price = float(product_price_str_cleaned) if product_price_str_cleaned else 0.0
                except ValueError:
                    product_price = 0.0 # Default if conversion fails

            # Debugging print statement for each container to see what's being found
            # print(f"DEBUG: Container {i+1} -> Name: '{product_name}', Price: '{product_price}'")

            # Only add to products_data if both name is found and price is positive (not 0 from parsing failure)
            if product_name != 'N/A' and product_price > 0.0:
                 products_data.append({
                    'product_name': product_name,
                    'product_price': product_price
                })
            # else:
                # print(f"DEBUG: Skipping container {i+1} due to incomplete/invalid data: Name='{product_name}', Price='{product_price}'")

        print(f"Extracted {len(products_data)} products.")
        return products_data

    except requests.exceptions.RequestException as e:
        print(f"Error during data extraction: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e} - Type: {type(e)}")
        return None
"""

with open('utils/extract.py', 'w') as f:
    f.write(extract_code_for_scraping)
print("Updated utils/extract.py with more robust web scraping logic")

# Reload the module to apply changes
import importlib
import utils.extract
importlib.reload(utils.extract)
print("Reloaded utils.extract module after update")
