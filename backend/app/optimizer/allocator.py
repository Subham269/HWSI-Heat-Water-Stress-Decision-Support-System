import pandas as pd
import numpy as np
import app.config as config

def optimize_allocation(blocks_df: pd.DataFrame, resource_type: str, total_units: int) -> dict:
    """Greedy allocation using marginal benefit."""
    params = config.ALLOCATION_PARAMS[resource_type]
    k_r = params["k_r"]
    a = params["a"]
    b = params["b"]
    
    df = blocks_df.copy()
    
    # Calculate Need_i^r = H^a * V^b
    df['need'] = (df['hazard_score'] ** a) * (df['vulnerability_score'] ** b)
    
    allocations = {block: 0 for block in df['block_id']}
    
    # Marginal benefit: B(u+1) - B(u)
    # B(u) = Pop * Need * [1 - exp(-k_r * u)]
    def marginal_benefit(pop, need, u):
        b_u = pop * need * (1 - np.exp(-k_r * u))
        b_u1 = pop * need * (1 - np.exp(-k_r * (u + 1)))
        return b_u1 - b_u
        
    for _ in range(total_units):
        best_block = None
        best_mb = -1
        
        for idx, row in df.iterrows():
            b_id = row['block_id']
            u = allocations[b_id]
            mb = marginal_benefit(row['total_population'], row['need'], u)
            
            if mb > best_mb:
                best_mb = mb
                best_block = b_id
                
        if best_block:
            allocations[best_block] += 1
            
    # Calculate total covered
    covered = 0
    for b_id, u in allocations.items():
        if u > 0:
            row = df[df['block_id'] == b_id].iloc[0]
            covered += row['total_population'] * row['need'] * (1 - np.exp(-k_r * u))
            
    return {
        "allocations": allocations,
        "total_benefit_covered": covered
    }
