// SPDX-License-Identifier: MIT

pragma solidity ^0.8.29;

import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol"; // NFT
import "@openzeppelin/contracts/utils/Counters.sol";

contract EventNFT is Context, AccessControl, ERC721 {
    using Counters for Counters.Counter;

    Counters.Counter private _ticketIds; // a counter to remember how many unique tickets now
    Counters.Counter[] private _ticketExistCounterList;
    Counters.Counter[] private _ticketSoldtCounterList;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE"); // unique role identifier
                                                             
    struct TicketDetails {
        uint8 ticketLevel; 
        uint256 purchasePrice;
        uint256 sellingPrice;
        bool forSale;
    }

    address private _organiser;
    address[] private customers;  
    uint256[] private ticketsForSale;
    
    uint256[] private _ticketPriceList;
    uint256[] private _ticketSupplyList;
    uint8 private _maxTicketLevel; // The levels of tickets are from 0 to _maxTicketLevel  

    mapping(uint256 => TicketDetails) private _ticketDetails;
    mapping(address => uint256[]) private purchasedTickets;

    constructor(
        string memory festName,
        string memory FestSymbol,
        uint8 maxTicketLevel,
        uint256[] memory ticketPriceList,
        uint256[] memory ticketSupplyList,
        address organiser
    ) ERC721(festName, FestSymbol) {
        _grantRole(MINTER_ROLE, organiser);
        _grantRole(MINTER_ROLE, _msgSender());

        _maxTicketLevel = maxTicketLevel;
        _ticketPriceList = ticketPriceList;
        _ticketSupplyList = ticketSupplyList;
        _organiser = organiser;
        initialTicketCounterList();
    }

    modifier isValidTicketCount(uint8 level) {
        //The first require can be removed.
        require(
            _ticketExistCounterList[level].current() < _ticketSupplyList[level],
            "Maximum ticket limit exceeded in this Level!"
        );
        _;
    }

    modifier isMinterRole() {
        require(
            hasRole(MINTER_ROLE, _msgSender()),
            "User must have minter role to mint"
        );
        _;
    }

    modifier hasUnsoldTicket(uint8 level){
        require(
            _ticketSoldtCounterList[level].current() < _ticketExistCounterList[level].current(),
            "The ticket in this level is sold out!"
        );
        _;
    }


    // check the price range  
    modifier isValidSellAmount(uint256 ticketId) {
        uint256 purchasePrice = _ticketDetails[ticketId].purchasePrice;
        uint256 sellingPrice = _ticketDetails[ticketId].sellingPrice;

        // the resell price can`t over than 110% of original price.
        require(
            purchasePrice + ((purchasePrice * 110) / 100) > sellingPrice,
            "Re-selling price is more than 110%"
        );
        _;
    }

    /*
     * Mint new tickets and assign it to operator
     * Access controlled by minter only
     * Returns new ticketId
     */
    function mint(address operator, uint8 level)
        internal
        virtual
        isMinterRole
        isValidTicketCount(level)
        returns (uint256)
    {
        _ticketIds.increment();
        _ticketExistCounterList[level].increment();
        uint256 newTicketId = _ticketIds.current();
        _mint(operator, newTicketId);
        _ticketDetails[newTicketId] = TicketDetails({
            purchasePrice: _ticketPriceList[level],
            sellingPrice: 0,
            ticketLevel: level, 
            forSale: false
        });

        return newTicketId;
    }

    /*
     * Bulk mint specified number of tickets to assign it to a operator
     * Modifier to check the ticket count is less than total supply
     */
    function bulkMintTickets(uint256 numOfTickets, uint8 ticketLevel, address operator)
        public
        virtual
        isValidTicketCount(ticketLevel)
    {
        require(
            (ticketCounts() + numOfTickets) <= 1000,  // max number of tickers is 1000
            "Number of tickets exceeds maximum ticket count"
        );

        for (uint256 i = 0; i < numOfTickets; i++) {
            mint(operator, ticketLevel);
        }
    }

    /*
     * Primary purchase for the tickets
     * Adds new customer if not exists
     * Adds buyer to tickets mapping
     * Update ticket details
     */
    function transferTicket(address buyer, uint8 level)
        public
        hasUnsoldTicket(level)
    {
        uint256 saleTicketId = getUnsoldTicketID(level); // The id of ticket is started from 1
        _ticketSoldtCounterList[level].increment();
        address owner = ownerOf(saleTicketId);
        transferFrom(owner, buyer, saleTicketId);

        if (!isCustomerExist(buyer)) {
            customers.push(buyer);
        }
        purchasedTickets[buyer].push(saleTicketId);
    }

    /*
     * Secondary purchase for the tickets
     * Modifier to validate that the selling price shouldn't exceed 110% of purchase price for peer to peer transfers
     * Adds new customer if not exists
     * Adds buyer to tickets mapping
     * Remove ticket from the seller and from sale
     * Update ticket details
     */
    function secondaryTransferTicket(address buyer, uint256 saleTicketId)
        public
        isValidSellAmount(saleTicketId)
    {
        address seller = ownerOf(saleTicketId);
        uint256 sellingPrice = _ticketDetails[saleTicketId].sellingPrice;
        uint8 ticketLevel = _ticketDetails[saleTicketId].ticketLevel;

        transferFrom(seller, buyer, saleTicketId);

        if (!isCustomerExist(buyer)) {
            customers.push(buyer);
        }

        purchasedTickets[buyer].push(saleTicketId);

        // removeTicketFromCustomer(seller, saleTicketId); //ERROR here
        removeTicketFromSale(saleTicketId); 

        _ticketDetails[saleTicketId] = TicketDetails({
            purchasePrice: sellingPrice,
            sellingPrice: 0,
            ticketLevel: ticketLevel,
            forSale: false
        });
    }

    /*
     * Add ticket for sale with its details
     * Validate that the selling price shouldn't exceed 110% of purchase price
     * Organiser can not use secondary market sale
     */
    function setSaleDetails(
        uint256 ticketId,
        uint256 sellingPrice,
        address operator
    ) public {
        uint256 purchasePrice = _ticketDetails[ticketId].purchasePrice;

        require(
            purchasePrice + ((purchasePrice * 110) / 100) > sellingPrice,
            "Re-selling price is more than 110%"
        );

        // // Should not be an organiser
        // require(
        //     !hasRole(MINTER_ROLE, _msgSender()),
        //     "Functionality only allowed for secondary market"
        // );

        _ticketDetails[ticketId].sellingPrice = sellingPrice;
        _ticketDetails[ticketId].forSale = true;

        if (!isSaleTicketAvailable(ticketId)) {
            ticketsForSale.push(ticketId);
        }

        // approve(operator, ticketId);
    }

    // Get ticket actual price
    function getTicketPrice(uint8 level) public view returns (uint256) {
        return _ticketPriceList[level];
    }

    // Get organiser's address
    function getOrganiser() public view returns (address) {
        return _organiser;
    }

    // Get current ticketId
    function ticketCounts() public view returns (uint256) {
        return _ticketIds.current();
    }

    // Get selling price for the ticket
    function getSellingPrice(uint256 ticketId) public view returns (uint256) {
        return _ticketDetails[ticketId].sellingPrice;
    }

    function getBasicInformation() 
        public
        view 
        returns (
            address ,
            string memory, 
            string memory,
            uint8 ,  
            uint256[] memory,
            uint256[] memory
        )
    {
        return (
            _organiser,
            name(),
            symbol(),
            _maxTicketLevel,
            _ticketPriceList,
            _ticketSupplyList
        );
    }

    function getEventStatus() 
        public
        view 
        returns (
            uint256,
            uint256[] memory,
            uint256[] memory,
            uint256[] memory
        )
    {   
        uint256[] memory ticketExistCounterList = new uint256[](_maxTicketLevel+1);
        for(uint8 level = 0; level < _maxTicketLevel+1; level++){
            ticketExistCounterList[level] = _ticketExistCounterList[level].current();
        }
        uint256[] memory ticketSoldtCounterList = new uint256[](_maxTicketLevel+1);
        for(uint8 level = 0; level < _maxTicketLevel+1; level++){
            ticketSoldtCounterList[level] = _ticketSoldtCounterList[level].current();
        }
        uint256[] memory _ticketsForSale = ticketsForSale; 
        return (
            _ticketIds.current(),
            _ticketsForSale,
            ticketExistCounterList, 
            ticketSoldtCounterList
        );
    }


    // Get ticket details
    function getTicketDetails(uint256 ticketId)
        public
        view
        returns (
            uint256 purchasePrice,
            uint256 sellingPrice,
            uint8 ticketLevel,
            bool forSale
        )
    {
        return (
            _ticketDetails[ticketId].purchasePrice,
            _ticketDetails[ticketId].sellingPrice,
            _ticketDetails[ticketId].ticketLevel,
            _ticketDetails[ticketId].forSale
        );
    }

    // Get all tickets owned by a customer
    function getTicketsOfCustomer(address customer)
        public
        view
        returns (uint256[] memory)
    {
        return purchasedTickets[customer];
    }

    // Utility function to check if customer exists to avoid redundancy
    function isCustomerExist(address buyer) internal view returns (bool) {
        for (uint256 i = 0; i < customers.length; i++) {
            if (customers[i] == buyer) {
                return true;
            }
        }
        return false;
    }

    // Utility function used to check if ticket is already for sale
    function isSaleTicketAvailable(uint256 ticketId)
        internal
        view
        returns (bool)
    {
        for (uint256 i = 0; i < ticketsForSale.length; i++) {
            if (ticketsForSale[i] == ticketId) {
                return true;
            }
        }
        return false;
    }

    // Utility function to remove ticket owned by customer from customer to ticket mapping
    function removeTicketFromCustomer(address customer, uint256 ticketId)
        internal
    {
        uint256 numOfTickets = purchasedTickets[customer].length;

        for (uint256 i = 0; i < numOfTickets; i++) {
            if (purchasedTickets[customer][i] == ticketId) {
                for (uint256 j = i + 1; j < numOfTickets; j++) {
                    purchasedTickets[customer][j - 1] = purchasedTickets[
                        customer
                    ][j];
                }
                purchasedTickets[customer].pop();
            }
        }
    }


    function removeTicketFromSale(uint256 ticketId) internal returns (bool) {
        require(ticketsForSale.length > 0, "Array is empty"); 

        for (uint256 i = 0; i < ticketsForSale.length; i++) {
            if (ticketsForSale[i] == ticketId) {
                require(i < ticketsForSale.length, "Index out of bounds"); 
                if (i < ticketsForSale.length - 1) {
                    ticketsForSale[i] = ticketsForSale[ticketsForSale.length - 1];
                }
                ticketsForSale.pop();
                return true;
            }
        }

        return false;
    }

    function getSumTicketNumber(uint256[] memory ticketSupplyList) 
        internal 
        pure
        returns (uint256)
    {
                    uint256 total = 0;
                    for (uint256 i = 0; i < ticketSupplyList.length; i++) {
                        total += ticketSupplyList[i];
                    }
                    return total;
    }

    function initialTicketCounterList() internal {
        for(uint256 i = 0; i < _maxTicketLevel+1; i++){
            _ticketExistCounterList.push(); // add a new counter
            _ticketSoldtCounterList.push(); // add a new counter
        }        
    }

    function getUnsoldTicketID(uint8 level)
        public
        view
        returns (uint256)
        {
            uint256 id = 1;  // started from 1 
            for (uint256 i = 0; i < level; i++){
                id += _ticketExistCounterList[i].current();
            }
            id += _ticketSoldtCounterList[level].current();

            return id;
        }

    function supportsInterface(bytes4 interfaceId)
    public
    view
    virtual
    override(AccessControl, ERC721)
    returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
