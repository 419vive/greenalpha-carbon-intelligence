"""
Carbon Tax Cost Assessment Module
Evaluates carbon tax costs across multiple jurisdictions and policies
"""
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TaxJurisdiction(Enum):
    """Carbon tax jurisdictions"""
    EU_ETS = "EU ETS"  # EU Emissions Trading System
    EU_CBAM = "EU CBAM"  # Carbon Border Adjustment Mechanism
    UK_ETS = "UK ETS"  # UK Emissions Trading System
    US_RGGI = "US RGGI"  # Regional Greenhouse Gas Initiative
    CALIFORNIA_CTS = "California CTS"  # California Cap-and-Trade
    CANADA_FEDERAL = "Canada Federal"
    CHINA_ETS = "China ETS"
    JAPAN_TAX = "Japan Carbon Tax"
    SOUTH_KOREA_KETS = "South Korea K-ETS"
    NEW_ZEALAND_ETS = "New Zealand ETS"

@dataclass
class CarbonTaxPolicy:
    """Carbon tax policy details"""
    jurisdiction: TaxJurisdiction
    current_price_per_ton: float  # USD per ton CO2e
    effective_date: str
    coverage_sectors: List[str]
    exemption_threshold_tons: float
    compliance_deadline: str
    penalty_rate: float  # Multiplier for non-compliance
    forecast_2025_price: float
    forecast_2030_price: float

@dataclass
class TaxAssessmentResult:
    """Carbon tax assessment result"""
    total_tax_liability_usd: float
    breakdown_by_jurisdiction: Dict[str, float]
    applicable_policies: List[str]
    compliance_recommendations: List[str]
    potential_savings: float
    optimization_opportunities: List[Dict]
    risk_assessment: Dict[str, str]

class CarbonTaxAssessor:
    """Assesses carbon tax costs and compliance requirements"""
    
    def __init__(self):
        self.tax_policies = self._initialize_tax_policies()
        self.carbon_credits_market = self._initialize_carbon_credits()
        self.tax_optimization_strategies = self._load_optimization_strategies()
        
    def _initialize_tax_policies(self) -> Dict[TaxJurisdiction, CarbonTaxPolicy]:
        """Initialize carbon tax policies database"""
        policies = {
            TaxJurisdiction.EU_ETS: CarbonTaxPolicy(
                jurisdiction=TaxJurisdiction.EU_ETS,
                current_price_per_ton=85.0,
                effective_date="2023-01-01",
                coverage_sectors=["power", "manufacturing", "aviation", "maritime"],
                exemption_threshold_tons=10000,
                compliance_deadline="2024-04-30",
                penalty_rate=2.0,
                forecast_2025_price=95.0,
                forecast_2030_price=120.0
            ),
            TaxJurisdiction.EU_CBAM: CarbonTaxPolicy(
                jurisdiction=TaxJurisdiction.EU_CBAM,
                current_price_per_ton=80.0,
                effective_date="2023-10-01",
                coverage_sectors=["cement", "iron", "steel", "aluminum", "fertilizers", "electricity", "hydrogen"],
                exemption_threshold_tons=150,
                compliance_deadline="2024-01-31",
                penalty_rate=1.5,
                forecast_2025_price=90.0,
                forecast_2030_price=115.0
            ),
            TaxJurisdiction.UK_ETS: CarbonTaxPolicy(
                jurisdiction=TaxJurisdiction.UK_ETS,
                current_price_per_ton=75.0,
                effective_date="2021-01-01",
                coverage_sectors=["power", "manufacturing", "aviation"],
                exemption_threshold_tons=10000,
                compliance_deadline="2024-04-30",
                penalty_rate=2.0,
                forecast_2025_price=85.0,
                forecast_2030_price=100.0
            ),
            TaxJurisdiction.CALIFORNIA_CTS: CarbonTaxPolicy(
                jurisdiction=TaxJurisdiction.CALIFORNIA_CTS,
                current_price_per_ton=30.0,
                effective_date="2013-01-01",
                coverage_sectors=["power", "industrial", "transportation", "buildings"],
                exemption_threshold_tons=25000,
                compliance_deadline="2024-11-01",
                penalty_rate=1.5,
                forecast_2025_price=35.0,
                forecast_2030_price=50.0
            ),
            TaxJurisdiction.CANADA_FEDERAL: CarbonTaxPolicy(
                jurisdiction=TaxJurisdiction.CANADA_FEDERAL,
                current_price_per_ton=65.0,
                effective_date="2019-01-01",
                coverage_sectors=["all"],
                exemption_threshold_tons=50000,
                compliance_deadline="2024-06-30",
                penalty_rate=1.8,
                forecast_2025_price=75.0,
                forecast_2030_price=170.0
            ),
            TaxJurisdiction.CHINA_ETS: CarbonTaxPolicy(
                jurisdiction=TaxJurisdiction.CHINA_ETS,
                current_price_per_ton=10.0,
                effective_date="2021-07-16",
                coverage_sectors=["power", "petrochemical", "chemical", "building materials", "steel", "non-ferrous", "paper", "aviation"],
                exemption_threshold_tons=26000,
                compliance_deadline="2024-12-31",
                penalty_rate=1.3,
                forecast_2025_price=15.0,
                forecast_2030_price=25.0
            ),
            TaxJurisdiction.JAPAN_TAX: CarbonTaxPolicy(
                jurisdiction=TaxJurisdiction.JAPAN_TAX,
                current_price_per_ton=2.0,
                effective_date="2012-10-01",
                coverage_sectors=["all"],
                exemption_threshold_tons=100000,
                compliance_deadline="2024-03-31",
                penalty_rate=1.2,
                forecast_2025_price=3.0,
                forecast_2030_price=10.0
            )
        }
        return policies
    
    def _initialize_carbon_credits(self) -> Dict[str, Dict]:
        """Initialize carbon credits market data"""
        return {
            "voluntary_credits": {
                "reforestation": {"price_per_ton": 15.0, "availability": "high"},
                "renewable_energy": {"price_per_ton": 20.0, "availability": "medium"},
                "carbon_capture": {"price_per_ton": 50.0, "availability": "low"},
                "blue_carbon": {"price_per_ton": 25.0, "availability": "medium"}
            },
            "compliance_credits": {
                "EU_allowances": {"price_per_ton": 85.0, "availability": "high"},
                "California_allowances": {"price_per_ton": 30.0, "availability": "high"},
                "RGGI_allowances": {"price_per_ton": 15.0, "availability": "medium"}
            }
        }
    
    def _load_optimization_strategies(self) -> List[Dict]:
        """Load tax optimization strategies"""
        return [
            {
                "strategy": "Carbon Credits Purchase",
                "description": "Purchase voluntary carbon credits to offset emissions",
                "potential_savings_percent": 20,
                "implementation_complexity": "low"
            },
            {
                "strategy": "Supply Chain Optimization",
                "description": "Switch to lower-carbon suppliers and transport modes",
                "potential_savings_percent": 35,
                "implementation_complexity": "medium"
            },
            {
                "strategy": "Process Efficiency",
                "description": "Improve manufacturing processes to reduce emissions",
                "potential_savings_percent": 25,
                "implementation_complexity": "high"
            },
            {
                "strategy": "Renewable Energy Transition",
                "description": "Switch to renewable energy sources",
                "potential_savings_percent": 40,
                "implementation_complexity": "high"
            },
            {
                "strategy": "Carbon Capture Implementation",
                "description": "Install carbon capture technology",
                "potential_savings_percent": 50,
                "implementation_complexity": "very high"
            }
        ]
    
    def calculate_tax_liability(self,
                               emissions_kg_co2e: float,
                               origin_country: str,
                               destination_country: str,
                               product_category: str,
                               include_forecast: bool = True) -> TaxAssessmentResult:
        """Calculate carbon tax liability across jurisdictions"""
        
        emissions_tons = emissions_kg_co2e / 1000
        applicable_policies = self._identify_applicable_policies(
            origin_country, destination_country, product_category
        )
        
        breakdown = {}
        total_liability = 0.0
        recommendations = []
        optimization_opportunities = []
        
        for policy in applicable_policies:
            # Check if emissions exceed threshold
            if emissions_tons > policy.exemption_threshold_tons:
                taxable_emissions = emissions_tons - policy.exemption_threshold_tons
                tax_amount = taxable_emissions * policy.current_price_per_ton
                breakdown[policy.jurisdiction.value] = tax_amount
                total_liability += tax_amount
                
                # Add compliance recommendation
                recommendations.append(
                    f"File {policy.jurisdiction.value} compliance report by {policy.compliance_deadline}"
                )
                
                # Identify optimization opportunities
                if tax_amount > 10000:  # Significant tax liability
                    optimization_opportunities.append({
                        "jurisdiction": policy.jurisdiction.value,
                        "current_tax": tax_amount,
                        "potential_reduction": tax_amount * 0.3,
                        "strategy": "Consider carbon credits or process optimization"
                    })
        
        # Calculate potential savings
        potential_savings = self._calculate_savings_opportunities(
            emissions_tons, total_liability
        )
        
        # Risk assessment
        risk_assessment = self._assess_compliance_risks(
            emissions_tons, applicable_policies
        )
        
        # Add forecast if requested
        if include_forecast:
            forecast_2025 = self._calculate_future_liability(
                emissions_tons, applicable_policies, 2025
            )
            forecast_2030 = self._calculate_future_liability(
                emissions_tons, applicable_policies, 2030
            )
            
            recommendations.append(
                f"Projected 2025 liability: ${forecast_2025:,.2f} (increase of {((forecast_2025/total_liability - 1) * 100):.1f}%)"
            )
            recommendations.append(
                f"Projected 2030 liability: ${forecast_2030:,.2f} (increase of {((forecast_2030/total_liability - 1) * 100):.1f}%)"
            )
        
        return TaxAssessmentResult(
            total_tax_liability_usd=total_liability,
            breakdown_by_jurisdiction=breakdown,
            applicable_policies=[p.jurisdiction.value for p in applicable_policies],
            compliance_recommendations=recommendations,
            potential_savings=potential_savings,
            optimization_opportunities=optimization_opportunities,
            risk_assessment=risk_assessment
        )
    
    def _identify_applicable_policies(self,
                                     origin_country: str,
                                     destination_country: str,
                                     product_category: str) -> List[CarbonTaxPolicy]:
        """Identify which tax policies apply"""
        applicable = []
        
        # Map countries to jurisdictions
        country_to_jurisdiction = {
            "Germany": [TaxJurisdiction.EU_ETS, TaxJurisdiction.EU_CBAM],
            "France": [TaxJurisdiction.EU_ETS, TaxJurisdiction.EU_CBAM],
            "UK": [TaxJurisdiction.UK_ETS],
            "USA": [TaxJurisdiction.CALIFORNIA_CTS],
            "Canada": [TaxJurisdiction.CANADA_FEDERAL],
            "China": [TaxJurisdiction.CHINA_ETS],
            "Japan": [TaxJurisdiction.JAPAN_TAX],
            "Hamburg": [TaxJurisdiction.EU_ETS, TaxJurisdiction.EU_CBAM],
            "Los Angeles": [TaxJurisdiction.CALIFORNIA_CTS],
            "Shanghai": [TaxJurisdiction.CHINA_ETS],
            "Mumbai": [],  # India doesn't have carbon tax yet
            "Detroit": [],  # No specific state carbon tax
            "Stockholm": [TaxJurisdiction.EU_ETS]
        }
        
        # Check destination country policies (import taxes)
        dest_jurisdictions = country_to_jurisdiction.get(destination_country, [])
        for jurisdiction in dest_jurisdictions:
            if jurisdiction in self.tax_policies:
                policy = self.tax_policies[jurisdiction]
                # Check if product category is covered
                if self._is_product_covered(product_category, policy):
                    applicable.append(policy)
        
        # Check origin country policies (export/production taxes)
        origin_jurisdictions = country_to_jurisdiction.get(origin_country, [])
        for jurisdiction in origin_jurisdictions:
            if jurisdiction in self.tax_policies and jurisdiction not in dest_jurisdictions:
                policy = self.tax_policies[jurisdiction]
                if self._is_product_covered(product_category, policy):
                    applicable.append(policy)
        
        return applicable
    
    def _is_product_covered(self, product_category: str, policy: CarbonTaxPolicy) -> bool:
        """Check if product category is covered by policy"""
        if "all" in policy.coverage_sectors:
            return True
        
        # Map product categories to sectors
        category_to_sector = {
            "steel": ["manufacturing", "iron", "steel"],
            "aluminum": ["manufacturing", "aluminum", "non-ferrous"],
            "cement": ["cement", "building materials"],
            "electronics": ["manufacturing", "industrial"],
            "textiles": ["manufacturing", "industrial"],
            "chemicals": ["chemical", "petrochemical"],
            "general": ["manufacturing", "industrial"]
        }
        
        product_sectors = category_to_sector.get(product_category.lower(), ["manufacturing"])
        
        for sector in product_sectors:
            if any(sector in policy_sector for policy_sector in policy.coverage_sectors):
                return True
        
        return False
    
    def _calculate_savings_opportunities(self,
                                        emissions_tons: float,
                                        current_liability: float) -> float:
        """Calculate potential tax savings"""
        savings = 0.0
        
        # Carbon credits option
        voluntary_credit_price = self.carbon_credits_market["voluntary_credits"]["reforestation"]["price_per_ton"]
        credit_cost = emissions_tons * voluntary_credit_price
        
        if credit_cost < current_liability:
            savings = current_liability - credit_cost
        
        # Process optimization (assume 25% reduction possible)
        optimized_emissions = emissions_tons * 0.75
        optimized_liability = current_liability * 0.75
        optimization_savings = current_liability - optimized_liability
        
        return max(savings, optimization_savings)
    
    def _assess_compliance_risks(self,
                                emissions_tons: float,
                                policies: List[CarbonTaxPolicy]) -> Dict[str, str]:
        """Assess compliance risks"""
        risks = {}
        
        if emissions_tons > 100000:
            risks["level"] = "high"
            risks["description"] = "Very high emissions require immediate action"
        elif emissions_tons > 50000:
            risks["level"] = "medium"
            risks["description"] = "Significant emissions require monitoring"
        else:
            risks["level"] = "low"
            risks["description"] = "Emissions within manageable range"
        
        # Check for upcoming deadlines
        today = datetime.now()
        for policy in policies:
            deadline = datetime.strptime(policy.compliance_deadline, "%Y-%m-%d")
            days_until_deadline = (deadline - today).days
            
            if days_until_deadline < 30:
                risks["urgent_deadline"] = f"{policy.jurisdiction.value} deadline in {days_until_deadline} days"
        
        return risks
    
    def _calculate_future_liability(self,
                                   emissions_tons: float,
                                   policies: List[CarbonTaxPolicy],
                                   year: int) -> float:
        """Calculate future tax liability based on forecasts"""
        total_future_liability = 0.0
        
        for policy in policies:
            if emissions_tons > policy.exemption_threshold_tons:
                taxable_emissions = emissions_tons - policy.exemption_threshold_tons
                
                if year == 2025:
                    future_price = policy.forecast_2025_price
                elif year == 2030:
                    future_price = policy.forecast_2030_price
                else:
                    # Linear interpolation for other years
                    current_year = 2024
                    if year < 2025:
                        future_price = policy.current_price_per_ton
                    elif year < 2030:
                        years_from_2025 = year - 2025
                        price_increase_per_year = (policy.forecast_2030_price - policy.forecast_2025_price) / 5
                        future_price = policy.forecast_2025_price + (years_from_2025 * price_increase_per_year)
                    else:
                        # Assume continued growth after 2030
                        years_from_2030 = year - 2030
                        annual_growth = (policy.forecast_2030_price - policy.forecast_2025_price) / 5
                        future_price = policy.forecast_2030_price + (years_from_2030 * annual_growth)
                
                total_future_liability += taxable_emissions * future_price
        
        return total_future_liability
    
    def recommend_carbon_credits(self,
                                emissions_tons: float,
                                budget_usd: float) -> Dict[str, any]:
        """Recommend carbon credit purchase strategy"""
        recommendations = {
            "total_emissions_to_offset": emissions_tons,
            "budget": budget_usd,
            "recommended_mix": [],
            "total_cost": 0.0,
            "emissions_covered": 0.0
        }
        
        # Sort credits by price (cheapest first)
        credits = []
        for credit_type, details in self.carbon_credits_market["voluntary_credits"].items():
            credits.append({
                "type": credit_type,
                "price_per_ton": details["price_per_ton"],
                "availability": details["availability"]
            })
        
        credits.sort(key=lambda x: x["price_per_ton"])
        
        remaining_emissions = emissions_tons
        remaining_budget = budget_usd
        
        for credit in credits:
            if remaining_emissions <= 0 or remaining_budget <= 0:
                break
            
            # Calculate how much we can buy
            max_tons_by_budget = remaining_budget / credit["price_per_ton"]
            tons_to_buy = min(remaining_emissions, max_tons_by_budget)
            
            if tons_to_buy > 0:
                cost = tons_to_buy * credit["price_per_ton"]
                recommendations["recommended_mix"].append({
                    "credit_type": credit["type"],
                    "tons": tons_to_buy,
                    "cost": cost,
                    "price_per_ton": credit["price_per_ton"]
                })
                
                recommendations["total_cost"] += cost
                recommendations["emissions_covered"] += tons_to_buy
                remaining_emissions -= tons_to_buy
                remaining_budget -= cost
        
        recommendations["coverage_percentage"] = (recommendations["emissions_covered"] / emissions_tons) * 100
        recommendations["remaining_emissions"] = remaining_emissions
        
        return recommendations
    
    def analyze_arbitrage_opportunities(self,
                                       emissions_tons: float,
                                       jurisdictions: List[str]) -> List[Dict]:
        """Identify carbon credit arbitrage opportunities"""
        opportunities = []
        
        for jurisdiction in jurisdictions:
            if jurisdiction in ["EU ETS", "EU CBAM"]:
                compliance_price = self.tax_policies[TaxJurisdiction.EU_ETS].current_price_per_ton
                
                # Check voluntary credit prices
                for credit_type, details in self.carbon_credits_market["voluntary_credits"].items():
                    if details["price_per_ton"] < compliance_price * 0.7:  # 30% discount threshold
                        spread = compliance_price - details["price_per_ton"]
                        potential_profit = spread * emissions_tons
                        
                        opportunities.append({
                            "jurisdiction": jurisdiction,
                            "credit_type": credit_type,
                            "compliance_price": compliance_price,
                            "credit_price": details["price_per_ton"],
                            "spread": spread,
                            "potential_profit": potential_profit,
                            "risk_level": "medium" if details["availability"] == "high" else "high"
                        })
        
        # Sort by potential profit
        opportunities.sort(key=lambda x: x["potential_profit"], reverse=True)
        
        return opportunities[:5]  # Return top 5 opportunities