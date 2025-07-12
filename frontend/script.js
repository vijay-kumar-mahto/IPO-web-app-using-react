// Global variables
let allIpos = [];
let filteredIpos = [];
let currentTab = 'all';

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const ipoGrid = document.getElementById('ipoGrid');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const noResults = document.getElementById('noResults');
const searchInput = document.getElementById('searchInput');
const sortSelect = document.getElementById('sortSelect');
const refreshBtn = document.getElementById('refreshBtn');
const modal = document.getElementById('ipoModal');
const modalTitle = document.getElementById('modalTitle');
const modalBody = document.getElementById('modalBody');

// Statistics elements
const totalIposEl = document.getElementById('totalIpos');
const openIposEl = document.getElementById('openIpos');
const upcomingIposEl = document.getElementById('upcomingIpos');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadIPOData();
});

// Event Listeners
function initializeEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.getAttribute('data-tab');
            switchTab(tab);
        });
    });

    // Search functionality
    searchInput.addEventListener('input', debounce(handleSearch, 300));

    // Sort functionality
    sortSelect.addEventListener('change', handleSort);

    // Refresh button
    refreshBtn.addEventListener('click', function() {
        this.querySelector('i').style.animation = 'spin 1s linear infinite';
        loadIPOData().finally(() => {
            this.querySelector('i').style.animation = '';
        });
    });

    // Modal close events
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
}

// API Functions
async function loadIPOData() {
    try {
        showLoading();
        hideError();
        
        const response = await fetch(`${API_BASE_URL}/ipos/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        allIpos = data.results || data; // Handle both paginated and non-paginated responses
        
        updateStatistics();
        filterAndDisplayIPOs();
        
    } catch (error) {
        console.error('Error loading IPO data:', error);
        showError(`Failed to load IPO data: ${error.message}`);
    } finally {
        hideLoading();
    }
}

async function loadIPODetails(ipoId) {
    try {
        const response = await fetch(`${API_BASE_URL}/ipos/${ipoId}/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error loading IPO details:', error);
        throw error;
    }
}

// UI Functions
function showLoading() {
    loading.style.display = 'block';
    ipoGrid.style.display = 'none';
    noResults.style.display = 'none';
}

function hideLoading() {
    loading.style.display = 'none';
    ipoGrid.style.display = 'grid';
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function updateStatistics() {
    const total = allIpos.length;
    const open = allIpos.filter(ipo => ipo.status === 'Open').length;
    const upcoming = allIpos.filter(ipo => ipo.status === 'Upcoming').length;
    
    animateNumber(totalIposEl, total);
    animateNumber(openIposEl, open);
    animateNumber(upcomingIposEl, upcoming);
}

function animateNumber(element, targetNumber) {
    const startNumber = parseInt(element.textContent) || 0;
    const duration = 1000;
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentNumber = Math.floor(startNumber + (targetNumber - startNumber) * progress);
        element.textContent = currentNumber;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// Tab and Filter Functions
function switchTab(tab) {
    currentTab = tab;
    
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
    
    filterAndDisplayIPOs();
}

function filterAndDisplayIPOs() {
    let filtered = [...allIpos];
    
    // Filter by tab
    if (currentTab !== 'all') {
        filtered = filtered.filter(ipo => ipo.status.toLowerCase() === currentTab.toLowerCase());
    }
    
    // Filter by search
    const searchTerm = searchInput.value.toLowerCase().trim();
    if (searchTerm) {
        filtered = filtered.filter(ipo => 
            ipo.company.company_name.toLowerCase().includes(searchTerm) ||
            (ipo.issue_type && ipo.issue_type.toLowerCase().includes(searchTerm))
        );
    }
    
    // Sort
    const sortBy = sortSelect.value;
    filtered.sort((a, b) => {
        switch (sortBy) {
            case 'company_name':
                return a.company.company_name.localeCompare(b.company.company_name);
            case 'open_date':
                return new Date(b.open_date || 0) - new Date(a.open_date || 0);
            case 'listing_gain':
                return (b.listing_gain || 0) - (a.listing_gain || 0);
            case 'current_return':
                return (b.current_return || 0) - (a.current_return || 0);
            default:
                return 0;
        }
    });
    
    filteredIpos = filtered;
    displayIPOs(filteredIpos);
}

function handleSearch() {
    filterAndDisplayIPOs();
}

function handleSort() {
    filterAndDisplayIPOs();
}

// Display Functions
function displayIPOs(ipos) {
    if (ipos.length === 0) {
        ipoGrid.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }
    
    ipoGrid.style.display = 'grid';
    noResults.style.display = 'none';
    
    ipoGrid.innerHTML = ipos.map(ipo => createIPOCard(ipo)).join('');
    
    // Add click listeners to cards
    document.querySelectorAll('.ipo-card').forEach(card => {
        card.addEventListener('click', function() {
            const ipoId = this.getAttribute('data-ipo-id');
            showIPODetails(ipoId);
        });
    });
}

function createIPOCard(ipo) {
    const statusClass = `status-${ipo.status.toLowerCase()}`;
    const listingGainClass = getGainClass(ipo.listing_gain);
    const currentReturnClass = getGainClass(ipo.current_return);
    
    return `
        <div class="ipo-card" data-ipo-id="${ipo.ipo_id}">
            <div class="ipo-header">
                <div class="company-info">
                    <h3>${ipo.company.company_name}</h3>
                    <div class="company-id">ID: ${ipo.company.company_id}</div>
                </div>
                <div class="status-badge ${statusClass}">
                    ${ipo.status}
                </div>
            </div>
            
            <div class="ipo-details">
                <div class="detail-item">
                    <div class="detail-label">Price Band</div>
                    <div class="detail-value">${ipo.price_band || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Issue Size</div>
                    <div class="detail-value">${ipo.issue_size || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Open Date</div>
                    <div class="detail-value">${formatDate(ipo.open_date)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Close Date</div>
                    <div class="detail-value">${formatDate(ipo.close_date)}</div>
                </div>
            </div>
            
            <div class="price-info">
                <div class="price-item">
                    <div class="price-label">IPO Price</div>
                    <div class="price-value">₹${formatPrice(ipo.ipo_price)}</div>
                </div>
                <div class="price-item">
                    <div class="price-label">Listing Gain</div>
                    <div class="price-value ${listingGainClass}">
                        ${formatPercentage(ipo.listing_gain)}
                    </div>
                </div>
                <div class="price-item">
                    <div class="price-label">Current Return</div>
                    <div class="price-value ${currentReturnClass}">
                        ${formatPercentage(ipo.current_return)}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Modal Functions
async function showIPODetails(ipoId) {
    try {
        modalTitle.textContent = 'Loading...';
        modalBody.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading IPO details...</p></div>';
        modal.style.display = 'block';
        
        const ipoDetails = await loadIPODetails(ipoId);
        
        modalTitle.textContent = `${ipoDetails.company.company_name} IPO Details`;
        modalBody.innerHTML = createIPODetailsHTML(ipoDetails);
        
    } catch (error) {
        modalTitle.textContent = 'Error';
        modalBody.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <span>Failed to load IPO details: ${error.message}</span>
            </div>
        `;
    }
}

function createIPODetailsHTML(ipo) {
    const statusClass = `status-${ipo.status.toLowerCase()}`;
    const listingGainClass = getGainClass(ipo.listing_gain);
    const currentReturnClass = getGainClass(ipo.current_return);
    
    return `
        <div class="modal-detail-grid">
            <div class="modal-detail-item">
                <div class="detail-label">Company Name</div>
                <div class="detail-value">${ipo.company.company_name}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Status</div>
                <div class="detail-value">
                    <span class="status-badge ${statusClass}">${ipo.status}</span>
                </div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Price Band</div>
                <div class="detail-value">${ipo.price_band || 'N/A'}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Issue Size</div>
                <div class="detail-value">${ipo.issue_size || 'N/A'}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Issue Type</div>
                <div class="detail-value">${ipo.issue_type || 'N/A'}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Open Date</div>
                <div class="detail-value">${formatDate(ipo.open_date)}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Close Date</div>
                <div class="detail-value">${formatDate(ipo.close_date)}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Listing Date</div>
                <div class="detail-value">${formatDate(ipo.listing_date)}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">IPO Price</div>
                <div class="detail-value">₹${formatPrice(ipo.ipo_price)}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Listing Price</div>
                <div class="detail-value">₹${formatPrice(ipo.listing_price)}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Current Market Price</div>
                <div class="detail-value">₹${formatPrice(ipo.current_market_price)}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Listing Gain</div>
                <div class="detail-value ${listingGainClass}">
                    ${formatPercentage(ipo.listing_gain)}
                </div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Current Return</div>
                <div class="detail-value ${currentReturnClass}">
                    ${formatPercentage(ipo.current_return)}
                </div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Created At</div>
                <div class="detail-value">${formatDateTime(ipo.created_at)}</div>
            </div>
            <div class="modal-detail-item">
                <div class="detail-label">Updated At</div>
                <div class="detail-value">${formatDateTime(ipo.updated_at)}</div>
            </div>
        </div>
    `;
}

function closeModal() {
    modal.style.display = 'none';
}

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateTimeString) {
    if (!dateTimeString) return 'N/A';
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatPrice(price) {
    if (price === null || price === undefined) return 'N/A';
    return parseFloat(price).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function formatPercentage(percentage) {
    if (percentage === null || percentage === undefined) return 'N/A';
    const value = parseFloat(percentage);
    const sign = value > 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
}

function getGainClass(value) {
    if (value === null || value === undefined) return 'gain-neutral';
    const numValue = parseFloat(value);
    if (numValue > 0) return 'gain-positive';
    if (numValue < 0) return 'gain-negative';
    return 'gain-neutral';
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Global functions for HTML onclick events
window.closeModal = closeModal;
window.hideError = hideError;

