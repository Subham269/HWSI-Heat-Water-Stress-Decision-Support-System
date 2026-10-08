import pandas as pd
import numpy as np

def normalize_indicators(df: pd.DataFrame, config) -> pd.DataFrame:
    """
    Normalize indicators to 0.05 - 1.0 based on thresholds.
    x' = 0.05 + 0.95 * clip((x-lo)/(hi-lo), 0, 1)
    """
    norm_df = df.copy()
    
    for comp, indicators in config.THRESHOLDS.items():
        for ind, (lo, hi) in indicators.items():
            if ind in norm_df.columns:
                val = norm_df[ind]
                
                if ind in config.INVERTED_INDICATORS:
                    # Invert so lower value -> higher risk
                    score = np.clip((hi - val) / (hi - lo), 0, 1)
                else:
                    score = np.clip((val - lo) / (hi - lo), 0, 1)
                    
                norm_df[f"norm_{ind}"] = 0.05 + 0.95 * score
                
    return norm_df
