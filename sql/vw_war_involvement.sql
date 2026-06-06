USE geopolitical_impact
GO

CREATE VIEW vw_war_involvement AS
SELECT Country, COUNT(*) AS War_Involvement_Count
FROM (
    SELECT Country_A AS Country FROM geopolitical_impact.dbo.global_conflicts_filtered
    UNION ALL
    SELECT Country_B AS Country FROM geopolitical_impact.dbo.global_conflicts_filtered
) AS combined
GROUP BY Country;