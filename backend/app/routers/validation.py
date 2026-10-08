from fastapi import APIRouter, Request
from app.models import ValidationResponse

router = APIRouter()

@router.get("/api/v1/validation", response_model=ValidationResponse)
def get_validation(request: Request):
    return request.app.state.validation_results
