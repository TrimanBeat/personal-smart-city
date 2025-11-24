from google.extract_google_sheets import extract_fact_diario
from google.clean_google_sheets import clean_fact_diario
from google.load_fact_diario import load_fact_diario

def run_pipeline():
    print("\n=== EXTRACT ===")
    df = extract_fact_diario()
    print(df.head())

    print("\n=== CLEAN ===")
    df = clean_fact_diario(df)
    print(df.head())

    print("\n=== LOAD ===")
    load_fact_diario(df)

    print("\n✓ Pipeline ejecutado correctamente\n")

if __name__ == "__main__":
    run_pipeline()
