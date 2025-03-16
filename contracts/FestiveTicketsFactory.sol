// SPDX-License-Identifier: MIT

pragma solidity ^0.8.29;

// import "@openzeppelin/contracts/access/Ownable.sol";
import "./FestivalNFT.sol";
import "./FestivalMarketplace.sol";

// contract FestiveTicketsFactory is Ownable {
contract FestiveTicketsFactory{
  address public owner = msg.sender;
  modifier onlyOwner() {
    require(
      msg.sender == owner,
      "This function is restricted to the contract's owner"
    );
    _;
  }

    struct Festival {
        string festName;
        string festSymbol;
        uint8 maxTicketLevel;
        uint256[] ticketPriceList; 
        uint256[] totalSupplyList;
        address marketplace;
    }

    address[] private activeFests;
    mapping(address => Festival) private activeFestsMapping;

    event Created(address ntfAddress, address marketplaceAddress);

    // constructor(address initialOwner) Ownable(initialOwner) {
        
    // }

    // Creates new NFT and a marketplace for its purchase
    function createNewFest(
        FestToken token,
        string memory festName,
        string memory festSymbol,
        uint8 maxTicketLevel,
        uint256[] memory ticketPriceList, 
        uint256[] memory totalSupplyList
    ) public onlyOwner returns (address) {
        FestivalNFT newFest =
            new FestivalNFT(
                festName,
                festSymbol,
                maxTicketLevel,
                ticketPriceList,
                totalSupplyList,
                msg.sender  // organizer
            );

        FestivalMarketplace newMarketplace =
            new FestivalMarketplace(token, newFest);  // create a new market of this festival

        address newFestAddress = address(newFest);

        activeFests.push(newFestAddress);
        activeFestsMapping[newFestAddress] = Festival({
            festName: festName,
            festSymbol: festSymbol,
            maxTicketLevel: maxTicketLevel,
            ticketPriceList: ticketPriceList,
            totalSupplyList: totalSupplyList,
            marketplace: address(newMarketplace)
        });

        emit Created(newFestAddress, address(newMarketplace));

        return newFestAddress;
    }

    // Get all active fests
    function getActiveFests() public view returns (address[] memory) {
        return activeFests;
    }

    // Get fest's details
    function getFestDetails(address festAddress)
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
            activeFestsMapping[festAddress].festName,
            activeFestsMapping[festAddress].festSymbol,
            activeFestsMapping[festAddress].maxTicketLevel,
            activeFestsMapping[festAddress].ticketPriceList,
            activeFestsMapping[festAddress].totalSupplyList,
            activeFestsMapping[festAddress].marketplace
        );
    }
}
