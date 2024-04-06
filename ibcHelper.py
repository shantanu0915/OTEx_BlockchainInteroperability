import json
import time
import socket
import pickle
from web3 import IPCProvider, Web3
from eth_account import Account
from web3.middleware.geth_poa import geth_poa_middleware

aliceAddress = "0xD0582e07c048e4ca48c4eF188a106d3313328a08"
srcGatewayAddress = "0xAE5c9318F3146d758D9Ef83e9d0a8011916d5E53"
charlieAddress = "0xcF55B4843e710fdBf1d46729c65b5C94e620F589"

bobAddress = "0x9BF455677A403482a27d148f4598CC301D30ABC3"
dstGatewayAddress = "0xe3eE7E3d9F1C99B0633B0A7e5563C68aA5BcF5af"
ellenAddress = "0x1eb87060E2AE67D6f41BD5e7a99648546a9059aF"

class IBCMessage:
    def __init__(self, version, messageType, senderAddress, recipientAddress,
                 senderGWAddress, recipientGWAddress, tokenBID, senderBID,
                 recipientBID, tokenValue, ownershipCertificate):
        self.version = version
        self.messageType = messageType
        self.senderAddress = senderAddress
        self.recipientAddress = recipientAddress
        self.senderGWAddress = senderGWAddress
        self.recipientGWAddress = recipientGWAddress
        self.tokenBID = tokenBID
        self.senderBID = senderBID
        self.recipientBID = recipientBID
        self.tokenValue = tokenValue
        self.ownershipCertificate = ownershipCertificate

class Node:
    def __init__(self, nodeName, utcFile, password):
        super().__init__()

        self.ipc = nodeName + '/geth.ipc'
        self.w3 = Web3(IPCProvider(self.ipc))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        self.utcFile = utcFile
        self.password = password
        
        with open(nodeName + "/keystore/" + utcFile) as keyfile:
            encrypted = keyfile.read()
        privateKey = self.w3.eth.account.decrypt(encrypted, password)
        self.privateKey = privateKey
        acct = Account.from_key(privateKey)
        self.publicKey = acct._key_obj.public_key
        self.address = acct.address
        
    def checkConnection(self):
        print("Is connected to ", self.ipc, ": ", self.w3.is_connected())


    def sendTransaction(self, fromAddr, toAddr, ibcMessage):
        transaction = {
            'from': fromAddr,
            'to': toAddr,
            'value': 1,
            'data': pickle.dumps(ibcMessage),
        }
        txHash = self.w3.eth.send_transaction(transaction)
        self.w3.eth.wait_for_transaction_receipt(txHash)
        return txHash.hex()
    
    def transactionListener(self):
        currentBlockNumber = self.w3.eth.block_number
        block = dict(self.w3.eth.get_block(currentBlockNumber))
        while True:
            try:
                block = dict(self.w3.eth.get_block(currentBlockNumber))
                if block and block.get("transactions"):
                    for transaction in block['transactions']:
                        txHash = transaction.hex()
                        transaction = self.w3.eth.get_transaction(txHash)
                        if transaction.to is not None and transaction.to.lower() == self.address.lower():
                            data = pickle.loads(transaction["input"])
                            return data
                currentBlockNumber += 1
            except Exception as e:
                # print("No transaction found in block",e)
                time.sleep(5)
        return
    
    def transactionFetcher(self,txHash):
        # Fetch the transaction
        transaction = self.w3.eth.get_transaction(txHash)
        return transaction

    # def deployContract(self, contract_bytecode, contract_abi):
    #     contract = self.web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    #     tx_hash = contract.constructor().transact({'from': self.address})
    #     tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
    #     contract_address = tx_receipt.contractAddress
    #     return contract_address
