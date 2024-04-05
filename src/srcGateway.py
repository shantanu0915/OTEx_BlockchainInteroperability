import ibcHelper
import threading
import pickle

def onChainListener(srcGateway):
    print("Transaction listening started at source gateway")
    data = srcGateway.transactionListener()
    print(data.messageType)

if __name__ == "__main__":

    srcGatewayUTCFile = "UTC--2024-04-05T08-43-13.525966715Z--ae5c9318f3146d758d9ef83e9d0a8011916d5e53"
    password = "1234"
    srcGateway = ibcHelper.Node("srcGateway", srcGatewayUTCFile, password)
    srcGateway.checkConnection()

    onChainListenerThread = threading.Thread(target=onChainListener, args=(srcGateway,))
    onChainListenerThread.start()