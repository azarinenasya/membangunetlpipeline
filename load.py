import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_to_csv(df, file_name='products.csv'):
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

def load_to_google_sheets(df, spreadsheet_url, json_key_path):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_url(spreadsheet_url).get_worksheet(0)
        
        # Bersihkan sheet sebelum upload baru (opsional)
        sheet.clear()
        
        # Upload header dan data
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("Data successfully uploaded to Google Sheets")
    except Exception as e:
        print(f"Error loading to Google Sheets: {e}")
