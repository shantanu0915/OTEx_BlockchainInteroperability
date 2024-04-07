import sys
sys.path.insert(1, '/home/shantu/IBC_Eth')
import ibcHelper
import threading
import pickle

aliceUTCFile = "UTC--2024-04-05T08-42-30.674053139Z--d0582e07c048e4ca48c4ef188a106d3313328a08"
password = "1234"
alice = ibcHelper.Node("alice", aliceUTCFile, password)
alice.checkConnection()

def onChainListener():
    print("Transaction listening started at Alice")
    data = alice.transactionListener()
    if(data.messageType == "OTAcceptResponse"):
        print("---- 14. Ownership Transfer Successful---- ")
    else:
        print("---- 14. Ownership Transfer Rejected---- ")

if __name__ == "__main__":

    print("---- 1. Alice mints the tokens for OTEx ----")
    print("From: Alice  To: Mint Token SC")
    print("Transaction Hash: ")

    print("---- 2. Alice locks the token ----")
    print("From: Alice  To: Lock Token SC")
    print("Transaction Hash: ")

    #Transaction Hash (Lock Token Hash as Ownership Certificate) to be genrated after the smart contract call 

    OTInitMessage = ibcHelper.IBCMessage(
        version=1,
        messageType="OTInit",
        senderAddress=ibcHelper.aliceAddress,
        recipientAddress=ibcHelper.bobAddress,
        senderGWAddress=ibcHelper.srcGatewayAddress,
        recipientGWAddress=ibcHelper.dstGatewayAddress,
        tokenBID="srcBID",
        senderBID="srcBID",
        recipientBID="dstBID",
        tokenValue=100,
        ownershipCertificate="Certificate" #Use the Lock Token Hash here
    )

    OTInitTransaction = alice.sendTransaction(OTInitMessage.senderAddress, OTInitMessage.senderGWAddress, OTInitMessage)
    print("---- 3. OT Init transaction to source gateway ----")
    print("From: Alice  To: Source Gateway")
    print("Transaction Hash: ", OTInitTransaction)

    onChainListenerThread = threading.Thread(target=onChainListener, args=())
    onChainListenerThread.start()

