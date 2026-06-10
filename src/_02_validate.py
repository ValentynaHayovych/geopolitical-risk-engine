from src.pipeline_logger import log

def validate(df):
    init_rows = len(df)
    
    # Step 1: deduplicate
    before_dup = len(df)
    df = df.drop_duplicates()
    dup_removed = before_dup - len(df)

    # Step 2: standardize
    df = df.copy()
    for col in ["Country_A", "Country_B", "Conflict_Type"]:
        df[col] = df[col].str.strip().str.title()
    
    # Step 3: handle_nulls for critical columns
    critical_columns = ["Country_A", "Country_B", "Year", "Outcome", 'Latitude', 'Longitude']
    
    cc_nulls = df[critical_columns].isnull().sum()
    cc_nulls = cc_nulls[cc_nulls > 0]

    if len(cc_nulls) > 0:
        log.warn("Nullable critical columns detected", detail=cc_nulls.to_dict())

    before_nulls = len(df)
    df = df.dropna(subset=critical_columns)
    nulls_removed = before_nulls - len(df)

    # non-critical nulls
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if len(nulls) > 0:
        log.warn("non-critical nulls", detail=nulls.to_dict())

    final_rows = len(df)

    # Summary logs
    log.kv("rows", f"{init_rows} → {final_rows}")
    log.kv("duplicates removed", dup_removed)
    log.kv("null rows removed", nulls_removed)

    return df
