#!/bin/bash

echo "===================================================================================="
# PostgreSQL setup
echo "Setting up PostgreSQL database..."


# Install PostgreSQL if not already installed
echo ""
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL not found. Installing PostgreSQL..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
else
    echo "PostgreSQL is already installed"
fi

# Check if PostgreSQL is running
echo ""
if ! sudo systemctl is-active --quiet postgresql; then
    echo "Starting PostgreSQL service..."
    sudo systemctl start postgresql
else
    echo "PostgreSQL is already running"
fi

# Create database user 'admin' if it doesn't exist
echo ""
echo "Creating database user 'admin'..."
sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'admin';" 2>/dev/null || echo "User 'admin' already exists"

# Grant necessary privileges to admin user
echo ""
echo "Granting privileges to admin user..."
sudo -u postgres psql -c "ALTER USER admin CREATEDB;"
sudo -u postgres psql -c "ALTER USER admin WITH SUPERUSER;"

# Check if the database already exists
echo ""
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw ipo_db; then
    echo "Database 'ipo_db' already exists"
else
    echo "Creating database 'ipo_db'..."
    sudo -u postgres createdb -O admin ipo_db
    echo "Database created successfully"
fi

# Grant all privileges on database to admin user
echo ""
echo "Granting database privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ipo_db TO admin;" 2>/dev/null || echo "Privileges already granted"

# Test connection
echo ""
echo "Testing database connection..."
if PGPASSWORD=admin psql -h localhost -U admin -d ipo_db -c "SELECT version();" > /dev/null 2>&1; then
    echo "✅ Database connection successful!"
else
    echo "❌ Database connection failed!"
    exit 1
fi

echo ""
echo "🎉 Database initialization complete!"
echo "📊 Database Details:"
echo "  Type: PostgreSQL"
echo "  Host: localhost:5432"
echo "  Database: ipo_db"
echo "  User: admin"
echo "  Password: admin"
echo ""
echo "🚀 Ready to run: python manage.py runserver"
echo "===================================================================================="



