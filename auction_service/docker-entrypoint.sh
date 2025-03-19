#!/usr/bin/env bash
set -e

wait_for_db() {
  echo "Waiting for database at $DB_HOST:$DB_PORT..."
  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    echo "Database is not ready yet..."
    sleep 1
  done
  echo "Database is ready!"
}

wait_for_db

echo "Applying Alembic migrations..."
alembic upgrade head

echo "Starting AuctionService..."
exec uvicorn main:app --host 0.0.0.0 --port 8004 --reload
