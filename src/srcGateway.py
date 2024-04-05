import ibcHelper

srcGatewayUTCFile = "UTC--2024-04-05T08-43-13.525966715Z--ae5c9318f3146d758d9ef83e9d0a8011916d5e53"
password = "1234"
srcGateway = ibcHelper.Node("alice", aliceUTCFile, password)
srcGateway.checkConnection()