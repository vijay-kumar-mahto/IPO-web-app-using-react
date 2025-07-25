#!/bin/bash

echo "🚀 Starting IPO Web Application..."
echo "===================================================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if service is running
is_service_running() {
    pgrep -f "$1" >/dev/null 2>&1
}

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Python
if ! command_exists python3; then
    echo -e "${RED}❌ Python3 is not installed. Please install Python3 first.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Python3 is available${NC}"
fi

# Check pip
if ! command_exists pip3; then
    echo -e "${RED}❌ pip3 is not installed. Please install pip3 first.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ pip3 is available${NC}"
fi

# Step 2: Setup PostgreSQL Database
echo ""
echo -e "${BLUE}🗄️  Setting up PostgreSQL database...${NC}"
cd backend
chmod +x init_db.sh
./init_db.sh

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database setup failed${NC}"
    exit 1
fi

# Step 3: Setup Python Virtual Environment (optional but recommended)
echo ""
echo -e "${BLUE}🐍 Setting up Python environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Step 4: Install Python dependencies
echo ""
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install Python dependencies${NC}"
    exit 1
fi

# Step 5: Run Django migrations
echo ""
echo -e "${BLUE}🔄 Setting up Django database...${NC}"
echo "Making migrations..."
python manage.py makemigrations
python manage.py makemigrations ipo_app
python manage.py makemigrations home
python manage.py makemigrations broker

echo "Applying migrations..."
python manage.py migrate

# Step 6: Create Django superuser
echo ""
echo -e "${BLUE}👤 Setting up Django superuser...${NC}"
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✅ Django superuser created (username: admin, password: admin)')
else:
    print('✅ Django superuser already exists')
"

# Step 7: Start Django development server in background
echo ""
echo -e "${BLUE}🚀 Starting Django development server...${NC}"
if is_service_running "manage.py runserver"; then
    echo -e "${YELLOW}⚠️  Django server is already running${NC}"
else
    nohup python manage.py runserver > django.log 2>&1 &
    DJANGO_PID=$!
    echo "Django server started with PID: $DJANGO_PID"

    # Wait for server to start
    echo "Waiting for server to start..."
    sleep 5

    # Check if server is running
    if curl -s http://localhost:8000/api/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Django server is running successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start Django server${NC}"
        echo "Check django.log for details"
        exit 1
    fi
fi

# Step 8: Setup frontend
echo ""
echo -e "${BLUE}🎨 Setting up frontend...${NC}"
cd ../frontend

# Check if we need to serve frontend
if command_exists python3; then
    echo "Starting frontend server..."
    echo -e "${YELLOW}💡 Frontend will be available at: http://localhost:8080${NC}"

    # Start frontend server in background
    nohup python3 -m http.server 8080 > frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "Frontend server started with PID: $FRONTEND_PID"
fi

# Final status
echo ""
echo "===================================================================================="
echo -e "${GREEN}🎉 IPO Web Application started successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Service Status:${NC}"
echo -e "   🔧 Backend API:  ${GREEN}http://localhost:8000/api/${NC}"
echo -e "   🎨 Frontend:     ${GREEN}http://localhost:8080${NC}"
echo -e "   🗄️  Database:    ${GREEN}PostgreSQL (ipo_db)${NC}"
echo -e "   👤 Admin User:   ${GREEN}admin / admin${NC}"
echo ""
echo -e "${BLUE}📁 Log Files:${NC}"
echo "   - Django: backend/django.log"
echo "   - Frontend: frontend/frontend.log"
echo ""
echo -e "${BLUE}🛑 To stop the services:${NC}"
echo "   pkill -f \"manage.py runserver\""
echo "   pkill -f \"python3 -m http.server\""
echo ""
echo -e "${YELLOW}📝 Note: Keep this terminal open or services will stop when you close it.${NC}"
echo "Press Ctrl+C to stop all services"

# Keep script running and handle Ctrl+C gracefully
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    pkill -f "manage.py runserver" 2>/dev/null
    pkill -f "python3 -m http.server" 2>/dev/null
    echo -e "${GREEN}✅ Services stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep the script running
echo "Services are running... Press Ctrl+C to stop"
while true; do
    sleep 1
done
