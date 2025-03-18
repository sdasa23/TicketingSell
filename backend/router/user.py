from fastapi import APIRouter, HTTPException
from web3 import HTTPProvider, Web3

from schemas.user import UserRequest, userResponse
from config import config

router = APIRouter()

w3 = Web3(HTTPProvider(config.web3_address))

@router.post("/new-user-bonus", response_model=userResponse)
async def send_tokens(request: UserRequest):
    user_address = request.user_address
    transaction_unit_number = 100* (10 ** 18) # five token coin 

    if not w3.is_address(user_address):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")
    
    nonce = w3.eth.get_transaction_count(config.publisher_account_hash)
    token_contract = w3.eth.contract(address = config.token_contract_address, abi = config.FestToken_abi)

    transaction = token_contract.functions.transfer(user_address, transaction_unit_number).build_transaction({
        "chainId": config.chain_id,
        "gas": 200000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=config.userKey)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    balance = token_contract.functions.balanceOf(user_address).call()

    return userResponse(
        user_address=user_address,
        balance=balance,
        transaction_hash=tx_receipt["transactionHash"].hex()
    )
