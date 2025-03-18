// SPDX-License-Identifier: MIT

pragma solidity 0.8.29;

import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./Migrations.sol";

contract FestToken is Context, ERC20 {
    address public owner = msg.sender;

    constructor() ERC20("FestToken", "FEST") {
        _mint(_msgSender(), 10000 * (10**uint256(decimals())));
    }

    modifier onlyOwner() {
        require(
        msg.sender == owner,
        "This function is restricted to the contract's owner"
        );
        _;
    }

    function mint(address to, uint256 amount) 
        public 
        onlyOwner 
    {
        _mint(to, amount);
    }

    function burn(uint256 amount) public{
        _burn(_msgSender(), amount);
    }
}

