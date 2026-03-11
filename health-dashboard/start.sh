#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$SCRIPT_DIR/backend"
FRONTEND="$SCRIPT_DIR/frontend"

echo "🏥 Starting Health Dashboard..."

# Check .env exists
if [ ! -f "$BACKEND/.env" ]; then
  echo "⚠️  No .env found. Copying from .env.example..."
  cp "$BACKEND/.env.example" "$BACKEND/.env"
  echo "👉 Edit $BACKEND/.env with your credentials before continuing."
  exit 1
fi

# Backend
echo "🐍 Installing Python dependencies..."
cd "$BACKEND"
pip install -r requirements.txt -q

echo "🚀 Starting backend on http://localhost:8000 ..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Frontend
echo "📦 Installing frontend dependencies..."
cd "$FRONTEND"
npm install -q

echo "🌐 Starting frontend on http://localhost:5173 ..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Dashboard running at: http://localhost:5173"
echo "   (Access from phone:   http://$(hostname -I | awk '{print $1}'):5173)"
echo ""
echo "Press Ctrl+C to stop."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
