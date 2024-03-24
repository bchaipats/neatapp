#!/bin/bash

# Drop and create table
export DB_CONNECTION_STRING="dbname=postgres user=postgres host=localhost password=postgres"
export MIGRATION_FP="migrations/table-creation.sql"
psql "$DB_CONNECTION_STRING" -c "DROP TABLE IF EXISTS neatapp;"
psql "$DB_CONNECTION_STRING" -f $MIGRATION_FP

# Clean up the mocked storage
export MOCKED_STORAGE="mocked_storage" # this directory is for demonstration purpose.
rm -rf MOCKED_STORAGE
