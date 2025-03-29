// SPDX-License-Identifier: MIT

pragma solidity ^0.8.29;

import "./EventNFT.sol";
import "./EventToken.sol"; 

contract EventMarketplace {
    EventToken private _token;
    EventNFT private _Event;

    address private _organiser;

    constructor(EventToken token, EventNFT Event) {
        _token = token;
        _Event = Event;
        _organiser = _Event.getOrganiser();
    }

    event Purchase(address indexed buyer, address seller, uint256 ticketId);

    // Purchase tickets from the organiser directly
    function purchaseTicket(uint8 ticketLevel, address buyer) public {
        _token.transferFrom(buyer, _organiser, _Event.getTicketPrice(ticketLevel));
        _Event.transferTicket(buyer, ticketLevel);
    }

    // Purchase ticket from the secondary market hosted by organiser
    function secondaryPurchase(uint256 ticketId, address buyer) public {
        address seller = _Event.ownerOf(ticketId);
        uint256 sellingPrice = _Event.getSellingPrice(ticketId);

        _token.transferFrom(buyer, seller, sellingPrice);  

        _Event.secondaryTransferTicket(buyer, ticketId);

        emit Purchase(buyer, seller, ticketId);
    }

}
