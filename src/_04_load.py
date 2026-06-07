from config import engine


def load(df, prediction):

    df.to_sql(
        name="global_conflicts",
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False
    )

    df.to_sql(
        name = "global_conflicts",
        con=engine,
        schema = "staging",
        if_exists="replace",
        index=False
    )

    df.to_sql(
        name="fact_conflicts", 
        con=engine,
        schema="analytics",
        if_exists="replace", 
        index=False
    )
    print(f"Loaded {len(df)} rows into fact_conflicts")

    prediction.to_sql(
        name="fact_country_conflict_predictions", 
        con=engine,
        schema="analytics",
        if_exists="replace",
        index=False
    )
    print(f"Loaded {len(prediction)} rows into fact_country_conflict_predictions")
