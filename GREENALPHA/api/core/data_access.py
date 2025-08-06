"""
High-Performance Data Access Layer for Carbon Calculator
Optimized for <500ms response time with intelligent caching
"""
import asyncio
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import sqlite3
import json
import logging
from pathlib import Path
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import pickle
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class EmissionDataPoint:
    """Single emission data point"""
    entity: str
    country_code: str
    year: int
    emissions_tonnes: float
    per_capita: Optional[float] = None
    gdp_intensity: Optional[float] = None

@dataclass
class CountryProfile:
    """Country emission profile with statistics"""
    country_code: str
    name: str
    latest_year: int
    total_emissions: float
    per_capita_emissions: float
    energy_mix: Dict[str, float]
    electricity_factor: float
    historical_trend: List[Tuple[int, float]]

class DataCache:
    """High-performance in-memory cache with TTL"""
    
    def __init__(self, max_size: int = 10000, default_ttl: int = 3600):
        self.cache = {}
        self.timestamps = {}
        self.access_count = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key not in self.cache:
            return None
        
        # Check TTL
        if datetime.now().timestamp() - self.timestamps[key] > self.default_ttl:
            self._remove(key)
            return None
        
        # Update access count for LRU
        self.access_count[key] = self.access_count.get(key, 0) + 1
        return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cached value with TTL"""
        # Cleanup if cache is full
        if len(self.cache) >= self.max_size:
            self._cleanup_lru()
        
        self.cache[key] = value
        self.timestamps[key] = datetime.now().timestamp()
        self.access_count[key] = 1
    
    def _remove(self, key: str):
        """Remove key from all cache structures"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
        self.access_count.pop(key, None)
    
    def _cleanup_lru(self):
        """Remove least recently used items"""
        # Remove 20% of items
        items_to_remove = int(self.max_size * 0.2)
        
        # Sort by access count (ascending)
        sorted_items = sorted(
            self.access_count.items(),
            key=lambda x: x[1]
        )
        
        for key, _ in sorted_items[:items_to_remove]:
            self._remove(key)
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()
        self.access_count.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": len(self.cache) / max(1, len(self.access_count))
        }

class CarbonDataManager:
    """
    High-performance carbon emission data manager
    Handles CSV data, caching, and fast lookups
    """
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path or self._find_data_path()
        self.cache = DataCache(max_size=5000, default_ttl=3600)
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # In-memory data structures for fast access
        self.emissions_data: Optional[pd.DataFrame] = None
        self.country_profiles: Dict[str, CountryProfile] = {}
        self.emission_factors: Dict[str, float] = {}
        
        # Performance tracking
        self.query_times = []
        self.last_loaded = None
        
        # Initialize data structures
        self._initialization_complete = False
        # Don't create task in __init__ to avoid event loop issues
        # Data will be initialized on first use
    
    async def ensure_initialized(self):
        """Ensure data manager is initialized"""
        if not self._initialization_complete:
            await self._initialize_data()
            self._initialization_complete = True
    
    def _find_data_path(self) -> str:
        """Find carbon data CSV file"""
        # Get the current directory and traverse up to find data
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        
        possible_paths = [
            project_root / "data" / "carbon_data.csv",
            project_root / "project 3.csv",  # Alternative name
            current_dir.parent / "data" / "carbon_data.csv",
            Path("/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/data/carbon_data.csv"),
            "../data/carbon_data.csv",
            "data/carbon_data.csv",
            "./carbon_data.csv"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return str(path)
        
        raise FileNotFoundError(f"Carbon data CSV file not found. Tried paths: {[str(p) for p in possible_paths]}")
    
    async def _initialize_data(self):
        """Initialize data structures asynchronously"""
        try:
            logger.info("Initializing carbon data...")
            start_time = datetime.now()
            
            # Load data in background thread
            loop = asyncio.get_event_loop()
            self.emissions_data = await loop.run_in_executor(
                self.executor, 
                self._load_emissions_data
            )
            
            # Build country profiles
            await loop.run_in_executor(
                self.executor,
                self._build_country_profiles
            )
            
            # Build emission factors lookup
            await loop.run_in_executor(
                self.executor,
                self._build_emission_factors
            )
            
            load_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Carbon data initialized in {load_time:.2f}s")
            self.last_loaded = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to initialize carbon data: {str(e)}")
            raise
    
    def _load_emissions_data(self) -> pd.DataFrame:
        """Load and preprocess emissions data"""
        try:
            # Load CSV with optimized dtypes
            df = pd.read_csv(
                self.data_path,
                dtype={
                    'Entity': 'category',
                    'Code': 'category', 
                    'Year': 'int16',
                    'Annual CO₂ emissions (tonnes )': 'float32'
                }
            )
            
            # Clean column names
            df.columns = ['entity', 'code', 'year', 'emissions_tonnes']
            
            # Remove rows with missing codes (global/regional aggregates)
            df = df.dropna(subset=['code'])
            df = df[df['code'] != '']
            
            # Sort by country and year for efficient queries
            df = df.sort_values(['code', 'year'])
            
            # Add calculated fields
            df['log_emissions'] = np.log1p(df['emissions_tonnes'])
            
            logger.info(f"Loaded {len(df)} emission records from {df['year'].min()} to {df['year'].max()}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load emissions data: {str(e)}")
            raise
    
    def _build_country_profiles(self):
        """Build country profiles for fast access"""
        if self.emissions_data is None:
            return
        
        try:
            profiles = {}
            
            for country_code in self.emissions_data['code'].unique():
                country_data = self.emissions_data[
                    self.emissions_data['code'] == country_code
                ].copy()
                
                if len(country_data) == 0:
                    continue
                
                # Get latest data
                latest_year = country_data['year'].max()
                latest_data = country_data[country_data['year'] == latest_year].iloc[0]
                
                # Calculate historical trend (last 10 years)
                recent_data = country_data[country_data['year'] >= latest_year - 10]
                historical_trend = [
                    (int(row['year']), float(row['emissions_tonnes']))
                    for _, row in recent_data.iterrows()
                ]
                
                # Estimate electricity emission factor based on emissions trend
                electricity_factor = self._estimate_electricity_factor(country_code, country_data)
                
                profile = CountryProfile(
                    country_code=country_code,
                    name=latest_data['entity'],
                    latest_year=int(latest_year),
                    total_emissions=float(latest_data['emissions_tonnes']),
                    per_capita_emissions=self._estimate_per_capita(country_code, latest_data['emissions_tonnes']),
                    energy_mix=self._get_energy_mix(country_code),
                    electricity_factor=electricity_factor,
                    historical_trend=historical_trend
                )
                
                profiles[country_code] = profile
            
            self.country_profiles = profiles
            logger.info(f"Built profiles for {len(profiles)} countries")
            
        except Exception as e:
            logger.error(f"Failed to build country profiles: {str(e)}")
    
    def _build_emission_factors(self):
        """Build emission factors lookup table"""
        try:
            # Calculate country-specific electricity emission factors
            factors = {}
            
            for code, profile in self.country_profiles.items():
                # Base electricity factor calculation
                base_factor = 0.475  # Global average kg CO2/kWh
                
                # Adjust based on country's emission intensity
                if profile.total_emissions > 0:
                    # Countries with higher total emissions tend to have dirtier grids
                    intensity_adjustment = min(2.0, profile.total_emissions / 1e9)  # Cap at 2x
                    factors[f"{code}_electricity"] = base_factor * intensity_adjustment
                else:
                    factors[f"{code}_electricity"] = base_factor
            
            self.emission_factors = factors
            logger.info(f"Built emission factors for {len(factors)} entries")
            
        except Exception as e:
            logger.error(f"Failed to build emission factors: {str(e)}")
    
    def _estimate_electricity_factor(self, country_code: str, country_data: pd.DataFrame) -> float:
        """Estimate electricity emission factor for country"""
        # Known factors for major countries (kg CO2/kWh)
        known_factors = {
            'USA': 0.385,
            'CHN': 0.644,
            'DEU': 0.338,
            'JPN': 0.462,
            'IND': 0.708,
            'BRA': 0.098,
            'CAN': 0.110,
            'GBR': 0.281,
            'FRA': 0.052,
            'RUS': 0.322,
        }
        
        if country_code in known_factors:
            return known_factors[country_code]
        
        # Estimate based on emission trends
        if len(country_data) > 5:
            recent_avg = country_data.tail(5)['emissions_tonnes'].mean()
            # Simple heuristic: higher total emissions -> dirtier grid
            return min(0.8, 0.2 + (recent_avg / 1e9) * 0.1)
        
        return 0.475  # Global average
    
    def _estimate_per_capita(self, country_code: str, total_emissions: float) -> float:
        """Estimate per capita emissions"""
        # Simplified population estimates (millions)
        populations = {
            'CHN': 1440, 'IND': 1380, 'USA': 331, 'IDN': 273, 'PAK': 220,
            'BRA': 212, 'NGA': 206, 'BGD': 164, 'RUS': 146, 'MEX': 128,
            'JPN': 126, 'PHL': 109, 'ETH': 115, 'VNM': 97, 'TUR': 84,
            'DEU': 83, 'IRN': 83, 'THA': 70, 'GBR': 67, 'FRA': 65,
        }
        
        population = populations.get(country_code, 50)  # Default 50M
        return total_emissions / (population * 1e6) if population > 0 else 0
    
    def _get_energy_mix(self, country_code: str) -> Dict[str, float]:
        """Get simplified energy mix for country"""
        # Simplified energy mix data (percentages)
        energy_mixes = {
            'USA': {'coal': 20, 'natural_gas': 40, 'renewable': 20, 'nuclear': 20},
            'CHN': {'coal': 57, 'natural_gas': 8, 'renewable': 28, 'nuclear': 7},
            'DEU': {'coal': 24, 'natural_gas': 16, 'renewable': 46, 'nuclear': 14},
            'JPN': {'coal': 32, 'natural_gas': 37, 'renewable': 20, 'nuclear': 11},
            'IND': {'coal': 61, 'natural_gas': 3, 'renewable': 25, 'nuclear': 11},
            'BRA': {'coal': 3, 'natural_gas': 9, 'renewable': 83, 'nuclear': 5},
            'CAN': {'coal': 7, 'natural_gas': 11, 'renewable': 68, 'nuclear': 14},
        }
        
        return energy_mixes.get(country_code, {
            'coal': 35, 'natural_gas': 25, 'renewable': 30, 'nuclear': 10
        })
    
    async def get_country_profile(self, country_code: str) -> Optional[CountryProfile]:
        """Get country profile with caching"""
        cache_key = f"profile_{country_code.upper()}"
        
        # Check cache first
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Get from memory
        profile = self.country_profiles.get(country_code.upper())
        if profile:
            self.cache.set(cache_key, profile)
        
        return profile
    
    async def get_emissions_history(
        self, 
        country_code: str, 
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> List[EmissionDataPoint]:
        """Get emissions history for country"""
        cache_key = f"history_{country_code}_{start_year}_{end_year}"
        
        # Check cache
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        if self.emissions_data is None:
            return []
        
        # Filter data
        country_data = self.emissions_data[
            self.emissions_data['code'] == country_code.upper()
        ]
        
        if start_year:
            country_data = country_data[country_data['year'] >= start_year]
        if end_year:
            country_data = country_data[country_data['year'] <= end_year]
        
        # Convert to data points
        history = [
            EmissionDataPoint(
                entity=row['entity'],
                country_code=row['code'],
                year=int(row['year']),
                emissions_tonnes=float(row['emissions_tonnes'])
            )
            for _, row in country_data.iterrows()
        ]
        
        # Cache result
        self.cache.set(cache_key, history)
        return history
    
    async def get_emission_factor(self, factor_key: str) -> Optional[float]:
        """Get emission factor with caching"""
        cache_key = f"factor_{factor_key}"
        
        # Check cache
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        
        # Get from memory
        factor = self.emission_factors.get(factor_key)
        if factor is not None:
            self.cache.set(cache_key, factor)
        
        return factor
    
    async def search_countries(self, query: str) -> List[Dict[str, str]]:
        """Search countries by name or code"""
        cache_key = f"search_{query.lower()}"
        
        # Check cache
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        query_lower = query.lower()
        results = []
        
        for code, profile in self.country_profiles.items():
            if (query_lower in profile.name.lower() or 
                query_lower in code.lower()):
                results.append({
                    "code": code,
                    "name": profile.name,
                    "latest_year": profile.latest_year,
                    "total_emissions": profile.total_emissions
                })
        
        # Sort by emissions (descending)
        results.sort(key=lambda x: x["total_emissions"], reverse=True)
        
        # Cache results
        self.cache.set(cache_key, results[:20])  # Top 20 results
        return results[:20]
    
    async def get_global_statistics(self) -> Dict[str, Any]:
        """Get global emission statistics"""
        cache_key = "global_stats"
        
        # Check cache
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        if self.emissions_data is None:
            return {}
        
        # Calculate global statistics
        latest_year = self.emissions_data['year'].max()
        latest_data = self.emissions_data[self.emissions_data['year'] == latest_year]
        
        stats = {
            "total_countries": len(self.country_profiles),
            "latest_year": int(latest_year),
            "global_emissions": float(latest_data['emissions_tonnes'].sum()),
            "top_emitters": [
                {
                    "country": profile.name,
                    "code": code,
                    "emissions": profile.total_emissions
                }
                for code, profile in sorted(
                    self.country_profiles.items(),
                    key=lambda x: x[1].total_emissions,
                    reverse=True
                )[:10]
            ],
            "data_coverage": {
                "years": f"{self.emissions_data['year'].min()}-{self.emissions_data['year'].max()}",
                "total_records": len(self.emissions_data)
            }
        }
        
        # Cache for longer period
        self.cache.set(cache_key, stats, ttl=7200)  # 2 hours
        return stats
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get data manager performance statistics"""
        return {
            "cache_stats": self.cache.stats(),
            "countries_loaded": len(self.country_profiles),
            "emission_factors": len(self.emission_factors),
            "last_loaded": self.last_loaded.isoformat() if self.last_loaded else None,
            "data_size": len(self.emissions_data) if self.emissions_data is not None else 0
        }
    
    async def refresh_data(self):
        """Refresh data from source"""
        logger.info("Refreshing carbon data...")
        self.cache.clear()
        await self._initialize_data()

# Global data manager instance
data_manager = CarbonDataManager()