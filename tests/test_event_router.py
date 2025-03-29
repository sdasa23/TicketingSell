import pytest
from fastapi.testclient import TestClient
from web3 import Web3
from unittest.mock import Mock, patch

from backend.router.event import router
from backend.schemas.event import eventRequest
from backend.config import config

# Create test client
client = TestClient(router)

# Mock Web3 setup
@pytest.fixture
def mock_web3():
    with patch('backend.router.event.Web3') as mock:
        # Mock common Web3 responses
        mock.to_checksum_address.return_value = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        mock.is_address.return_value = True
        
        # Mock contract deployment responses
        mock_contract = Mock()
        mock_contract.constructor.return_value.build_transaction.return_value = {
            "chainId": 1,
            "gas": 2000000,
            "gasPrice": 20000000000,
            "nonce": 0,
        }
        
        mock.eth.contract.return_value = mock_contract
        mock.eth.get_transaction_count.return_value = 0
        mock.eth.wait_for_transaction_receipt.return_value = {
            "contractAddress": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        }
        yield mock

@pytest.mark.asyncio
async def test_create_event_success(mock_web3):
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=2,
        ticketPriceList=[100, 200, 300],
        ticketSupplyList=[50, 30, 20],
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    
    assert response.status_code == 200
    assert "event_address" in response.json()
    assert "market_address" in response.json()

@pytest.mark.asyncio
async def test_create_event_invalid_address():
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=2,
        ticketPriceList=[100, 200, 300],
        ticketSupplyList=[50, 30, 20],
        organiser="invalid_address"  # Invalid ethereum address
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "Invalid Ethereum address" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_event_abi():
    response = client.get("/get-event-abi")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # ABI should be a list

@pytest.mark.asyncio
async def test_search_event_inf():
    # Mock contract call response
    with patch('backend.router.event.getBasicInformation') as mock_get_inf:
        mock_get_inf.return_value = {
            "organizer": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            "name": "Test Festival",
            "symbol": "TEST",
            "maxTicketLevel": 2,
            "ticketPriceList": [100, 200, 300],
            "ticketSupplyList": [50, 30, 20]
        }
        
        response = client.get("/search-event-inf?event_address=0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Festival"
        assert response.json()["symbol"] == "TEST"

@pytest.mark.asyncio
async def test_search_event_status():
    # Mock contract call response
    with patch('backend.router.event.getEventStatus') as mock_get_status:
        mock_get_status.return_value = {
            "currentTicketIds": [1, 2, 3],
            "ticketsForSale": [True, True, False],
            "ticketExistCounterList": [50, 30, 20],
            "ticketSoldtCounterList": [10, 5, 2]
        }
        
        response = client.get("/search-event-status?event_address=0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        assert response.status_code == 200
        assert isinstance(response.json()["currentTicketIds"], list)
        assert isinstance(response.json()["ticketsForSale"], list)

@pytest.mark.asyncio
async def test_create_event_empty_ticket_lists():
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=0,
        ticketPriceList=[],
        ticketSupplyList=[],
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "Ticket lists cannot be empty" in respon
    se.json()["detail"]

@pytest.mark.asyncio
async def test_create_event_mismatched_lists():
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=2,
        ticketPriceList=[100, 200],  # Only 2 prices
        ticketSupplyList=[50, 30, 20],  # But 3 supply values
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "Price list and supply list must have matching lengths" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_event_negative_values():
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=2,
        ticketPriceList=[100, -200, 300],  # Negative price
        ticketSupplyList=[50, 30, -20],    # Negative supply
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "Negative values are not allowed" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_event_zero_supply():
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=2,
        ticketPriceList=[100, 200, 300],
        ticketSupplyList=[50, 0, 20],  # Zero supply for one level
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "Ticket supply must be greater than zero" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_event_very_large_numbers():
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=2,
        ticketPriceList=[2**256 - 1],  # Max uint256 value
        ticketSupplyList=[2**256 - 1],  # Max uint256 value
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "Value exceeds maximum allowed" in response.json()["detail"]

@pytest.mark.asyncio
async def test_search_event_inf_invalid_address():
    response = client.get("/search-event-inf?event_address=invalid_address")
    assert response.status_code == 400
    assert "Invalid Ethereum address format" in response.json()["detail"]

@pytest.mark.asyncio
async def test_search_event_inf_non_existent_contract():
    with patch('backend.router.event.getBasicInformation') as mock_get_inf:
        mock_get_inf.side_effect = Exception("Contract not found")
        
        response = client.get("/search-event-inf?event_address=0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        assert response.status_code == 404
        assert "Event contract not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_event_special_characters():
    test_request = eventRequest(
        festName="Test Festival !@#$%^&*()",  # Special characters in name
        festSymbol="T@ST",                    # Special characters in symbol
        maxTicketLevel=2,
        ticketPriceList=[100, 200, 300],
        ticketSupplyList=[50, 30, 20],
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "Invalid characters in festival name or symbol" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_event_max_ticket_level_mismatch():
    test_request = eventRequest(
        festName="Test Festival",
        festSymbol="TEST",
        maxTicketLevel=5,  # Claims 5 levels
        ticketPriceList=[100, 200, 300],  # But only provides 3 levels
        ticketSupplyList=[50, 30, 20],
        organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    response = client.post("/create-new-event", json=test_request.dict())
    assert response.status_code == 400
    assert "maxTicketLevel does not match provided ticket lists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_web3_connection_failure():
    with patch('backend.router.event.Web3') as mock_web3:
        mock_web3.side_effect = Exception("Connection failed")
        
        test_request = eventRequest(
            festName="Test Festival",
            festSymbol="TEST",
            maxTicketLevel=2,
            ticketPriceList=[100, 200, 300],
            ticketSupplyList=[50, 30, 20],
            organiser="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        )
        
        response = client.post("/create-new-event", json=test_request.dict())
        assert response.status_code == 503
        assert "Blockchain connection error" in response.json()["detail"] 