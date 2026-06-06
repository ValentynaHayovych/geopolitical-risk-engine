USE geopolitical_impact
GO

CREATE OR ALTER VIEW vw_gdp_gap_group_stats AS
SELECT 
    GDP_Gap_Label,
    COUNT(*) AS Conflict_Count,
    ROUND(AVG(Economic_Loss_USD_Billions), 2) AS Avg_Economic_Loss,
    SUM(Economic_Loss_USD_Billions) AS Total_Economic_Loss,
    AVG(Total_Deaths) AS Avg_Deaths,
    SUM(Total_Deaths) AS Total_Deaths
FROM dbo.global_conflicts_filtered
GROUP BY GDP_Gap_Label;