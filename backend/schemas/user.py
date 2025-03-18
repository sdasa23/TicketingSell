from pydantic import BaseModel

class UserRequest(BaseModel):
    user_address: str

class userResponse(BaseModel):
    user_address: str
    balance: int
    transaction_hash: str