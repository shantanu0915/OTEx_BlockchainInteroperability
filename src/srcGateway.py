import sys
sys.path.insert(1, '/home/shantu/IBC_Eth')
import ibcHelper
import threading
import pickle
import socket

srcGatewayUTCFile = "UTC--2024-04-05T08-43-13.525966715Z--ae5c9318f3146d758d9ef83e9d0a8011916d5e53"
password = "1234"
srcGateway = ibcHelper.Node("srcGateway", srcGatewayUTCFile, password)
srcGateway.checkConnection()

srcToDstSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Source to Destination socket created")
dstPort = 12345
dstIP = '192.168.111.211'
srcToDstSocket.connect((dstIP, dstPort))
print("Connected to destination")

def onChainListener():
    print("Transaction listening started at source gateway")
    data = srcGateway.transactionListener()
    print(data.messageType)
    print("---- 5. Preparing IBC Message ----")
    if(data.messageType == "OTInit"):
        OTRequestMessage = ibcHelper.IBCMessage(
            version=1,
            messageType="OTRequest",
            senderAddress=data.senderAddress,
            recipientAddress=data.recipientAddress,
            senderGWAddress=data.senderGWAddress,
            recipientGWAddress=data.recipientGWAddress,
            tokenBID=data.tokenBID,
            senderBID=data.senderBID,
            recipientBID=data.recipientBID,
            tokenValue=data.tokenValue,
            ownershipCertificate=data.ownershipCertificate #Use the Lock Token Hash here
        )
        print("---- 6. OT Request to destination gateway ----")
        print("From: Source Gateway  To: Destination Gateway")
        srcToDstSocket.send(pickle.dumps(OTRequestMessage))

def offChainListener():
    while True:
        data = srcToDstSocket.recv(16384)
        if len(data) == 0:
            return
        data = pickle.loads(data)
        if(data.messageType == "OTAcceptResponse" or data.messageType == "OTRejectResponse"):
            OTResponseTransaction = srcGateway.sendTransaction(data.recipientGWAddress, data.recipientAddress, data)
            print("---- 13. OTResponse sent to Alice ----")
            print("From: Source Gateway  To: Alice")
            print("Transaction Hash: ", OTResponseTransaction)
        elif(data.messageType == "OERequest"):
            print("---- 5. OEResponse received ----")

            print("---- 6. Signature Verificaton ----")
            print("From: Source Gateway  To: Verify Signature SC")
            print("Transaction Hash: ")

            print("---- 8. Unlock Token ----")
            print("From: Source Gateway  To: Token Locking SC")
            print("Transaction Hash: ")

            print("---- 9. Transfer Token to Charlie ----")
            print("From: Source Gateway  To: Charlie")
            print("Transaction Hash: ")

            print("---- 10. Prepare OEResponse Message ----")
            OEResponseMessage = ibcHelper.IBCMessage(
                version=1,
                messageType="OEResponse",
                senderAddress=ibcHelper.charlieAddress,
                recipientAddress=ibcHelper.bobAddress,
                senderGWAddress=ibcHelper.srcGatewayAddress,
                recipientGWAddress=ibcHelper.dstGatewayAddress,
                tokenBID=data.tokenBID,
                senderBID=data.senderBID,
                recipientBID=data.recipientBID,
                tokenValue=data.tokenValue,
                ownershipCertificate=data.ownershipCertificate #Transaction hash for successful Token transfer
            )

            print("---- 11. OE Response to destination gateway ----")
            print("From: Source Gateway  To: Destination Gateway")
            srcToDstSocket.send(pickle.dumps(OEResponseMessage))
            srcToDstSocket.close()
            return
        

            


if __name__ == "__main__":

    onChainListenerThread = threading.Thread(target=onChainListener, args=())
    onChainListenerThread.start()

    offchainIBCMessageListener_thread = threading.Thread(target=offChainListener(),args=())
    offchainIBCMessageListener_thread.start()