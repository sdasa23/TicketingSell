// SPDX-License-Identifier: MIT

pragma solidity >=0.4.22 <0.9.0;

contract Migrations {
  address public owner = msg.sender;
  uint public last_completed_migration;

// This is a modifier that restricts the function must be used by contract owner.
  modifier onlyOwner() {
    require(
      msg.sender == owner,
      "This function is restricted to the contract's owner"
    );
    _;
  }

  function setCompleted(uint completed) public onlyOwner {
    last_completed_migration = completed;
  }
}
