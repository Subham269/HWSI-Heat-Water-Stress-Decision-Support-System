import pandas as pd
import numpy as np
from app.engine.normalize import normalize_indicators
from app.engine.ahp import get_weights_from_config
import app.config as config

def compute_hwsi(blocks_df: pd.DataFrame) -> pd.DataFrame:
    """Compute HWSI and component scores."""
    
    weights, _ = get_weights_from_config(config)
    
    norm_df = normalize_indicators(blocks_df, config)
    result = norm_df.copy()
    
    # Compute component scores
    for comp in ["hazard", "exposure", "vulnerability"]:
        inds = config.INDICATOR_NAMES[comp]
        w = weights[comp]
        
        # Weighted mean of normalized indicators
        cols = [f"norm_{i}" for i in inds if f"norm_{i}" in norm_df.columns]
        if cols:
            vals = norm_df[cols].values
            w_sub = w[:len(cols)]
            w_sub = w_sub / w_sub.sum()
            result[f"{comp}_score"] = np.average(vals, axis=1, weights=w_sub)
        else:
            result[f"{comp}_score"] = 0.5

    # Geometric aggregation HWSI = H^wh * E^we * V^wv
    w_comp = weights["components"]
    h = result["hazard_score"]
    e = result["exposure_score"]
    v = result["vulnerability_score"]
    
    result["hwsi_score"] = (h**w_comp[0]) * (e**w_comp[1]) * (v**w_comp[2])
    
    # Calculate lens sub-scores per PRD §3
    heat_cols = [c for c in ["norm_heat_index", "norm_warm_nights", "norm_tmin_ma"] if c in norm_df.columns]
    if heat_cols:
        result["heat_hazard"] = norm_df[heat_cols].mean(axis=1)
    else:
        result["heat_hazard"] = result["hazard_score"]

    water_cols = [c for c in ["norm_precip_deficit", "norm_et", "norm_sm_slope", "norm_pct_piped_coverage", "norm_extraction_pct", "norm_arsenic_affected", "norm_fluoride_affected"] if c in norm_df.columns]
    if water_cols:
        result["water_stress"] = norm_df[water_cols].mean(axis=1)
    else:
        result["water_stress"] = (result["hazard_score"] + result["vulnerability_score"]) / 2.0

    # Assign bands
    def get_band(score):
        if score < config.BANDS["low"]: return "Low"
        elif score < config.BANDS["moderate"]: return "Moderate"
        elif score < config.BANDS["high"]: return "High"
        else: return "Very High"
        
    result["risk_band"] = result["hwsi_score"].apply(get_band)
    result["rank"] = result["hwsi_score"].rank(ascending=False, method="min").astype(int)
    
    return result

def get_scenario_hwsi_df(app_state, extra_days: int = 0) -> pd.DataFrame:
    """Retrieve or dynamically compute HWSI dataframe for given extra_days scenario (0, 1, 2)."""
    if extra_days <= 0:
        return getattr(app_state, 'hwsi_df', None)
    
    cache_key = f"hwsi_df_extra_{extra_days}"
    cached_df = getattr(app_state, cache_key, None)
    if cached_df is not None:
        return cached_df
        
    raw_data = getattr(app_state, 'raw_data', None)
    if not raw_data:
        return getattr(app_state, 'hwsi_df', None)
        
    from app.engine.etl import calculate_weather_features_for_block
    df_base = raw_data["blocks_df"].copy()
    forecasts = raw_data.get("forecasts", {})
    
    weather_rows = []
    for b_id in df_base['block_id']:
        f_data = forecasts.get(b_id, {})
        w_feats = calculate_weather_features_for_block(f_data, extra_days=extra_days)
        w_feats['block_id'] = b_id
        weather_rows.append(w_feats)
        
    df_weather = pd.DataFrame(weather_rows)
    weather_cols = ["heat_index", "warm_nights", "precip_deficit", "et", "sm_slope", "tmin_ma"]
    df_base = df_base.drop(columns=[c for c in weather_cols if c in df_base.columns])
    df_base = df_base.merge(df_weather, on='block_id', how='left')
    scenario_df = compute_hwsi(df_base)
    setattr(app_state, cache_key, scenario_df)
    return scenario_df
