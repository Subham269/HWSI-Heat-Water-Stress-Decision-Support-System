import pandas as pd
import numpy as np

def compute_heat_index(tmax_c: float, rh_pct: float) -> float:
    """Calculate Heat Index using NWS Rothfusz regression equation."""
    t_f = tmax_c * 9.0 / 5.0 + 32.0
    rh = max(0.0, min(100.0, rh_pct))
    
    hi_f = (
        -42.379
        + 2.04901523 * t_f
        + 10.14333127 * rh
        - 0.22475541 * t_f * rh
        - 6.83783e-3 * (t_f ** 2)
        - 5.481717e-2 * (rh ** 2)
        + 1.22874e-3 * (t_f ** 2) * rh
        + 8.5282e-4 * t_f * (rh ** 2)
        - 1.99e-6 * (t_f ** 2) * (rh ** 2)
    )
    # Convert back to Celsius
    hi_c = (hi_f - 32.0) * 5.0 / 9.0
    return round(float(hi_c), 2)

def compute_warm_nights(tmin_list: list, threshold=22.0) -> int:
    """Count consecutive warm nights exceeding threshold (default 22.0°C for WB autumn climate)."""
    consecutive = 0
    max_consecutive = 0
    for t in tmin_list:
        if t >= threshold:
            consecutive += 1
            max_consecutive = max(max_consecutive, consecutive)
        else:
            consecutive = 0
    return max_consecutive

def compute_soil_moisture_slope(sm_list: list) -> float:
    """Compute rate of soil moisture depletion (drying rate slope)."""
    if len(sm_list) < 2:
        return 0.0
    x = np.arange(len(sm_list))
    y = np.array(sm_list)
    slope = float(np.polyfit(x, y, 1)[0])
    return round(slope, 4)

def calculate_weather_features_for_block(daily_forecast: dict, extra_days: int = 0) -> dict:
    """
    Extract PRD Section 7 derived environmental features from daily forecast.
    extra_days (0 to 2) simulates compounding heat and water stress progression.
    """
    horizon = 5

    tmax_vals = daily_forecast.get("temperature_2m_max", [38.0] * horizon)[:horizon]
    tmin_vals = daily_forecast.get("temperature_2m_min", [26.0] * horizon)[:horizon]
    rh_vals = daily_forecast.get("relative_humidity_2m_max", [60.0] * horizon)[:horizon]
    precip_vals = daily_forecast.get("precipitation_sum", [0.0] * horizon)[:horizon]
    et_vals = daily_forecast.get("et0_fao_evapotranspiration", [5.5] * horizon)[:horizon]
    sm_vals = daily_forecast.get("soil_moisture_0_to_7cm_mean", [0.20] * horizon)[:horizon]

    # Baseline derived features
    max_t = float(np.max(tmax_vals))
    mean_rh = float(np.mean(rh_vals))
    base_hi = compute_heat_index(max_t, mean_rh)
    base_wn = compute_warm_nights(tmin_vals, threshold=22.0)
    
    tot_precip = float(np.sum(precip_vals))
    base_precip_def = round(float((25.0 - tot_precip) / 25.0 * 100.0), 2)
    base_et = round(float(np.sum(et_vals)), 2)
    base_sm_slope = compute_soil_moisture_slope(sm_vals)
    base_tmin_ma = round(float(pd.Series(tmin_vals).rolling(3, min_periods=1).mean().max()), 2)

    if extra_days > 0:
        # PRD §12: Compounding heatwave & drying stress over extended duration (+1 to +2 days)
        heat_index = round(base_hi + 1.5 * extra_days, 2)
        warm_nights = min(5, base_wn + (extra_days if base_wn > 0 or extra_days >= 2 else 0))
        precip_deficit = min(100.0, round(base_precip_def + 4.0 * extra_days, 2))
        cum_et = round(base_et * (1.0 + 0.15 * extra_days), 2)
        sm_slope = round(base_sm_slope - 0.005 * extra_days, 4)
        tmin_ma = round(base_tmin_ma + 0.5 * extra_days, 2)
    else:
        heat_index = base_hi
        warm_nights = base_wn
        precip_deficit = base_precip_def
        cum_et = base_et
        sm_slope = base_sm_slope
        tmin_ma = base_tmin_ma
    
    return {
        "heat_index": heat_index,
        "warm_nights": warm_nights,
        "precip_deficit": precip_deficit,
        "et": cum_et,
        "sm_slope": sm_slope,
        "tmin_ma": tmin_ma
    }
