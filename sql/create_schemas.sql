USE geopolitical_risk_engine
GO

IF NOT EXISTS(SELECT * FROM sys.schemas WHERE name = 'raw')
	EXEC('CREATE SCHEMA raw');

IF NOT EXISTS(SELECT * FROM sys.schemas WHERE name = 'staging')
	EXEC('CREATE SCHEMA staging');

IF NOT EXISTS(SELECT * FROM sys.schemas WHERE name = 'analytics')
	EXEC('CREATE SCHEMA analytics');