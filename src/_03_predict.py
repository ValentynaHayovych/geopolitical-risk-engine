from sklearn.linear_model import PoissonRegressor
import pandas as pd
import numpy as np

def conflict_involvment_prediction(df):
    
    # Melts Country_A and Country_B into a single Country column with corresponding Conflict_Count and Years
    def melted_country_conflicts(df):
        country_conflicts = (
            df.melt(id_vars=["Year"], value_vars=["Country_A", "Country_B"], value_name="Country")
            .groupby(["Year", "Country"])
            .size()
            .reset_index(name="Conflict_Count")
        )

        return country_conflicts

    # Adds predictions for countries conflict involvment for 2025 and 2026 using Poisson Regression
    def pr_prediction(country_name, table):
        X = table[['Year']]
        y = table['Conflict_Count']

        model = PoissonRegressor()
        model.fit(X, y)

        future_years = pd.DataFrame({"Year": [2025, 2026]})
        predictions = np.round(model.predict(future_years)).astype(int)

        return pd.DataFrame({
            "Country": country_name,
            "Year": [2025, 2026],
            "Conflict_Count": predictions,
            "Is_Prediction": True
        })

    all_predictions = []

    country_conflicts = melted_country_conflicts(df)
    country_conflicts["Is_Prediction"] = False

    for country, group in country_conflicts.groupby("Country"):
        pred_df = pr_prediction(country, group)
        all_predictions.append(pred_df)

    all_predictions_df = pd.concat(all_predictions, ignore_index=True)
    final_df = pd.concat([country_conflicts, all_predictions_df], ignore_index=True)

    return final_df




