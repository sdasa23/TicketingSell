from fastapi import FastAPI, HTTPException
from initial_ticketing_platform import initial_env
from web3 import HTTPProvider,Web3
import json
from pydantic import BaseModel

app = FastAPI()

web3_address = 'http://127.0.0.1:8545'
publisher_account_hash = '0xC459cc3AC9f8462Be2EF00aAD02fAc7af2e97b14'
userKey = '0xda09f8cdec20b7c8334ce05b27e6797bef01c1ad79c59381666467552c5012e3'
chain_id = 1337
# token_contract_address = initial_env(web3_address,chain_id, publisher_account_hash, userKey)
token_contract_address = "0x21107f38881CC98802EA490d967E3469F8973Dc0"

w3 = Web3(HTTPProvider(web3_address))
with open("compiled_code.json", "r") as file:
    compiled_sol = json.load(file)

FestToken_bytecode = compiled_sol["contracts"]["FestToken.sol"]["FestToken"]["evm"]["bytecode"]["object"]
FestToken_abi = compiled_sol["contracts"]["FestToken.sol"]["FestToken"]["abi"]
# token_contract = w3.eth.contract(abi=FestToken_abi, bytecode=FestToken_bytecode)
token_contract = w3.eth.contract(address = token_contract_address, abi=FestToken_abi)

FestivalNFT_bytecode = compiled_sol["contracts"]["FestivalNFT.sol"]["FestivalNFT"]["evm"]["bytecode"]["object"]
FestivalNFT_abi = compiled_sol["contracts"]["FestivalNFT.sol"]["FestivalNFT"]["abi"]
festivalNTF_contract = w3.eth.contract(abi=FestivalNFT_abi, bytecode=FestivalNFT_bytecode)

FestivalMarketplace_bytecode = compiled_sol["contracts"]["FestivalMarketplace.sol"]["FestivalMarketplace"]["evm"]["bytecode"]["object"]
FestivalMarketplace_abi = compiled_sol["contracts"]["FestivalMarketplace.sol"]["FestivalMarketplace"]["abi"]
market_contract = w3.eth.contract(abi=FestivalMarketplace_abi, bytecode=FestivalMarketplace_bytecode)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q":q}

# @app.get("/items/{item_id}")
# def create_event(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q":q}

class UserRequest(BaseModel):
    user_address: str

class userResponse(BaseModel):
    user_address: str
    balance: int
    transaction_hash: str

@app.post("/new-user-bonus", response_model=userResponse)
async def send_tokens(request: UserRequest):
    user_address = request.user_address
    transaction_unit_number = 10 ** 18 # one FEST 

    if not w3.is_address(user_address):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")
    
    nonce = w3.eth.get_transaction_count(publisher_account_hash)

    transaction = token_contract.functions.transfer(user_address, transaction_unit_number).build_transaction({
        "chainId": chain_id,
        "gas": 200000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=userKey)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    balance = token_contract.functions.balanceOf(user_address).call()

    return userResponse(
        user_address=user_address,
        balance=balance,
        transaction_hash=tx_receipt["transactionHash"].hex()
    )

# async def send_tokens(request: UserRequest):