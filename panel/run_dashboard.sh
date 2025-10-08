#!/bin/bash
# GIFT Oceanographic Intelligence Platform - Startup Script

echo "🌊 Starting GIFT Oceanographic Intelligence Platform..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if data file exists
DATA_FILE="../data/GIFT_database_prepared.csv"
if [ ! -f "$DATA_FILE" ]; then
    echo "⚠️  WARNING: Data file not found at $DATA_FILE"
    echo "Please ensure GIFT_database_prepared.csv is in the correct location."
    echo ""
fi

# Run Streamlit app
echo "🚀 Launching dashboard..."
echo "=================================================="
echo ""
echo "📊 Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app/main.py
