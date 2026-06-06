USE geopolitical_impact
GO

CREATE VIEW vw_economic_loss_by_conflict_type AS
SELECT Conflict_Type,
	SUM(Economic_Loss_USD_Billions) AS Total_Economic_Loss,
	AVG(Economic_Loss_USD_Billions) AS Average_Economic_Loss
FROM dbo.global_conflicts_filtered
GROUP BY Conflict_Type;