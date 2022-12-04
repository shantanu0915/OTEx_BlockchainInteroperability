import json
import web3
import ast
import pickle
import ibc_helper
import socket

from web3 import Web3, HTTPProvider, IPCProvider#, TestRPCProvider
from web3.contract import ConciseContract
from web3.middleware import geth_poa_middleware
from Crypto.PublicKey import RSA
from hashlib import sha512

#####################################################################################    
# connecting to nodes of Auxiliary blockchain

utcFile1 = "UTC--2022-05-01T18-18-26.662254672Z--d4f8a73bc70ea10d04fdeda49c6ec589c0b1bfbe"
utcFile2 = "UTC--2022-05-01T18-18-55.642832491Z--5fa2b8d476bd40bc6a4ce82eea9fbc3af2a442c3"
password = "1234"

aux1 = ibc_helper.IBC("aux", "node1", utcFile1, password) 
aux2 = ibc_helper.IBC("aux", "node2", utcFile2, password) 

aux1.checkConnection()
aux2.checkConnection()
print()

aux1Account = aux1.w3.eth.accounts[0]
aux2Account = aux2.w3.eth.accounts[0]

#####################################################################################
#Socket Connection to Source

aux2srcPort = 54321
aux2dstPort = 65432

aux2srcSocket = socket.socket()
print("Aux to Source Socket Created Successfully")

aux2dstSocket = socket.socket()
print("Aux to Destination Socket Created Successfully")

aux2srcSocket.bind(('', aux2srcPort))
print("Socket binded to %s" %(aux2srcPort))

aux2dstSocket.bind(('', aux2dstPort))
print("Socket binded to %s" %(aux2dstPort))

aux2srcSocket.listen(1)
print("Aux Socket Listening for Source")

aux2dstSocket.listen(1)
print("Aux Socket Listening for Destination")

s, sAddr = aux2srcSocket.accept()
d, dAddr = aux2dstSocket.accept()

print("Connected to Src via socket at: ", sAddr)
print("Connected to Dst via socket at: ", dAddr)
print()



