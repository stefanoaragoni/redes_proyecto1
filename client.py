
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
                    self.server.process(forever=False)

                    if not self.server.logged_in:
                        print("\n--> ¡Inicio de sesión fallido!")
                        opcion_principal = 0
                        
                elif opcion_principal == 3:
                    print("\n--> ¡Hasta luego!")
                    exit()
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 3.")
                    opcion_principal = 0


            