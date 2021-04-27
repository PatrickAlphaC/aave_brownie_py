
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract BorrowAndLend {

    AggregatorV3Interface internal priceFeed;

    // Kovan
    // DAI/ETH
    // 0x22B58f1EbEDfCA50feF632bD73368b2FdA96D541
    // 0x773616E4d11A78F511299002da57A0a94577F1f4

    constructor(address AggregatorAddress) public {
        priceFeed = AggregatorV3Interface(AggregatorAddress);
    }

    function borrow(address asset, uint256 amount, uint256 interestRateMode) public {

    }

    function getLatestPrice() public view returns (int) {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }
}
