from daylio.extract_daylio import extract_daylio
from daylio.transform_daylio import transform_daylio
from daylio.load_daylio import load_daylio

def run_pipeline():
    print("\n=== EXTRACT ===")
    df = extract_daylio("data/daylio_export.csv")
    print(df.head())

    print("\n=== TRANSFORM ===")
    df = transform_daylio(df)
    print(df.head())

    print("\n=== LOAD ===")
    load_daylio(df)

    print("\n✓ Pipeline Daylio ejecutado correctamente\n")

if __name__ == "__main__":
    run_pipeline()
