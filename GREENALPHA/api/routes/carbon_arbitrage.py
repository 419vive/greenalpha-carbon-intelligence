"""
API Endpoints for Carbon Arbitrage Analysis
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import asyncio

from api.core.carbon_arbitrage import CarbonArbitrageAnalyzer

router = APIRouter()
analyzer = CarbonArbitrageAnalyzer()

class ArbitrageRequest(BaseModel):
    """Request model for arbitrage analysis"""
    countries: Optional[List[str]] = Field(None, description="Specific countries to analyze")
    min_volume_threshold: float = Field(100000, description="Minimum volume threshold in tonnes")
    time_horizon_months: int = Field(12, description="Analysis time horizon in months")

@router.post("/arbitrage/credit-opportunities")
async def get_credit_opportunities(request: ArbitrageRequest):
    """
    Identify carbon credit generation opportunities
    """
    try:
        opportunities = await analyzer.identify_credit_generation_opportunities(
            request.min_volume_threshold
        )
        
        # Filter by countries if specified
        if request.countries:
            opportunities = [
                opp for opp in opportunities 
                if opp.country_code in request.countries
            ]
        
        formatted_opportunities = []
        for opp in opportunities:
            formatted_opportunities.append({
                "country_code": opp.country_code,
                "country_name": opp.country_name,
                "opportunity_type": opp.opportunity_type,
                "estimated_volume_tonnes": round(opp.estimated_volume_tonnes, 0),
                "price_differential": round(opp.price_differential, 2),
                "expected_roi_percent": round(opp.expected_roi_percent, 1),
                "risk_score": round(opp.risk_score, 1),
                "time_horizon_months": opp.time_horizon_months,
                "confidence_score": round(opp.confidence_score, 2)
            })
        
        return {
            "analysis_parameters": {
                "min_volume_threshold": request.min_volume_threshold,
                "countries_filter": request.countries,
                "time_horizon_months": request.time_horizon_months
            },
            "opportunities_found": len(formatted_opportunities),
            "total_estimated_volume": sum([opp["estimated_volume_tonnes"] for opp in formatted_opportunities]),
            "opportunities": formatted_opportunities
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Credit opportunity analysis failed: {str(e)}")

@router.get("/arbitrage/price-differentials")
async def get_price_differentials():
    """
    Identify profitable price differentials between carbon markets
    """
    try:
        differentials = analyzer.identify_price_differentials()
        
        return {
            "analysis_timestamp": "2025-08-06",
            "differentials_found": len(differentials),
            "best_opportunity": differentials[0] if differentials else None,
            "price_differentials": differentials
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price differential analysis failed: {str(e)}")

@router.get("/arbitrage/market-intelligence")
async def get_market_intelligence():
    """
    Get current carbon market intelligence and pricing
    """
    try:
        market_data = {}
        
        for market_name, price in analyzer.carbon_prices.items():
            intelligence = analyzer.market_intelligence.get(market_name)
            
            market_data[market_name] = {
                "current_price_usd_per_tonne": price,
                "price_trend_percent": intelligence.price_trend_percent if intelligence else 0,
                "volatility_index": intelligence.volatility_index if intelligence else 0.5,
                "market_depth": intelligence.market_depth if intelligence else "unknown",
                "regulatory_stability": intelligence.regulatory_stability if intelligence else "unknown"
            }
        
        return {
            "markets_analyzed": len(market_data),
            "highest_price": max(analyzer.carbon_prices.values()),
            "lowest_price": min(analyzer.carbon_prices.values()),
            "average_price": sum(analyzer.carbon_prices.values()) / len(analyzer.carbon_prices),
            "markets": market_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market intelligence retrieval failed: {str(e)}")

@router.post("/arbitrage/country-analysis/{country_code}")
async def analyze_country_emissions(
    country_code: str,
    years: int = Query(5, description="Number of years to analyze")
):
    """
    Analyze emission trends for a specific country
    """
    try:
        country_code = country_code.upper()
        
        trend_analysis = await analyzer.analyze_emission_trends(country_code, years)
        
        return {
            "country_code": country_code,
            "analysis_period_years": years,
            "trend_analysis": trend_analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Country analysis failed: {str(e)}")

@router.post("/arbitrage/comprehensive-report")
async def generate_comprehensive_report(request: ArbitrageRequest):
    """
    Generate comprehensive carbon arbitrage analysis report
    """
    try:
        report = await analyzer.generate_arbitrage_report()
        
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/arbitrage/regulatory-access")
async def get_regulatory_access():
    """
    Get regulatory access matrix for carbon markets by country
    """
    try:
        return {
            "regulatory_access_matrix": analyzer.regulatory_access,
            "available_markets": list(analyzer.carbon_prices.keys()),
            "note": "Shows which carbon markets each country can access for trading"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Regulatory access retrieval failed: {str(e)}")

@router.get("/arbitrage/market-opportunities-summary")
async def get_market_opportunities_summary():
    """
    Get high-level summary of current arbitrage opportunities
    """
    try:
        # Get quick summary data
        price_differentials = analyzer.identify_price_differentials()
        
        # Calculate summary metrics
        max_price_diff = max([diff["profit_per_tonne"] for diff in price_differentials]) if price_differentials else 0
        avg_roi = sum([diff["expected_roi_percent"] for diff in price_differentials]) / len(price_differentials) if price_differentials else 0
        
        return {
            "market_summary": {
                "total_markets": len(analyzer.carbon_prices),
                "price_range": {
                    "min": min(analyzer.carbon_prices.values()),
                    "max": max(analyzer.carbon_prices.values()),
                    "spread": max(analyzer.carbon_prices.values()) - min(analyzer.carbon_prices.values())
                },
                "arbitrage_opportunities": {
                    "price_differentials_found": len(price_differentials),
                    "max_profit_per_tonne": round(max_price_diff, 2),
                    "average_roi_percent": round(avg_roi, 1)
                }
            },
            "top_opportunities": price_differentials[:3],
            "market_status": "active" if price_differentials else "limited_opportunities"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market summary failed: {str(e)}")

@router.post("/arbitrage/roi-calculator")
async def calculate_arbitrage_roi(
    investment_amount: float = Query(..., description="Investment amount in USD"),
    target_market: str = Query(..., description="Target market for arbitrage"),
    volume_tonnes: float = Query(..., description="Volume in tonnes CO2"),
    holding_period_months: int = Query(6, description="Holding period in months")
):
    """
    Calculate ROI for specific arbitrage opportunity
    """
    try:
        if target_market not in analyzer.carbon_prices:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown market. Available: {list(analyzer.carbon_prices.keys())}"
            )
        
        target_price = analyzer.carbon_prices[target_market]
        
        # Simple ROI calculation
        gross_revenue = volume_tonnes * target_price
        transaction_costs = gross_revenue * 0.05  # 5% transaction costs
        net_revenue = gross_revenue - transaction_costs
        
        profit = net_revenue - investment_amount
        roi_percent = (profit / investment_amount) * 100 if investment_amount > 0 else 0
        
        # Annualized ROI
        annualized_roi = roi_percent * (12 / holding_period_months)
        
        return {
            "calculation_parameters": {
                "investment_amount": investment_amount,
                "target_market": target_market,
                "volume_tonnes": volume_tonnes,
                "holding_period_months": holding_period_months,
                "market_price": target_price
            },
            "financial_analysis": {
                "gross_revenue": round(gross_revenue, 2),
                "transaction_costs": round(transaction_costs, 2),
                "net_revenue": round(net_revenue, 2),
                "profit": round(profit, 2),
                "roi_percent": round(roi_percent, 1),
                "annualized_roi_percent": round(annualized_roi, 1)
            },
            "risk_assessment": {
                "market_volatility": analyzer.market_intelligence.get(target_market, {}).volatility_index or 0.5,
                "regulatory_stability": analyzer.market_intelligence.get(target_market, {}).regulatory_stability or "unknown"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ROI calculation failed: {str(e)}")