# PostgreSQL Setup Guide for IPO Web App

## 🐘 Database Configuration

The project is now configured to use **PostgreSQL** with the following credentials:

- **Database Name**: `ipo_db`
- **Username**: `admin`
- **Password**: `admin`
- **Host**: `localhost`
- **Port**: `5432`

## 🚀 Quick Setup (Recommended)

### Step 1: Setup PostgreSQL Database
```bash
cd /home/vijay/PycharmProjects/ipo-web-app/backend
chmod +x setup_postgresql.sh
./setup_postgresql.sh
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
chmod +x init_db.sh
./init_db.sh
```

### Step 4: Run the Server
```bash
python manage.py runserver
```

## 🔧 Manual Setup (Alternative)

### 1. Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2. Start PostgreSQL Service
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 3. Create Database User
```bash
sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'admin';"
sudo -u postgres psql -c "ALTER USER admin CREATEDB;"
sudo -u postgres psql -c "ALTER USER admin WITH SUPERUSER;"
```

### 4. Create Database
```bash
sudo -u postgres createdb -O admin ipo_db
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ipo_db TO admin;"
```

### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Django Superuser
```bash
python manage.py createsuperuser
# Use: username=admin, password=admin
```

### 8. Start Development Server
```bash
python manage.py runserver
```

## 🔍 Verify Setup

### Test Database Connection
```bash
PGPASSWORD=admin psql -h localhost -U admin -d ipo_db -c "SELECT version();"
```

### Access Points
- **API Root**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Database**: Connect using any PostgreSQL client with the above credentials

## 🛠️ Troubleshooting

### PostgreSQL Service Issues
```bash
# Check service status
sudo systemctl status postgresql

# Restart service
sudo systemctl restart postgresql
```

### Connection Issues
```bash
# Check if PostgreSQL is listening
sudo netstat -plunt | grep postgres

# Check PostgreSQL configuration
sudo nano /etc/postgresql/*/main/postgresql.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

### Permission Issues
```bash
# Reset user permissions
sudo -u postgres psql -c "ALTER USER admin WITH SUPERUSER;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ipo_db TO admin;"
```

## 📊 Database Schema

The database includes the following tables:
- **Companies**: Company information and logos
- **IPOs**: IPO details, pricing, and status
- **Documents**: RHP and DRHP PDF files
- **Django Auth**: User authentication tables

All tables are created according to the project specifications with proper relationships and constraints.