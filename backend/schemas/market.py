from pydantic import BaseModel

class buyResquest(BaseModel):
    buy_address: str
    buy_level: int
