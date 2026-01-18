"""
SimpleSUMO Core Module
======================

Core XML generation and SUMO file handling.
"""

from .xml_generators import (
    # Data Classes
    Node,
    Edge,
    Connection,
    Phase,
    TrafficLight,
    VehicleType,
    Route,
    Vehicle,
    Flow,
    
    # Generators
    NetworkGenerator,
    RouteGenerator,
    ConfigGenerator,
    AdditionalGenerator,
    
    # Helpers
    kmh_to_ms,
    ms_to_kmh,
    calculate_webster_cycle,
)

__all__ = [
    'Node',
    'Edge', 
    'Connection',
    'Phase',
    'TrafficLight',
    'VehicleType',
    'Route',
    'Vehicle',
    'Flow',
    'NetworkGenerator',
    'RouteGenerator',
    'ConfigGenerator',
    'AdditionalGenerator',
    'kmh_to_ms',
    'ms_to_kmh',
    'calculate_webster_cycle',
]
