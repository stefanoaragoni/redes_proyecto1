import slixmpp
import prettytable

class Server(slixmpp.ClientXMPP):

    '''
    init: Constructor de la clase Server. Inicializa los handlers de eventos y el estado de logged_in.
    '''

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.logged_in = False

    #-------------------------------------------------------------------------------------------------------------------
    '''
    start: Función que se ejecuta al iniciar sesión en el servidor de forma asincrónica.
    '''

    async def start(self, event):
        try:
            self.send_presence()                                            # Enviar presencia  
            self.get_roster()                                               # Obtener roster           
            self.logged_in = True                                           # Cambiar el estado de logged_in a True

        except Exception as e:
            print(f"Error: {e}")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    message: Función que se ejecuta de forma asincrónica al recibir un mensaje.
    '''

    async def message(self, msg):
        person = msg['from'].bare                                         # Obtener el emisor del mensaje
            
        if msg['type'] in ('chat', 'normal'):                               # Si el mensaje es de tipo chat o normal
            table = prettytable.PrettyTable()                               # Crear una tabla para mostrar el mensaje
            table.field_names = ["Usuario", "Mensaje"]
            table.add_row([person, msg['body']])                       # Agregar emisor y mensaje a la tabla
            
            print("\n\n----- NUEVO MENSAJE -----\n")
            print(table)
            print("\n----------------------\n")

        elif msg['type'] == 'groupchat':
            table = prettytable.PrettyTable()                               # Crear una tabla para mostrar el mensaje
            table.field_names = ["Usuario", "Grupo", "Mensaje"]
            table.add_row([person, msg['mucroom'], msg['body']])       # Agregar emisor, grupo y mensaje a la tabla
            
            print("\n\n----- NUEVO MENSAJE -----\n")
            print(table)
            print("\n----------------------\n")


    #-------------------------------------------------------------------------------------------------------------------

    def get_connections(self):
        roster = self.client_roster                                         # Obtener el roster del usuario actual
        connections = []
        
        for jid in roster.keys():                                           # Por cada contacto en el roster
            
            if jid != self.boundjid.bare:                                   # Si el contacto no es el usuario actual

                obj_jid = roster[jid]                                       # Obtener el objeto del contacto
                resources = obj_jid.resources
                for res, data in resources.items():
                    show = data['show']                                    # Obtener el estado del contacto

                    if show is None:                                        # Si el contacto no tiene estado
                        show = "Conectado"
                    elif show == "chat":                                    # Si el contacto está chateando
                        show = "Conectado"
                    elif show == "away":                                    # Si el contacto está ausente
                        show = "Ausente"
                    elif show == "xa":                                      # Si el contacto está ausente por un tiempo largo
                        show = "Ausente por un tiempo largo"
                    elif show == "dnd":                                     # Si el contacto no quiere ser molestado
                        show = "No molestar"
                    elif show == "unavailable":                             # Si el contacto no está disponible
                        show = "No disponible"

                    connections.append((jid, show))

        return connections                                                  # Devolver una lista de tuplas (jid, tipo de presencia)
    

# *********************************************************************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************


import xmpp
class ServerUser():

    '''
    register: Función que registra un usuario en el servidor con librería xmpp.
    '''

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


 