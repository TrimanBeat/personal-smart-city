import pandas as pd

def extract_daylio(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df
