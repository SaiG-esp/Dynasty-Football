CREATE TABLE defensive_intel (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) UNIQUE,
    havoc_score DECIMAL(5, 2),
    sacks_pg DECIMAL(5, 2),
    turnovers_pg DECIMAL(5, 2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);