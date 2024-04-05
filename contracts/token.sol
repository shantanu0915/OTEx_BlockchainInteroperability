pragma solidity >=0.7.0 <0.9.0;
// SPDX-License-Identifier: MIT
import '@openzeppelin/contracts/token/ERC20/ERC20.sol';

contract Token is ERC20{
  constructor(address initialOwner)
    ERC20("MyToken", "MTK")
  {}
  
  function mint(address to, uint256 amount) public {
    _mint(to, amount);
  }
}
