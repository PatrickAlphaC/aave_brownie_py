
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@aave/contracts/interfaces/ILendingPool.sol";
import "@aave/contracts/interfaces/ILendingPoolAddressesProvider.sol";

contract BorrowFromAave {
    ILendingPoolAddressesProvider public lendingPoolAddressesProvider; 
    ILendingPool public lendingPool;

    // Kovan
    // DAI/ETH
    // 0x22B58f1EbEDfCA50feF632bD73368b2FdA96D541
    // 0x773616E4d11A78F511299002da57A0a94577F1f4

    constructor(address _LendingPoolAddressesProviderAdddress) public {
        lendingPoolAddressesProvider = ILendingPoolAddressesProvider(_LendingPoolAddressesProviderAdddress);
        lendingPool = ILendingPool(lendingPoolAddressesProvider.getLendingPool());
    }
}
