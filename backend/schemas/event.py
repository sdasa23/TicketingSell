from pydantic import BaseModel
from typing import List

class eventRequest(BaseModel):
    festName: str
    festSymbol: str
    maxTicketLevel: int
    ticketPriceList: List[int]
    ticketSupplyList: List[int]
    organiser: str

class mintTicketsRequest(BaseModel):
    event_address: str
    organiser: str
    priv_key: str
    level: int
    ticketNumber: int 

class eventResponse(BaseModel):
    event_address: str
    market_address: str

class searchEventInfResponse(BaseModel):
    organizer: str
    name: str
    symbol: str
    maxTicketLevel: int
    ticketPriceList: List[int]
    ticketSupplyList: List[int]

class searchEventStatusResponse(BaseModel):
    currentTicketIds: int
    ticketsForSale: List[int]
    ticketExistCounterList: List[int]
    ticketSoldtCounterList: List[int]
