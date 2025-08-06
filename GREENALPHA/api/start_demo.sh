#!/bin/bash

# GreenAlpha Carbon Calculator Demo Launcher
# This script starts the demo website for executives

echo "🌱 Starting GreenAlpha Carbon Calculator Demo..."
echo "⚡ Production-ready API with <500ms response time"
echo ""

# Kill any existing processes on port 8000
echo "🔄 Cleaning up any existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "No existing processes found"

# Start the server
echo "🚀 Starting server..."
cd "/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/api"
python main.py &

# Wait for server to start
echo "⏳ Waiting for server to initialize..."
sleep 5

# Check if server is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server is running successfully!"
    echo ""
    echo "🌐 Demo website: http://localhost:8000"
    echo "📚 API documentation: http://localhost:8000/docs"
    echo "🏥 Health check: http://localhost:8000/health"
    echo ""
    echo "📋 Quick test scenarios:"
    echo "   • Smartphone China→USA (Air freight)"
    echo "   • Laptop Germany→Japan (Sea freight)"  
    echo "   • T-shirt India→UK (Sea freight)"
    echo ""
    echo "🎯 Features:"
    echo "   • Real-time carbon calculations"
    echo "   • IPCC 2021 compliant methodology"
    echo "   • 222 countries supported"
    echo "   • Business ROI calculator"
    echo "   • Executive-ready visualizations"
    echo ""
    echo "Press Ctrl+C to stop the server"
    
    # Open browser if available
    if command -v open &> /dev/null; then
        echo "🔗 Opening demo in browser..."
        open http://localhost:8000
    fi
    
    # Keep script running
    wait
else
    echo "❌ Failed to start server"
    exit 1
fi