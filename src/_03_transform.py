from src.pipeline_logger import log
import pandas as pd

def select_columns(df, columns):
    df = df[columns]
    return df

def filter_land_only(df):
    df = df[df["Land_Valid"] == 1] # Filtered Earth land coordinates + 100 km buffer zone. Taken from ML project, see README.
    return df

def filter_year_valid(df):
    df = df[df["Year_Valid"] == 1] # Filtered events with valid Country independence year (between 1950 and 2024). Taken from ML project, see README.
    return df

def add_winner(df):
    df = df.copy()
    df["Winner"] = df.apply(
        lambda row: row["Country_A"] if row["Outcome"] == "Victory_A"
        else row["Country_B"] if row["Outcome"] == "Victory_B"
        else row["Outcome"],
        axis=1
    )
    return df

def add_gdp_gap(df):
    df = df.copy()
    df["GDP_Gap"] = abs(df["GDP_A_Billions"] - df["GDP_B_Billions"]).round(1)

    df["GDP_GAP_Label"] = pd.cut(
        df['GDP_Gap'],
        bins = [0, 5000, 11000, float('inf')],
        labels = ['Low', 'Medium', 'High']
    )
    return df

def transform(df, columns):
    init_rows = len(df)
    init_cols = len(df.columns)

    # Transform steps
    df = select_columns(df, columns)
    df = filter_land_only(df)
    df = filter_year_valid(df)
    df = add_winner(df)
    df = add_gdp_gap(df)

    final_rows = len(df)
    final_cols = len(df.columns)


    log.kv("columns", f"{init_cols} → {final_cols}")
    log.kv("rows", f"{init_rows} → {final_rows}")
    log.kv("derived", ["Winner", "GDP_Gap", "GDP_GAP_Label"])

    return df




