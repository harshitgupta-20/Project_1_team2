from fastapi import APIRouter, Query
from typing import Optional
router = APIRouter(prefix="/tools", tags=["Tools"])

@router.get("/")
def get_tools(
    category: Optional[str] = None,
    pricing_type: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=1, le=5)
):
    
    result=tools
    if category:
        result=[t for t in result if t['category']==category]


    if pricing_type:
        result=[t for t in result if t['pricing_type']==pricing_type]

    if min_rating:
        result=[t for t in result if t['rating']==min_rating]
    
    return result
