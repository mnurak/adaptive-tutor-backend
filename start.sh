#!/bin/bash

# Find and kill any old Gunicorn processes to ensure a clean start
echo "--- Stopping any running Gunicorn processes... ---"
pkill -f gunicorn

# Give the OS a moment to release the port
sleep 1

# Start the new Gunicorn server
echo "--- Starting new Gunicorn server... ---"
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000