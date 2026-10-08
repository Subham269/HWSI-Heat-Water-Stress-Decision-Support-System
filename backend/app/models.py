from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class BlockRiskResponse(BaseModel):
    block_id: str
    block_name: str
    district: str
    hwsi: float
    band: str
    rank: int
    h_score: float
    e_score: float
    v_score: float
    heat_hazard: float
    water_stress: float
    stability_pct: float
    # Backward-compatible fields
    hwsi_score: Optional[float] = None
    hazard_score: Optional[float] = None
    exposure_score: Optional[float] = None
    vulnerability_score: Optional[float] = None
    risk_band: Optional[str] = None

class IndicatorDetail(BaseModel):
    name: str
    raw_value: float
    normalized: float
    weight: float
    unit: str
    lens: str # 'heat' | 'water' | 'both'
    data_type: str # 'LIVE' | 'STATIC' | 'PERIODIC' | 'MOCK'
    last_updated: str

class ComponentDetail(BaseModel):
    score: float
    weight: float
    indicators: List[IndicatorDetail]

class BlockComponents(BaseModel):
    h: ComponentDetail
    e: ComponentDetail
    v: ComponentDetail

class BlockExplanation(BaseModel):
    block_id: str
    block_name: str
    district: str
    hwsi: float
    band: str
    rank: int
    total_blocks: int
    stability_pct: float
    components: BlockComponents
    heat_summary: str
    water_summary: str
    people_summary: str
    indicators: List[IndicatorDetail]
    # Backward-compatible fields
    hwsi_score: Optional[float] = None
    data_freshness: Optional[str] = None
    rationale: Optional[str] = None

class AllocationRequest(BaseModel):
    tankers: int
    cooling_units: int
    extra_days: Optional[int] = 0

class BlockAllocation(BaseModel):
    block_id: str
    block_name: str
    district: str
    tankers: int
    cooling_units: int
    need_score: float
    population: float
    rationale: str

class AllocationResult(BaseModel):
    method: str
    total_coverage: float
    allocations: List[BlockAllocation]

class AllocationResponse(BaseModel):
    optimizer: AllocationResult
    baseline_hwsi: AllocationResult
    baseline_proportional: AllocationResult

class DataSource(BaseModel):
    name: str
    type: str # 'LIVE' | 'STATIC' | 'PERIODIC' | 'MOCK'
    last_updated: str
    resolution: str
    source: str

class DataStatusResponse(BaseModel):
    sources: List[DataSource]

class ValidationResponse(BaseModel):
    ahp_cr: float
    top5_stability: Dict[str, float]
    sensitivity_note: str
    backtest_accuracy: Optional[float] = None
    sensitivity_draws: Optional[int] = 100
