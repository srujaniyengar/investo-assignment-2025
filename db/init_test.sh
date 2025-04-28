#!/bin/bash
set -e

# Ensure environment variables are set
if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_DB" ]; then
  echo "Error: POSTGRES_USER or POSTGRES_DB environment variable is not set."
  exit 1
fi

# Get the script's directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Check if the database exists and create it if not
echo "Checking if database '$POSTGRES_DB' exists..."
psql -U "$POSTGRES_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || psql -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB"

# Initialize the database by creating the table
echo "Creating the table..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$SCRIPT_DIR/create_table.sql"

# Load the data using the \copy command
if [ -f "$SCRIPT_DIR/data.csv" ]; then
  echo "Copying data from 'data.csv' into the database..."
  PGPASSWORD="$POSTGRES_PASSWORD" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy ticker_data(datetime, close, high, low, open, volume, instrument) FROM '$SCRIPT_DIR/data.csv' DELIMITER ',' CSV HEADER;"
  echo "Data copied successfully."
else
  echo "Error: 'data.csv' not found in the current directory."
  exit 1
fi

echo "Database initialized successfully."