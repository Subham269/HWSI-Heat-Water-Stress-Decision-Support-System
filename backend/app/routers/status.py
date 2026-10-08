from fastapi import APIRouter
from typing import List
from app.models import DataSource

router = APIRouter()

@router.get("/api/v1/data-status", response_model=List[DataSource])
def get_data_status():
    return [
        DataSource(name="Weather Forecast (Open-Meteo)", type="LIVE", last_updated="2026-10-08T06:00:00Z", resolution="CD Block Centroid", source="Open-Meteo API"),
        DataSource(name="Demographics & Workers", type="STATIC", last_updated="2011-03-01T00:00:00Z", resolution="CD Block (Census PCA)", source="Census of India 2011"),
        DataSource(name="Groundwater Stage of Extraction", type="PERIODIC", last_updated="2023-11-15T00:00:00Z", resolution="CD Block", source="CGWB / India-WRIS"),
        DataSource(name="Piped Water Coverage (FHTC)", type="PERIODIC", last_updated="2024-03-01T00:00:00Z", resolution="CD Block", source="Jal Jeevan Mission Dashboard"),
        DataSource(name="Arsenic & Fluoride Flags", type="STATIC", last_updated="2023-01-01T00:00:00Z", resolution="CD Block", source="WB Public Health Engineering Dept"),
        DataSource(name="Hospital Beds & Health Capacity", type="MOCK", last_updated="2026-10-08T00:00:00Z", resolution="District Broadcast", source="National Health Mission (Proxy)"),
        DataSource(name="Resource Inventory (Tankers/ORS)", type="MOCK", last_updated="2026-10-08T00:00:00Z", resolution="CD Block", source="Simulated District Store")
    ]
