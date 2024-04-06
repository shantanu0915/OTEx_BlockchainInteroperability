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
dstPort = 54321
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
        srcToDstSocket.send(pickle.dumps(OTRequestMessage))

def offChainListener():
    OTResponse = pickle.loads(srcToDstSocket.recv(16384))
    print("---- 13. OTResponse received ----")
    srcGateway.sendTransaction(OTResponse.recipientGWAddress, OTResponse.recipientAddress, OTResponse)

if __name__ == "__main__":

    onChainListenerThread = threading.Thread(target=onChainListener, args=())
    onChainListenerThread.start()

    offchainIBCMessageListener_thread = threading.Thread(target=offChainListener(),args=())
    offchainIBCMessageListener_thread.start()