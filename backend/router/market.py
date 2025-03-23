from fastapi import APIRouter
from config import config
from web3 import Web3, HTTPProvider

from schemas.market import firstMarketPurchaseRequest, secondMarketSaleRequest, secondMarketPurchaseRequest
from crud.market import insertNewTicketForSale, getMarketAddress, getAllTicketOnsale, deleteSoldTicket

router = APIRouter()

w3 = Web3(HTTPProvider(config.web3_address))

@router.post("/first-market/purchase")
async def purchaseTicket(request: firstMarketPurchaseRequest):
    request.market_address = Web3.to_checksum_address(request.market_address)
    request.event_address = Web3.to_checksum_address(request.event_address)
    request.buyer_address = Web3.to_checksum_address(request.buyer_address)
    checksum_address = Web3.to_checksum_address(request.market_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventMarketplace_abi)
    nonce = w3.eth.get_transaction_count(config.admin_address)
    
    transaction = contract.functions.purchaseTicket(request.buy_level, request.buyer_address).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= config.admin_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    event_checksum_address = Web3.to_checksum_address(request.event_address)
    EventNTF_contract = w3.eth.contract(address=event_checksum_address, abi=config.EventNFT_abi)
    ticketId_recently = EventNTF_contract.functions.getUnsoldTicketID(request.buy_level).call() - 1
    return ticketId_recently


@router.post("/second-market/sale")
async def saleTicket(request: secondMarketSaleRequest):
    checksum_address = Web3.to_checksum_address(request.event_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventNFT_abi)
    nonce = w3.eth.get_transaction_count(config.admin_address)
    market_address = getMarketAddress(checksum_address)
    transaction = contract.functions.setSaleDetails(request.ticketId, request.sale_price, market_address).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= config.admin_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    request.saler_address = Web3.to_checksum_address(request.saler_address)
    insertNewTicketForSale(checksum_address, request.ticketId, market_address, request.saler_address, request.sale_price )
    
    return market_address

@router.post("/second-market/purchase" )
async def secondaryPurchase(request: secondMarketPurchaseRequest):
    request.market_address = Web3.to_checksum_address(request.market_address)
    request.buyer_address = Web3.to_checksum_address(request.buyer_address)
    request.event_address = Web3.to_checksum_address(request.event_address)

    contract = w3.eth.contract(address=request.market_address, abi=config.EventMarketplace_abi)
    nonce = w3.eth.get_transaction_count(config.admin_address)
    
    transaction = contract.functions.secondaryPurchase(request.ticketId, request.buyer_address).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= config.admin_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    EventNTF_contract = w3.eth.contract(abi=config.EventNFT_abi, address=request.event_address)
    owner_address = EventNTF_contract.functions.ownerOf(request.ticketId).call()
    if owner_address == request.buyer_address:
        deleteSoldTicket(request.event_address, request.ticketId)
        return request.ticketId
    else:
        return False

@router.get("/get-event-market-address")
async def getEventMarketAddress(eventAddress: str):
    eventAddress = Web3.to_checksum_address(eventAddress)
    return getMarketAddress(eventAddress)
    
@router.get("/get-all-tickets-on-sale")
async def getTicketOnsale():
    return getAllTicketOnsale()