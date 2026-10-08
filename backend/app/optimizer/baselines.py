import pandas as pd
import numpy as np
import app.config as config

def compute_baselines(blocks_df: pd.DataFrame, resource_type: str, total_units: int) -> dict:
    """Compute baseline allocations."""
    params = config.ALLOCATION_PARAMS[resource_type]
    k_r = params["k_r"]
    a = params["a"]
    b = params["b"]
    
    df = blocks_df.copy()
    df['need'] = (df['hazard_score'] ** a) * (df['vulnerability_score'] ** b)
    df = df.sort_values(by='hwsi_score', ascending=False)
    
    # Baseline 1: Highest-HWSI-first
    b1_alloc = {b: 0 for b in df['block_id']}
    units_left = total_units
    for b_id in df['block_id']:
        if units_left > 0:
            b1_alloc[b_id] = 1
            units_left -= 1
            
    # Calculate benefit for B1
    b1_covered = 0
    for b_id, u in b1_alloc.items():
        if u > 0:
            row = df[df['block_id'] == b_id].iloc[0]
            b1_covered += row['total_population'] * row['need'] * (1 - np.exp(-k_r * u))
            
    # Baseline 2: Proportional
    total_pop_need = (df['total_population'] * df['need']).sum()
    b2_alloc = {b: 0 for b in df['block_id']}
    
    for _, row in df.iterrows():
        b_id = row['block_id']
        share = (row['total_population'] * row['need']) / total_pop_need
        # Round to int, ensure we don't exceed total
        b2_alloc[b_id] = int(np.round(share * total_units))
        
    b2_covered = 0
    for b_id, u in b2_alloc.items():
        if u > 0:
            row = df[df['block_id'] == b_id].iloc[0]
            b2_covered += row['total_population'] * row['need'] * (1 - np.exp(-k_r * u))
            
    return {
        "highest_hwsi": {"allocations": b1_alloc, "total_benefit_covered": b1_covered},
        "proportional": {"allocations": b2_alloc, "total_benefit_covered": b2_covered}
    }
