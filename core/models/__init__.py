"""Core data models for UHIP - used by both Dashboard and Simulator"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal
from enum import Enum

class UnitType(str, Enum):
    """Reactor/Unit types"""
    NPP = "npp"  # Nuclear Power Plant
    SMR = "smr"  # Small Modular Reactor
    RENEWABLE = "renewable"  # Solar/Wind
    BATTERY = "battery"  # Energy storage

class MetricType(str, Enum):
    """Types of measurements"""
    POWER_OUTPUT = "power_output_mw"
    FREQUENCY = "grid_frequency_hz"
    LOAD = "load_demand_mw"
    RENEWABLE_OUTPUT = "renewable_output_mw"
    BATTERY_LEVEL = "battery_level_mwh"

@dataclass
class Plant:
    """Nuclear Power Plant entity"""
    id: str
    name: str
    location: str
    country: str
    lat: float
    lon: float
    total_capacity_mw: float
    units: List['Unit'] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Unit:
    """Individual reactor/generation unit"""
    id: str
    name: str
    plant_id: str
    unit_type: UnitType
    capacity_mw: float
    min_load_pct: float = 50.0  # Minimum stable load
    ramp_rate_mw_per_h: float = 100.0  # Rate of change
    status: Literal['operational', 'maintenance', 'shutdown'] = 'operational'
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class TimeSeries:
    """Time-series measurement data"""
    unit_id: str
    metric_type: MetricType
    timestamp: datetime
    value: float
    unit: str = "MW"
    source: Optional[str] = None  # Data source (e.g., 'ua-energy', 'simulation')

@dataclass
class LoadProfile:
    """Load/demand profile for simulation"""
    profile_type: Literal['city', 'industrial', 'datacenter', 'custom']
    name: str
    hourly_demand_mw: List[float]  # 24 hourly values
    yearly_kwh: float  # Annual energy demand
    peak_load_mw: float
    description: Optional[str] = None

@dataclass
class RenewableProfile:
    """Solar/Wind renewable energy profile"""
    resource_type: Literal['solar', 'wind']
    location: str
    hourly_capacity_factor: List[float]  # 24 hourly values (0-1)
    installed_capacity_mw: float
    annual_energy_kwh: float
    description: Optional[str] = None

@dataclass
class Battery:
    """Energy storage (battery) system"""
    capacity_mwh: float
    charge_rate_mw: float
    discharge_rate_mw: float
    round_trip_efficiency: float = 0.85  # 0-1
    min_soc_pct: float = 20.0  # Minimum state of charge
    max_soc_pct: float = 100.0  # Maximum state of charge

@dataclass
class EmissionMetrics:
    """CO2 and emissions data"""
    timestamp: datetime
    unit_id: str
    co2_g_per_kwh: float
    avoided_co2_tonnes: float  # Tonnes of CO2 avoided vs fossil fuel baseline
    grid_avg_co2_g_per_kwh: float  # Grid average for comparison

__all__ = [
    'UnitType',
    'MetricType',
    'Plant',
    'Unit',
    'TimeSeries',
    'LoadProfile',
    'RenewableProfile',
    'Battery',
    'EmissionMetrics',
]
