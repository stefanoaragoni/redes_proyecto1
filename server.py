import xmpp
from sleekxmpp import ClientXMPP

class Server(ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def process_init(self):
        self.process(threaded=True)
        
    def login(self):
        if self.connect():
            return True
        else:
            return False
        
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(f"Received message from {msg['from']}: {msg['body']}")

    def send_xmpp_message(self, recipient, message):
        self.send_message(mto=recipient, mbody=message, mtype='chat')


class ServerUser():

    def register(self, username, password):
        jid = xmpp.protocol.JID(username)
        self.xmpp_client = xmpp.Client(jid.getDomain(), debug=[]) 

        if not self.xmpp_client.connect():
            print("Failed to connect to the XMPP server.")
            return False

        result = bool(xmpp.features.register(self.xmpp_client, jid.getDomain(), {'username': jid.getNode(), 'password': password}))

        if result:
            return True
        else:
            return False


 