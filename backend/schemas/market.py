from pydantic import BaseModel

class firstMarketPurchaseRequest(BaseModel):
    event_address: str
    market_address: str
    buyer_address: str
    buy_level: int
    priv_key: str

class secondMarketSaleRequest(BaseModel):
    event_address: str
    market_address: str
    saler_address: str
    priv_key: str
    ticketId: int
    sale_price: int

class secondMarketPurchaseRequest(BaseModel):
    event_address: str
    market_address: str
    buyer_address: str
    ticketId: int
    priv_key: str