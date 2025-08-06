"""
Carbon Arbitrage Analysis Engine
Identifies profitable carbon credit trading opportunities based on emission patterns and market data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import asyncio
from .data_access import data_manager

@dataclass
class ArbitrageOpportunity:
    """Carbon arbitrage opportunity"""
    country_code: str
    country_name: str
    opportunity_type: str  # "credits_generation", "price_differential", "regulatory_gap"
    estimated_volume_tonnes: float
    price_differential: float
    expected_roi_percent: float
    risk_score: float  # 0-10, lower is better
    time_horizon_months: int
    confidence_score: float  # 0-1, higher is better
    
@dataclass 
class MarketIntelligence:
    """Market intelligence for carbon trading"""
    current_price_usd_per_tonne: float
    price_trend_percent: float  # 3-month trend
    volatility_index: float  # 0-1
    market_depth: str  # "thin", "moderate", "deep"
    regulatory_stability: str  # "stable", "changing", "uncertain"

class CarbonArbitrageAnalyzer:
    """
    Advanced carbon arbitrage opportunity identification and analysis
    """
    
    def __init__(self):
        # Current carbon credit prices by market (USD/tonne)
        self.carbon_prices = {
            "EU_ETS": 85.50,
            "CALIFORNIA": 28.75,
            "RGGI": 14.20,
            "KOREA": 22.10,
            "QUEBEC": 26.30,
            "VOLUNTARY": 15.80,
            "AVIATION": 90.20,
            "ARTICLE_6": 45.60
        }
        
        # Market characteristics
        self.market_intelligence = {
            "EU_ETS": MarketIntelligence(85.50, 12.5, 0.35, "deep", "stable"),
            "CALIFORNIA": MarketIntelligence(28.75, -5.2, 0.28, "moderate", "stable"),
            "RGGI": MarketIntelligence(14.20, 18.7, 0.45, "moderate", "stable"),
            "KOREA": MarketIntelligence(22.10, 8.3, 0.52, "thin", "changing"),
            "VOLUNTARY": MarketIntelligence(15.80, 25.1, 0.78, "thin", "uncertain")
        }
        
        # Country regulatory frameworks and carbon market access
        self.regulatory_access = {
            "USA": ["CALIFORNIA", "RGGI", "VOLUNTARY"],
            "DEU": ["EU_ETS", "VOLUNTARY", "ARTICLE_6"],
            "GBR": ["EU_ETS", "VOLUNTARY", "ARTICLE_6"], 
            "FRA": ["EU_ETS", "VOLUNTARY", "ARTICLE_6"],
            "CHN": ["VOLUNTARY", "ARTICLE_6"],
            "JPN": ["VOLUNTARY", "ARTICLE_6"],
            "CZE": ["EU_ETS", "VOLUNTARY"],
            "UKR": ["VOLUNTARY", "ARTICLE_6"],
            "IND": ["VOLUNTARY", "ARTICLE_6"],
            "BRA": ["VOLUNTARY", "ARTICLE_6"]
        }
        
    async def analyze_emission_trends(self, country_code: str, years: int = 5) -> Dict:
        """Analyze emission trends for arbitrage potential"""
        await data_manager.ensure_initialized()
        
        # Get recent emission history
        current_year = 2017  # Latest year in dataset
        start_year = current_year - years
        
        history = await data_manager.get_emissions_history(
            country_code, start_year, current_year
        )
        
        if len(history) < 3:
            return {"trend": "insufficient_data", "arbitrage_potential": 0}
        
        # Calculate trend metrics
        emissions_data = [(point.year, point.emissions_tonnes) for point in history]
        emissions_data.sort()
        
        years_list = [x[0] for x in emissions_data]
        emissions_list = [x[1] for x in emissions_data]
        
        # Linear regression for trend
        if len(emissions_list) >= 2:
            x = np.array(years_list)
            y = np.array(emissions_list)
            
            # Calculate trend
            trend_slope = np.polyfit(x, y, 1)[0]
            trend_percent = (trend_slope / np.mean(y)) * 100
            
            # Calculate volatility
            year_changes = [
                (emissions_list[i] - emissions_list[i-1]) / emissions_list[i-1] * 100
                for i in range(1, len(emissions_list))
            ]
            volatility = np.std(year_changes) if year_changes else 0
            
            # Recent momentum (last 2 years vs previous)
            if len(emissions_list) >= 4:
                recent_avg = np.mean(emissions_list[-2:])
                previous_avg = np.mean(emissions_list[-4:-2])
                momentum = (recent_avg - previous_avg) / previous_avg * 100
            else:
                momentum = trend_percent
                
            return {
                "trend_slope": trend_slope,
                "trend_percent": trend_percent,
                "volatility": volatility,
                "momentum": momentum,
                "latest_emissions": emissions_list[-1],
                "arbitrage_potential": self._calculate_arbitrage_potential(
                    trend_percent, volatility, momentum
                )
            }
        
        return {"trend": "calculation_error", "arbitrage_potential": 0}
    
    def _calculate_arbitrage_potential(
        self, 
        trend_percent: float, 
        volatility: float, 
        momentum: float
    ) -> float:
        """Calculate arbitrage potential score (0-10)"""
        
        # Declining emissions = positive for credit generation
        trend_score = max(0, -trend_percent / 5)  # Convert negative trend to positive score
        
        # Lower volatility = better predictability
        volatility_score = max(0, 5 - volatility / 2)
        
        # Strong negative momentum = good for credits
        momentum_score = max(0, -momentum / 3)
        
        # Weighted combination
        potential = (0.4 * trend_score + 0.3 * volatility_score + 0.3 * momentum_score)
        return min(10, potential)
    
    async def identify_credit_generation_opportunities(
        self, 
        min_volume_threshold: float = 100000  # tonnes
    ) -> List[ArbitrageOpportunity]:
        """Identify countries with strong carbon credit generation potential"""
        
        await data_manager.ensure_initialized()
        opportunities = []
        
        # Analyze all countries with sufficient data
        for country_code, profile in data_manager.country_profiles.items():
            if profile.total_emissions < min_volume_threshold:
                continue
                
            try:
                trend_analysis = await self.analyze_emission_trends(country_code, 5)
                
                if trend_analysis["arbitrage_potential"] >= 5:  # Good potential threshold
                    
                    # Estimate credit volume (assume 50% of emission reduction can be credited)
                    if trend_analysis["trend_percent"] < -2:  # At least 2% annual decline
                        annual_reduction = abs(trend_analysis["latest_emissions"] * 
                                             trend_analysis["trend_percent"] / 100)
                        potential_credits = annual_reduction * 0.5  # Conservative estimate
                        
                        # Calculate expected value and ROI
                        available_markets = self.regulatory_access.get(country_code, ["VOLUNTARY"])
                        best_market_price = max([
                            self.carbon_prices[market] for market in available_markets
                            if market in self.carbon_prices
                        ])
                        
                        # Risk assessment
                        risk_score = self._assess_risk(
                            country_code, 
                            trend_analysis["volatility"],
                            available_markets
                        )
                        
                        # ROI calculation (assume 30% transaction costs)
                        gross_value = potential_credits * best_market_price
                        net_value = gross_value * 0.7
                        estimated_cost = potential_credits * 5  # $5/tonne development cost
                        roi = ((net_value - estimated_cost) / estimated_cost) * 100
                        
                        if roi > 15:  # Minimum 15% ROI threshold
                            opportunities.append(ArbitrageOpportunity(
                                country_code=country_code,
                                country_name=profile.name,
                                opportunity_type="credits_generation",
                                estimated_volume_tonnes=potential_credits,
                                price_differential=best_market_price - 5,  # vs development cost
                                expected_roi_percent=roi,
                                risk_score=risk_score,
                                time_horizon_months=12,
                                confidence_score=min(1.0, trend_analysis["arbitrage_potential"] / 10)
                            ))
                        
            except Exception as e:
                continue  # Skip countries with data issues
        
        # Sort by expected ROI
        opportunities.sort(key=lambda x: x.expected_roi_percent, reverse=True)
        return opportunities[:10]  # Top 10 opportunities
    
    def identify_price_differentials(self) -> List[Dict]:
        """Identify profitable price differentials between carbon markets"""
        
        differentials = []
        markets = list(self.carbon_prices.keys())
        
        for i, market_a in enumerate(markets):
            for market_b in markets[i+1:]:
                price_a = self.carbon_prices[market_a]
                price_b = self.carbon_prices[market_b]
                
                # Calculate potential profit (assume 10% transaction costs)
                if price_a > price_b:
                    profit_per_tonne = (price_a - price_b) * 0.9 - price_b * 0.1
                    source_market = market_b
                    target_market = market_a
                else:
                    profit_per_tonne = (price_b - price_a) * 0.9 - price_a * 0.1
                    source_market = market_a
                    target_market = market_b
                
                if profit_per_tonne > 5:  # Minimum $5/tonne profit
                    roi = (profit_per_tonne / min(price_a, price_b)) * 100
                    
                    # Risk assessment based on market characteristics
                    source_intel = self.market_intelligence.get(source_market)
                    target_intel = self.market_intelligence.get(target_market)
                    
                    risk_score = self._assess_cross_market_risk(source_intel, target_intel)
                    
                    differentials.append({
                        "source_market": source_market,
                        "target_market": target_market,
                        "source_price": min(price_a, price_b),
                        "target_price": max(price_a, price_b),
                        "profit_per_tonne": profit_per_tonne,
                        "expected_roi_percent": roi,
                        "risk_score": risk_score,
                        "regulatory_complexity": self._assess_regulatory_complexity(
                            source_market, target_market
                        )
                    })
        
        # Sort by profit potential
        differentials.sort(key=lambda x: x["profit_per_tonne"], reverse=True)
        return differentials
    
    def _assess_risk(
        self, 
        country_code: str, 
        volatility: float, 
        available_markets: List[str]
    ) -> float:
        """Assess risk score for carbon credit opportunity (0-10, lower is better)"""
        
        # Base country risk (simplified scoring)
        country_risk_scores = {
            "USA": 2, "DEU": 1, "GBR": 2, "FRA": 1, "JPN": 2, "CAN": 2,
            "CHN": 5, "IND": 6, "BRA": 5, "RUS": 7, "UKR": 8, "CZE": 3
        }
        
        country_risk = country_risk_scores.get(country_code, 5)  # Default moderate risk
        
        # Volatility risk
        volatility_risk = min(3, volatility / 10)  # Cap at 3 points
        
        # Market access risk
        market_risk = 3 - min(2, len(available_markets) - 1)  # More markets = less risk
        
        # Regulatory risk
        regulatory_risk = 2 if "EU_ETS" in available_markets else 3
        
        total_risk = country_risk + volatility_risk + market_risk + regulatory_risk
        return min(10, max(0, total_risk))
    
    def _assess_cross_market_risk(
        self, 
        source_intel: Optional[MarketIntelligence], 
        target_intel: Optional[MarketIntelligence]
    ) -> float:
        """Assess risk for cross-market arbitrage"""
        
        if not source_intel or not target_intel:
            return 8.0  # High risk if no intelligence
        
        # Volatility risk
        avg_volatility = (source_intel.volatility_index + target_intel.volatility_index) / 2
        volatility_risk = avg_volatility * 3
        
        # Market depth risk
        depth_scores = {"deep": 0, "moderate": 1, "thin": 3}
        depth_risk = (
            depth_scores.get(source_intel.market_depth, 2) + 
            depth_scores.get(target_intel.market_depth, 2)
        )
        
        # Regulatory risk
        reg_scores = {"stable": 0, "changing": 2, "uncertain": 4}
        reg_risk = max(
            reg_scores.get(source_intel.regulatory_stability, 2),
            reg_scores.get(target_intel.regulatory_stability, 2)
        )
        
        total_risk = volatility_risk + depth_risk + reg_risk
        return min(10, max(0, total_risk))
    
    def _assess_regulatory_complexity(self, market_a: str, market_b: str) -> str:
        """Assess regulatory complexity for cross-market trades"""
        
        # Simplified complexity matrix
        if "EU_ETS" in [market_a, market_b] and "CALIFORNIA" in [market_a, market_b]:
            return "high"
        elif "VOLUNTARY" in [market_a, market_b]:
            return "low"
        elif market_a.startswith("ARTICLE") or market_b.startswith("ARTICLE"):
            return "very_high"
        else:
            return "moderate"
    
    async def generate_arbitrage_report(self) -> Dict:
        """Generate comprehensive arbitrage analysis report"""
        
        # Credit generation opportunities
        credit_opportunities = await self.identify_credit_generation_opportunities()
        
        # Price differential opportunities
        price_differentials = self.identify_price_differentials()
        
        # Market summary
        total_opportunity_value = sum([
            opp.estimated_volume_tonnes * opp.price_differential 
            for opp in credit_opportunities
        ])
        
        best_credit_opportunity = credit_opportunities[0] if credit_opportunities else None
        best_price_differential = price_differentials[0] if price_differentials else None
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "market_overview": {
                "total_markets_analyzed": len(self.carbon_prices),
                "highest_price_market": max(self.carbon_prices.items(), key=lambda x: x[1]),
                "lowest_price_market": min(self.carbon_prices.items(), key=lambda x: x[1]),
                "average_market_price": np.mean(list(self.carbon_prices.values()))
            },
            "credit_generation": {
                "opportunities_found": len(credit_opportunities),
                "total_estimated_value_usd": total_opportunity_value,
                "best_opportunity": {
                    "country": best_credit_opportunity.country_name if best_credit_opportunity else None,
                    "roi_percent": best_credit_opportunity.expected_roi_percent if best_credit_opportunity else 0,
                    "volume_tonnes": best_credit_opportunity.estimated_volume_tonnes if best_credit_opportunity else 0
                } if best_credit_opportunity else None,
                "opportunities": [
                    {
                        "country": opp.country_name,
                        "country_code": opp.country_code,
                        "volume_tonnes": opp.estimated_volume_tonnes,
                        "roi_percent": opp.expected_roi_percent,
                        "risk_score": opp.risk_score,
                        "confidence": opp.confidence_score
                    } for opp in credit_opportunities[:5]
                ]
            },
            "price_arbitrage": {
                "differentials_found": len(price_differentials),
                "best_opportunity": best_price_differential,
                "opportunities": price_differentials[:5]
            },
            "recommendations": {
                "immediate_actions": self._generate_action_recommendations(
                    credit_opportunities, price_differentials
                ),
                "risk_warnings": self._generate_risk_warnings(
                    credit_opportunities, price_differentials
                )
            }
        }
    
    def _generate_action_recommendations(
        self, 
        credit_ops: List[ArbitrageOpportunity], 
        price_diffs: List[Dict]
    ) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        if credit_ops:
            best_credit = credit_ops[0]
            if best_credit.expected_roi_percent > 30:
                recommendations.append(
                    f"HIGH PRIORITY: Establish carbon credit development in "
                    f"{best_credit.country_name} with {best_credit.expected_roi_percent:.1f}% ROI"
                )
        
        if price_diffs:
            best_diff = price_diffs[0]
            if best_diff["profit_per_tonne"] > 15:
                recommendations.append(
                    f"PRICE ARBITRAGE: {best_diff['source_market']} to {best_diff['target_market']} "
                    f"opportunity worth ${best_diff['profit_per_tonne']:.2f}/tonne"
                )
        
        # Market timing recommendations
        rising_markets = [
            market for market, intel in self.market_intelligence.items()
            if intel.price_trend_percent > 10
        ]
        if rising_markets:
            recommendations.append(
                f"MARKET TIMING: Consider positions in rising markets: {', '.join(rising_markets)}"
            )
        
        return recommendations
    
    def _generate_risk_warnings(
        self, 
        credit_ops: List[ArbitrageOpportunity], 
        price_diffs: List[Dict]
    ) -> List[str]:
        """Generate risk warnings"""
        
        warnings = []
        
        # High-risk opportunities
        high_risk_credits = [op for op in credit_ops if op.risk_score > 7]
        if high_risk_credits:
            warnings.append(
                f"HIGH RISK: {len(high_risk_credits)} credit opportunities have elevated risk scores"
            )
        
        # Volatile markets
        volatile_markets = [
            market for market, intel in self.market_intelligence.items()
            if intel.volatility_index > 0.6
        ]
        if volatile_markets:
            warnings.append(
                f"VOLATILITY WARNING: High volatility in markets: {', '.join(volatile_markets)}"
            )
        
        # Regulatory uncertainty
        uncertain_markets = [
            market for market, intel in self.market_intelligence.items()
            if intel.regulatory_stability == "uncertain"
        ]
        if uncertain_markets:
            warnings.append(
                f"REGULATORY RISK: Uncertain regulatory environment in: {', '.join(uncertain_markets)}"
            )
        
        return warnings

# Example usage
if __name__ == "__main__":
    async def main():
        analyzer = CarbonArbitrageAnalyzer()
        
        # Generate comprehensive report
        report = await analyzer.generate_arbitrage_report()
        
        print("=== CARBON ARBITRAGE ANALYSIS REPORT ===")
        print(f"Timestamp: {report['report_timestamp']}")
        print(f"\nCredit Generation Opportunities: {report['credit_generation']['opportunities_found']}")
        print(f"Total Estimated Value: ${report['credit_generation']['total_estimated_value_usd']:,.0f}")
        
        if report['credit_generation']['best_opportunity']:
            best = report['credit_generation']['best_opportunity']
            print(f"Best Opportunity: {best['country']} ({best['roi_percent']:.1f}% ROI)")
        
        print(f"\nPrice Arbitrage Opportunities: {report['price_arbitrage']['differentials_found']}")
        if report['price_arbitrage']['best_opportunity']:
            best_arb = report['price_arbitrage']['best_opportunity']
            print(f"Best Price Differential: {best_arb['source_market']} → {best_arb['target_market']}")
            print(f"Profit: ${best_arb['profit_per_tonne']:.2f}/tonne")
        
        print(f"\nRecommendations:")
        for rec in report['recommendations']['immediate_actions']:
            print(f"• {rec}")
        
        print(f"\nRisk Warnings:")
        for warning in report['recommendations']['risk_warnings']:
            print(f"⚠ {warning}")
    
    asyncio.run(main())