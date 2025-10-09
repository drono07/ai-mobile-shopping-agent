#!/bin/bash

# Stop and remove existing container if it exists
docker stop mobile-shop-postgres 2>/dev/null || true
docker rm mobile-shop-postgres 2>/dev/null || true

# Start PostgreSQL with dummy credentials
docker run --name mobile-shop-postgres \
  -e POSTGRES_DB=mobile_shop_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_INITDB_ARGS="--auth-host=scram-sha-256 --auth-local=trust" \
  -p 5433:5432 \
  -d postgres:15

# Wait for PostgreSQL to start
sleep 5

# Grant superuser privileges
docker exec mobile-shop-postgres psql -U postgres -d mobile_shop_db -c "ALTER USER postgres CREATEDB SUPERUSER;"

echo "PostgreSQL started with dummy credentials:"
echo "Database: mobile_shop_db"
echo "User: postgres"
echo "Password: password"
echo "Port: 5432"
