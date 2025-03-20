from fastapi import APIRouter
from web3 import HTTPProvider,Web3

from schemas.event import eventRequest, eventResponse, searchEventInfResponse, searchEventStatusResponse, mintTicketsRequest
from config import config
from crud.event import insertNewEvent
router = APIRouter()

w3 = Web3(HTTPProvider(config.web3_address))

@router.post("/create-new-event", response_model = eventResponse)
async def create_event(request: eventRequest):
    publisher_address = request.organiser

    nonce = w3.eth.get_transaction_count(publisher_address, 'pending')
    EventNTF_contract = w3.eth.contract(abi=config.EventNFT_abi, bytecode=config.EventNFT_bytecode)

    transaction = EventNTF_contract.constructor(request.festName, request.festSymbol, request.maxTicketLevel, 
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
    
    nonce = w3.eth.get_transaction_count(publisher_address, 'pending')
    market_contract = w3.eth.contract(abi=config.EventMarketplace_abi, bytecode=config.EventMarketplace_bytecode)

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

    #mint all ticket
    EventNTF_contract = w3.eth.contract(address = event_address, abi = config.EventNFT_abi)

    for i in range(request.maxTicketLevel):
        nonce = w3.eth.get_transaction_count(publisher_address, 'pending')
        ticketLevel = i
        ticketAmount = request.ticketSupplyList[i]
        transaction = EventNTF_contract.functions.bulkMintTickets(ticketAmount, ticketLevel, publisher_address).build_transaction({
            "chainId": config.chain_id,
            "gas": 160000000000000,
            "gasPrice":  w3.eth.gas_price,
            "nonce": nonce
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
    #approve all tickets to market
    nonce = w3.eth.get_transaction_count(publisher_address, 'pending') 

    transaction = EventNTF_contract.functions.setApprovalForAll(market_address, True).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    insertNewEvent(request.festName, request.festSymbol, event_address, market_address, request.organiser)

    return eventResponse(
        event_address = event_address,
        market_address = market_address
    )

@router.post("/mint-tickets", response_model = searchEventStatusResponse)
async def mint_tickets(request: mintTicketsRequest):
    checksum_address = Web3.to_checksum_address(request.event_address)
    contract = w3.eth.contract(address=checksum_address, abi=config.EventNFT_abi)
    nonce = w3.eth.get_transaction_count(request.organiser)
    
    transaction = contract.functions.bulkMintTickets(request.ticketNumber, request.level, request.organiser).build_transaction({
        "chainId": config.chain_id,
        "gas": 160000000000000,
        "gasPrice":  w3.eth.gas_price,
        "nonce": nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= request.priv_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    eventInf = await getEventStatus(checksum_address)
    return eventInf

@router.get("/search-event-inf/{event_address}", response_model = searchEventInfResponse)
async def responseEventInf(event_address: str):
    eventInf = await getBasicInformation(event_address)
    return eventInf

@router.get("/search-event-status/{event_address}", response_model = searchEventStatusResponse)
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
