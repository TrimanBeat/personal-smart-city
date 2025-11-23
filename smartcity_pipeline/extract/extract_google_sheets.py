import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def extract_fact_diario():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credenciales.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("TuHoja").worksheet("Respuestas")
    data = sheet.get_all_records()

    return pd.DataFrame(data)
