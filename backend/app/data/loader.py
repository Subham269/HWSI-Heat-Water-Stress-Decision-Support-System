import pandas as pd
import json
import os
import logging
from app.data.weather import get_block_centroids, fetch_live_forecasts
from app.engine.etl import calculate_weather_features_for_block

logger = logging.getLogger(__name__)

async def load_all_data(data_dir: str, extra_days: int = 0):
    """Load, merge datasets, and compute environmental features from live forecasts."""
    df_map = pd.read_csv(f"{data_dir}/block_id_map.csv")
    
    # Load ground truth tables
    df_cen = pd.read_csv(f"{data_dir}/census/census_indicators.csv")
    df_gw = pd.read_csv(f"{data_dir}/groundwater/groundwater.csv")
    df_jjm = pd.read_csv(f"{data_dir}/jjm/jjm_coverage.csv")
    df_con = pd.read_csv(f"{data_dir}/contamination/contamination.csv")
    df_hlt = pd.read_csv(f"{data_dir}/health/health_capacity.csv")
    df_res = pd.read_csv(f"{data_dir}/mock/resource_inventory.csv")
    
    # Merge static and periodic baselines
    df = df_map.merge(df_cen, on='block_id', how='left')
    df = df.merge(df_gw, on='block_id', how='left')
    df = df.merge(df_jjm, on='block_id', how='left')
    df = df.merge(df_con, on='block_id', how='left')
    df = df.merge(df_hlt, on='block_id', how='left')
    df = df.merge(df_res, on='block_id', how='left')
    
    with open(f"{data_dir}/blocks.geojson", "r") as f:
        geojson = json.load(f)
        
    centroids = get_block_centroids(geojson)
    forecasts = await fetch_live_forecasts(centroids, days=7)
    
    # Apply ETL transforms for each block based on forecast window
    weather_rows = []
    for b_id in df['block_id']:
        f_data = forecasts.get(b_id, {})
        w_feats = calculate_weather_features_for_block(f_data, extra_days=extra_days)
        w_feats['block_id'] = b_id
        weather_rows.append(w_feats)
        
    df_weather = pd.DataFrame(weather_rows)
    df = df.merge(df_weather, on='block_id', how='left')
    
    return {
        "blocks_df": df,
        "geojson": geojson,
        "forecasts": forecasts,
        "centroids": centroids
    }
