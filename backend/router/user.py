from fastapi import APIRouter, HTTPException
from web3 import HTTPProvider, Web3

from schemas.user import UserRequest, userResponse
from crud.user import isNewUser, insertNewUser
from config import config

router = APIRouter()

w3 = Web3(HTTPProvider(config.web3_address))

@router.get("/new-user-bonus", response_model=userResponse)
async def send_tokens(address: str):
    user_address = Web3.to_checksum_address(address)

    if not w3.is_address(user_address):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")
    
    token_contract = w3.eth.contract(address = config.token_contract_address, abi = config.EventToken_abi)

    if isNewUser(user_address):
        balance = token_contract.functions.balanceOf(user_address).call()
        return userResponse(
            is_new_user = False,
            user_address=user_address,
            balance=balance,
            transaction_hash= ""
        )

    transaction_unit_number = 100* (10 ** 18) # 100 token coins 

    nonce = w3.eth.get_transaction_count(config.publisher_account_hash)
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

    insertNewUser(user_address)

    return userResponse(
        is_new_user= True,
        user_address=user_address,
        balance=balance,
        transaction_hash=tx_receipt["transactionHash"].hex()
    )


