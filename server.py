import slixmpp
import prettytable
import xmpp
import asyncio
import time
import client
import curio
import aioconsole 

# *********************************************************************************************************************
# ░██████╗██╗░██████╗░███╗░░██╗  ██╗░░░██╗██████╗░
# ██╔════╝██║██╔════╝░████╗░██║  ██║░░░██║██╔══██╗
# ╚█████╗░██║██║░░██╗░██╔██╗██║  ██║░░░██║██████╔╝
# ░╚═══██╗██║██║░░╚██╗██║╚████║  ██║░░░██║██╔═══╝░
# ██████╔╝██║╚██████╔╝██║░╚███║  ╚██████╔╝██║░░░░░
# ╚═════╝░╚═╝░╚═════╝░╚═╝░░╚══╝  ░╚═════╝░╚═╝░░░░░
# *********************************************************************************************************************

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
        

# *********************************************************************************************************************
# ██╗░░░░░░█████╗░░██████╗░  ██╗███╗░░██╗
# ██║░░░░░██╔══██╗██╔════╝░  ██║████╗░██║
# ██║░░░░░██║░░██║██║░░██╗░  ██║██╔██╗██║
# ██║░░░░░██║░░██║██║░░╚██╗  ██║██║╚████║
# ███████╗╚█████╔╝╚██████╔╝  ██║██║░╚███║
# ╚══════╝░╚════╝░░╚═════╝░  ╚═╝╚═╝░░╚══╝
# *********************************************************************************************************************
        

class Server(slixmpp.ClientXMPP):

    '''
    init: Constructor de la clase Server. Inicializa los handlers de eventos y el estado de logged_in.
    '''

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("muc::invitation", self.handle_group_chat_invite)
        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status", self.changed_status)
        self.add_event_handler("presence", self.request_handler)
        self.logged_in = False
        
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
            
            print("\n\n----- NUEVO MENSAJE -----")
            print(table)
            print("-------------------------\n")

        elif msg['type'] == 'groupchat':
            table = prettytable.PrettyTable()                               # Crear una tabla para mostrar el mensaje
            table.field_names = ["Usuario", "Grupo", "Mensaje"]
            table.add_row([person, msg['mucroom'], msg['body']])       # Agregar emisor, grupo y mensaje a la tabla
            
            print("\n\n----- NUEVO MENSAJE -----")
            print(table)
            print("-------------------------\n")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    handle_group_chat_invite: Función que se ejecuta de forma asincrónica al recibir una invitación a un grupo.
    '''

    async def handle_group_chat_invite(self, invitation):
        print("\n\n----- INVITACIÓN A GRUPO -----")
        print(f"--> Has sido invitado al grupo {invitation['from']} por {invitation['from'].bare}.")
        
        opcion = await self.mostrar_menu_invitacion()

        if opcion == 1:
            # Aceptar invitación
            self.plugin['xep_0045'].joinMUC(invitation['from'], self.boundjid.user, wait=True)
            print(f"--> Has sido agregado al grupo {invitation['from']}.")

        elif opcion == 2:
            # Rechazar invitación
            print(f"--> Has rechazado la invitación al grupo {invitation['from']}.")

        print("--------------------------------\n")


    #-------------------------------------------------------------------------------------------------------------------
    '''
    send_friend_request: Función que envía una solicitud de amistad a un usuario.
    '''

    async def send_friend_request(self):
        print("\n\n----- AGREGAR CONTACTO -----")
        recipient_jid = await self.solicitar_usuario()

        if recipient_jid == self.boundjid.bare:
            print("\n--> No puedes agregarte a ti mismo como contacto.")

        else:
            self.send_presence(pto=recipient_jid, ptype='subscribe')
            print(f"--> Se ha enviado una solicitud de contacto a {recipient_jid}.")

        print("----------------------------\n") 
        
    #-------------------------------------------------------------------------------------------------------------------
    '''
    request_handler: Revisa si la presence subscription fue aceptada o rechazada.
    '''

    async def request_handler(self, presence):
        # Si usuario envio solicitud de amistad
        if presence['type'] == 'subscribe':
            # Aceptar solicitud de amistad automáticamente
            self.send_presence(pto=presence['from'], ptype='subscribed')

            print("\n\n----- SOLICITUD DE AMISTAD -----")
            print(f"--> Se ha agregado a {presence['from']} a tus contactos.")
            print("--------------------------------\n") 

        # Si usuario rechazo solicitud de amistad
        elif presence['type'] == 'unsubscribed':
            print("\n\n----- SOLICITUD DE AMISTAD -----")
            print(f"--> {presence['from']} ha rechazado tu solicitud de amistad / te eliminó de sus contactos.")
            print("--------------------------------\n") 
            self.send_presence(pto=presence['from'], ptype='unsubscribe')

    #--------------------------------------------------------------------------------------------------------------------
    '''
    changed_status: Función que se ejecuta de forma asincrónica al cambiar el estado de un contacto.
    '''

    async def changed_status(self, presence):
        # Si un usuario se conecta o desconecta
        if presence['type'] == 'available' or presence['type'] == 'unavailable' or presence['type'] == 'xa' or presence['type'] == 'away' or presence['type'] == 'dnd':
            jid = presence['from'].bare
            show = presence['type']

            if jid != self.boundjid.bare:                             # Si el contacto no el usuario actual

                if show == 'available':                                 # Si el contacto está chateando
                    show = "Conectado"
                elif show == "away":                                    # Si el contacto está ausente
                    show = "Ausente"
                elif show == "xa":                                      # Si el contacto está ausente por un tiempo largo
                    show = "Ausente por un tiempo largo"
                elif show == "dnd":                                     # Si el contacto no quiere ser molestado
                    show = "No molestar"
                elif show == "unavailable":                             # Si el contacto no está disponible
                    show = "Desconectado"


                print("\n\n----- NOTIFICACION: ESTADO DE CONTACTO -----")
                print(f"--> El estado de {jid} ha cambiado: {show}.")
                print("--------------------------------------------\n")            

        # Si un usuario se pone un mensaje de presencia / status
        elif presence['type'] == 'status':
            jid = presence['from'].bare
            show = presence['status']

            if jid != self.boundjid.bare:                             # Si el contacto no el usuario actual

                print("\n\n----- NOTIFICACION: STATUS -----")
                print(f"--> {jid}: {show}.")
                print("---------------------------------\n")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    get_connections: Función que obtiene los contactos del usuario actual y su estado.
    '''

    async def get_connections(self):
        await self.get_roster()
        roster = self.client_roster                                         # Obtener el roster del usuario actual
        connections = []
        
        for jid in roster.keys():                                           # Por cada contacto en el roster
            
            if jid != self.boundjid.bare:                                   # Si el contacto no es el usuario actual

                obj_jid = roster[jid]                                       # Obtener el objeto del contacto
                resources = obj_jid.resources

                if len(resources) == 0:                                     # Si el contacto no tiene recursos
                    show = "Desconectado"
                    status = ""

                else:
                    for res, data in resources.items():
                        show = data['show']                                    # Obtener el estado del contacto
                        status = data['status']                                 # Obtener el mensaje de presencia del contacto

                        if status is None:                                      # Si el contacto no tiene mensaje de presencia
                            status = ""

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
                        else:
                            show = "Conectado"

                connections.append((jid, show, status))

        print("\n\n----- CONTACTOS -----")

        if len(connections) == 0:
            print("--> No tienes contactos.")

        else:
            table = prettytable.PrettyTable()
            table.field_names = ["Usuario", "Estado", "Mensaje de presencia"]

            for connection in connections:
                table.add_row([connection[0], connection[1], connection[2]])

            print(table)
                
        print("---------------------\n")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    user_contact_details: Funcion que muestra detalles de contacto de un usuario (nombre, grupos, estado, correo, etc).
    '''

    async def user_contact_details(self):
        print("\n----- DETALLES DE CONTACTO -----")
        recipient_jid = await self.solicitar_usuario()
        print(f"--> Buscando detalles de {recipient_jid}...\n")

        await self.get_roster()
        roster = self.client_roster

        if recipient_jid in roster.keys():
            obj_jid = roster[recipient_jid]
            resources = obj_jid.resources
            show = ""

            if len(resources) == 0:                                     # Si el contacto no tiene recursos
                show = "Desconectado"
                status = ""

            for res, data in resources.items():
                show = data['show']                                    # Obtener el estado del contacto
                status = data['status']                                 # Obtener el mensaje de presencia del contacto

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
                else:
                    show = "Conectado"

            print(f"Nombre: {obj_jid.jid.split('@')[0]}")
            print(f"Correo: {obj_jid.jid}")
            print(f"Estado: {show}")
            print(f"Mensaje de presencia: {status}")

        else:
            print("--> No tienes un contacto con ese nombre.")

        print("------------------------------\n")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    send_msg_to_user: Función que envía un mensaje a un usuario.
    '''

    async def send_msg_to_user(self):
        print("\n----- ENVIAR MENSAJE A USUARIO -----")
        recipient_jid = await self.solicitar_usuario()
        user_input = await aioconsole.ainput("Mensaje: ")

        self.send_message(mto=recipient_jid, mbody=user_input, mtype='chat')
        print(f"--> Mensaje enviado a {recipient_jid}.")
        print("----------------------\n")


#-------------------------------------------------------------------------------------------------------------------
# ░██████╗████████╗░█████╗░██████╗░████████╗
# ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
# ╚█████╗░░░░██║░░░███████║██████╔╝░░░██║░░░
# ░╚═══██╗░░░██║░░░██╔══██║██╔══██╗░░░██║░░░
# ██████╔╝░░░██║░░░██║░░██║██║░░██║░░░██║░░░
# ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░
#-------------------------------------------------------------------------------------------------------------------
    '''
    start: Función que se ejecuta al iniciar sesión en el servidor de forma asincrónica.
    '''

    async def start(self, event):
        try:
            self.send_presence()                                            # Enviar presencia  
            self.get_roster()                                               # Obtener roster           
            self.logged_in = True                                           # Cambiar el estado de logged_in a True

            # asyncio create thread that concurrently runs the xmpp_menu function
            xmpp_menu_task = asyncio.create_task(self.xmpp_menu())
            await xmpp_menu_task

            

        except Exception as e:
            print(f"Error: {e}")

#-------------------------------------------------------------------------------------------------------------------
# ███╗░░░███╗███████╗███╗░░██╗██╗░░░██╗
# ████╗░████║██╔════╝████╗░██║██║░░░██║
# ██╔████╔██║█████╗░░██╔██╗██║██║░░░██║
# ██║╚██╔╝██║██╔══╝░░██║╚████║██║░░░██║
# ██║░╚═╝░██║███████╗██║░╚███║╚██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░╚═════╝░
#-------------------------------------------------------------------------------------------------------------------
    '''
    xmpp_menu: Función que muestra el menú de comunicación y ejecuta las funciones correspondientes a cada opción.
    '''

    async def xmpp_menu(self):

        opcion_comunicacion = 0
        while opcion_comunicacion != 9:
            opcion_comunicacion = await self.mostrar_menu_comunicacion()

            if opcion_comunicacion == 1:
                # Mostrar todos los contactos y su estado
                await self.get_connections()
                await asyncio.sleep(1)

            elif opcion_comunicacion == 2:
                # Agregar un usuario a tus contactos
                await self.send_friend_request()
                await asyncio.sleep(1)

            elif opcion_comunicacion == 3:
                # Mostrar detalles de contacto de un usuario
                await self.user_contact_details()
                await asyncio.sleep(1)

            elif opcion_comunicacion == 4:
                # Escribirle a usuario/contacto
                await self.send_msg_to_user()
                await asyncio.sleep(1)

            elif opcion_comunicacion == 5:
                # Participar en conversaciones grupales
                await asyncio.sleep(1)
                
            elif opcion_comunicacion == 6:
                # Definir mensaje de presencia
                await asyncio.sleep(1)

            elif opcion_comunicacion == 7:
                # Enviar/recibir archivos
                await asyncio.sleep(1)

            elif opcion_comunicacion == 8:
                # Cerrar sesión con una cuenta
                print("\n--> Sesión cerrada. Hasta luego.")
                self.disconnect()
                exit()

            elif opcion_comunicacion == 9:
                # Eliminar la cuenta del servidor
                print("\n--> Cuenta eliminada. Hasta luego.")
                await asyncio.sleep(1)

            else:
                print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 11.\n")
                await asyncio.sleep(1)


    async def mostrar_menu_comunicacion(self):
            print("\n----- MENÚ DE COMUNICACIÓN -----")
            print("1) Mostrar todos los contactos y su estado")
            print("2) Agregar un usuario a tus contactos")
            print("3) Mostrar detalles de contacto de un usuario")
            print("4) Escribirle a usuario/contacto")
            print("5) Conversaciones grupales")
            print("6) Definir mensaje de presencia")
            print("7) Enviar archivos")
            print("8) Cerrar sesión")
            print("9) Eliminar la cuenta del servidor")

            while True:
                try:
                    opcion = int(await aioconsole.ainput("Ingrese el número de la opción deseada: "))
                    if opcion in range(1, 9):
                        return opcion
                    else:
                        print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 9.\n")
                except ValueError:
                    print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    async def solicitar_usuario(self):
        while True:
            usuario = await aioconsole.ainput("Ingrese el nombre de usuario: ")
            if usuario != "":
                usuario = usuario.split("@")[0] + "@alumchat.xyz"
                return usuario
            else:
                print("\n--> Usuario inválido. Por favor, ingrese un valor no vacío.")

    async def mostrar_menu_invitacion(self):
        print("\n1) Aceptar invitación")
        print("2) Rechazar invitación")

        while True:
            try:
                opcion = int(await aioconsole.ainput("Ingrese el número de la opción deseada: "))
                if opcion in [1, 2]:
                    return opcion
                else:
                    print("\n--> Opción no válida. Por favor, ingrese 1 o 2.\n")
            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")



