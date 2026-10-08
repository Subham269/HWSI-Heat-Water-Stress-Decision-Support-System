"""
Configuration for HWSI Engine including AHP weights and normalization thresholds.
"""

# AHP Weights configuration
AHP_MATRICES = {
    # Main components: Hazard, Exposure, Vulnerability
    "components": [
        [1, 2, 3],     # Hazard is 2x more important than Exp, 3x than Vuln
        [1/2, 1, 2],   # Exposure is 2x more important than Vuln
        [1/3, 1/2, 1]  # Vulnerability
    ],
    
    # Hazard indicators: Heat Index, Warm Nights, Precip Deficit, ET, SM, Tmin
    "hazard": [
        [1, 2, 3, 4, 4, 3],
        [1/2, 1, 2, 3, 3, 2],
        [1/3, 1/2, 1, 2, 2, 1],
        [1/4, 1/3, 1/2, 1, 1, 1/2],
        [1/4, 1/3, 1/2, 1, 1, 1/2],
        [1/3, 1/2, 1, 2, 2, 1]
    ],
    
    # Exposure indicators: Pop Density, Outdoor Workers
    "exposure": [
        [1, 1/2],
        [2, 1]
    ],
    
    # Vulnerability indicators: Piped Coverage, Extraction, Arsenic, Fluoride, Beds, Elderly, Children
    "vulnerability": [
        [1, 2, 3, 3, 2, 4, 4],     # Piped coverage
        [1/2, 1, 2, 2, 1, 3, 3],   # Extraction
        [1/3, 1/2, 1, 1, 1/2, 2, 2], # Arsenic
        [1/3, 1/2, 1, 1, 1/2, 2, 2], # Fluoride
        [1/2, 1, 2, 2, 1, 3, 3],   # Beds
        [1/4, 1/3, 1/2, 1/2, 1/3, 1, 1], # Elderly
        [1/4, 1/3, 1/2, 1/2, 1/3, 1, 1]  # Children
    ]
}

INDICATOR_NAMES = {
    "hazard": ["heat_index", "warm_nights", "precip_deficit", "et", "sm_slope", "tmin_ma"],
    "exposure": ["population_density", "pct_outdoor_workers"],
    "vulnerability": ["pct_piped_coverage", "extraction_pct", "arsenic_affected", "fluoride_affected", "beds_per_1000", "pct_elderly", "pct_children"]
}

# Normalization Thresholds (lo, hi)
THRESHOLDS = {
    "hazard": {
        "heat_index": (35.0, 45.0), # °C
        "warm_nights": (0, 5),      # days
        "precip_deficit": (-50, 50),# %
        "et": (0, 50),              # mm
        "sm_slope": (-0.1, 0.1),    # slope
        "tmin_ma": (20.0, 30.0)     # °C
    },
    "exposure": {
        "population_density": (100, 2000),
        "pct_outdoor_workers": (10, 70)
    },
    "vulnerability": {
        "pct_piped_coverage": (0, 100),   # Inverted
        "extraction_pct": (40, 120),
        "arsenic_affected": (0, 1),
        "fluoride_affected": (0, 1),
        "beds_per_1000": (0, 3),          # Inverted
        "pct_elderly": (5, 15),
        "pct_children": (10, 20)
    }
}

INVERTED_INDICATORS = ["pct_piped_coverage", "beds_per_1000"]

# Allocation Parameters
ALLOCATION_PARAMS = {
    "tankers": {
        "k_r": 0.5,
        "a": 0.4, # weight of H
        "b": 0.6  # weight of V
    },
    "cooling_units": {
        "k_r": 0.2,
        "a": 0.6,
        "b": 0.4
    }
}

BANDS = {
    "low": 0.25,
    "moderate": 0.50,
    "high": 0.75
}
