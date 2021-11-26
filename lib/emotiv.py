from websockets import connect


class Emotiv:
    def __init__(self, headsetId:  str, clientSecret: str, clientId: str, url="wss://localhost:6868"):
        self.ws = connect(url)
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.headsetId = headsetId
        self.cortexToken = None

    def connect(self):
        self.ws.send({
            "id": 1,
            "jsonrpc": "requestAccess",
            "params": {
                "clientId": self.clientId,
                "clientSecret": self.clientSecret
            }
        })
        ac = self.ws.recv()["result"]["accessGranted"]
        if not ac:
            return "hello"

        self.ws.send({
            "id": 1,
            "jsonrpc": "autorize",
            "params": {
                "clientId": self.clientId,
                "clientSecret": self.clientId
            }
        })
        self.cortexToken = self.ws.recv()["results"]["cortexToken"]

        self.ws.send({
            "id": 1,
            "jsonrpc": "createSession",
            "params": {
                "cortexToken": self.cortexToken,
                "headset": self.headsetId,
                "status": "open"
            }
        })
        self.sessionId = self.ws.recv()["results"]

        self.ws.send({
            "id": 1,
            "jsonrpc": "subscribe",
            "params": {
                "cortexToken": self.cortexToken,
                "headset": self.headsetId,
                "status": "open"
            }
        })
