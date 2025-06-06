// SPDX-License-Identifier: MIT

pragma solidity 0.8.29;

import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./Migrations.sol";

contract EventToken is Context, ERC20 {
    address public owner = msg.sender;

    constructor() ERC20("EventToken", "EVENT") {
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

    // function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool) {
    //     _transfer(sender, recipient, amount);
    //     return true;
    // }
}

