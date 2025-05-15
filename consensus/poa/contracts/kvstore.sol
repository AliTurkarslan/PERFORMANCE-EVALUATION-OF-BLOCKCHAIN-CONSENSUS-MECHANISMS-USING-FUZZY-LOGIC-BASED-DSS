// contracts/kvstore.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract KVStore {
    mapping(string => string) store;

    function set(string memory key, string memory value) public {
        store[key] = value;
    }

    function get(string memory key) public view returns (string memory) {
        return store[key];
    }
}
