#!/bin/bash
set -e

# The dumps in /pg_data_prod were produced by `pg_dump` against a server
# where the superuser is named "postgres"; every object's OWNER TO clause
# refers to that role. Our cluster's bootstrap superuser is $POSTGRES_USER
# instead, so create a "postgres" role for those clauses to resolve to.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    CREATE ROLE postgres WITH SUPERUSER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "tiled_catalog" -f /pg_data_prod/tiled-db
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "data" -f /pg_data_prod/data
