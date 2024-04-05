// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract VerifySignature {
   
    function recoverSigner(bytes32 _ethSignedMessageHash, bytes32 r, bytes32 s, uint8 v) public pure returns (address){
        return ecrecover(_ethSignedMessageHash, v, r, s);
    }

}
