
import time
from server import Server, ServerUser
import prettytable
import threading

class Client():

    # This is the constructor for the Client class
    def __init__(self):
        self.server = None

    def mostrar_menu_principal(self):
        print("\n----- MENÚ PRINCIPAL -----")
        print("1) Registrar una nueva cuenta en el servidor")
        print("2) Iniciar sesión con una cuenta")
        print("3) Salir\n")
        
        while True:
            try:
                opcion = int(input("Ingrese el número de la opción deseada: "))
                if opcion in [1, 2, 3]:
                    return opcion
                else:
                    print("\n--> Opción no válida. Por favor, ingrese 1, 2 o 3.\n")
                    
            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    def mostrar_menu_comunicacion(self):
        print("\n----- MENÚ DE COMUNICACIÓN -----")
        print("1) Mostrar todos los contactos y su estado")
        print("2) Agregar un usuario a tus contactos")
        print("3) Mostrar detalles de contacto de un usuario")
        print("4) Escribirle a usuario/contacto")
        print("5) Conversaciones grupales")
        print("6) Definir mensaje de presencia")
        print("7) Enviar notificaciones")
        print("8) Enviar archivos")
        print("9) Cerrar sesión")
        print("10) Eliminar la cuenta del servidor")

        while True:
            try:
                opcion = int(input("Ingrese el número de la opción deseada: "))
                if opcion in range(1, 12):
                    return opcion
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 11.\n")
            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    def solicitar_usuario_contrasena(self):
        while True:
            usuario = input("\nIngrese su nombre de usuario: ")
            contrasena = input("Ingrese su contraseña: ")
            if usuario != "" and contrasena != "":

                usuario = usuario.split("@")[0] + "@alumchat.xyz"

                return usuario, contrasena
            else:
                print("\n--> Usuario y/o contraseña inválidos. Por favor, ingrese valores no vacíos.")

    def customMenu(self, options, menu):
        while True:
            print(f"\n----- {menu} -----")
            for i in range(len(options)):
                print(f"{i+1}) {options[i]}")

            try:
                opcion = int(input("Ingrese el número de la opción deseada: "))
                if opcion in range(1, len(options)+1):
                    return opcion
                else:
                    print(f"\n--> Opción no válida. Por favor, ingrese un número del 1 al {len(options)}.\n")

            except ValueError:
                print("\n--> Entrada inválida. Por favor, ingrese un número entero.\n")

    def solicitar_usuario(self):
        while True:
            usuario = input("Ingrese el nombre de usuario: ")
            if usuario != "":
                usuario = usuario.split("@")[0] + "@alumchat.xyz"
                return usuario
            else:
                print("\n--> Usuario inválido. Por favor, ingrese un valor no vacío.")

    def main(self):
        while True:
            opcion_principal = 0
            success = False

            while not success:
                opcion_principal = self.mostrar_menu_principal()

                if opcion_principal == 1:
                    # Registrar una nueva cuenta en el servidor
                    usuario, contrasena = self.solicitar_usuario_contrasena()
                    serverUser = ServerUser()

                    if serverUser.register(usuario, contrasena):
                        print("\n--> ¡Registro exitoso!")
                    else:
                        print("\n--> ¡Registro fallido!")
                        opcion_principal = 0

                elif opcion_principal == 2:
                    # Iniciar sesión con una cuenta
                    usuario, contrasena = self.solicitar_usuario_contrasena()
                    self.server = Server(usuario, contrasena)

                    self.server.connect(disable_starttls=True)
                    self.xmpp_thread = threading.Thread(target=self.server.process, kwargs={'forever': True})
                    self.xmpp_thread.start()

                    while not self.server.logged_in:
                        pass

                    success = True
                    print("\n--> ¡Inicio de sesión exitoso!")
                        
                elif opcion_principal == 3:
                    print("\n--> ¡Hasta luego!")
                    exit()
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 3.")
                    opcion_principal = 0


            while opcion_principal in [1, 2]:
                opcion_comunicacion = self.mostrar_menu_comunicacion()

                if opcion_comunicacion == 1:
                    # Mostrar todos los contactos y su estado
                    connections = self.server.get_connections()
                    print("\n----- CONTACTOS -----")

                    if len(connections) == 0:
                        print("No tienes contactos.")

                    else:
                        table = prettytable.PrettyTable()
                        table.field_names = ["Usuario", "Estado"]

                        for connection in connections:
                            table.add_row([connection[0], connection[1]])

                        print(table)
                            
                    print("----------------------\n")
                    time.sleep(2)

                elif opcion_comunicacion == 2:
                    # Agregar un usuario a tus contactos

                    print("\n----- AGREGAR CONTACTO -----")
                    recipient_jid = self.solicitar_usuario()
                    self.server.send_friend_request(recipient_jid)
                    print(f"Se ha enviado una solicitud de contacto a {recipient_jid}.")
                    print("----------------------\n") 
                    time.sleep(2)

                elif opcion_comunicacion == 3:
                    # Mostrar detalles de contacto de un usuario
                    time.sleep(2)

                elif opcion_comunicacion == 4:
                    user_input = input("Type a message to send: ")
                    recipient_jid = "maldonado20261@alumchat.xyz"

                    self.server.send_message_to_user(recipient_jid, user_input)
                    time.sleep(2)

                elif opcion_comunicacion == 5:
                    # Participar en conversaciones grupales
                    time.sleep(2)
                    
                elif opcion_comunicacion == 6:
                    # Definir mensaje de presencia
                    time.sleep(2)

                elif opcion_comunicacion == 7:
                    # Enviar/recibir notificaciones
                    time.sleep(2)

                elif opcion_comunicacion == 8:
                    # Enviar/recibir archivos
                    time.sleep(2)

                elif opcion_comunicacion == 9:
                    # Cerrar sesión con una cuenta
                    self.xmpp_thread.join()
                    time.sleep(2)

                elif opcion_comunicacion == 10:
                    # Eliminar la cuenta del servidor
                    self.xmpp_thread.join()
                    time.sleep(2)

                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 11.")