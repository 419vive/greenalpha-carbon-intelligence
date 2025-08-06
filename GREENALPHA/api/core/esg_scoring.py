"""
ESG (Environmental, Social, Governance) Scoring System
Comprehensive ESG assessment for suppliers and supply chains
"""
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import logging
import numpy as np

logger = logging.getLogger(__name__)

class ESGCategory(Enum):
    """ESG assessment categories"""
    ENVIRONMENTAL = "Environmental"
    SOCIAL = "Social"
    GOVERNANCE = "Governance"

class RiskLevel(Enum):
    """ESG risk levels"""
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"

@dataclass
class ESGMetrics:
    """Detailed ESG metrics"""
    # Environmental metrics
    carbon_intensity: float  # kg CO2e per unit
    renewable_energy_percent: float  # 0-100
    water_usage_efficiency: float  # 0-100
    waste_recycling_rate: float  # 0-100
    biodiversity_impact: float  # 0-100 (lower is better)
    
    # Social metrics
    labor_practices_score: float  # 0-100
    community_engagement: float  # 0-100
    health_safety_record: float  # 0-100
    diversity_inclusion: float  # 0-100
    supply_chain_transparency: float  # 0-100
    
    # Governance metrics
    board_diversity: float  # 0-100
    ethics_compliance: float  # 0-100
    risk_management: float  # 0-100
    shareholder_rights: float  # 0-100
    anti_corruption_measures: float  # 0-100

@dataclass
class ESGScore:
    """ESG scoring result"""
    overall_score: float  # 0-100
    environmental_score: float
    social_score: float
    governance_score: float
    risk_level: RiskLevel
    strengths: List[str]
    weaknesses: List[str]
    improvement_recommendations: List[Dict]
    compliance_status: Dict[str, bool]
    peer_comparison: Dict[str, float]

class ESGScoringEngine:
    """Engine for calculating and analyzing ESG scores"""
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.regulatory_requirements = self._load_regulatory_requirements()
        self.scoring_weights = self._initialize_scoring_weights()
        self.certification_standards = self._load_certification_standards()
    
    def _load_industry_benchmarks(self) -> Dict[str, Dict]:
        """Load industry-specific ESG benchmarks"""
        return {
            "manufacturing": {
                "environmental": {"avg": 55, "top_quartile": 75},
                "social": {"avg": 60, "top_quartile": 80},
                "governance": {"avg": 65, "top_quartile": 85}
            },
            "technology": {
                "environmental": {"avg": 70, "top_quartile": 85},
                "social": {"avg": 75, "top_quartile": 90},
                "governance": {"avg": 70, "top_quartile": 85}
            },
            "energy": {
                "environmental": {"avg": 45, "top_quartile": 65},
                "social": {"avg": 55, "top_quartile": 75},
                "governance": {"avg": 60, "top_quartile": 80}
            },
            "retail": {
                "environmental": {"avg": 50, "top_quartile": 70},
                "social": {"avg": 65, "top_quartile": 85},
                "governance": {"avg": 60, "top_quartile": 80}
            }
        }
    
    def _load_regulatory_requirements(self) -> Dict[str, Dict]:
        """Load regulatory ESG requirements"""
        return {
            "EU_CSRD": {  # Corporate Sustainability Reporting Directive
                "min_environmental_score": 50,
                "min_social_score": 50,
                "min_governance_score": 60,
                "required_disclosures": ["carbon_emissions", "water_usage", "diversity_metrics"]
            },
            "SEC_Climate": {  # SEC Climate Disclosure Rules
                "min_environmental_score": 45,
                "required_disclosures": ["climate_risks", "emissions_scope_1_2_3"]
            },
            "UK_Modern_Slavery": {
                "min_social_score": 60,
                "required_disclosures": ["supply_chain_audit", "labor_practices"]
            },
            "TCFD": {  # Task Force on Climate-related Financial Disclosures
                "min_environmental_score": 55,
                "min_governance_score": 65,
                "required_disclosures": ["climate_governance", "risk_management", "metrics_targets"]
            }
        }
    
    def _initialize_scoring_weights(self) -> Dict[str, float]:
        """Initialize scoring weights for different ESG components"""
        return {
            "environmental": 0.35,
            "social": 0.35,
            "governance": 0.30,
            # Sub-weights for environmental
            "carbon_intensity": 0.30,
            "renewable_energy": 0.25,
            "water_efficiency": 0.15,
            "waste_recycling": 0.15,
            "biodiversity": 0.15,
            # Sub-weights for social
            "labor_practices": 0.25,
            "community": 0.20,
            "health_safety": 0.25,
            "diversity": 0.15,
            "transparency": 0.15,
            # Sub-weights for governance
            "board_diversity": 0.20,
            "ethics": 0.25,
            "risk_mgmt": 0.25,
            "shareholder": 0.15,
            "anti_corruption": 0.15
        }
    
    def _load_certification_standards(self) -> Dict[str, Dict]:
        """Load ESG certification standards"""
        return {
            "B_Corp": {"min_overall_score": 80, "verified_areas": ["environmental", "social", "governance"]},
            "ISO_14001": {"min_environmental_score": 70, "verified_areas": ["environmental"]},
            "SA8000": {"min_social_score": 75, "verified_areas": ["social"]},
            "Fair_Trade": {"min_social_score": 70, "verified_areas": ["social"]},
            "Carbon_Neutral": {"min_environmental_score": 80, "carbon_offset_required": True},
            "LEED": {"min_environmental_score": 75, "verified_areas": ["environmental"]}
        }
    
    def calculate_esg_score(self,
                          company_data: Dict,
                          industry: str = "manufacturing") -> ESGScore:
        """Calculate comprehensive ESG score"""
        
        # Extract or estimate metrics
        metrics = self._extract_metrics(company_data)
        
        # Calculate component scores
        environmental_score = self._calculate_environmental_score(metrics)
        social_score = self._calculate_social_score(metrics)
        governance_score = self._calculate_governance_score(metrics)
        
        # Calculate weighted overall score
        overall_score = (
            environmental_score * self.scoring_weights["environmental"] +
            social_score * self.scoring_weights["social"] +
            governance_score * self.scoring_weights["governance"]
        )
        
        # Determine risk level
        risk_level = self._determine_risk_level(overall_score)
        
        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses(
            environmental_score, social_score, governance_score, metrics
        )
        
        # Generate improvement recommendations
        recommendations = self._generate_recommendations(
            environmental_score, social_score, governance_score, metrics
        )
        
        # Check compliance status
        compliance_status = self._check_compliance(
            environmental_score, social_score, governance_score
        )
        
        # Compare with peers
        peer_comparison = self._compare_with_peers(
            environmental_score, social_score, governance_score, industry
        )
        
        return ESGScore(
            overall_score=overall_score,
            environmental_score=environmental_score,
            social_score=social_score,
            governance_score=governance_score,
            risk_level=risk_level,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_recommendations=recommendations,
            compliance_status=compliance_status,
            peer_comparison=peer_comparison
        )
    
    def _extract_metrics(self, company_data: Dict) -> ESGMetrics:
        """Extract or estimate ESG metrics from company data"""
        # Default values if not provided
        defaults = {
            "carbon_intensity": 50,
            "renewable_energy_percent": 30,
            "water_usage_efficiency": 60,
            "waste_recycling_rate": 50,
            "biodiversity_impact": 40,
            "labor_practices_score": 65,
            "community_engagement": 60,
            "health_safety_record": 70,
            "diversity_inclusion": 55,
            "supply_chain_transparency": 60,
            "board_diversity": 50,
            "ethics_compliance": 70,
            "risk_management": 65,
            "shareholder_rights": 70,
            "anti_corruption_measures": 75
        }
        
        # Override with actual data if available
        metrics_data = {**defaults, **company_data.get("esg_metrics", {})}
        
        # Adjust based on certifications
        if "certifications" in company_data:
            certs = company_data["certifications"]
            if "ISO14001" in certs:
                metrics_data["environmental_score"] = max(metrics_data.get("environmental_score", 60), 70)
            if "B-Corp" in certs:
                metrics_data["overall_boost"] = 10
            if "Carbon-Neutral" in certs:
                metrics_data["carbon_intensity"] = min(metrics_data["carbon_intensity"], 20)
        
        return ESGMetrics(
            carbon_intensity=100 - metrics_data["carbon_intensity"],  # Invert for scoring
            renewable_energy_percent=metrics_data["renewable_energy_percent"],
            water_usage_efficiency=metrics_data["water_usage_efficiency"],
            waste_recycling_rate=metrics_data["waste_recycling_rate"],
            biodiversity_impact=100 - metrics_data["biodiversity_impact"],  # Invert
            labor_practices_score=metrics_data["labor_practices_score"],
            community_engagement=metrics_data["community_engagement"],
            health_safety_record=metrics_data["health_safety_record"],
            diversity_inclusion=metrics_data["diversity_inclusion"],
            supply_chain_transparency=metrics_data["supply_chain_transparency"],
            board_diversity=metrics_data["board_diversity"],
            ethics_compliance=metrics_data["ethics_compliance"],
            risk_management=metrics_data["risk_management"],
            shareholder_rights=metrics_data["shareholder_rights"],
            anti_corruption_measures=metrics_data["anti_corruption_measures"]
        )
    
    def _calculate_environmental_score(self, metrics: ESGMetrics) -> float:
        """Calculate environmental component score"""
        weights = self.scoring_weights
        
        score = (
            metrics.carbon_intensity * weights["carbon_intensity"] +
            metrics.renewable_energy_percent * weights["renewable_energy"] +
            metrics.water_usage_efficiency * weights["water_efficiency"] +
            metrics.waste_recycling_rate * weights["waste_recycling"] +
            metrics.biodiversity_impact * weights["biodiversity"]
        )
        
        # Normalize to 0-100
        return min(100, max(0, score))
    
    def _calculate_social_score(self, metrics: ESGMetrics) -> float:
        """Calculate social component score"""
        weights = self.scoring_weights
        
        score = (
            metrics.labor_practices_score * weights["labor_practices"] +
            metrics.community_engagement * weights["community"] +
            metrics.health_safety_record * weights["health_safety"] +
            metrics.diversity_inclusion * weights["diversity"] +
            metrics.supply_chain_transparency * weights["transparency"]
        )
        
        return min(100, max(0, score))
    
    def _calculate_governance_score(self, metrics: ESGMetrics) -> float:
        """Calculate governance component score"""
        weights = self.scoring_weights
        
        score = (
            metrics.board_diversity * weights["board_diversity"] +
            metrics.ethics_compliance * weights["ethics"] +
            metrics.risk_management * weights["risk_mgmt"] +
            metrics.shareholder_rights * weights["shareholder"] +
            metrics.anti_corruption_measures * weights["anti_corruption"]
        )
        
        return min(100, max(0, score))
    
    def _determine_risk_level(self, overall_score: float) -> RiskLevel:
        """Determine ESG risk level based on overall score"""
        if overall_score >= 80:
            return RiskLevel.VERY_LOW
        elif overall_score >= 65:
            return RiskLevel.LOW
        elif overall_score >= 50:
            return RiskLevel.MEDIUM
        elif overall_score >= 35:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH
    
    def _identify_strengths_weaknesses(self,
                                      env_score: float,
                                      soc_score: float,
                                      gov_score: float,
                                      metrics: ESGMetrics) -> Tuple[List[str], List[str]]:
        """Identify ESG strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Environmental assessment
        if env_score >= 70:
            strengths.append("Strong environmental performance")
        elif env_score < 50:
            weaknesses.append("Environmental impact needs improvement")
        
        if metrics.renewable_energy_percent >= 50:
            strengths.append("High renewable energy usage")
        elif metrics.renewable_energy_percent < 20:
            weaknesses.append("Low renewable energy adoption")
        
        # Social assessment
        if soc_score >= 70:
            strengths.append("Excellent social responsibility")
        elif soc_score < 50:
            weaknesses.append("Social practices need attention")
        
        if metrics.health_safety_record >= 80:
            strengths.append("Outstanding health & safety record")
        elif metrics.health_safety_record < 60:
            weaknesses.append("Health & safety improvements needed")
        
        # Governance assessment
        if gov_score >= 70:
            strengths.append("Strong governance structure")
        elif gov_score < 50:
            weaknesses.append("Governance framework needs strengthening")
        
        if metrics.ethics_compliance >= 80:
            strengths.append("High ethical standards")
        elif metrics.ethics_compliance < 60:
            weaknesses.append("Ethics compliance needs improvement")
        
        return strengths, weaknesses
    
    def _generate_recommendations(self,
                                 env_score: float,
                                 soc_score: float,
                                 gov_score: float,
                                 metrics: ESGMetrics) -> List[Dict]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Environmental recommendations
        if env_score < 70:
            if metrics.carbon_intensity < 50:
                recommendations.append({
                    "category": "Environmental",
                    "priority": "High",
                    "action": "Implement carbon reduction strategy",
                    "potential_score_improvement": 10,
                    "estimated_cost": "Medium",
                    "timeline": "6-12 months"
                })
            
            if metrics.renewable_energy_percent < 30:
                recommendations.append({
                    "category": "Environmental",
                    "priority": "Medium",
                    "action": "Increase renewable energy sourcing",
                    "potential_score_improvement": 8,
                    "estimated_cost": "High",
                    "timeline": "12-18 months"
                })
        
        # Social recommendations
        if soc_score < 70:
            if metrics.diversity_inclusion < 50:
                recommendations.append({
                    "category": "Social",
                    "priority": "Medium",
                    "action": "Develop diversity and inclusion program",
                    "potential_score_improvement": 5,
                    "estimated_cost": "Low",
                    "timeline": "3-6 months"
                })
            
            if metrics.supply_chain_transparency < 60:
                recommendations.append({
                    "category": "Social",
                    "priority": "High",
                    "action": "Enhance supply chain transparency",
                    "potential_score_improvement": 7,
                    "estimated_cost": "Medium",
                    "timeline": "6-9 months"
                })
        
        # Governance recommendations
        if gov_score < 70:
            if metrics.board_diversity < 40:
                recommendations.append({
                    "category": "Governance",
                    "priority": "Medium",
                    "action": "Improve board diversity",
                    "potential_score_improvement": 6,
                    "estimated_cost": "Low",
                    "timeline": "3-12 months"
                })
            
            if metrics.risk_management < 60:
                recommendations.append({
                    "category": "Governance",
                    "priority": "High",
                    "action": "Strengthen risk management framework",
                    "potential_score_improvement": 8,
                    "estimated_cost": "Medium",
                    "timeline": "6-9 months"
                })
        
        # Sort by priority and potential improvement
        recommendations.sort(key=lambda x: (
            {"High": 0, "Medium": 1, "Low": 2}[x["priority"]],
            -x["potential_score_improvement"]
        ))
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _check_compliance(self,
                         env_score: float,
                         soc_score: float,
                         gov_score: float) -> Dict[str, bool]:
        """Check compliance with various ESG standards"""
        compliance = {}
        
        for standard, requirements in self.regulatory_requirements.items():
            compliant = True
            
            if "min_environmental_score" in requirements:
                if env_score < requirements["min_environmental_score"]:
                    compliant = False
            
            if "min_social_score" in requirements:
                if soc_score < requirements["min_social_score"]:
                    compliant = False
            
            if "min_governance_score" in requirements:
                if gov_score < requirements["min_governance_score"]:
                    compliant = False
            
            compliance[standard] = compliant
        
        return compliance
    
    def _compare_with_peers(self,
                          env_score: float,
                          soc_score: float,
                          gov_score: float,
                          industry: str) -> Dict[str, float]:
        """Compare scores with industry peers"""
        benchmarks = self.industry_benchmarks.get(industry, self.industry_benchmarks["manufacturing"])
        
        return {
            "environmental_vs_avg": env_score - benchmarks["environmental"]["avg"],
            "social_vs_avg": soc_score - benchmarks["social"]["avg"],
            "governance_vs_avg": gov_score - benchmarks["governance"]["avg"],
            "environmental_percentile": self._calculate_percentile(env_score, benchmarks["environmental"]),
            "social_percentile": self._calculate_percentile(soc_score, benchmarks["social"]),
            "governance_percentile": self._calculate_percentile(gov_score, benchmarks["governance"])
        }
    
    def _calculate_percentile(self, score: float, benchmark: Dict) -> float:
        """Calculate percentile ranking based on benchmark"""
        avg = benchmark["avg"]
        top_quartile = benchmark["top_quartile"]
        
        if score >= top_quartile:
            # Top 25%
            return 75 + (score - top_quartile) / (100 - top_quartile) * 25
        elif score >= avg:
            # Between average and top quartile
            return 50 + (score - avg) / (top_quartile - avg) * 25
        else:
            # Below average
            return score / avg * 50
    
    def generate_esg_report(self, esg_score: ESGScore, company_name: str) -> Dict:
        """Generate comprehensive ESG report"""
        return {
            "company": company_name,
            "assessment_date": datetime.now().isoformat(),
            "executive_summary": {
                "overall_score": esg_score.overall_score,
                "risk_level": esg_score.risk_level.value,
                "recommendation": self._get_executive_recommendation(esg_score.overall_score)
            },
            "detailed_scores": {
                "environmental": esg_score.environmental_score,
                "social": esg_score.social_score,
                "governance": esg_score.governance_score
            },
            "strengths": esg_score.strengths,
            "weaknesses": esg_score.weaknesses,
            "improvement_plan": esg_score.improvement_recommendations,
            "compliance_status": esg_score.compliance_status,
            "peer_comparison": esg_score.peer_comparison,
            "next_review_date": (datetime.now() + timedelta(days=365)).isoformat()
        }
    
    def _get_executive_recommendation(self, score: float) -> str:
        """Generate executive recommendation based on score"""
        if score >= 80:
            return "Excellent ESG performance. Maintain current practices and consider industry leadership opportunities."
        elif score >= 65:
            return "Good ESG performance. Focus on identified improvement areas to achieve excellence."
        elif score >= 50:
            return "Moderate ESG performance. Implement recommended improvements to reduce risk."
        elif score >= 35:
            return "Below average ESG performance. Urgent action needed to address critical gaps."
        else:
            return "Poor ESG performance. Comprehensive ESG transformation required immediately."