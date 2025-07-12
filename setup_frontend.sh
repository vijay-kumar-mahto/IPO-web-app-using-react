#!/bin/bash

echo "🚀 Setting up IPO Dashboard Frontend..."

# Check if Django server is running
echo "🔍 Checking if Django server is running..."
if curl -s http://localhost:8000/api/ > /dev/null; then
    echo "✅ Django server is running!"
else
    echo "⚠️  Django server is not running. Starting it now..."
    echo "🔧 Running migrations..."
    python manage.py migrate
    
    echo "🚀 Starting Django development server..."
    python manage.py runserver &
    SERVER_PID=$!
    
    echo "⏳ Waiting for server to start..."
    sleep 5
    
    if curl -s http://localhost:8000/api/ > /dev/null; then
        echo "✅ Django server started successfully!"
        echo "📝 Server PID: $SERVER_PID"
    else
        echo "❌ Failed to start Django server"
        exit 1
    fi
fi

cd ..

echo ""
echo "🎉 Frontend setup complete!"
echo ""
echo "📂 Frontend files created in: ./frontend/"
echo "   - index.html      (Main dashboard)"
echo "   - launch.html     (Launcher with backend check)"
echo "   - styles.css      (Complete styling)"
echo "   - script.js       (JavaScript functionality)"
echo "   - README.md       (Documentation)"
echo ""
echo "🌐 How to access:"
echo "   1. Open frontend/launch.html in your browser"
echo "   2. Or directly open frontend/index.html"
echo "   3. Or serve with: cd frontend && python -m http.server 8080"
echo ""
echo "🔗 URLs:"
echo "   - Backend API: http://localhost:8000/api/"
echo "   - Frontend: file://$(pwd)/frontend/index.html"
echo ""