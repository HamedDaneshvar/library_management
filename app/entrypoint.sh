#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database connection..."
while ! nc -z $POSTGRES_SERVER $POSTGRES_PORT; do
  sleep 0.1
done

# Run database migrations
alembic upgrade head

# Insert initial data
python initial_data.py

# Start the application
uvicorn --reload --host 0.0.0.0 --port 80 --log-level info "app.main:app"
