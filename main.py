from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_google_sheets

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
        load_to_csv(df_cleaned)
        
        # Load to Google Sheets (pastikan file json sudah ada)
        # load_to_google_sheets(df_cleaned, GSHEET_URL, JSON_KEY)
        
        print("--- ETL Pipeline Completed Successfully ---")
    else:
        print("No data extracted. Pipeline stopped.")

if __name__ == "__main__":
    main()
