import pandas as pd

def extract(filepath):
    df = pd.read_csv(filepath)
    print(f"Extracted data: {len(df)} rows, {len(df.columns)} columns")
    return df