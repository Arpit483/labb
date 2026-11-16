// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
Assignment 4 - Write a program in solidity to create Student data. Use the following constructs:
• Structures
• Arrays
• Fallback
Deploy this as smart contract on Ethereum and Observe the transaction fee and Gas values.
*/

contract StudentData {
    // Structure to store student information
    struct Student {
        uint256 rollNo;
        string name;
        uint256 marks;
    }

    Student[] public students;

    function addStudent(
        uint256 _rollNo,
        string memory _name,
        uint256 _marks
    ) public {
        students.push(Student(_rollNo, _name, _marks));
    }

    function getStudentCount() public view returns (uint256) {
        return students.length;
    }

    function getStudent(uint256 index)
        public
        view
        returns (uint256, string memory, uint256)
    {
        require(index < students.length, "Invalid student index");
        Student memory s = students[index];
        return (s.rollNo, s.name, s.marks);
    }

    // Fallback function executes for unmatched calls or calls with calldata that do not match a function
    fallback() external payable {
    }

    // Accept plain ETH transfers
    receive() external payable {
    }
}
