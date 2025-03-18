from fastapi import APIRouter

router = APIRouter()

@router.post("/buy-ticket" )
async def buy_a_ticket():
    return {}