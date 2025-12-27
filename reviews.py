from fastapi import APIRouter, HTTPException
from schemas.review import ReviewCreate


router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/")
def submit_review(review: ReviewCreate):
    tool = next((t for t in tools if t["id"] == review.tool_id), None)

    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    new_review = {
        "id": data.review_id_counter,
        "tool_id": review.tool_id,
        "rating": review.rating,
        "comment": review.comment,
        "status": "pending"
    }

    data.review_id_counter += 1
    reviews.append(new_review)

    return {"message": "Review submitted and pending approval"}
