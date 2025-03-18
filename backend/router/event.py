from fastapi import APIRouter
from web3 import HTTPProvider,Web3

from schemas.event import eventRequest, eventResponse, searchEventInfResponse
from config import config

router = APIRouter()

w3 = Web3(HTTPProvider(config.web3_address))

@router.post("/create-new-event", response_model = eventResponse)
async def create_event(request: eventRequest):
    publisher_address = request.organiser

    nonce = w3.eth.get_transaction_count(publisher_address)
    festivalNTF_contract = w3.eth.contract(abi=config.FestivalNFT_abi, bytecode=config.FestivalNFT_bytecode)

    transaction = festivalNTF_contract.constructor(request.festName, request.festSymbol, request.maxTicketLevel, 
                                                   request.ticketPriceList, request.ticketSupplyList, request.organiser).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce,
        "from": request.organiser
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    event_address = tx_receipt["contractAddress"]
    
    #create ticket market of this event
    
    nonce = w3.eth.get_transaction_count(publisher_address)
    market_contract = w3.eth.contract(abi=config.FestivalMarketplace_abi, bytecode=config.FestivalMarketplace_bytecode)

    transaction = market_contract.constructor(config.token_contract_address, event_address).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce,
        "from": request.organiser
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    market_address = tx_receipt["contractAddress"]

    return eventResponse(
        event_address = event_address,
        market_address = market_address
    )

@router.get("/search-event/{event_address}", response_model = searchEventInfResponse)
async def responseEventInf(event_address: str):
    max_level = await searchEventMaxLevel(event_address)
    return searchEventInfResponse(
        maxTicketLevel=max_level
    )






async def searchEventMaxLevel(event_address: str):
    checksum_address = Web3.to_checksum_address(event_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.FestivalNFT_abi)
    level = contract.functions.getMaxTicketLevel().call()
    return level 
