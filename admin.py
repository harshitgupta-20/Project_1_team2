from fastapi import APIRouter, HTTPException
from schemas.tool import ToolCreate
from schemas.review import ReviewModerate, ReviewStatus



router = APIRouter(prefix="/admin", tags=["Admin"])


# -------------------------------------------------
# 1️⃣ Admin: View ALL reviews
# -------------------------------------------------
@router.get("/reviews")
def get_all_reviews():
    """
    Admin can view all reviews (approved, denied, pending)
    """
    return reviews


# -------------------------------------------------
# 2️⃣ Admin: View ONLY pending reviews
# -------------------------------------------------
@router.get("/reviews/pending")
def get_pending_reviews():
    """
    Admin can view reviews that are waiting for approval
    """
    return [r for r in reviews if r["status"] == "pending"]


# -------------------------------------------------
# 3️⃣ Admin: Add a new AI tool
# -------------------------------------------------
@router.post("/tools")
def add_tool(tool: ToolCreate):
    new_tool = {
        "id": data.tool_id_counter,
        "name": tool.name,
        "use_case": tool.use_case,
        "category": tool.category,
        "pricing_type": tool.pricing_type,
        "rating": 0.0
    }

    data.tool_id_counter += 1
    tools.append(new_tool)

    return {
        "message": "Tool added successfully",
        "tool": new_tool
    }


# -------------------------------------------------
# 4️⃣ Admin: Approve or Deny a review
# -------------------------------------------------
@router.put("/reviews/{review_id}")
def moderate_review(review_id: int, payload: ReviewModerate):

    review = next((r for r in reviews if r["id"] == review_id), None)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review["status"] = payload.status

    # ✅ Recalculate rating ONLY if approved
    if payload.status == ReviewStatus.approved:
        approved_ratings = [
            r["rating"]
            for r in reviews
            if r["tool_id"] == review["tool_id"]
            and r["status"] == ReviewStatus.approved
        ]

        tool = next(t for t in tools if t["id"] == review["tool_id"])
        tool["rating"] = round(
            sum(approved_ratings) / len(approved_ratings), 2
        )

    return {
        "message": "Review moderated successfully",
        "review_id": review_id,
        "status": payload.status
    }
