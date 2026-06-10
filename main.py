from src.pipeline_logger import log
from src._01_extract import extract_from_csv, extract_from_sql
from src._02_validate import validate
from src._03_transform import transform
from src.columns import columns
from src._04_predict import conflict_involvment_prediction
from src._05_load import load_raw, load_staging, load_analytics, load_prediction_fact


if __name__ =="__main__":

    log.start()

    # Stage 1
    log.phase(1, "Extract & load → raw")
    df = extract_from_csv("data/global_conflicts_anomalies.csv")
    load_raw(df)
    log.ok("Extraction & load complete")
    
    # Stage 2
    log.phase(2, "Validate & load → staging")
    df = extract_from_sql("global_conflicts", schema="raw")
    df = validate(df)
    load_staging(df)
    log.ok("Validation & load complete")

    # Stage 3
    log.phase(3, "Transform & load → analytics")
    df = extract_from_sql("global_conflicts", schema="staging")
    df = transform(df, columns)
    load_analytics(df)
    log.ok("Transformation & load complete")

    # Predict
    log.phase(4, "Predict & load → analytics")
    df = extract_from_sql("fact_conflicts", schema="analytics")
    predictions = conflict_involvment_prediction(df)
    load_prediction_fact(predictions)
    log.ok("Prediction & load complete")

    log.finish(
        summary={
            "raw ingested": f"{len(df) + len(predictions)} rows",
            "fact rows loaded": f"{len(df)} rows",
            "predictions loaded": f"{len(predictions)} rows"
        }
    )
