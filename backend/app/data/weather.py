import httpx
import pandas as pd
from typing import List, Tuple

async def fetch_forecast(centroids: List[Tuple[float, float]]) -> pd.DataFrame:
    """
    Fetch weather forecast from Open-Meteo.
    Mocking this for the hackathon to avoid rate limits, 
    but leaving the structure.
    """
    # Mock response
    return pd.DataFrame()
