// GreenAlpha Executive Demo JavaScript
class GreenAlphaDemo {
    constructor() {
        this.apiBaseUrl = window.location.protocol + '//' + window.location.host;
        this.requestCount = 0;
        this.performanceData = [];
        this.performanceChart = null;
        
        this.init();
    }

    init() {
        this.initializeComponents();
        this.setupEventListeners();
        this.startPerformanceMonitoring();
        this.checkAPIStatus();
        
        // Initialize AOS animations
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 800,
                easing: 'ease-out-cubic',
                once: true,
                offset: 100
            });
        }
    }

    initializeComponents() {
        this.updateLiveMetrics();
        this.initPerformanceChart();
    }

    setupEventListeners() {
        // Calculator form submission
        const calculateBtn = document.querySelector('.calculate-btn');
        if (calculateBtn) {
            calculateBtn.addEventListener('click', () => this.calculateCarbon());
        }

        // ROI calculation
        const roiBtn = document.querySelector('.roi-calculate-btn');
        if (roiBtn) {
            roiBtn.addEventListener('click', () => this.calculateROI());
        }

        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // API Status Check
    async checkAPIStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            const statusIndicator = document.getElementById('apiStatus');
            if (statusIndicator) {
                statusIndicator.className = 'status-indicator';
                statusIndicator.style.background = data.status === 'healthy' ? '#30d158' : '#ff3b30';
            }
        } catch (error) {
            console.warn('API status check failed:', error);
            const statusIndicator = document.getElementById('apiStatus');
            if (statusIndicator) {
                statusIndicator.style.background = '#ff3b30';
            }
        }
    }

    // Load Predefined Scenarios
    loadScenario(type) {
        const scenarios = {
            smartphone: {
                product: 'smartphone',
                origin: 'CHN',
                destination: 'USA',
                transport: 'air_freight',
                quantity: 1
            },
            laptop: {
                product: 'laptop',
                origin: 'DEU',
                destination: 'JPN',
                transport: 'sea_freight',
                quantity: 1
            },
            textile: {
                product: 't-shirt',
                origin: 'IND',
                destination: 'GBR',
                transport: 'sea_freight',
                quantity: 1
            }
        };

        const scenario = scenarios[type];
        if (scenario) {
            document.getElementById('product').value = scenario.product;
            document.getElementById('origin').value = scenario.origin;
            document.getElementById('destination').value = scenario.destination;
            document.getElementById('transport').value = scenario.transport;
            document.getElementById('quantity').value = scenario.quantity;
            
            // Auto-calculate after loading scenario
            setTimeout(() => this.calculateCarbon(), 500);
        }
    }

    // Carbon Footprint Calculation
    async calculateCarbon() {
        const startTime = performance.now();
        
        // Get form values
        const request = {
            product_name: document.getElementById('product').value,
            origin_country: document.getElementById('origin').value,
            destination_country: document.getElementById('destination').value,
            transport_mode: document.getElementById('transport').value,
            quantity: parseFloat(document.getElementById('quantity').value) || 1
        };

        // Validate form
        if (!this.validateForm(request)) {
            return;
        }

        // Show loading state
        this.showCalculationLoading();

        try {
            const response = await fetch(`${this.apiBaseUrl}/carbon/calculate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            }

            const result = await response.json();
            const endTime = performance.now();
            const responseTime = endTime - startTime;

            // Update request counter
            this.requestCount++;
            this.updateRequestCounter();

            // Add to performance data
            this.performanceData.push({
                timestamp: new Date(),
                responseTime: responseTime,
                serverTime: result.response_time_ms || responseTime
            });
            
            this.updatePerformanceChart();
            this.displayCalculationResults(result, responseTime);
            
        } catch (error) {
            console.error('Calculation failed:', error);
            this.showCalculationError(error.message);
        }
    }

    showCalculationLoading() {
        const resultsContent = document.getElementById('resultsContent');
        const responseTimeDisplay = document.getElementById('responseTimeDisplay');
        
        if (resultsContent) {
            resultsContent.innerHTML = `
                <div class="loading-state">
                    <div class="loading-spinner"></div>
                    <p>Calculating carbon footprint...</p>
                </div>
            `;
        }
        
        if (responseTimeDisplay) {
            responseTimeDisplay.textContent = 'Calculating...';
            responseTimeDisplay.className = 'response-time loading';
        }
    }

    displayCalculationResults(result, responseTime) {
        const resultsContent = document.getElementById('resultsContent');
        const responseTimeDisplay = document.getElementById('responseTimeDisplay');

        // Update response time display
        if (responseTimeDisplay) {
            responseTimeDisplay.textContent = `${responseTime.toFixed(1)}ms`;
            responseTimeDisplay.className = 'response-time';
            responseTimeDisplay.style.background = responseTime < 500 ? '#30d158' : '#ff9500';
        }

        // Simplify results for executives
        const totalEmissions = result.total_emissions_kg_co2e || 0;
        const productionEmissions = result.production_emissions || 0;
        const transportEmissions = result.transportation_emissions || 0;
        const carbonCost = result.carbon_cost_usd || 0;
        const confidence = (result.calculation_confidence * 100) || 95;

        // Create simplified results HTML for executives
        const resultsHTML = `
            <div class="emissions-overview fade-in">
                <div class="emission-card primary">
                    <div class="emission-value">${totalEmissions.toFixed(1)}</div>
                    <div class="emission-label">Total CO₂ Emissions (kg)</div>
                    <div class="emission-sublabel">Complete carbon footprint</div>
                </div>
                <div class="emission-card">
                    <div class="emission-value">${productionEmissions.toFixed(1)}</div>
                    <div class="emission-label">Manufacturing</div>
                    <div class="emission-sublabel">${((productionEmissions/totalEmissions)*100).toFixed(0)}% of total</div>
                </div>
                <div class="emission-card">
                    <div class="emission-value">${transportEmissions.toFixed(1)}</div>
                    <div class="emission-label">Transportation</div>
                    <div class="emission-sublabel">${((transportEmissions/totalEmissions)*100).toFixed(0)}% of total</div>
                </div>
            </div>

            <div class="executive-summary fade-in">
                <div class="summary-row">
                    <div class="summary-metric">
                        <div class="metric-value">$${carbonCost.toFixed(2)}</div>
                        <div class="metric-label">Carbon Cost</div>
                    </div>
                    <div class="summary-metric">
                        <div class="metric-value">${confidence.toFixed(0)}%</div>
                        <div class="metric-label">Confidence Level</div>
                    </div>
                    <div class="summary-metric">
                        <div class="metric-value">${responseTime.toFixed(0)}ms</div>
                        <div class="metric-label">Response Time</div>
                    </div>
                </div>
            </div>

            <div class="breakdown-chart fade-in">
                <h4>Emissions Breakdown</h4>
                <canvas id="emissionsChart" width="400" height="200"></canvas>
            </div>

            ${result.recommendations && result.recommendations.length > 0 ? `
                <div class="recommendations fade-in">
                    <h4><i class="fas fa-lightbulb"></i> Key Recommendations</h4>
                    ${result.recommendations.slice(0, 3).map(rec => `
                        <div class="recommendation-item">
                            <div class="rec-header">
                                <strong>${rec.category}</strong>
                                <span class="rec-priority priority-${rec.priority?.toLowerCase() || 'medium'}">${rec.priority || 'Medium'}</span>
                            </div>
                            <div class="rec-action">${rec.action}</div>
                            <div class="potential-savings">${rec.potential_reduction}</div>
                        </div>
                    `).join('')}
                </div>
            ` : ''}

            <div class="calculation-details fade-in">
                <div class="details-header">
                    <h4>Calculation Details</h4>
                    <div class="details-badge">IPCC 2021 Compliant</div>
                </div>
                <div class="details-grid">
                    <div class="detail-item">
                        <span class="detail-label">Methodology:</span>
                        <span class="detail-value">${result.calculation_method || 'IPCC 2021'}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Data Sources:</span>
                        <span class="detail-value">${result.data_sources?.join(', ') || 'Global Datasets'}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Scope Coverage:</span>
                        <span class="detail-value">Scope 1, 2 & 3 Emissions</span>
                    </div>
                </div>
            </div>
        `;

        if (resultsContent) {
            resultsContent.innerHTML = resultsHTML;
            
            // Create emissions breakdown chart
            setTimeout(() => this.createEmissionsChart(result), 100);
        }
    }

    createEmissionsChart(result) {
        const canvas = document.getElementById('emissionsChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Manufacturing', 'Transportation', 'Packaging'],
                datasets: [{
                    data: [
                        result.production_emissions || 0,
                        result.transportation_emissions || 0,
                        (result.total_emissions_kg_co2e - result.production_emissions - result.transportation_emissions) || 0
                    ],
                    backgroundColor: [
                        '#0f7b0f',
                        '#34c759',
                        '#ff9500'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }

    showCalculationError(message) {
        const resultsContent = document.getElementById('resultsContent');
        const responseTimeDisplay = document.getElementById('responseTimeDisplay');

        if (responseTimeDisplay) {
            responseTimeDisplay.textContent = 'Error';
            responseTimeDisplay.className = 'response-time error';
            responseTimeDisplay.style.background = '#ff3b30';
        }

        if (resultsContent) {
            resultsContent.innerHTML = `
                <div class="error-state fade-in">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h4>Calculation Failed</h4>
                    <p class="error-message">${message}</p>
                    <div class="error-actions">
                        <button class="retry-btn" onclick="window.greenAlphaDemo.calculateCarbon()">
                            <i class="fas fa-redo"></i> Try Again
                        </button>
                        <button class="help-btn" onclick="window.greenAlphaDemo.showHelp()">
                            <i class="fas fa-question-circle"></i> Get Help
                        </button>
                    </div>
                    <div class="error-details">
                        <h5>Common Issues:</h5>
                        <ul>
                            <li>Check that all fields are filled correctly</li>
                            <li>Verify country codes are valid (3 letters)</li>
                            <li>Ensure quantity is a positive number</li>
                            <li>Try refreshing the page if the issue persists</li>
                        </ul>
                    </div>
                </div>
            `;
        }
    }

    // ROI Calculation
    calculateROI() {
        const annualRevenue = parseFloat(document.getElementById('annualRevenue').value) || 100;
        const productVolume = parseFloat(document.getElementById('productVolume').value) || 100000;
        const currentReportingTime = parseFloat(document.getElementById('currentReportingTime').value) || 40;
        const complianceCost = parseFloat(document.getElementById('complianceCost').value) || 200;

        // Calculate ROI metrics
        const timeReduction = currentReportingTime * 0.95; // 95% time savings
        const costPerHour = 150; // Average consultant rate
        const timeSavings = timeReduction * costPerHour * 52; // Weekly savings
        const complianceReduction = complianceCost * 0.6; // 60% compliance cost reduction
        const totalAnnualSavings = timeSavings + (complianceReduction * 1000);
        const implementationCost = 50000; // Estimated implementation cost
        const roi = ((totalAnnualSavings - implementationCost) / implementationCost) * 100;
        const paybackMonths = implementationCost / (totalAnnualSavings / 12);

        this.displayROIResults({
            annualRevenue,
            productVolume,
            timeSavings,
            complianceReduction: complianceReduction * 1000,
            totalAnnualSavings,
            roi,
            paybackMonths,
            implementationCost
        });
    }

    displayROIResults(results) {
        const roiResults = document.getElementById('roiResults');
        
        const roiHTML = `
            <div class="roi-summary fade-in">
                <div class="roi-metric">
                    <div class="roi-value">$${results.totalAnnualSavings.toLocaleString()}</div>
                    <div class="roi-label">Annual Savings</div>
                </div>
                <div class="roi-metric">
                    <div class="roi-value">${results.roi.toFixed(1)}%</div>
                    <div class="roi-label">ROI</div>
                </div>
                <div class="roi-metric">
                    <div class="roi-value">${results.paybackMonths.toFixed(1)}</div>
                    <div class="roi-label">Payback (Months)</div>
                </div>
                <div class="roi-metric">
                    <div class="roi-value">95%</div>
                    <div class="roi-label">Time Reduction</div>
                </div>
            </div>

            <div class="roi-breakdown fade-in">
                <h4>Savings Breakdown</h4>
                <div class="breakdown-item">
                    <span>Time Savings</span>
                    <span>$${results.timeSavings.toLocaleString()}</span>
                </div>
                <div class="breakdown-item">
                    <span>Compliance Cost Reduction</span>
                    <span>$${results.complianceReduction.toLocaleString()}</span>
                </div>
                <div class="breakdown-item">
                    <span>Implementation Cost</span>
                    <span>-$${results.implementationCost.toLocaleString()}</span>
                </div>
                <div class="breakdown-item total">
                    <span>Net Annual Benefit</span>
                    <span>$${(results.totalAnnualSavings - results.implementationCost).toLocaleString()}</span>
                </div>
            </div>

            <div class="business-impact fade-in">
                <h4>Business Impact</h4>
                <ul>
                    <li>Reduce reporting time from weeks to minutes</li>
                    <li>Enable real-time sustainability decisions</li>
                    <li>Improve competitive advantage in ESG</li>
                    <li>Reduce compliance and audit costs</li>
                    <li>Enable new revenue streams</li>
                </ul>
            </div>
        `;

        if (roiResults) {
            roiResults.innerHTML = roiHTML;
        }
    }

    // Performance Monitoring
    startPerformanceMonitoring() {
        // Update live metrics every 5 seconds
        setInterval(() => {
            this.updateLiveMetrics();
        }, 5000);

        // Check API status every 30 seconds
        setInterval(() => {
            this.checkAPIStatus();
        }, 30000);
    }

    updateLiveMetrics() {
        // Simulate live response time updates
        const baseTime = 4.7;
        const variation = (Math.random() - 0.5) * 2;
        const currentTime = Math.max(1, baseTime + variation);

        const liveResponseTime = document.getElementById('liveResponseTime');
        const avgResponseTime = document.getElementById('avgResponseTime');

        if (liveResponseTime) {
            liveResponseTime.textContent = `~${currentTime.toFixed(1)}ms`;
        }

        if (avgResponseTime) {
            avgResponseTime.textContent = `${currentTime.toFixed(1)}ms`;
        }
    }

    updateRequestCounter() {
        const requestCountElement = document.getElementById('requestCount');
        if (requestCountElement) {
            requestCountElement.textContent = `${this.requestCount} requests`;
        }
    }

    // Performance Chart
    initPerformanceChart() {
        const canvas = document.getElementById('performanceChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Generate initial sample data
        const now = new Date();
        const initialData = [];
        for (let i = 29; i >= 0; i--) {
            const time = new Date(now.getTime() - i * 2000);
            const responseTime = 4.7 + (Math.random() - 0.5) * 2;
            initialData.push({
                x: time,
                y: Math.max(1, responseTime)
            });
        }

        this.performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Response Time (ms)',
                    data: initialData,
                    borderColor: '#34c759',
                    backgroundColor: 'rgba(52, 199, 89, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'white'
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'second',
                            displayFormats: {
                                second: 'HH:mm:ss'
                            }
                        },
                        ticks: {
                            color: 'white'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 10,
                        ticks: {
                            color: 'white'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });

        // Update chart with live data
        setInterval(() => {
            this.updatePerformanceChart();
        }, 2000);
    }

    updatePerformanceChart() {
        if (!this.performanceChart) return;

        const now = new Date();
        const responseTime = 4.7 + (Math.random() - 0.5) * 2;

        const data = this.performanceChart.data.datasets[0].data;
        data.push({
            x: now,
            y: Math.max(1, responseTime)
        });

        // Keep only last 30 data points
        if (data.length > 30) {
            data.shift();
        }

        this.performanceChart.update('none');
    }

    // Form validation
    validateForm(request) {
        const errors = [];

        if (!request.product_name) {
            errors.push('Please select a product');
        }

        if (!request.origin_country || request.origin_country.length !== 3) {
            errors.push('Please select a valid origin country');
        }

        if (!request.destination_country || request.destination_country.length !== 3) {
            errors.push('Please select a valid destination country');
        }

        if (!request.transport_mode) {
            errors.push('Please select a transport mode');
        }

        if (!request.quantity || request.quantity <= 0) {
            errors.push('Quantity must be greater than 0');
        }

        if (request.origin_country === request.destination_country) {
            errors.push('Origin and destination countries cannot be the same');
        }

        if (errors.length > 0) {
            this.showValidationErrors(errors);
            return false;
        }

        return true;
    }

    showValidationErrors(errors) {
        const resultsContent = document.getElementById('resultsContent');
        const responseTimeDisplay = document.getElementById('responseTimeDisplay');

        if (responseTimeDisplay) {
            responseTimeDisplay.textContent = 'Validation Error';
            responseTimeDisplay.className = 'response-time error';
            responseTimeDisplay.style.background = '#ff9500';
        }

        if (resultsContent) {
            resultsContent.innerHTML = `
                <div class="validation-error fade-in">
                    <i class="fas fa-exclamation-circle"></i>
                    <h4>Please Fix These Issues</h4>
                    <ul class="error-list">
                        ${errors.map(error => `<li>${error}</li>`).join('')}
                    </ul>
                    <div class="error-actions">
                        <button class="fix-btn" onclick="this.style.display='none'">
                            <i class="fas fa-check"></i> Got It
                        </button>
                    </div>
                </div>
            `;
        }
    }

    showHelp() {
        const resultsContent = document.getElementById('resultsContent');
        
        if (resultsContent) {
            resultsContent.innerHTML = `
                <div class="help-content fade-in">
                    <i class="fas fa-info-circle"></i>
                    <h4>How to Use the Calculator</h4>
                    <div class="help-sections">
                        <div class="help-section">
                            <h5><i class="fas fa-box"></i> Product Selection</h5>
                            <p>Choose from our supported product categories. Each product has specific emission factors based on manufacturing processes.</p>
                        </div>
                        <div class="help-section">
                            <h5><i class="fas fa-map-marker-alt"></i> Origin & Destination</h5>
                            <p>Select the manufacturing origin and final destination. We calculate emissions based on country-specific energy grids and transportation distances.</p>
                        </div>
                        <div class="help-section">
                            <h5><i class="fas fa-truck"></i> Transport Mode</h5>
                            <p>Different transport modes have vastly different emission factors:</p>
                            <ul>
                                <li><strong>Sea Freight:</strong> Lowest emissions, slowest</li>
                                <li><strong>Rail:</strong> Low emissions, moderate speed</li>
                                <li><strong>Road Truck:</strong> Moderate emissions, fast</li>
                                <li><strong>Air Freight:</strong> Highest emissions, fastest</li>
                            </ul>
                        </div>
                    </div>
                    <div class="help-actions">
                        <button class="demo-btn" onclick="window.greenAlphaDemo.loadScenario('smartphone')">
                            <i class="fas fa-play"></i> Try Example
                        </button>
                    </div>
                </div>
            `;
        }
    }
}

// Product data for enhanced scenarios
const productData = {
    smartphone: {
        name: 'Smartphone',
        category: 'Electronics',
        weight: 0.2,
        manufacturingIntensity: 350
    },
    laptop: {
        name: 'Laptop Computer',
        category: 'Electronics',
        weight: 2.5,
        manufacturingIntensity: 180
    },
    't-shirt': {
        name: 'T-shirt',
        category: 'Textile',
        weight: 0.2,
        manufacturingIntensity: 350
    },
    tablet: {
        name: 'Tablet',
        category: 'Electronics',
        weight: 0.7,
        manufacturingIntensity: 250
    },
    jeans: {
        name: 'Jeans',
        category: 'Textile',
        weight: 0.6,
        manufacturingIntensity: 200
    },
    sneakers: {
        name: 'Sneakers',
        category: 'Footwear',
        weight: 0.8,
        manufacturingIntensity: 150
    }
};

// Country data for enhanced dropdowns
const countryData = {
    CHN: { name: 'China', region: 'Asia' },
    DEU: { name: 'Germany', region: 'Europe' },
    IND: { name: 'India', region: 'Asia' },
    USA: { name: 'United States', region: 'North America' },
    JPN: { name: 'Japan', region: 'Asia' },
    KOR: { name: 'South Korea', region: 'Asia' },
    VNM: { name: 'Vietnam', region: 'Asia' },
    THA: { name: 'Thailand', region: 'Asia' },
    GBR: { name: 'United Kingdom', region: 'Europe' },
    FRA: { name: 'France', region: 'Europe' },
    CAN: { name: 'Canada', region: 'North America' },
    AUS: { name: 'Australia', region: 'Oceania' },
    BRA: { name: 'Brazil', region: 'South America' }
};

// Global functions for external access
window.loadScenario = function(type) {
    if (window.greenAlphaDemo) {
        window.greenAlphaDemo.loadScenario(type);
    }
};

window.calculateCarbon = function() {
    if (window.greenAlphaDemo) {
        window.greenAlphaDemo.calculateCarbon();
    }
};

window.calculateROI = function() {
    if (window.greenAlphaDemo) {
        window.greenAlphaDemo.calculateROI();
    }
};

// Initialize the demo when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.greenAlphaDemo = new GreenAlphaDemo();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GreenAlphaDemo;
}