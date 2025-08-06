# 🌿 GreenAlpha User Manual & Setup Guide
## Complete Guide to Carbon Intelligence Platform

---

## 🚀 **Quick Start Guide**

### **Option 1: Instant Access (Recommended)**
```bash
# Navigate to the project directory
cd "/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/api"

# Start the server
python main.py

# Open your browser to: http://localhost:8000
```

### **Option 2: Docker Deployment**
```bash
# From the project root directory
cd "/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA"

# Build and start with Docker Compose
docker-compose up --build

# Access at: http://localhost:8000
```

---

## 🎯 **Platform Access Guide**

### **Main Portal**: http://localhost:8000
- **Auto-redirect**: Takes you to the platform selection page
- **Three platforms** available: Calculator, Dashboard, Analytics

### **Direct Platform Access**
- 🧮 **Calculator**: http://localhost:8000/static/simple.html
- 📊 **Dashboard**: http://localhost:8000/static/dashboard.html  
- 🔬 **Analytics**: http://localhost:8000/static/analytics.html
- 📖 **API Docs**: http://localhost:8000/docs

---

## 🧮 **Carbon Calculator User Guide**

### **Demo Scenarios (One-Click Testing)**
1. **📱 High-Impact Scenario**: Smartphone China→USA (Air Freight)
2. **💻 Eco-Friendly Scenario**: Laptop Germany→Japan (Sea Freight)  
3. **👕 Fashion Industry**: T-shirt India→UK (Sea Freight)

### **Manual Calculation Steps**
1. **Select Product**: Choose from dropdown (smartphone, laptop, t-shirt, etc.)
2. **Origin Country**: Select manufacturing location
3. **Destination Country**: Choose final delivery location
4. **Transport Mode**: Pick shipping method
   - Air Freight: Fast, high emissions
   - Sea Freight: Slow, low emissions  
   - Road Truck: Medium speed/emissions
   - Rail: Eco-friendly option
5. **Quantity**: Enter number of units
6. **Click Calculate**: Results in <500ms

### **Understanding Results**
```
Total Emissions: 78.0 kg CO₂e
├── Production: 75.9 kg (manufacturing)
└── Transportation: 2.0 kg (shipping)

Response Time: 45ms
Confidence: 90% (IPCC 2021 compliant)
```

---

## 📊 **Executive Dashboard Guide**

### **Main Features**
- **Real-time KPIs**: Carbon metrics and cost tracking
- **Interactive Charts**: Chart.js visualizations
- **Performance Monitoring**: Response times and system health
- **Export Functions**: CSV/JSON data download
- **Action Buttons**: Quick access to calculations

### **Dashboard Widgets**
1. **Header Metrics**: Key performance indicators
2. **Control Panel**: Calculation controls
3. **KPI Grid**: Business metrics overview
4. **Chart Containers**: Visual data representation
5. **Status Indicators**: System health monitoring

### **Export Functionality**
- **Generate Report**: Comprehensive analysis export
- **Export Data**: Raw data in CSV/JSON format
- **Performance Stats**: System metrics download

---

## 🔬 **Analytics Platform Guide**

### **Advanced Visualizations**
- **Global Heatmap**: World emissions visualization with D3.js
- **Time Series Analysis**: Historical trend tracking
- **Transport Analysis**: Route optimization insights
- **Sector Breakdown**: Industry-specific emissions
- **Arbitrage Charts**: Carbon trading opportunities

### **Interactive Features**
- **Zoom/Pan**: Navigate global maps
- **Hover Details**: Context-sensitive information
- **Filter Controls**: Customize data views
- **Animation Controls**: Time-series playback
- **Export Options**: High-resolution chart downloads

---

## 🛠️ **Technical Setup Instructions**

### **System Requirements**
- **Python**: 3.11+ required
- **RAM**: 2GB+ recommended
- **Storage**: 500MB for data and dependencies
- **Network**: Internet connection for real-time data

### **Installation Steps**

#### **1. Environment Setup**
```bash
# Ensure Python 3.11+ is installed
python --version

# Navigate to project directory
cd "/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/api"

# Install dependencies (if needed)
pip install -r requirements.txt
```

#### **2. Data Verification**
```bash
# Check data files exist
ls ../data/carbon_data.csv

# Verify data loading
python -c "from core.data_access import data_manager; import asyncio; asyncio.run(data_manager.ensure_initialized())"
```

#### **3. Server Start**
```bash
# Start development server
python main.py

# Server should show:
# "INFO: Uvicorn running on http://0.0.0.0:8000"
# "INFO: Carbon calculation engine initialized successfully"
```

#### **4. Health Check**
```bash
# Test API health
curl http://localhost:8000/health

# Should return: {"status": "healthy", ...}
```

---

## 🐳 **Docker Deployment Guide**

### **Development Mode**
```bash
# Start with live reload
docker-compose up --build

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### **Production Mode**
```bash
# Production deployment with Nginx
docker-compose --profile production up --build

# Scale API instances
docker-compose up --scale api=3

# Monitor health
docker-compose exec api curl localhost:8000/health
```

---

## 🔧 **API Integration Guide**

### **Basic API Usage**

#### **Health Check**
```bash
curl -X GET "http://localhost:8000/health"
```

#### **Carbon Calculation**
```bash
curl -X POST "http://localhost:8000/carbon/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "smartphone",
    "quantity": 1,
    "origin_country": "CHN",
    "destination_country": "USA",
    "transport_mode": "air_freight"
  }'
```

### **Python Integration Example**
```python
import requests

# Calculate carbon footprint
response = requests.post(
    'http://localhost:8000/carbon/calculate',
    json={
        'product_name': 'smartphone',
        'quantity': 1,
        'origin_country': 'CHN',
        'destination_country': 'USA',
        'transport_mode': 'air_freight'
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"Carbon footprint: {data['total_emissions_kg_co2e']:.1f} kg CO₂e")
    print(f"Cost impact: ${data['carbon_cost_usd']:.2f}")
else:
    print(f"Error: {response.status_code}")
```

### **JavaScript Integration Example**
```javascript
async function calculateCarbon() {
    const response = await fetch('http://localhost:8000/carbon/calculate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            product_name: 'smartphone',
            quantity: 1,
            origin_country: 'CHN',
            destination_country: 'USA',
            transport_mode: 'air_freight'
        })
    });
    
    const data = await response.json();
    console.log(`Carbon footprint: ${data.total_emissions_kg_co2e} kg CO₂e`);
}
```

---

## 🚨 **Troubleshooting Guide**

### **Common Issues**

#### **Server Won't Start**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing processes
pkill -f "python.*main"

# Restart server
python main.py
```

#### **404 Errors on Frontend**
- **Solution**: Use http://localhost:8000 (not direct HTML file access)
- **Alternative**: Access via http://localhost:8000/static/simple.html

#### **API Calculation Errors**
```bash
# Check system health
curl http://localhost:8000/health

# Verify data loading
python -c "from core.data_access import data_manager; print(data_manager.get_performance_stats())"
```

#### **Import Errors**
```bash
# Ensure you're in the correct directory
cd "/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/api"

# Check Python path
python -c "import sys; print(sys.path)"
```

### **Performance Issues**

#### **Slow Response Times**
- **Check**: System health endpoint for performance metrics
- **Solution**: Restart server if memory usage high
- **Monitor**: Response times should be <500ms

#### **Memory Usage**
```bash
# Monitor memory usage
docker stats (if using Docker)

# Restart services if needed
docker-compose restart api
```

---

## 📈 **Best Practices**

### **For End Users**
1. **Use Demo Scenarios**: Quick validation of system functionality
2. **Batch Calculations**: Use batch API for multiple calculations
3. **Export Results**: Save reports for compliance documentation
4. **Monitor Performance**: Check response times for optimal experience

### **For Developers**  
1. **API Documentation**: Always refer to /docs for latest endpoints
2. **Error Handling**: Implement proper try-catch for API calls
3. **Rate Limiting**: Respect API rate limits for production use
4. **Health Checks**: Monitor /health endpoint for system status

### **For System Administrators**
1. **Docker Deployment**: Use containerized deployment for production
2. **Health Monitoring**: Set up monitoring for /health endpoint
3. **Log Management**: Monitor application logs for issues
4. **Backup Strategy**: Regular backup of calculation results

---

## 🔒 **Security Considerations**

### **Development Environment**
- **CORS**: Restricted to localhost origins
- **Error Messages**: Detailed for debugging
- **Health Endpoint**: Exposed for monitoring

### **Production Environment**
- **API Keys**: Implement authentication (future enhancement)
- **Rate Limiting**: Prevent abuse (future enhancement)
- **HTTPS**: Use SSL certificates
- **Container Security**: Non-root user in Docker containers

---

## 📞 **Support Resources**

### **Documentation**
- **API Reference**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **System Health**: http://localhost:8000/health
- **Platform Info**: http://localhost:8000/api

### **File Locations**
- **Main Application**: `/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/api/`
- **Frontend Files**: `/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/api/static/`
- **Data Files**: `/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/data/`
- **Documentation**: `/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/docs/`

### **Quick Commands Reference**
```bash
# Start server
python main.py

# Check health
curl http://localhost:8000/health

# Test calculation
curl -X POST http://localhost:8000/carbon/calculate -H "Content-Type: application/json" -d '{"product_name":"smartphone","quantity":1,"origin_country":"CHN","destination_country":"USA","transport_mode":"air_freight"}'

# Docker deployment
docker-compose up --build

# View documentation
open http://localhost:8000/docs
```

---

## 🎉 **Success Indicators**

### **System is Working When:**
- ✅ Server starts with "Carbon calculation engine initialized successfully"
- ✅ Health endpoint returns status: "healthy"
- ✅ Frontend loads at http://localhost:8000
- ✅ Demo scenarios complete in <500ms
- ✅ All three platforms (Calculator, Dashboard, Analytics) accessible

### **Performance Targets**
- **Response Time**: <500ms for carbon calculations
- **System Health**: All components showing "healthy" status
- **Data Coverage**: 222 countries, 18,646+ emission records loaded
- **Accuracy**: 90%+ confidence scores on calculations

---

*Ready to revolutionize your carbon intelligence? Start with http://localhost:8000*