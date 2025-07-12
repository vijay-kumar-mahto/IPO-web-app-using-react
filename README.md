# IPO Web Application

A web application for displaying IPO-related data with a React.js frontend and Django REST API backend.

## Project Structure

```
ipo-web-app/
├── backend/         # Django REST API
├── frontend/        # React.js frontend (to be developed)
```

## Backend Setup

### Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite for development)

### Installation

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
   - Username: admin
   - Password: admin (for development only)

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the admin panel at:
   ```
   http://127.0.0.1:8000/admin/
   ```

### API Endpoints

- Companies: `/api/companies/`
- IPOs: `/api/ipos/`
- Documents: `/api/documents/`
- Brokers: `/api/broker/brokers/`
- Home: `/api/home/`

#### Special IPO Endpoints

- Upcoming IPOs: `/api/ipos/upcoming/`
- Open IPOs: `/api/ipos/open/`
- Listed IPOs: `/api/ipos/listed/`

## Frontend Setup (To Be Developed)

The frontend will be developed using React.js and will consume the Django REST API.

## Database Schema

### Companies
- `company_id`: INT, PK, Auto-Increment
- `company_name`: VARCHAR(255), NOT NULL
- `company_logo`: VARCHAR(255) (URL/File path)

### IPOs
- `ipo_id`: INT, PK, Auto-Increment
- `company_id`: INT, FK → `Companies.company_id`
- `price_band`: VARCHAR(50)
- `open_date`: DATE
- `close_date`: DATE
- `issue_size`: VARCHAR(100)
- `issue_type`: VARCHAR(50)
- `listing_date`: DATE
- `status`: ENUM('Upcoming', 'Open', 'Closed', 'Listed')
- `ipo_price`: DECIMAL(10,2)
- `listing_price`: DECIMAL(10,2)
- `listing_gain`: DECIMAL(5,2)
- `current_market_price`: DECIMAL(10,2)
- `current_return`: DECIMAL(5,2)

### Documents
- `document_id`: INT, PK, Auto-Increment
- `ipo_id`: INT, FK → `IPOs.ipo_id`
- `rhp_pdf`: VARCHAR(255)
- `drhp_pdf`: VARCHAR(255)

### Brokers
- `broker_id`: INT, PK, Auto-Increment
- `broker_name`: VARCHAR(255), NOT NULL
- `broker_logo`: VARCHAR(255) (URL/File path)
- `website_url`: VARCHAR(255)
- `description`: TEXT
- `min_account_size`: DECIMAL(10,2)
- `account_opening_link`: VARCHAR(255)