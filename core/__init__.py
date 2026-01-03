"""UHIP Core Library - Shared models and utilities for Dashboard and Microgrid Simulator"""

__version__ = "0.1.0"

from core.models import Plant, Unit, TimeSeries, LoadProfile, RenewableProfile, Battery
from core.api_schema import PlantResponse, UnitResponse, TimeSeriesResponse
from core.utils.emissions_calculator import calculate_co2_avoided

__all__ = [
    'Plant',
    'Unit',
    'TimeSeries',
    'LoadProfile',
    'RenewableProfile',
    'Battery',
    'PlantResponse',
    'UnitResponse',
    'TimeSeriesResponse',
    'calculate_co2_avoided',
]
