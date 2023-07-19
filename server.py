import xmpp

class Server:

    # Constructor
    def __init__(self, server, port):
        self.server = server
        self.port = port

    # Register a new account in the server
    def register(self, username, password):
        jid = xmpp.JID(username)
        self.client = xmpp.Client(jid.getDomain(), debug=[])
        self.client.connect(server=(self.server, self.port))






