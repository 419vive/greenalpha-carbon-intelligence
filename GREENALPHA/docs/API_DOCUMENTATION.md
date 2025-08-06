# 🌿 GreenAlpha Carbon Intelligence API Documentation

## Overview
GreenAlpha provides a comprehensive RESTful API for carbon footprint calculations, supply chain optimization, and ESG analytics with sub-500ms response times and 95%+ accuracy.

## Base URL
- **Production**: `https://api.greenalpha.com`
- **Development**: `http://localhost:8000`

## Authentication
Currently open for demo purposes. Production deployment will require API keys.

## Quick Start

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

### 2. Calculate Carbon Footprint
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

---

## 🧮 Carbon Calculator Endpoints

### POST /carbon/calculate
Calculate comprehensive carbon footprint for product shipment.

**Request Body:**
```json
{
  "product_name": "smartphone",
  "quantity": 1,
  "origin_country": "CHN",
  "destination_country": "USA", 
  "transport_mode": "air_freight",
  "product_category": "electronics",
  "weight_kg": 0.5,
  "origin_latitude": 39.9042,
  "origin_longitude": 116.4074,
  "destination_latitude": 40.7128,
  "destination_longitude": -74.0060,
  "custom_emission_factors": {
    "production_override": 50.0
  }
}
```

**Response:**
```json
{
  "total_emissions_kg_co2e": 78.0,
  "production_emissions": 75.95,
  "transportation_emissions": 2.04,
  "scope_1_emissions": 9.85,
  "scope_2_emissions": 65.69,
  "scope_3_emissions": 2.44,
  "carbon_cost_usd": 1.50,
  "carbon_trading_opportunities": [
    {
      "market": "Voluntary Carbon Market",
      "price_per_tonne": 15.0,
      "liquidity": "medium",
      "potential_value": 1.17,
      "eligibility": ["global"]
    }
  ],
  "calculation_confidence": 90.0,
  "response_time_ms": 45.2,
  "calculation_method": "IPCC_2021_Guidelines",
  "data_sources": ["IPCC", "IEA", "EPA", "ISO14067"],
  "production_breakdown": {
    "total_production": 75.95,
    "energy_emissions": 65.69,
    "material_emissions": 0.41,
    "process_emissions": 9.85,
    "material_breakdown": {
      "steel": 0.057,
      "aluminum": 0.173,
      "plastic_pet": 0.176
    }
  },
  "transport_breakdown": {
    "total_transport": 2.04,
    "direct_transport": 1.63,
    "upstream_fuel": 0.33,
    "infrastructure": 0.08,
    "emission_factor_used": 0.602
  },
  "uncertainty_analysis": {
    "production_uncertainty": 15.5,
    "transport_uncertainty": 30.0,
    "overall_uncertainty": 18.2
  },
  "recommendations": [
    {
      "category": "Transportation",
      "action": "Consider sea freight instead of air freight",
      "potential_reduction": "Up to 95% transport emissions",
      "priority": "High"
    }
  ]
}
```

### POST /carbon/calculate/batch
Process multiple carbon calculations in parallel (max 100).

**Request:**
```json
{
  "calculations": [
    {
      "product_name": "smartphone",
      "quantity": 1,
      "origin_country": "CHN",
      "destination_country": "USA",
      "transport_mode": "air_freight"
    }
  ],
  "include_summary": true
}
```

### GET /carbon/factors/emission
Retrieve all available emission factors and their sources.

### GET /carbon/factors/country/{country_code}
Get country-specific emission factors and energy profiles.

---

## 🚛 Transport Optimization Endpoints

### POST /transport/optimize/route
Optimize transportation routes for minimal carbon footprint and cost.

**Request:**
```json
{
  "origin": "Shanghai, China",
  "destination": "Los Angeles, USA",
  "product_type": "electronics",
  "weight_kg": 1000,
  "delivery_urgency": "normal",
  "budget_constraint": 5000,
  "optimization_priority": "carbon_minimal"
}
```

**Response:**
```json
{
  "optimal_route": {
    "mode": "sea_freight",
    "total_distance_km": 11500,
    "estimated_days": 14,
    "total_cost_usd": 2800,
    "carbon_emissions_kg": 920,
    "route_segments": [
      {
        "from": "Shanghai Port",
        "to": "Long Beach Port",
        "mode": "sea_freight",
        "distance_km": 11200,
        "emissions_kg": 896
      }
    ]
  },
  "alternative_routes": [
    {
      "mode": "air_freight",
      "total_cost_usd": 8500,
      "carbon_emissions_kg": 11000,
      "estimated_days": 2
    }
  ],
  "carbon_savings": {
    "vs_air_freight": "92% reduction",
    "absolute_savings_kg": 10080
  }
}
```

---

## 🏭 Supplier Recommendations

### POST /recommendations/recommend/suppliers
Get AI-powered supplier recommendations based on carbon footprint and ESG scores.

**Request:**
```json
{
  "product_category": "electronics",
  "target_country": "USA",
  "volume_units": 1000,
  "budget_usd": 50000,
  "carbon_priority": 0.7,
  "cost_priority": 0.3,
  "required_certifications": ["ISO14001", "LEED"],
  "max_distance_km": 15000
}
```

---

## 💰 Carbon Arbitrage Analysis

### GET /arbitrage/comprehensive-report
Generate comprehensive carbon arbitrage opportunities report.

**Response:**
```json
{
  "market_analysis": {
    "total_opportunities": 1247,
    "total_potential_value_usd": 15600000,
    "avg_profit_margin_percent": 23.4,
    "risk_adjusted_return": 18.7
  },
  "top_opportunities": [
    {
      "opportunity_id": "ARB_001_EU_CA",
      "source_market": "EU_ETS",
      "destination_market": "CALIFORNIA",
      "price_differential_per_tonne": 12.50,
      "volume_available_tonnes": 50000,
      "profit_potential_usd": 625000,
      "risk_score": "medium",
      "execution_timeframe": "2-4 weeks"
    }
  ]
}
```

---

## 📊 Global Statistics

### GET /carbon/stats/global
Retrieve global carbon emission statistics and trends.

### GET /carbon/stats/performance
Get API performance metrics and system statistics.

---

## 🏥 Health & Monitoring

### GET /health
System health check with component status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-05T10:30:00.000Z",
  "service": "GreenAlpha Carbon Footprint Engine",
  "version": "1.0.0",
  "components": {
    "data_manager": {
      "status": "healthy",
      "countries_loaded": 222,
      "data_records": 18646
    },
    "calculation_engine": {
      "status": "healthy",
      "avg_response_time_ms": 45.2,
      "total_calculations": 1547
    }
  }
}
```

---

## 📝 Request/Response Formats

### Standard Error Response
```json
{
  "detail": "Error message description",
  "timestamp": "2025-01-05T10:30:00.000Z",
  "error_code": "INVALID_INPUT",
  "request_id": "req_12345"
}
```

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Internal Server Error
- `503` - Service Unavailable

---

## 🚀 Performance Specifications

- **Response Time**: <500ms for 95% of requests
- **Calculation Accuracy**: >95% (IPCC 2021 compliant)
- **Concurrent Users**: 100+ supported
- **Data Coverage**: 222 countries, 18,646 emission records
- **Uptime**: 99.9% availability target

---

## 🔧 Integration Examples

### Python
```python
import requests

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

data = response.json()
print(f"Carbon footprint: {data['total_emissions_kg_co2e']:.1f} kg CO₂e")
```

### JavaScript
```javascript
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
```

---

## 🛠️ Development Setup

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd greenalpha

# Install dependencies
pip install -r api/requirements.txt

# Start development server
python api/main.py

# API documentation available at:
# http://localhost:8000/docs
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.yml --profile production up
```

---

## 📞 Support & Resources

- **Interactive API Docs**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc` (ReDoc)
- **Health Status**: `/health`
- **System Info**: `/api`

For technical support or feature requests, please contact the development team or open an issue in the project repository.