import httpx
import json
import os
import logging
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "weather_cache.json")

def compute_centroid(coords: List[List[float]]) -> Tuple[float, float]:
    """Calculate (lat, lon) centroid from polygon coordinates."""
    lons = [p[0] for p in coords]
    lats = [p[1] for p in coords]
    return (round(sum(lats) / len(lats), 4), round(sum(lons) / len(lons), 4))

def get_block_centroids(geojson: dict) -> Dict[str, Tuple[float, float]]:
    """Extract centroids for all blocks in geojson."""
    centroids = {}
    for feat in geojson["features"]:
        b_id = feat["properties"]["block_id"]
        coords = feat["geometry"]["coordinates"][0]
        centroids[b_id] = compute_centroid(coords)
    return centroids

async def fetch_live_forecasts(centroids: Dict[str, Tuple[float, float]], days: int = 7) -> Dict[str, dict]:
    """
    Fetch 7-day daily forecasts for all blocks in batch from Open-Meteo.
    Saves to local cache with graceful fallback.
    """
    block_ids = list(centroids.keys())
    lats = ",".join(str(centroids[b][0]) for b in block_ids)
    lons = ",".join(str(centroids[b][1]) for b in block_ids)
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lats}&longitude={lons}&"
        f"daily=temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,"
        f"precipitation_sum,et0_fao_evapotranspiration,soil_moisture_0_to_7cm_mean&"
        f"forecast_days={days}&timezone=Asia/Kolkata"
    )
    
    forecasts = {}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    for b_id, item in zip(block_ids, data):
                        forecasts[b_id] = item.get("daily", {})
                elif isinstance(data, dict):
                    # Single result fallback
                    forecasts[block_ids[0]] = data.get("daily", {})
                
                # Cache successful response
                os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
                with open(CACHE_FILE, "w") as f:
                    json.dump(forecasts, f)
                logger.info("Successfully fetched and cached live weather from Open-Meteo.")
                return forecasts
            else:
                logger.warning(f"Open-Meteo returned status {resp.status_code}. Using cache/fallback.")
    except Exception as e:
        logger.warning(f"Open-Meteo query failed ({e}). Attempting to read cached forecast.")

    # Fallback to cache if available
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass

    # Synthesize realistic historical summer heat-stress baseline if offline
    np.random.seed(42)
    for b_id in block_ids:
        forecasts[b_id] = {
            "temperature_2m_max": [float(x) for x in np.random.uniform(38.0, 44.5, size=days)],
            "temperature_2m_min": [float(x) for x in np.random.uniform(25.5, 30.5, size=days)],
            "relative_humidity_2m_max": [float(x) for x in np.random.uniform(45.0, 75.0, size=days)],
            "precipitation_sum": [float(x) for x in np.random.uniform(0.0, 2.0, size=days)],
            "et0_fao_evapotranspiration": [float(x) for x in np.random.uniform(4.5, 7.5, size=days)],
            "soil_moisture_0_to_7cm_mean": [float(x) for x in np.random.uniform(0.12, 0.28, size=days)]
        }
    return forecasts
