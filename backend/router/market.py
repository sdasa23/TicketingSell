from fastapi import APIRouter
from config import config
from web3 import Web3, HTTPProvider

from schemas.market import firstMarketPurchaseRequest, secondMarketSaleRequest, secondMarketPurchaseRequest

router = APIRouter()

w3 = Web3(HTTPProvider(config.web3_address))

@router.post("/first-market/purchase")
async def purchaseTicket(request: firstMarketPurchaseRequest):
    checksum_address = Web3.to_checksum_address(request.market_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventMarketplace_abi)
    nonce = w3.eth.get_transaction_count(request.buyer_address)
    
    transaction = contract.functions.purchaseTicket(request.buy_level).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    EventNTF_contract = w3.eth.contract(abi=config.EventNFT_abi, address=request.event_address)
    ticketId_recently = EventNTF_contract.functions.getUnsoldTicketID(request.buy_level).call() - 1
    return ticketId_recently


@router.post("/second-market/sale")
async def saleTicket(request: secondMarketSaleRequest):
    checksum_address = Web3.to_checksum_address(request.event_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventNFT_abi)
    nonce = w3.eth.get_transaction_count(request.saler_address)
    
    transaction = contract.functions.setSaleDetails(request.ticketId, request.sale_price, request.market_address).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    #approve this tickets to market
    nonce = w3.eth.get_transaction_count(request.saler_address, 'pending') 

    transaction = contract.functions.approve(request.market_address, request.ticketId).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return True

@router.post("/second-market/purchase" )
async def secondaryPurchase(request: secondMarketPurchaseRequest):
    checksum_address = Web3.to_checksum_address(request.market_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventMarketplace_abi)
    nonce = w3.eth.get_transaction_count(request.buyer_address)
    
    transaction = contract.functions.secondaryPurchase(request.ticketId).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    EventNTF_contract = w3.eth.contract(abi=config.EventNFT_abi, address=request.event_address)
    owner_address = EventNTF_contract.functions.ownerOf(request.ticketId).call()
    if owner_address == request.buyer_address:
        return request.ticketId
    else:
        return False




