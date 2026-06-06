USE geopolitical_impact
GO

CREATE VIEW vw_yearly_trend AS
SELECT Year,
	COUNT(*) AS Total_Conflicts,
	SUM(Total_Deaths) as Total_Deaths,
	SUM(Economic_Loss_USD_Billions) as Total_Economic_Loss
FROM dbo.global_conflicts_filtered
GROUP BY Year;