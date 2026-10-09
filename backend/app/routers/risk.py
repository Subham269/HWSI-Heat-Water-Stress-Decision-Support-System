from fastapi import APIRouter, Request
from typing import List
import pandas as pd
from app.models import BlockRiskResponse
from app.engine.hwsi import get_scenario_hwsi_df

router = APIRouter()

@router.get("/api/v1/blocks/risk-index", response_model=List[BlockRiskResponse])
def get_risk_index(request: Request, extra_days: int = 0):
    df = get_scenario_hwsi_df(request.app.state, extra_days)
    if df is None:
        df = request.app.state.hwsi_df
        
    stability_dict = getattr(request.app.state, 'stability_map', {})
    
    results = []
    for _, row in df.iterrows():
        b_id = row['block_id']
        stab = float(stability_dict.get(b_id, 0.75))
        hwsi_val = float(row['hwsi_score'])
        h_val = float(row['hazard_score'])
        e_val = float(row['exposure_score'])
        v_val = float(row['vulnerability_score'])
        heat_h = float(row['heat_hazard']) if 'heat_hazard' in row else h_val
        water_s = float(row['water_stress']) if 'water_stress' in row else (h_val + v_val) / 2.0
        band_val = str(row['risk_band'])
        
        results.append(BlockRiskResponse(
            block_id=b_id,
            block_name=row['block_name'],
            district=row['district'],
            hwsi=hwsi_val,
            band=band_val,
            rank=int(row['rank']),
            h_score=h_val,
            e_score=e_val,
            v_score=v_val,
            heat_hazard=heat_h,
            water_stress=water_s,
            stability_pct=stab,
            # Backward-compatible fields
            hwsi_score=hwsi_val,
            hazard_score=h_val,
            exposure_score=e_val,
            vulnerability_score=v_val,
            risk_band=band_val
        ))
    return results

@router.get("/api/v1/blocks.geojson")
def get_geojson(request: Request):
    return request.app.state.geojson
