# IPO Dashboard Frontend

A modern, responsive web interface for displaying IPO (Initial Public Offering) data using vanilla HTML, CSS, and JavaScript.

## Features

### 📊 Dashboard Overview
- **Real-time Statistics**: Total IPOs, Open IPOs, and Upcoming IPOs counters
- **Beautiful UI**: Modern gradient design with glassmorphism effects
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### 🔍 Filtering & Search
- **Tab Navigation**: Filter IPOs by status (All, Upcoming, Open, Listed, Closed)
- **Search Functionality**: Search IPOs by company name or issue type
- **Sorting Options**: Sort by company name, open date, listing gain, or current return
- **Real-time Updates**: Instant filtering and searching with debounced input

### 📱 IPO Cards
- **Comprehensive Information**: Company name, status, price band, issue size, dates
- **Financial Metrics**: IPO price, listing gain, current return with color-coded indicators
- **Status Badges**: Color-coded status indicators for easy identification
- **Interactive Cards**: Hover effects and click-to-view details

### 🔍 Detailed View
- **Modal Interface**: Click any IPO card to view detailed information
- **Complete Data**: All available IPO information in an organized grid layout
- **Easy Navigation**: Close modal with ESC key or click outside

### 🎨 Visual Features
- **Gradient Backgrounds**: Beautiful color gradients throughout the interface
- **Smooth Animations**: Card hover effects, loading spinners, and transitions
- **Color-coded Gains**: Green for positive, red for negative, gray for neutral
- **Font Awesome Icons**: Professional icons throughout the interface

## File Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # Complete CSS styling with responsive design
├── script.js           # JavaScript functionality and API integration
└── README.md          # This documentation file
```

## API Integration

The frontend connects to the Django REST API backend:

- **Base URL**: `http://localhost:8000/api`
- **Main Endpoint**: `/ipos/` - Fetches all IPO data
- **Detail Endpoint**: `/ipos/{id}/` - Fetches specific IPO details

### API Data Structure

The frontend expects IPO objects with the following structure:
```json
{
  "ipo_id": 1,
  "company": {
    "company_id": 1,
    "company_name": "Company Name"
  },
  "status": "Open|Upcoming|Closed|Listed",
  "price_band": "₹100-120",
  "open_date": "2024-01-15",
  "close_date": "2024-01-18",
  "issue_size": "₹500 Cr",
  "issue_type": "Book Built",
  "listing_date": "2024-01-22",
  "ipo_price": 110.00,
  "listing_price": 125.50,
  "listing_gain": 14.09,
  "current_market_price": 130.00,
  "current_return": 18.18
}
```

## Usage

### Running the Frontend

1. **Start the Django Backend**:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Open the Frontend**:
   - Simply open `index.html` in any modern web browser
   - Or serve it using a local server:
     ```bash
     # Using Python
     cd frontend
     python -m http.server 8080
     
     # Using Node.js
     npx serve .
     ```

3. **Access the Dashboard**:
   - Direct file: `file:///path/to/frontend/index.html`
   - Local server: `http://localhost:8080`

### Navigation

1. **Browse IPOs**: Use the tab navigation to filter by status
2. **Search**: Type in the search box to find specific companies
3. **Sort**: Use the dropdown to sort IPOs by different criteria
4. **View Details**: Click any IPO card to see complete information
5. **Refresh**: Click the refresh button to reload data from the API

## Browser Compatibility

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

## Features in Detail

### Responsive Design
- **Mobile-first approach** with breakpoints at 768px and 480px
- **Flexible grid layouts** that adapt to screen size
- **Touch-friendly interface** with appropriate button sizes

### Error Handling
- **Network error handling** with user-friendly messages
- **Loading states** with animated spinners
- **Graceful degradation** when data is unavailable

### Performance
- **Debounced search** to reduce API calls
- **Efficient DOM updates** with minimal reflows
- **Optimized animations** using CSS transforms

### Accessibility
- **Keyboard navigation** support
- **Screen reader friendly** with proper ARIA labels
- **High contrast** color schemes for better visibility

## Customization

### Styling
- Modify `styles.css` to change colors, fonts, or layout
- CSS custom properties are used for easy theme customization
- Responsive breakpoints can be adjusted for different screen sizes

### Functionality
- Add new filter options in the JavaScript
- Implement additional sorting criteria
- Extend the modal with more detailed information

### API Configuration
- Change `API_BASE_URL` in `script.js` to point to different backend
- Modify data mapping if API structure changes
- Add authentication headers if required

## Future Enhancements

- 📈 **Charts and Graphs**: Add visual representations of IPO performance
- 🔔 **Real-time Updates**: WebSocket integration for live data
- 💾 **Offline Support**: Service worker for offline functionality
- 🎯 **Advanced Filters**: Date range, price range, and sector filters
- 📊 **Export Features**: Download IPO data as CSV or PDF
- 🌙 **Dark Mode**: Toggle between light and dark themes