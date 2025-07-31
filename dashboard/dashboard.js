// ShadowLens Dashboard JavaScript
let websiteHistory = [];
let filteredHistory = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔒 ShadowLens Dashboard: Initializing...');
    loadWebsiteHistory();
    setupEventListeners();
});

function setupEventListeners() {
    // Search functionality
    document.getElementById('search-box').addEventListener('input', function(e) {
        filterWebsites();
    });

    // Risk filter
    document.getElementById('risk-filter').addEventListener('change', function(e) {
        filterWebsites();
    });
}

function loadWebsiteHistory() {
    // Try to load from JSON file
    fetch('dashboard_data.json')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('No data file found');
            }
        })
        .then(data => {
            if (data && data.websiteHistory && data.websiteHistory.length > 0) {
                websiteHistory = data.websiteHistory;
                displayWebsites();
                updateStats();
                console.log('✅ Loaded real data from JSON file');
            } else {
                showEmptyState();
            }
        })
        .catch(error => {
            console.log('No saved data found, showing empty state');
            showEmptyState();
        });
}

function showEmptyState() {
    const websiteList = document.getElementById('website-list');
    websiteList.innerHTML = `
        <div class="no-data">
            <i class="fas fa-search"></i>
            <p>No website analyses yet</p>
            <p style="font-size: 0.9rem; margin-top: 10px; color: #718096;">
                Start analyzing websites with the test script to see data here
            </p>
        </div>
    `;
    
    // Reset stats to zero
    document.getElementById('total-websites').textContent = '0';
    document.getElementById('high-risk-count').textContent = '0';
    document.getElementById('safe-count').textContent = '0';
    document.getElementById('avg-risk-score').textContent = '0';
}

function displayWebsites() {
    const websiteList = document.getElementById('website-list');
    const searchTerm = document.getElementById('search-box').value.toLowerCase();
    const riskFilter = document.getElementById('risk-filter').value;

    // Filter websites
    filteredHistory = websiteHistory.filter(website => {
        const matchesSearch = website.url.toLowerCase().includes(searchTerm);
        const matchesRisk = riskFilter === 'all' || website.recommendation.toLowerCase() === riskFilter;
        return matchesSearch && matchesRisk;
    });

    if (filteredHistory.length === 0) {
        if (websiteHistory.length === 0) {
            showEmptyState();
        } else {
            websiteList.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-search"></i>
                    <p>No websites found matching your criteria</p>
                </div>
            `;
        }
        return;
    }

    // Sort by timestamp (newest first)
    filteredHistory.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    websiteList.innerHTML = filteredHistory.map(website => {
        const timeAgo = getTimeAgo(new Date(website.timestamp));
        const riskClass = getRiskClass(website.recommendation);
        
        return `
            <div class="website-item">
                <div class="website-header">
                    <div class="website-url">${website.url}</div>
                    <div class="risk-badge ${riskClass}">${website.recommendation}</div>
                </div>
                <div class="website-time">${timeAgo}</div>
                <div class="website-details">
                    <div class="detail-item">
                        <div class="detail-label">Risk Score</div>
                        <div class="detail-value">${website.riskScore}/10</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Threats</div>
                        <div class="detail-value">${website.privacyThreats ? website.privacyThreats.length : 0}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Forms</div>
                        <div class="detail-value">${website.forms || 0}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Sensitive Fields</div>
                        <div class="detail-value">${website.sensitiveFields || 0}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Verification</div>
                        <div class="detail-value">${website.verificationStatus || 'Unknown'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">SSL</div>
                        <div class="detail-value">${website.sslCertificate ? '✅' : '❌'}</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function getTimeAgo(date) {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    return `${Math.floor(diffInSeconds / 86400)}d ago`;
}

function getRiskClass(recommendation) {
    const risk = recommendation.toLowerCase();
    if (risk === 'safe') return 'risk-safe';
    if (risk === 'moderate') return 'risk-moderate';
    if (risk === 'caution') return 'risk-caution';
    if (risk === 'dangerous' || risk === 'high risk') return 'risk-dangerous';
    return 'risk-moderate';
}

function filterWebsites() {
    displayWebsites();
}

function updateStats() {
    const totalWebsites = websiteHistory.length;
    const highRiskCount = websiteHistory.filter(w => 
        w.recommendation === 'Dangerous' || w.recommendation === 'High Risk'
    ).length;
    const safeCount = websiteHistory.filter(w => w.recommendation === 'Safe').length;
    const avgRiskScore = totalWebsites > 0 ? 
        Math.round(websiteHistory.reduce((sum, w) => sum + (w.riskScore || 0), 0) / totalWebsites) : 0;

    document.getElementById('total-websites').textContent = totalWebsites;
    document.getElementById('high-risk-count').textContent = highRiskCount;
    document.getElementById('safe-count').textContent = safeCount;
    document.getElementById('avg-risk-score').textContent = avgRiskScore;
}

function refreshData() {
    console.log('🔄 Refreshing dashboard data...');
    loadWebsiteHistory();
}

function exportData() {
    if (websiteHistory.length === 0) {
        alert('No data to export. Start analyzing websites first.');
        return;
    }

    const data = {
        exportDate: new Date().toISOString(),
        totalWebsites: websiteHistory.length,
        websites: websiteHistory
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `shadowlens-export-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log('📊 Data exported successfully');
}

console.log('🔒 ShadowLens Dashboard: Ready! (Real Data Only)'); 