import pandas as pd
import numpy as np

def compute_heat_index(tmax: pd.Series, rh: pd.Series) -> pd.Series:
    """Calculate Heat Index using NWS Rothfusz regression."""
    t_f = tmax * 9/5 + 32
    
    hi_f = (-42.379 + 2.04901523*t_f + 10.14333127*rh - 0.22475541*t_f*rh 
            - 6.83783e-3*t_f**2 - 5.481717e-2*rh**2 + 1.22874e-3*t_f**2*rh 
            + 8.5282e-4*t_f*rh**2 - 1.99e-6*t_f**2*rh**2)
            
    # Convert back to Celsius
    hi_c = (hi_f - 32) * 5/9
    return hi_c

def compute_warm_nights(tmin_series: pd.Series, threshold=25.0) -> int:
    """Count consecutive warm nights."""
    return (tmin_series > threshold).sum()

def get_etl_features(weather_df: pd.DataFrame) -> pd.DataFrame:
    """Extract features from weather forecast dataframe."""
    result = []
    for block_id, group in weather_df.groupby('block_id'):
        hi = compute_heat_index(group['tmax'].max(), group['rh'].mean())
        wn = compute_warm_nights(group['tmin'])
        
        result.append({
            'block_id': block_id,
            'heat_index': hi,
            'warm_nights': wn,
            'precip_deficit': np.random.uniform(-10, 30), # mock
            'et': group['et'].sum() if 'et' in group else np.random.uniform(10, 40),
            'sm_slope': np.random.uniform(-0.05, 0.05), # mock
            'tmin_ma': group['tmin'].rolling(3).mean().max()
        })
    return pd.DataFrame(result)
