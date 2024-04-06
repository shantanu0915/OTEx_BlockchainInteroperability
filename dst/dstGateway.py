import sys
sys.path.insert(1, '/home/shantu/IBC_Eth')
import ibcHelper
import threading
import pickle
import socket

dstGatewayUTCFile = "UTC--2024-04-05T10-34-21.561749752Z--e3ee7e3d9f1c99b0633b0a7e5563c68aa5bcf5af"
password = "1234"
dstGateway = ibcHelper.Node("dstGateway", dstGatewayUTCFile, password)
dstGateway.checkConnection()

dstToSrcSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dstToSrcSocket.bind(('192.168.111.211', 54321))
dstToSrcSocket.listen(1)
print("Destination Socket Listening")

conn, addr = dstToSrcSocket.accept()
print("Connected to src via socket at: ", addr)

def offChainListener():
    OTRequest = pickle.loads(conn.recv(16384))
    if(OTRequest.messageType == "OTRequest"):
        print("---- 7. OTRequest received ----")
        print("---- 9. OTRequest sent to recipient ----")
        dstGateway.sendTransaction(OTRequest.recipientGWAddress, OTRequest.recipientAddress, OTRequest)

def onChainListener():
    print("Transaction listening started at destination gateway")
    data = dstGateway.transactionListener()
    if(data.messageType == "y"):
        OTResponseMessage = ibcHelper.IBCMessage(
            version=1,
            messageType="OTAcceptResponse",
            senderAddress=ibcHelper.bobAddress,
            recipientAddress=ibcHelper.aliceAddress,
            senderGWAddress=ibcHelper.dstGatewayAddress,
            recipientGWAddress=ibcHelper.srcGatewayAddress,
            tokenBID="srcBID",
            senderBID="srcBID",
            recipientBID="dstBID",
            tokenValue=data.tokenValue,
            ownershipCertificate=data.ownershipCertificate #Use the Lock Token Hash here
        )
        print("---- 11. Preparing Accept Response ----")
    elif(data.messageType == "n"):
        OTResponseMessage = ibcHelper.IBCMessage(
            version=1,
            messageType="OTRejectResponse",
            senderAddress=ibcHelper.bobAddress,
            recipientAddress=ibcHelper.aliceAddress,
            senderGWAddress=ibcHelper.dstGatewayAddress,
            recipientGWAddress=ibcHelper.srcGatewayAddress,
            tokenBID="srcBID",
            senderBID="srcBID",
            recipientBID="dstBID",
            tokenValue=data.tokenValue,
            ownershipCertificate=data.ownershipCertificate #Use the Lock Token Hash here
        )
        print("---- 11. Preparing Reject Response ----")    
    print("---- 12. Sending OT Response to source gateway ----")
    conn.send(pickle.dumps(OTResponseMessage))

if __name__ == "__main__":

    onChainListenerThread = threading.Thread(target=onChainListener, args=())
    onChainListenerThread.start()

    offchainIBCMessageListenerThread = threading.Thread(target=offChainListener,args=())
    offchainIBCMessageListenerThread.start()