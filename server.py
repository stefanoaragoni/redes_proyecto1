import slixmpp
import logging

class Server(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.logged_in = False

    async def start(self, event):
        try:
            self.send_presence()
            self.get_roster()
            self.logged_in = True

        except Exception as e:
            print(f"Error: {e}")

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(f"Received message from {msg['from']}: {msg['body']}")

import xmpp
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


 