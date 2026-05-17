
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
