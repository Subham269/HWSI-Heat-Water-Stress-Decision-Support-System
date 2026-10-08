import pandas as pd
import json
import os
import numpy as np

def load_all_data(data_dir: str):
    """Load and merge all CSV files."""
    df_map = pd.read_csv(f"{data_dir}/block_id_map.csv")
    
    # Load other datasets
    df_cen = pd.read_csv(f"{data_dir}/census/census_indicators.csv")
    df_gw = pd.read_csv(f"{data_dir}/groundwater/groundwater.csv")
    df_jjm = pd.read_csv(f"{data_dir}/jjm/jjm_coverage.csv")
    df_con = pd.read_csv(f"{data_dir}/contamination/contamination.csv")
    df_hlt = pd.read_csv(f"{data_dir}/health/health_capacity.csv")
    df_res = pd.read_csv(f"{data_dir}/mock/resource_inventory.csv")
    
    # Merge
    df = df_map.merge(df_cen, on='block_id', how='left')
    df = df.merge(df_gw, on='block_id', how='left')
    df = df.merge(df_jjm, on='block_id', how='left')
    df = df.merge(df_con, on='block_id', how='left')
    df = df.merge(df_hlt, on='block_id', how='left')
    df = df.merge(df_res, on='block_id', how='left')
    
    # Add mock weather features directly
    np.random.seed(42)
    df['heat_index'] = np.random.uniform(36, 44, size=len(df))
    df['warm_nights'] = np.random.randint(0, 5, size=len(df))
    df['precip_deficit'] = np.random.uniform(-20, 40, size=len(df))
    df['et'] = np.random.uniform(10, 40, size=len(df))
    df['sm_slope'] = np.random.uniform(-0.08, 0.05, size=len(df))
    df['tmin_ma'] = np.random.uniform(22, 29, size=len(df))
    
    with open(f"{data_dir}/blocks.geojson", "r") as f:
        geojson = json.load(f)
        
    return {"blocks_df": df, "geojson": geojson}
