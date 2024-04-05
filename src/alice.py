import ibcHelper

aliceUTCFile = "UTC--2024-04-05T08-42-30.674053139Z--d0582e07c048e4ca48c4ef188a106d3313328a08"
password = "1234"
alice = ibcHelper.Node("alice", aliceUTCFile, password)
alice.checkConnection()

ibcMessage = ibcHelper.IBCMessage(
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
        ownershipCertificate="Certificate"
    )

OTInit = alice.sendTransaction(ibcMessage.senderAddress, ibcMessage.senderGWAddress, ibcMessage)
print("OT Initiate Hash: ", OTInit)