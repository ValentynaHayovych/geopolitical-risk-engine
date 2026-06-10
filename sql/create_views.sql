-- Required for Power BI compatibility

USE geopolitical_risk_engine
GO

CREATE OR ALTER VIEW dbo.fact_conflicts AS
    SELECT * FROM analytics.fact_conflicts;
GO

CREATE OR ALTER VIEW dbo.fact_country_conflict_predictions AS
    SELECT * FROM analytics.fact_country_conflict_predictions;
GO