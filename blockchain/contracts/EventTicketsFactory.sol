// SPDX-License-Identifier: MIT

pragma solidity ^0.8.29;

import "./EventNFT.sol";
import "./EventMarketplace.sol";

contract EventTicketsFactory {
    
  address public owner = msg.sender;

    address[] private activeEvents;

    event Created(address ntfAddress, address marketplaceAddress);

    constructor() {
        
    }

    // Creates new NFT and a marketplace for its purchase
    function createNewEvent(
        EventToken token,
        string memory EventName,
        string memory EventSymbol,
        uint8 maxTicketLevel,
        uint256[] memory ticketPriceList, 
        uint256[] memory totalSupplyList
    ) public returns (address) {
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

        emit Created(newEventAddress, address(newMarketplace));

        return newEventAddress;
    }

    // Get all active Events
    function getActiveEvents() public view returns (address[] memory) {
        return activeEvents;
    }

}
