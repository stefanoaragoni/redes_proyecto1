# *********************************************************************************************************************
# ███████╗██╗ ██████╗ ███╗   ██╗    ██╗   ██╗██████╗ 
# ██╔════╝██║██╔════╝ ████╗  ██║    ██║   ██║██╔══██╗
# ███████╗██║██║  ███╗██╔██╗ ██║    ██║   ██║██████╔╝
# ╚════██║██║██║   ██║██║╚██╗██║    ██║   ██║██╔═══╝ 
# ███████║██║╚██████╔╝██║ ╚████║    ╚██████╔╝██║     
# ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚═╝     
# *********************************************************************************************************************

import xmpp

class ServerUser():

    '''
    register: Función que registra un usuario en el servidor con librería xmpp
    '''

    def register(self, username, password):
        jid = xmpp.protocol.JID(username)
        self.xmpp_client = xmpp.Client(jid.getDomain(), debug=[]) 

        if not self.xmpp_client.connect():
            print("--> No se pudo conectar al servidor XMPP.")
            return False

        #-----> Generado por GitHub Copilot
        result = bool(xmpp.features.register(self.xmpp_client, jid.getDomain(), {'username': jid.getNode(), 'password': password}))
        #-------------------------------

        if result:
            return True
        else:
            return False
        
# *********************************************************************************************************************
# ██╗      ██████╗  ██████╗     ██╗███╗   ██╗
# ██║     ██╔═══██╗██╔════╝     ██║████╗  ██║
# ██║     ██║   ██║██║  ███╗    ██║██╔██╗ ██║
# ██║     ██║   ██║██║   ██║    ██║██║╚██╗██║
# ███████╗╚██████╔╝╚██████╔╝    ██║██║ ╚████║
# ╚══════╝ ╚═════╝  ╚═════╝     ╚═╝╚═╝  ╚═══╝
# *********************************************************************************************************************

from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream import ElementBase, ET, register_stanza_plugin
import slixmpp
import prettytable
import threading
import asyncio
import aioconsole 
import base64
import time 

class Server(slixmpp.ClientXMPP):

    '''
    init: Constructor de la clase Server. Inicializa los handlers de eventos y el estado de logged_in.
    '''

    def __init__(self, jid, password):
        super().__init__(jid, password)
        #-----> Plugins generados por GitHub Copilot
        self.register_plugin('xep_0030')                                   # Registrar plugin: Service Discovery
        self.register_plugin('xep_0045')                                   # Registrar plugin: Multi-User Chat
        self.register_plugin('xep_0085')                                   # Registrar plugin: Chat State Notifications
        self.register_plugin('xep_0199')                                   # Registrar plugin: XMPP Ping
        self.register_plugin('xep_0353')                                   # Registrar plugin: Chat Markers
        #-------------------------------

        #-----> Stanza personalizada
        self.register_stanza(self.delete_account)

        #-----> Handlers de eventos
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status", self.changed_status)
        self.add_event_handler("presence", self.request_handler)
        self.add_event_handler("groupchat_message", self.group_message)

        self.logged_in = False
        
    #-------------------------------------------------------------------------------------------------------------------
    '''
    start: Función que se ejecuta al iniciar sesión en el servidor de forma asincrónica.
    '''

    async def start(self, event):
        try:
            self.send_presence()                                            # Enviar presencia  
            self.get_roster()                                               # Obtener roster           

            # Creación de hilo para manejar el menú de comunicación
            xmpp_menu_task = asyncio.create_task(self.xmpp_menu())
            await xmpp_menu_task            

        except Exception as e:
            print(f"Error: {e}")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    xmpp_menu: Función que muestra el menú de comunicación y ejecuta las funciones correspondientes a cada opción.
    '''

    async def xmpp_menu(self):

        print("\n--> Sesión iniciada. Bienvenidx.\n\n")
        self.logged_in = True

        print("---------- MENSAJES / NOTIFICACIONES ----------")
        await asyncio.sleep(3)
        print("\n\n-----------------------------------------------\n")

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
                opcion_grupo = await self.menu_grupos()

                if opcion_grupo == 1:
                    # Enviar mensaje en grupo
                    await self.send_group_message()
                
                elif opcion_grupo == 2:
                    # Crear grupo nuevo
                    await self.create_group()

                await asyncio.sleep(1)
                
            elif opcion_comunicacion == 6:
                # Definir mensaje de presencia
                await self.set_presence()
                await asyncio.sleep(1)

            elif opcion_comunicacion == 7:
                # Enviar/recibir archivos
                await self.send_file_to()
                await asyncio.sleep(1)

            elif opcion_comunicacion == 8:
                # Cerrar sesión con una cuenta
                print("\n--> Sesión cerrada. Hasta luego.")
                self.disconnect()
                exit()

            elif opcion_comunicacion == 9:
                # Eliminar la cuenta del servidor
                await self.delete_account()
                await asyncio.sleep(1)

            else:
                print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 11.\n")
                await asyncio.sleep(1)

# *********************************************************************************************************************
#  █████╗ ███████╗██╗███╗   ██╗ ██████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
# ██╔══██╗██╔════╝██║████╗  ██║██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗
# ███████║███████╗██║██╔██╗ ██║██║     ██████╔╝██║   ██║██╔██╗ ██║██║   ██║
# ██╔══██║╚════██║██║██║╚██╗██║██║     ██╔══██╗██║   ██║██║╚██╗██║██║   ██║
# ██║  ██║███████║██║██║ ╚████║╚██████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
# ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
# *********************************************************************************************************************
    '''
    message: Función que se ejecuta de forma asincrónica al recibir un mensaje.
    '''

    async def message(self, msg):
        if msg['type'] == 'chat' and "file_transfer_request" in msg['body']:        # Recibir archivo
            person = msg['from'].bare                                               # Obtener el emisor del mensaje
            nombre_archivo = msg['body'].split(":")[1]                              # Obtener el nombre del archivo
            contenido_archivo = msg['body'].split(":")[2]                           # Obtener el contenido del archivo

            print("\n\n----- NUEVO ARCHIVO -----")
            print(f"De: {person}")
            print(f"Archivo: {nombre_archivo}")
            print("-------------------------")

            file_data = base64.b64decode(contenido_archivo)
            nombre_archivo = "recibido_" + nombre_archivo

            with open(nombre_archivo, "wb") as file:
                file.write(file_data)


        elif msg['type'] == 'chat':
            person = msg['from'].bare                                         # Obtener el emisor del mensaje
                
            if msg['type'] in ('chat', 'normal'):                               # Si el mensaje es de tipo chat o normal
                table = prettytable.PrettyTable()                               # Crear una tabla para mostrar el mensaje
                table.field_names = ["Usuario", "Mensaje"]
                table.add_row([person, msg['body']])                       # Agregar emisor y mensaje a la tabla
                
                print("\n\n----- NUEVO MENSAJE -----")
                print(table)
                print("-------------------------")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    group_message: Función que se ejecuta de forma asincrónica al recibir un mensaje de un grupo.
    '''

    async def group_message(self, msg):
        if msg['mucnick'] != self.boundjid.user:
            print("\n\n----- MENSAJE DE GRUPO -----")
            print(f"Grupo: {str(msg['from']).split('/')[0]}")
            print(f"De: {msg['mucnick']}")
            print(f"Mensaje: {msg['body']}")
            print("--------------------------------")

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
        print("----------------------")
 
    #-------------------------------------------------------------------------------------------------------------------
    '''
    send_group_message: Función que envía un mensaje a un grupo.
    '''

    async def send_group_message(self):
        response = await self.plugin['xep_0030'].get_items(jid="conference.alumchat.xyz", node="")

        values = response['disco_items']['items']
        grupos = []

        for value in values:
            grupos.append((value[0], value[2]))

        opcion = await self.seleccionar_grupo(grupos)
        JID_grupo = grupos[opcion-1][0]

        await self.plugin['xep_0045'].join_muc(JID_grupo, self.boundjid.user)       # Se une al grupo, en caso de que no esté unido

        print("\n--> Escriba el mensaje que desea enviar al grupo.")
        user_input = await aioconsole.ainput("Mensaje: ")

        self.send_message(mto=JID_grupo, mbody=user_input, mtype='groupchat')
        print(f"--> Mensaje enviado a {grupos[opcion-1][0]}")
        print("----------------------")

    #-------------------------------------------------------------------------------------------------------------------
    '''
    send_file: Función que envía un archivo a un usuario.
    '''

    async def send_file_to(self):
        print("\n----- ENVIAR ARCHIVO A USUARIO -----")
        recipient_jid = await self.solicitar_usuario()
        file_path = await aioconsole.ainput("Ingrese la ruta del archivo: ")
        file_name = file_path.split("/")[-1]

        # Intentar abrir el archivo
        file_data = None
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
        except FileNotFoundError:
            print("\n--> Archivo no encontrado.")
            print("----------------------")
            return
        
        file_data_base64 = base64.b64encode(file_data).decode('utf-8')
        
        self.send_message(mto=recipient_jid, mbody=f"file_transfer_request:{file_name}:{file_data_base64}", mtype="chat")
        file.close()

    #-------------------------------------------------------------------------------------------------------------------
    '''
    create_group: Función que crea un grupo.
    '''

    async def create_group(self):
        nombre = await self.crear_grupo()
        nombre = nombre.replace("@", "") + "@conference.alumchat.xyz"

        await self.plugin['xep_0045'].join_muc(nombre, self.boundjid.user, password=None)

        #-----> Generado por ChatGPT para poner el grupo como público y persistente
        form = await self.plugin['xep_0045'].get_room_config(nombre)
        form['muc#roomconfig_publicroom'] = True
        form['muc#roomconfig_persistentroom'] = True
        await self.plugin['xep_0045'].set_room_config(nombre, form)
        #-------------------------------

        await self.plugin['xep_0045'].join_muc(nombre, self.boundjid.user, password=None)

        print(f"--> Grupo {nombre} creado.")
        print("----------------------")

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
            print("--------------------------------") 

        # Si usuario rechazo solicitud de amistad
        elif presence['type'] == 'unsubscribed':
            print("\n\n----- SOLICITUD DE AMISTAD -----")
            print(f"--> {presence['from']} ha rechazado tu solicitud de amistad / te eliminó de sus contactos.")
            print("--------------------------------") 
            self.send_presence(pto=presence['from'], ptype='unsubscribe')

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

        print("----------------------------") 
       
    #-------------------------------------------------------------------------------------------------------------------
    '''
    get_connections: Función que obtiene los contactos del usuario actual y su estado.
    '''

    async def get_connections(self):
        await self.get_roster()
        roster = self.client_roster                                         # Obtener el roster del usuario actual
        connections = []
        
        for jid in roster.keys():                                           # Por cada contacto en el roster
            
            if jid != self.boundjid.bare and "@conference.alumchat.xyz" not in jid: # Si el contacto no es el usuario actual

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
                
        print("---------------------")

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

        print("------------------------------")

    #--------------------------------------------------------------------------------------------------------------------
    '''
    changed_status: Función que se ejecuta de forma asincrónica al cambiar el estado de un contacto.
    '''

    async def changed_status(self, presence):
        jid = presence['from'].bare
        show = presence['type']
        status = presence['status']

        if "@conference.alumchat.xyz" in jid:
            return

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

            print("\n\n----- NOTIFICACION: ESTADO / MENSAJE -----")

            if status == "":
                print(f"-Usuario: {jid}\n-Estado: {show}")
            else:
                print(f"-Usuario: {jid}\n-Estado: {show}\n-Mensaje: {status}")

            print("------------------------------------------")       

    #-------------------------------------------------------------------------------------------------------------------
    '''
    set_presence: Función que define el mensaje de presencia del usuario.
    '''

    async def set_presence(self):
        opcion = await self.mostrar_menu_estado()

        if opcion == 1:
            mensaje = await aioconsole.ainput("Ingrese el mensaje de presencia: ")
            self.send_presence(pstatus=mensaje)

            print("\n--> Mensaje de presencia modificado.")

        elif opcion == 2:
            estado = await self.solicitar_estado()
            if estado == 1:
                self.send_presence(pshow="chat")
            elif estado == 2:
                self.send_presence(pshow="away")
            elif estado == 3:
                self.send_presence(pshow="xa")
            elif estado == 4:
                self.send_presence(pshow="dnd")
            elif estado == 5:
                self.send_presence(pshow="unavailable")

            print("\n--> Estado modificado.")

        print("----------------------")
        
        # Menu - Definir mensaje o estado

    #-------------------------------------------------------------------------------------------------------------------
    '''
    delete_account: Función que elimina la cuenta del servidor.
    '''

    async def delete_account(self):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['from'] = self.boundjid.user
    
        # ---> Generado por GitHub Copilot
        query = ET.Element('{jabber:iq:register}query')
        remove_element = ET.SubElement(query, 'remove')
        iq.append(query)
        # ------------------------------

        try:
            response = await iq.send()
            print("Eliminando cuenta...")
            time.sleep(3)

            if response['type'] == 'result':
                self.disconnect()
                print("\n--> Cuenta eliminada. Hasta luego.")
                exit()
            else:
                print("\n--> No se pudo eliminar la cuenta.")
        except (IqError, IqTimeout) as e:
            print("\n--> No se pudo eliminar la cuenta.")

# *********************************************************************************************************************
# ███╗   ███╗███████╗███╗   ██╗██╗   ██╗███████╗
# ████╗ ████║██╔════╝████╗  ██║██║   ██║██╔════╝
# ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║███████╗
# ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║╚════██║
# ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝███████║
# ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
# *********************************************************************************************************************

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
                    if opcion in range(1, 10):
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

    async def mostrar_menu_estado(self):
        print("\n----- MENÚ DE MENSAJE DE PRESENCIA -----")
        print("1) Modificar mensaje")
        print("2) Modificar estado")

        while True:
            try:
                opcion = int(await aioconsole.ainput("Ingrese el número de la opción deseada: "))
                if opcion in range(1, 3):
                    return opcion
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 2.\n")
            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    async def solicitar_estado(self):
        print("\n--> Estados disponibles:")
        print("1) Conectado")
        print("2) Ausente")
        print("3) Ausente por un tiempo largo")
        print("4) No molestar")
        print("5) Desconectado")

        while True:
            try:
                opcion = int(await aioconsole.ainput("Ingrese el número de la opción deseada: "))
                if opcion in range(1, 6):
                    return opcion
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 5.\n")
            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    async def menu_grupos(self):
        print("\n----- MENÚ DE GROUP CHATS -----")
        print("1) Enviar mensaje en grupo")
        print("2) Crear grupo nuevo")

        while True:
            try:
                opcion = int(await aioconsole.ainput("Ingrese el número de la opción deseada: "))
                if opcion in range(1, 3):
                    return opcion
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 2.\n")
            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    async def seleccionar_grupo(self, grupos):
        print("\n--> Grupos disponibles:")
        for i in range(len(grupos)):
            print(f"{i+1}) {grupos[i][0]}")

        while True:
            try:
                opcion = int(await aioconsole.ainput("Ingrese el número de la opción deseada: "))
                if opcion in range(1, len(grupos)+1):
                    return opcion
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 2.\n")
            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    async def crear_grupo(self):
        nombre = await aioconsole.ainput("Ingrese el nombre del grupo: ")
        return nombre




