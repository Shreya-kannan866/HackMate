from fastapi import APIRouter

router = APIRouter(prefix="/reputation", tags=["Reputation"])

@router.get("/")
def get_reputation():
    return {"reputation": 0}