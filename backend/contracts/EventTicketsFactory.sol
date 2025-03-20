// SPDX-License-Identifier: MIT

pragma solidity ^0.8.29;

// import "@openzeppelin/contracts/access/Ownable.sol";
import "./EventNFT.sol";
import "./EventMarketplace.sol";

// contract EventTicketsFactory is Ownable {
contract EventTicketsFactory{
  address public owner = msg.sender;
  modifier onlyOwner() {
    require(
      msg.sender == owner,
      "This function is restricted to the contract's owner"
    );
    _;
  }

    struct Event {
        string EventName;
        string EventSymbol;
        uint8 maxTicketLevel;
        uint256[] ticketPriceList; 
        uint256[] totalSupplyList;
        address marketplace;
    }

    address[] private activeEvents;
    mapping(address => Event) private activeEventsMapping;

    event Created(address ntfAddress, address marketplaceAddress);

    // constructor(address initialOwner) Ownable(initialOwner) {
        
    // }

    // Creates new NFT and a marketplace for its purchase
    function createNewEvent(
        EventToken token,
        string memory EventName,
        string memory EventSymbol,
        uint8 maxTicketLevel,
        uint256[] memory ticketPriceList, 
        uint256[] memory totalSupplyList
    ) public onlyOwner returns (address) {
        EventNFT newEvent =
            new EventNFT(
                EventName,
                EventSymbol,
                maxTicketLevel,
                ticketPriceList,
                totalSupplyList,
                msg.sender  // organizer
            );

        EventMarketplace newMarketplace =
            new EventMarketplace(token, newEvent);  // create a new market of this Event

        address newEventAddress = address(newEvent);

        activeEvents.push(newEventAddress);
        activeEventsMapping[newEventAddress] = Event({
            EventName: EventName,
            EventSymbol: EventSymbol,
            maxTicketLevel: maxTicketLevel,
            ticketPriceList: ticketPriceList,
            totalSupplyList: totalSupplyList,
            marketplace: address(newMarketplace)
        });

        emit Created(newEventAddress, address(newMarketplace));

        return newEventAddress;
    }

    // Get all active Events
    function getActiveEvents() public view returns (address[] memory) {
        return activeEvents;
    }

    // Get Event's details
    function getEventDetails(address EventAddress)
        public
        view
        returns (
            string memory,
            string memory,
            uint8,
            uint256[] memory,
            uint256[] memory,
            address
        )
    {
        return (
            activeEventsMapping[EventAddress].EventName,
            activeEventsMapping[EventAddress].EventSymbol,
            activeEventsMapping[EventAddress].maxTicketLevel,
            activeEventsMapping[EventAddress].ticketPriceList,
            activeEventsMapping[EventAddress].totalSupplyList,
            activeEventsMapping[EventAddress].marketplace
        );
    }
}
