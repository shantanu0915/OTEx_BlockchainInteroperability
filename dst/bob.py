import sys
sys.path.insert(1, '/home/shantu/IBC_Eth')
import ibcHelper
import threading
import pickle

bobUTCFile = "UTC--2024-04-05T10-33-17.825323275Z--9bf455677a403482a27d148f4598cc301d30abc3"
password = "1234"
bob = ibcHelper.Node("bob", bobUTCFile, password)
bob.checkConnection()

def onChainListener():
    print("Transaction listening started at Bob")
    data = bob.transactionListener()
    print("Ownership Request received from: ", data.senderAddress)
    response = input("Do you wish to accept (y/n): ")
    data.messageType = response
    print("---- 10. Sending Accept/Reject Response ----")
    bob.sendTransaction(ibcHelper.bobAddress, ibcHelper.dstGatewayAddress, data)


if __name__ == "__main__":
    
    onChainListenerThread = threading.Thread(target=onChainListener, args=())
    onChainListenerThread.start()