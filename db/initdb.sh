#!/bin/bash
set -e

# Initialize the database by creating the table and copying the data
echo "Initializing the database..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /db/create_table.sql
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /db/cpy_data.sql
echo "Database initialized successfully."