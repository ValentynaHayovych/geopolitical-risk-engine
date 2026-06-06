import pandas as pd

def select_columns(df, columns):
    df = df[columns]
    print(f"Columns selected: {len(df.columns)}")
    return df

def filter_land_only(df):
    df = df[df["Land_Valid"] == 1]
    print(f"Filtered dataset based on land coordinates. Kept {len(df)} rows.")
    return df

def filter_year_valid(df):
    df = df[df["Year_Valid"] == 1]
    print(f"Filtered dataset based on valid year. Kept {len(df)} rows.")
    return df

def add_winner(df):
    df["Winner"] = df.apply(
        lambda row: row["Country_A"] if row["Outcome"] == "Victory_A"
        else row["Country_B"] if row["Outcome"] == "Victory_B"
        else row["Outcome"],
        axis=1
    )
    return df

def add_gdp_gap(df):
    df["GDP_Gap"] = abs(df["GDP_A_Billions"] - df["GDP_B_Billions"]).round(1)

    df["GDP_GAP_Label"] = pd.cut(
        df['GDP_Gap'],
        bins = [0, 5000, 11000, float('inf')],
        labels = ['Low', 'Medium', 'High']
    )
    return df

def transform(df, columns):
    df = select_columns(df, columns)
    df = filter_land_only(df)
    df = filter_year_valid(df)
    df = add_winner(df)
    df = add_gdp_gap(df)
    return df




