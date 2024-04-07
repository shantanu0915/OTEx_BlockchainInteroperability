import sys
sys.path.insert(1, '/home/shantu/IBC_Eth')
import ibcHelper
import threading
import pickle
import time

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
    OTResponseTransaction = bob.sendTransaction(ibcHelper.bobAddress, ibcHelper.dstGatewayAddress, data)
    print("---- 10. Sending Accept/Reject Response ----")
    print("From: Bob  To: Destination Gateway")
    print("Transaction Hash: ", OTResponseTransaction)

    time.sleep(5)
    response = input("Do you wish to use Ownership Execution (y/n): ")
    if(response == "y"):
        OERequestMessage = ibcHelper.IBCMessage(
            version=1,
            messageType="OEInit",
            senderAddress=ibcHelper.bobAddress,
            recipientAddress=ibcHelper.aliceAddress,
            senderGWAddress=ibcHelper.dstGatewayAddress,
            recipientGWAddress=ibcHelper.srcGatewayAddress,
            tokenBID="srcBID",
            senderBID="srcBID",
            recipientBID="dstBID",
            tokenValue=data.tokenValue,
            ownershipCertificate=data.ownershipCertificate #Sign the Ownership Certificate here and send signature
        )
        OEInitTransaction = bob.sendTransaction(OERequestMessage.senderAddress, OERequestMessage.senderGWAddress, OERequestMessage)
        print("---- 1. OE Init by Bob ----")
        print("From: Bob  To: Destination Gateway")
        print("Transaction Hash: ", OEInitTransaction)


if __name__ == "__main__":
    
    onChainListenerThread = threading.Thread(target=onChainListener, args=())
    onChainListenerThread.start()