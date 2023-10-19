# -*- coding: utf-8 -*-
# Colores para utilizar
rojo = "\033[31m"
verde = "\033[32m"
azul = "\033[34m"
default = "\033[0m"
from src.Usuarios import Usuario
from src.Numeros import Numeros
from src.Gestor import Gestor
import getpass
import os
import time

# Función para limpiar la pantalla de la consola
def clear():
    if os.name == 'nt':  # Si el sistema operativo es Windows, ejecutamos el comando cls
        os.system('cls')
    else:  # Y si no es Windows, ejecutamos el comando clear
        os.system('clear')

# Inicializamos una variable de la clase Gestor
gestor = Gestor()
# Variable para activar que el número siempre aparezca arriba
debuger = True
# Logeo de los usuarios
clear()
print(azul + "BIENVENIDO")
# Tiempo antes de iniciar sesión
print("==========\n")
print("Por favor, introduce tu usuario y contraseña para continuar (Si no estás registrado, introduce el usuario que quieres y el programa te dará la opción de logearte)\n" + default)
# Comprueba si se ha podido logear; si no lo ha conseguido, se queda en bucle hasta conseguirlo
loginCorrecto = False
while (loginCorrecto == False):
    usuarioLogin = Usuario(input("Introduce tu usuario: "))
    if len(usuarioLogin.nombre) > 6:  # Se asegura de que el nombre de usuario no es demasiado largo
        contrasenaCorrecta = False
        print(rojo + "El usuario no puede tener más de 7 caracteres" + default)
        input()
        clear()
    elif gestor.comprobarUsuario(usuarioLogin.nombre):  # Comprueba si el usuario introducido existe
        # Comprueba si la contraseña es correcta y si no, sigue dentro del bucle
        contrasenaCorrecta = False
        while (contrasenaCorrecta == False):
            usuarioLogin.contrasena = getpass.getpass("Introduce tu contraseña (no se verá lo que escribes): ")
            if gestor.logeoUsuario(usuarioLogin):  # Comprueba si el logeo del usuario es correcto
                print(verde + "Se ha registrado con éxito" + default)
                loginCorrecto = True
                contrasenaCorrecta = True
            else:  # Si no lo es, le obliga a permanecer en el bucle
                print(rojo + "La contraseña es incorrecta" + default)
                contrasenaCorrecta = False
    else:  # Si no existe el usuario introducido, le pregunta si desea registrarse
        registro = input("El usuario no existe, ¿deseas registrarte con ese usuario (S/N): ")
        if str(registro).lower() == "s":  # Comprueba si la elección es la de realizar el registro
            usuarioLogin.contrasena = getpass.getpass("Introduce la contraseña para tu usuario (no se verá lo que escribes): ")
            gestor.registroUsuario(usuarioLogin)  # Realiza el registro agregándolo al fichero
            print(verde + "Usuario registrado con éxito" + default)
            loginCorrecto = True
        else:
            clear()
            loginCorrecto = False
usuarioLogin = gestor.getUsuario(usuarioLogin.nombre)
input(azul + "Pulsa una tecla para continuar..." + default)
clear()

# Menú
opcion = 0
while opcion != 3:
    try:
        print(azul + "EL JUEGO DE LOS MUERTOS Y HERIDOS")
        print("=================================")
        print("1.- Jugar")
        print("2.- Ranking")
        print("3.- Salir\n")
        opcion = int(input(default + "Selecciona qué quieres realizar (1-3): "))

        if opcion == 1:
            # Comienzo de juego
            gestor.nuevoNumero()
            gestor.ganado = False
            intentos = 0
            while True:
                clear()
                inicioTiempo = time.time()
                if debuger:
                    print(gestor.numeroAdivinar)
                numCorrecto = False
                print(gestor.juego())
                while numCorrecto == False:
                    if intentos != gestor.INTENTOS:
                        numero = input("Introduce el número: ")
                    if gestor.numeroEsValido(numero):
                        gestor.introducirNumero(numero)
                        numCorrecto = True
                    else:
                        print(rojo + "El número introducido tiene que ser de 4 dígitos, no puede estar repetido y ninguna de las 4 cifras puede ser la misma 2 veces" + default)

                intentos += 1
                puntos = gestor.INTENTOS*10 - intentos * 10
                if gestor.ganado:
                    clear()
                    finalTiempo = time.time()
                    tiempoTotal = int(finalTiempo - inicioTiempo)
                    print(gestor.juego())
                    print(verde + "\n\t\t¡Enhorabuena, has acertado el número!" + default)
                    print(f"\n\t{azul}Intentos: {default}{intentos}\t{azul}Puntos: {default}{puntos}\t{azul}Tiempo: {default}{tiempoTotal}s")
                    print(f"\n\t{azul}Usuario Actual: {default}{usuarioLogin.nombre}\t{azul}Puntos: {default}{usuarioLogin.puntos}\t{azul}Tiempo: {default}{usuarioLogin.tiempo}\n")
                    gestor.numerosIntroducidos = []
                    guardar = 0
                    while guardar != 1 and guardar != 2:
                        try:
                            guardar = int(input("¿Deseas registrar esta partida o quedarte con tus puntos y tiempo actuales? 1.-Si 2.-No: "))
                            if guardar != 1 and guardar != 2:
                                print(rojo + "La opción elegida no es correcta, introduce 1 o 2" + default)
                            elif guardar == 1:
                                if usuarioLogin.puntos == "None":
                                    gestor.asignarPuntosTiempo(usuarioLogin, puntos, tiempoTotal)
                                else:
                                    gestor.asignarPuntosTiempo(usuarioLogin, int(usuarioLogin.puntos) + puntos, tiempoTotal)
                                print(verde + "Datos almacenados correctamente..." + default)
                            elif guardar == 2:
                                print(rojo + "Saliendo al menú sin almacenar ningún dato..." + default)
                        except ValueError:
                            print(rojo + "La opción elegida no es correcta, introduce 1 o 2" + default)
                    break
                if intentos == gestor.INTENTOS:
                    print(rojo+f"Lo siento, has perdido :(, el numero era {gestor.numeroAdivinar} y pierdes 10 puntos"+default)
                    if usuarioLogin.puntos == "None":
                        gestor.asignarPuntosTiempo(usuarioLogin, -10, usuarioLogin.tiempo)
                    else:
                        gestor.asignarPuntosTiempo(usuarioLogin, int(usuarioLogin.puntos) -10, usuarioLogin.tiempo)
                    gestor.numerosIntroducidos = []
                    break
            input()
            clear()
        elif opcion == 2:
            # Ranking
            clear()
            opcion = 3
            while opcion != 1 and opcion != 2:  # Bucle para comprobar si la opción seleccionada es correcta y si no lo es, le mantiene dentro
                opcion = int(input("¿Quieres ver el ranking de 1.-Tiempo o el de 2.-Puntos? (1-2): "))
                if opcion != 1 and opcion != 2:  # Mensaje para la opción incorrecta
                    print(rojo + "Tienes que seleccionar 1 o 2" + default)
                    input()
                    clear()
                elif opcion == 1:
                    clear()
                    print(gestor.ranking(False))  # Muestra el ranking por tiempo
                    input(azul + "Pulsa una tecla para continuar...")
                    clear()
                elif opcion == 2:
                    clear()
                    print(gestor.ranking())  # Muestra el ranking por puntos
                    input(azul + "Pulsa una tecla para continuar...")
                    clear()

        elif opcion == 3:
            print(verde + "\n¡Espero que hayas disfrutado del juego! CHAO :)" + default)  # Finalización del programa
            input()

    except ValueError:  # Comprobación de si el valor introducido es correcto y si no lo es, muestra un mensaje y le muestra de nuevo el menú
        print(rojo + "\nEl valor introducido no es válido" + default)
        opcion = 0
        input()
        clear()