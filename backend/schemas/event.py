from pydantic import BaseModel
from typing import List

class eventRequest(BaseModel):
    festName: str
    festSymbol: str
    maxTicketLevel: int
    ticketPriceList: List[int]
    ticketSupplyList: List[int]
    organiser: str
    priv_key: str

class eventResponse(BaseModel):
    event_address: str
    market_address: str

class searchEventInfResponse(BaseModel):
    maxTicketLevel: int