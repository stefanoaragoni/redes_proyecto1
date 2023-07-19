
class Client():

    # This is the constructor for the Client class
    def __init__(self):
        pass

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



    def main(self):
        while True:
            opcion_principal = self.mostrar_menu_principal()

            if opcion_principal == 1:
                # Registrar una nueva cuenta en el servidor
                pass
            elif opcion_principal == 2:
                # Iniciar sesión con una cuenta
                pass
            elif opcion_principal == 3:
                print("\n--> ¡Hasta luego!")
                break
            else:
                print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 3.")

            while opcion_principal in [1, 2]:
                opcion_comunicacion = self.mostrar_menu_comunicacion()

                if opcion_comunicacion == 1:
                    # Mostrar todos los contactos y su estado
                    pass
                elif opcion_comunicacion == 2:
                    # Agregar un usuario a los contactos
                    pass
                elif opcion_comunicacion == 3:
                    # Mostrar detalles de contacto de un usuario
                    pass
                elif opcion_comunicacion == 4:
                    # Comunicación 1 a 1 con cualquier usuario/contacto
                    pass
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
                    break
                else:
                    print("\n--> Opción no válida. Por favor, ingrese un número del 1 al 11.")