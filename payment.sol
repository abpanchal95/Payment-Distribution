pragma solidity ^0.8.0;

// SPDX-License-Identifier: MIT

contract Payment {
    address public contract_owner;
    
    struct Contributor {
        address addr;
        uint share;
    }
    
    Contributor[] public contributors;

    constructor() {
        contract_owner = msg.sender; // address of creator of contract
    }

    //to add contributors in contract
    function add(address _addr, uint256 _share) public restricted {
        contributors.push(Contributor(_addr, _share));
    }

    //to find particular user from address
    function find(address _addr) internal view returns (uint256 id_) {
        for (uint256 i = 0; i < contributors.length; i++) {
            if (contributors[i].addr == _addr) {
                return i;
            }
        }
        revert("Contributor does not exist");
    }

    //someone buying product and distibuting to users
    function buy_item() public payable {
        require(contributors.length > 0);
        for (uint256 i = 0; i < contributors.length; i++) {
            uint256 amount = 0;
            amount = percent(msg.value, contributors[i].share);
            payable(contributors[i].addr).transfer(amount);
        }
    }

    //calculating percentage amount
    function percent(uint256 amount, uint256 fraction) public pure returns (uint256) {
        //require((amount / 10000) * 10000 == amount, 'too small');
        return (amount * fraction) / 10000; //fraction of 2.15 is  215
    }

    modifier restricted() {
        require(msg.sender == contract_owner); //only owner can do
        _;
    }
}
