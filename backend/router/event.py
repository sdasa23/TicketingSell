from fastapi import APIRouter, HTTPException
from web3 import HTTPProvider,Web3

from schemas.event import eventRequest, eventResponse, searchEventInfResponse, searchEventStatusResponse, mintTicketsRequest
from config import config
from crud.event import insertNewEvent, getAllEvents
router = APIRouter()

w3 = Web3(HTTPProvider(config.web3_address))

@router.post("/create-new-event", response_model = eventResponse)
async def create_event(request: eventRequest):
    nonce = w3.eth.get_transaction_count(config.admin_address, 'pending')
    EventNTF_contract = w3.eth.contract(abi=config.EventNFT_abi, bytecode=config.EventNFT_bytecode)
    request.organiser = Web3.to_checksum_address(request.organiser)

    if not w3.is_address(request.organiser):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")
    
    transaction = EventNTF_contract.constructor(request.festName, request.festSymbol, request.maxTicketLevel, 
                                                   request.ticketPriceList, request.ticketSupplyList, request.organiser).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce,
        "from": config.admin_address
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= config.admin_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    event_address = tx_receipt["contractAddress"]
    
    #create ticket market of this event
    nonce = w3.eth.get_transaction_count(config.admin_address, 'pending')
    market_contract = w3.eth.contract(abi=config.EventMarketplace_abi, bytecode=config.EventMarketplace_bytecode)

    transaction = market_contract.constructor(config.token_contract_address, event_address).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce,
        "from": config.admin_address
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= config.admin_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    market_address = tx_receipt["contractAddress"]

    #mint all ticket
    EventNTF_contract = w3.eth.contract(address = event_address, abi = config.EventNFT_abi)

    for i in range(request.maxTicketLevel + 1):
        nonce = w3.eth.get_transaction_count(config.admin_address, 'pending')
        ticketLevel = i
        ticketAmount = request.ticketSupplyList[i]
        transaction = EventNTF_contract.functions.bulkMintTickets(ticketAmount, ticketLevel, request.organiser).build_transaction({
            "chainId": config.chain_id,
            "gas": 160000000000000,
            "gasPrice":  w3.eth.gas_price,
            "nonce": nonce
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, private_key= config.admin_key)

        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
    #approve all tickets to market
    # nonce = w3.eth.get_transaction_count(config.admin_address, 'pending') 

    # transaction = EventNTF_contract.functions.setApprovalForAll(market_address, True).build_transaction({
    #     "chainId": config.chain_id,
    #     "gas": 160000000000000,
    #     "gasPrice":  w3.eth.gas_price,
    #     "nonce": nonce
    # })

    # signed_txn = w3.eth.account.sign_transaction(transaction, private_key= config.admin_key)

    # tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    insertNewEvent(request.festName, request.festSymbol, event_address, market_address, request.organiser)

    return eventResponse(
        event_address = event_address,
        market_address = market_address
    )

# @router.post("/mint-tickets", response_model = searchEventStatusResponse)
# async def mint_tickets(request: mintTicketsRequest):
#     checksum_address = Web3.to_checksum_address(request.event_address)
#     contract = w3.eth.contract(address=checksum_address, abi=config.EventNFT_abi)
#     nonce = w3.eth.get_transaction_count(request.organiser)
    
#     transaction = contract.functions.bulkMintTickets(request.ticketNumber, request.level, request.organiser).build_transaction({
#         "chainId": config.chain_id,
#         "gas": 160000000000000,
#         "gasPrice":  w3.eth.gas_price,
#         "nonce": nonce
#     })

#     signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

#     tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
#     tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#     eventInf = await getEventStatus(checksum_address)
#     return eventInf


@router.get("/get-event-abi")
async def responseAllEvents():
    return config.EventNFT_abi


@router.get("/get-all-events")
async def responseAllEvents():
    return getAllEvents()


@router.get("/search-event-inf", response_model = searchEventInfResponse)
async def responseEventInf(event_address: str):
    eventInf = await getBasicInformation(event_address)
    return eventInf

@router.get("/search-event-status", response_model = searchEventStatusResponse)
async def responseEventStatus(event_address: str):
    eventInf = await getEventStatus(event_address)
    return eventInf



async def getBasicInformation(event_address: str):
    checksum_address = Web3.to_checksum_address(event_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventNFT_abi)
    eventInf = contract.functions.getBasicInformation().call()
    return searchEventInfResponse(
        organizer=eventInf[0],
        name=eventInf[1],
        symbol=eventInf[2],
        maxTicketLevel=eventInf[3],
        ticketPriceList=eventInf[4],
        ticketSupplyList=eventInf[5]
    ) 

async def getEventStatus(event_address: str):
    checksum_address = Web3.to_checksum_address(event_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventNFT_abi)
    eventInf = contract.functions.getEventStatus().call()
    return searchEventStatusResponse(
        currentTicketIds= eventInf[0],
        ticketsForSale= eventInf[1],
        ticketExistCounterList= eventInf[2],
        ticketSoldtCounterList= eventInf[3]
    ) 
