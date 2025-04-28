#!/bin/bash
set -e

# Drop the existing ticker_data table if it exists
echo "Dropping existing ticker_data table (if exists)..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  DROP TABLE IF EXISTS ticker_data;
EOSQL

# Create the ticker_data table
echo "Creating ticker_data table..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /db/create_table.sql
echo "Test database initialized successfully."