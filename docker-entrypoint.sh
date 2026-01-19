#! /usr/bin/env bash

# Run Alembic uprgade
alembic upgrade head

# Start the PolicyNest app
uvicorn app.main:app --host 0.0.0.0 --port 8000