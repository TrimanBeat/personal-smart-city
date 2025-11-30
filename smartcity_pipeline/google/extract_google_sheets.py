import gspread
import pandas as pd
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

def extract_fact_diario():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.getenv("CREDENTIALS_JSON"), scope
    )
    
    client = gspread.authorize(creds)
    
    sheet = client.open(os.getenv("SHEET_NAME")).sheet1

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    return df
