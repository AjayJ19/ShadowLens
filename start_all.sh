#!/bin/bash
echo "Starting ShadowLens..."

# Start backend in background
echo "Starting backend..."
./start_backend.sh &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start dashboard
echo "Starting dashboard..."
./start_dashboard.sh &
DASHBOARD_PID=$!

echo "ShadowLens started!"
echo "Backend: http://localhost:5000"
echo "Dashboard: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $DASHBOARD_PID; exit" INT
wait
