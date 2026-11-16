// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
Assignment 3 - Write a smart contract on a test network, for Bank account of a customer for following operations:
• Deposit money
• Withdraw Money
• Show balance
*/

contract Bank {
    mapping(address => uint256) public balanceOf;

    function deposit() public payable {
        require(msg.value > 0, "Amount must be greater than zero");
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) public {
        require(amount > 0, "Amount must be greater than zero");
        require(
            amount <= balanceOf[msg.sender],
            "Insufficient balance"
        );
        balanceOf[msg.sender] -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
    }

    function getBalance() public view returns (uint256) {
        return balanceOf[msg.sender];
    }
}
