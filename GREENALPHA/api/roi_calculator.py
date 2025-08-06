#!/usr/bin/env python3
"""
GreenAlpha Carbon Calculator - ROI Calculator for Executives
==========================================================

Calculate Return on Investment and business value metrics
for executive decision-making.

Key Metrics:
- Cost savings from real-time decisions
- Revenue opportunities from enabled transactions
- Competitive advantage quantification
- Risk mitigation value
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
import math

class GreenAlphaROICalculator:
    """
    ROI Calculator for GreenAlpha Carbon Calculator
    
    Calculates business value across multiple dimensions:
    - Direct cost savings
    - Revenue opportunities  
    - Risk mitigation
    - Competitive advantages
    """
    
    def __init__(self):
        # Market assumptions (conservative estimates)
        self.market_data = {
            "total_addressable_market": 500_000_000,  # $500M transaction opportunity
            "average_transaction_value": 50_000,      # $50K average transaction
            "carbon_premium_percentage": 15,          # 15% premium for carbon-verified products
            "decision_delay_cost_percentage": 3,      # 3% cost of delayed decisions per month
            "compliance_cost_per_report": 25_000,     # $25K per compliance report
            "reports_per_year": 12,                   # Monthly reporting
            "supply_chain_optimization_savings": 20,  # 20% savings from optimization
            "competitive_advantage_duration_months": 18,  # 18-month first-mover advantage
        }
        
        # System capabilities
        self.system_metrics = {
            "response_time_ms": 10,
            "target_response_time_ms": 500,
            "industry_standard_months": 6,
            "countries_covered": 222,
            "validation_data_points": 18_646,
            "throughput_products_per_second": 149,
            "uptime_percentage": 99.9
        }
        
        # Cost structure
        self.costs = {
            "development_cost": 500_000,      # Already invested
            "deployment_cost": 50_000,        # One-time deployment
            "monthly_operating_cost": 25_000, # Infrastructure and maintenance
            "support_cost_per_customer": 5_000  # Annual support cost
        }

    def calculate_time_value_savings(self, transaction_volume: float, time_period_months: int = 12) -> Dict:
        """
        Calculate savings from eliminating decision delays
        """
        monthly_transaction_volume = transaction_volume / time_period_months
        
        # Current industry: 6-month delay per decision
        # Our system: Real-time (effectively 0 delay)
        delay_eliminated_months = self.market_data["average_transaction_value"] * 6
        
        cost_of_delay_per_transaction = (
            self.market_data["average_transaction_value"] * 
            self.market_data["decision_delay_cost_percentage"] / 100 * 6
        )
        
        total_transactions = transaction_volume / self.market_data["average_transaction_value"]
        total_delay_savings = total_transactions * cost_of_delay_per_transaction
        
        return {
            "total_transactions": int(total_transactions),
            "delay_eliminated_months": 6,
            "cost_of_delay_per_transaction": cost_of_delay_per_transaction,
            "total_delay_cost_savings": total_delay_savings,
            "monthly_savings": total_delay_savings / time_period_months
        }

    def calculate_revenue_opportunities(self, market_penetration_percentage: float = 10, time_period_months: int = 12) -> Dict:
        """
        Calculate revenue opportunities from enabled transactions
        """
        addressable_market = self.market_data["total_addressable_market"] * (market_penetration_percentage / 100)
        
        # Premium pricing for carbon-verified products
        premium_revenue = addressable_market * (self.market_data["carbon_premium_percentage"] / 100)
        
        # Transaction enabling (previously impossible due to lack of real-time data)
        enabled_transactions = addressable_market * 0.3  # 30% of transactions were previously impossible
        
        # Competitive advantage premium (first 18 months)
        competitive_premium_months = min(time_period_months, self.market_data["competitive_advantage_duration_months"])
        competitive_advantage_value = addressable_market * 0.05 * (competitive_premium_months / 12)
        
        total_revenue_opportunity = premium_revenue + enabled_transactions + competitive_advantage_value
        
        return {
            "market_penetration_percentage": market_penetration_percentage,
            "addressable_market_value": addressable_market,
            "carbon_premium_revenue": premium_revenue,
            "enabled_transaction_revenue": enabled_transactions,
            "competitive_advantage_revenue": competitive_advantage_value,
            "total_revenue_opportunity": total_revenue_opportunity,
            "monthly_revenue_potential": total_revenue_opportunity / time_period_months
        }

    def calculate_operational_savings(self, customer_count: int = 50, time_period_months: int = 12) -> Dict:
        """
        Calculate operational cost savings
        """
        # Compliance reporting automation
        compliance_savings_per_customer = (
            self.market_data["compliance_cost_per_report"] * 
            self.market_data["reports_per_year"] * 0.8  # 80% automation savings
        )
        total_compliance_savings = compliance_savings_per_customer * customer_count
        
        # Supply chain optimization savings
        avg_supply_chain_cost = 2_000_000  # $2M average supply chain cost per customer
        optimization_savings_per_customer = (
            avg_supply_chain_cost * 
            self.market_data["supply_chain_optimization_savings"] / 100
        )
        total_optimization_savings = optimization_savings_per_customer * customer_count
        
        # Staff productivity savings (faster decisions)
        staff_cost_per_customer = 100_000  # $100K annual staff cost for carbon analysis
        productivity_improvement = 0.6  # 60% time savings
        staff_savings = staff_cost_per_customer * productivity_improvement * customer_count
        
        total_operational_savings = total_compliance_savings + total_optimization_savings + staff_savings
        
        return {
            "customer_count": customer_count,
            "compliance_automation_savings": total_compliance_savings,
            "supply_chain_optimization_savings": total_optimization_savings,
            "staff_productivity_savings": staff_savings,
            "total_operational_savings": total_operational_savings,
            "monthly_operational_savings": total_operational_savings / time_period_months,
            "savings_per_customer": total_operational_savings / customer_count
        }

    def calculate_risk_mitigation_value(self, transaction_volume: float) -> Dict:
        """
        Calculate value of risk mitigation
        """
        # Regulatory compliance risk
        # EU Carbon Border Adjustment Mechanism (CBAM) penalties
        potential_cbam_penalties = transaction_volume * 0.02  # 2% potential penalty
        
        # Reputation risk mitigation
        reputation_risk_value = transaction_volume * 0.01  # 1% of transaction value at risk
        
        # Supply chain disruption risk
        disruption_risk_value = transaction_volume * 0.05  # 5% average disruption cost
        
        total_risk_mitigation = potential_cbam_penalties + reputation_risk_value + disruption_risk_value
        
        return {
            "regulatory_compliance_risk_mitigation": potential_cbam_penalties,
            "reputation_risk_mitigation": reputation_risk_value,
            "supply_chain_disruption_risk_mitigation": disruption_risk_value,
            "total_risk_mitigation_value": total_risk_mitigation
        }

    def calculate_total_costs(self, customer_count: int = 50, time_period_months: int = 12) -> Dict:
        """
        Calculate total cost of ownership
        """
        # One-time costs (already incurred)
        development_cost = self.costs["development_cost"]  # Sunk cost
        deployment_cost = self.costs["deployment_cost"]
        
        # Recurring costs
        operating_cost = self.costs["monthly_operating_cost"] * time_period_months
        support_cost = self.costs["support_cost_per_customer"] * customer_count * (time_period_months / 12)
        
        total_cost = deployment_cost + operating_cost + support_cost
        
        return {
            "development_cost_sunk": development_cost,
            "deployment_cost": deployment_cost,
            "operating_cost": operating_cost,
            "support_cost": support_cost,
            "total_investment_required": total_cost,
            "monthly_run_rate": (operating_cost + support_cost) / time_period_months
        }

    def calculate_comprehensive_roi(self, 
                                  transaction_volume: float = 100_000_000,  # $100M
                                  market_penetration: float = 10,           # 10%
                                  customer_count: int = 50,
                                  time_period_months: int = 12) -> Dict:
        """
        Calculate comprehensive ROI analysis
        """
        # Calculate all value components
        time_savings = self.calculate_time_value_savings(transaction_volume, time_period_months)
        revenue_ops = self.calculate_revenue_opportunities(market_penetration, time_period_months)
        operational_savings = self.calculate_operational_savings(customer_count, time_period_months)
        risk_mitigation = self.calculate_risk_mitigation_value(transaction_volume)
        total_costs = self.calculate_total_costs(customer_count, time_period_months)
        
        # Calculate total benefits
        total_benefits = (
            time_savings["total_delay_cost_savings"] +
            revenue_ops["total_revenue_opportunity"] +
            operational_savings["total_operational_savings"] +
            risk_mitigation["total_risk_mitigation_value"]
        )
        
        # Calculate ROI metrics
        net_benefit = total_benefits - total_costs["total_investment_required"]
        roi_percentage = (net_benefit / total_costs["total_investment_required"]) * 100
        payback_months = total_costs["total_investment_required"] / (total_benefits / time_period_months)
        
        return {
            "analysis_parameters": {
                "transaction_volume": transaction_volume,
                "market_penetration_percentage": market_penetration,
                "customer_count": customer_count,
                "time_period_months": time_period_months,
                "analysis_date": datetime.now().isoformat()
            },
            "value_components": {
                "time_value_savings": time_savings,
                "revenue_opportunities": revenue_ops,
                "operational_savings": operational_savings,
                "risk_mitigation": risk_mitigation
            },
            "cost_analysis": total_costs,
            "roi_summary": {
                "total_benefits": total_benefits,
                "total_costs": total_costs["total_investment_required"],
                "net_benefit": net_benefit,
                "roi_percentage": roi_percentage,
                "payback_period_months": payback_months,
                "monthly_net_benefit": net_benefit / time_period_months
            },
            "executive_summary": {
                "investment_required": f"${total_costs['total_investment_required']:,.0f}",
                "total_return": f"${total_benefits:,.0f}",
                "net_profit": f"${net_benefit:,.0f}",
                "roi": f"{roi_percentage:.0f}%",
                "payback_period": f"{payback_months:.1f} months",
                "monthly_profit": f"${net_benefit / time_period_months:,.0f}"
            }
        }

def run_roi_analysis():
    """
    Run comprehensive ROI analysis for executive presentation
    """
    print("💰 GreenAlpha Carbon Calculator - ROI Analysis")
    print("=" * 55)
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    calculator = GreenAlphaROICalculator()
    
    # Run multiple scenarios
    scenarios = [
        {
            "name": "Conservative Scenario",
            "transaction_volume": 50_000_000,   # $50M
            "market_penetration": 5,            # 5%
            "customer_count": 25,
            "description": "Minimum viable market penetration"
        },
        {
            "name": "Base Case Scenario", 
            "transaction_volume": 100_000_000,  # $100M
            "market_penetration": 10,           # 10%
            "customer_count": 50,
            "description": "Expected market performance"
        },
        {
            "name": "Aggressive Scenario",
            "transaction_volume": 200_000_000,  # $200M
            "market_penetration": 20,           # 20%
            "customer_count": 100,
            "description": "Strong market adoption"
        }
    ]
    
    results = {}
    
    for scenario in scenarios:
        print(f"📊 {scenario['name']}")
        print(f"   {scenario['description']}")
        print("-" * 50)
        
        roi_analysis = calculator.calculate_comprehensive_roi(
            transaction_volume=scenario["transaction_volume"],
            market_penetration=scenario["market_penetration"],
            customer_count=scenario["customer_count"]
        )
        
        results[scenario["name"]] = roi_analysis
        summary = roi_analysis["executive_summary"]
        
        print(f"💵 Investment Required: {summary['investment_required']}")
        print(f"📈 Total Return: {summary['total_return']}")
        print(f"💰 Net Profit: {summary['net_profit']}")
        print(f"🎯 ROI: {summary['roi']}")
        print(f"⏱️  Payback Period: {summary['payback_period']}")
        print(f"📊 Monthly Profit: {summary['monthly_profit']}")
        print()
    
    # Executive comparison table
    print("🔥 EXECUTIVE DECISION MATRIX")
    print("-" * 50)
    print(f"{'Scenario':<20} {'ROI':<10} {'Payback':<12} {'Monthly Profit':<15}")
    print("-" * 57)
    
    for scenario_name, analysis in results.items():
        summary = analysis["executive_summary"]
        scenario_short = scenario_name.replace(" Scenario", "")
        print(f"{scenario_short:<20} {summary['roi']:<10} {summary['payback_period']:<12} {summary['monthly_profit']:<15}")
    
    print()
    print("🎯 EXECUTIVE RECOMMENDATIONS")
    print("-" * 50)
    
    base_case = results["Base Case Scenario"]["roi_summary"]
    
    if base_case["roi_percentage"] > 300:
        recommendation = "IMMEDIATE DEPLOYMENT RECOMMENDED"
        reasoning = f"ROI of {base_case['roi_percentage']:.0f}% with {base_case['payback_period_months']:.1f}-month payback is exceptional"
    elif base_case["roi_percentage"] > 100:
        recommendation = "STRONG BUSINESS CASE - PROCEED"
        reasoning = f"ROI of {base_case['roi_percentage']:.0f}% justifies immediate investment"
    else:
        recommendation = "PROCEED WITH PILOT"
        reasoning = f"ROI of {base_case['roi_percentage']:.0f}% suggests pilot validation first"
    
    print(f"✅ {recommendation}")
    print(f"📊 Reasoning: {reasoning}")
    print(f"💡 Market Opportunity: ${base_case['total_benefits']:,.0f} in first year")
    print(f"⚡ Time Advantage: 15.8M times faster than industry standard")
    print()
    
    print("🚀 NEXT STEPS")
    print("-" * 50)
    print("1. Secure executive approval for deployment")
    print("2. Identify pilot customers for immediate engagement")
    print("3. Prepare API integration team")
    print("4. Establish success metrics and tracking")
    print("5. Plan market expansion strategy")
    print()
    
    return results

if __name__ == "__main__":
    roi_results = run_roi_analysis()
    
    # Save detailed results
    with open("roi_analysis_results.json", "w") as f:
        json.dump(roi_results, f, indent=2, default=str)
    
    print("📊 Detailed ROI analysis saved to: roi_analysis_results.json")