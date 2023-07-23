
from server import Server, ServerUser
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
        print("2) Agregar un usuario a los contactos")
        print("3) Mostrar detalles de contacto de un usuario")
        print("4) Comunicación 1 a 1 con cualquier usuario/contacto")
        print("5) Participar en conversaciones grupales")
        print("6) Definir mensaje de presencia")
        print("7) Enviar notificaciones")
        print("8) Enviar archivos")
        print("9) Cerrar sesión con una cuenta")
        print("10) Eliminar la cuenta del servidor")
        print("11) Volver al menú principal\n")

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
                    #usuario, contrasena = self.solicitar_usuario_contrasena()
                    usuario = "alberto20261@alumchat.xyz"
                    contrasena = "Onika1009!"
                    self.server = Server(usuario, contrasena)

                    self.server.connect(disable_starttls=True)
                    self.xmpp_thread = threading.Thread(target=self.server.process, kwargs={'forever': True})
                    self.xmpp_thread.start()

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
                    for connection in connections:
                        print(f"{connection[0]} - {connection[1]}")
                    print("----------------------\n")

                elif opcion_comunicacion == 2:
                    # Agregar un usuario a los contactos
                    pass
                elif opcion_comunicacion == 3:
                    # Mostrar detalles de contacto de un usuario
                    pass
                elif opcion_comunicacion == 4:
                    user_input = input("Type a message to send: ")
                    recipient_jid = "maldonado20261@alumchat.xyz"

                    self.server.send_message_to_user(recipient_jid, user_input)

                elif opcion_comunicacion == 5:
                    # Participar en conversaciones grupales
                    pass
                elif opcion_comunicacion == 6:
                    # Definir mensaje de presencia
                    pass
                elif opcion_comunicacion == 7:
                    # Enviar/recibir notificaciones
                    pass
                elif opcion_comunicacion == 8:
                    # Enviar/recibir archivos
                    pass
                elif opcion_comunicacion == 9:
                    # Cerrar sesión con una cuenta
                    pass
                elif opcion_comunicacion == 10:
                    # Eliminar la cuenta del servidor
                    pass
                elif opcion_comunicacion == 11:
                    self.xmpp_thread.join()
                    break
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 11.")