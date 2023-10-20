# Clase que se encarga de comprobar la inserción correcta en los ficheros para los datos y el control de aciertos
from src.Usuarios import Usuario
from src.Numeros import Numeros
import random

# Colores para los mensajes en la consola
rojo = "\033[31m"
verde = "\033[32m"
azul = "\033[34m"
default = "\033[0m"

# Clase Gestor
class Gestor:
    INTENTOS = 14  # Constante con el número de intentos
    __numeroAdivinar = 0
    __ganado = False  # Variable para saber si la partida ha sido ganada o no
    __usuarios = []  # Lista donde se almacenan todos los usuarios del fichero
    __numerosIntroducidos = []  # Lista donde se almacenan los números introducidos por el usuario
    __pathFichero = "./src/usuarios.txt"  # Ruta del fichero de los usuarios

    def __init__(self):
        # Constructor: inicializa la lista de usuarios y crea el fichero si no existe
        try:
            ficheroUsuarios = open(self.__pathFichero, "r")
            for linea in ficheroUsuarios:
                datos = linea.split("*")
                self.__usuarios.append(Usuario(datos[0].strip(), datos[1].strip(), datos[2].strip(), datos[3].strip()))
            ficheroUsuarios.close()
        except FileNotFoundError:
            ficheroUsuarios = open(self.__pathFichero, "x")
            ficheroUsuarios.close()

    # Getters y setters
    @property
    def usuarios(self):
        return self.__usuarios

    @usuarios.setter
    def usuarios(self, usuarios):
        self.__usuarios = usuarios

    @property
    def numerosIntroducidos(self):
        return self.__numerosIntroducidos

    @numerosIntroducidos.setter
    def numerosIntroducidos(self, numerosIntroducidos):
        self.__numerosIntroducidos = numerosIntroducidos

    @property
    def numeroAdivinar(self):
        return self.__numeroAdivinar

    @property
    def ganado(self):
        return self.__ganado

    @ganado.setter
    def ganado(self, ganado: bool):
        self.__ganado = ganado

    def comprobarUsuario(self, nombre):
        # Validador de si existe o no existe el usuario
        tempUser = Usuario(nombre)
        if tempUser in self.__usuarios:
            return True
        return False

    def logeoUsuario(self, usuario: Usuario):
        # Comprueba si la contraseña es correcta, devuelve True si lo es, False si no
        if (usuario.contrasena == self.__usuarios[self.__usuarios.index(usuario)].contrasena):
            return True
        return False

    def asignarPuntosTiempo(self, usuario: Usuario, puntos, tiempo):
        # Actualiza los puntos y tiempo del usuario y guarda los cambios en el fichero
        self.__usuarios.remove(usuario)
        usuario.puntos = puntos
        usuario.tiempo = tiempo
        self.__usuarios.append(usuario)
        self.__reescribirFichero()

    def registroUsuario(self, usuario: Usuario):
        # Registra un nuevo usuario con puntos y tiempo iniciales y guarda la información en el fichero
        usuario.puntos = "None"
        usuario.tiempo = "None"
        self.__usuarios.append(usuario)
        self.__reescribirFichero()

    def ranking(self, puntos=True):
        # Genera y muestra el ranking de usuarios, ya sea por puntos o tiempo
        ranking = ""
        usuariosOrdenadosRanking = []
        if puntos:
            ranking += azul + "RANKING DE USUARIOS CON MEJOR PUNTUACIÓN\n========================================\n\n"
            usuarioAgregar = None
            restaPorNones = 0
            for usuario in self.__usuarios:
                if isinstance(usuario, Usuario):
                    if usuario.puntos == "None":
                        restaPorNones += 1
            while len(usuariosOrdenadosRanking) != len(self.__usuarios) - restaPorNones:
                puntosMax = float('-inf')
                tiempoMin = float('inf')
                for usuario in self.__usuarios:
                    if isinstance(usuario, Usuario):
                        if (usuario.puntos != "None" and int(usuario.puntos) > puntosMax and usuario not in usuariosOrdenadosRanking) or \
                                (usuario.puntos != "None" and int(usuario.puntos) == puntosMax and usuario.tiempo != "None" and int(usuario.tiempo) < tiempoMin and usuario not in usuariosOrdenadosRanking):
                            puntosMax = int(usuario.puntos)
                            tiempoMin = int(usuario.tiempo)
                            usuarioAgregar = usuario
                usuariosOrdenadosRanking.append(usuarioAgregar)
        else:
            ranking += azul + "RANKING DE USUARIOS CON MEJOR TIEMPO\n====================================\n\n"
            usuarioAgregar = None
            restaPorNones = 0
            for usuario in self.__usuarios:
                if isinstance(usuario, Usuario):
                    if usuario.tiempo == "None":
                        restaPorNones += 1
            while len(usuariosOrdenadosRanking) != len(self.__usuarios) - restaPorNones:
                puntosMax = float('-inf')
                tiempoMin = float('inf')
                for usuario in self.__usuarios:
                    if isinstance(usuario, Usuario):
                        if (usuario.tiempo != "None" and int(usuario.tiempo) < tiempoMin and usuario not in usuariosOrdenadosRanking) or \
                                (usuario.tiempo != "None" and int(usuario.tiempo) == tiempoMin and usuario.puntos != "None" and int(usuario.puntos) > puntosMax and usuario not in usuariosOrdenadosRanking):
                            puntosMax = int(usuario.puntos)
                            tiempoMin = int(usuario.tiempo)
                            usuarioAgregar = usuario
                usuariosOrdenadosRanking.append(usuarioAgregar)

        ranking += verde + "\tUSUARIO\t\tPUNTOS\t\tTIEMPO\n\t-------\t\t------\t\t------\n" + default
        posicion = 1
        for usuario in usuariosOrdenadosRanking:
            if isinstance(usuario, Usuario):
                ranking += f"{posicion}.-\t{usuario.nombre}\t\t{int(usuario.puntos)}\t\t{int(usuario.tiempo)}s\n"
                posicion += 1
        return ranking

    def __reescribirFichero(self):
        # Reescribe la información de usuarios en el fichero
        try:
            ficheroUsuarios = open(self.__pathFichero, "w")
            for usuario in self.__usuarios:
                ficheroUsuarios.write(usuario.__str__() + "\n")
            ficheroUsuarios.close()
        except FileNotFoundError:
            ficheroUsuarios = open(self.__pathFichero, "x")
            ficheroUsuarios.close()

    def getUsuario(self, nombre_usuario): 
    # Devuelve el usuario solicitado
        for usuario in self.__usuarios:
            if isinstance(usuario, Usuario) and usuario.nombre == nombre_usuario:
                return usuario
        return None  # Devuelve None si no se encuentra el usuario
    
    def nuevoNumero(self):
        # Genera un nuevo número aleatorio para adivinar
        tempNum = random.sample(range(10), 4)
        numero = ""
        for num in tempNum:
            numero += str(num)
        self.__numeroAdivinar = numero

    def introducirNumero(self, numero):
        # Introduce un nuevo número, verifica cuántos muertos y heridos hay, y actualiza la información del juego
        muertos = 0
        heridos = 0
        for i in range(0, 4):
            if numero[i] == self.__numeroAdivinar[i]:
                muertos += 1
            elif self.__numeroAdivinar.__contains__(numero[i]):
                heridos += 1
        self.__numerosIntroducidos.append(Numeros(numero, muertos, heridos))
        if numero == self.__numeroAdivinar:
            self.__ganado = True

    def numeroEsValido(self, num) -> bool:
        # Verifica si el número es válido (no repetido y consta de 4 dígitos)
        valido = True
        for numero in self.__numerosIntroducidos:
            if isinstance(numero, Numeros):
                if numero.numero == num:
                    valido = False
                    break
        if not num.isdigit() or len(num) != 4:
            valido = False
        if len(num) != len(set(num)):
            valido = False
        return valido

    def juego(self):
        # Genera la representación del juego en la consola
        juego = ""
        juego += azul + "EL JUEGO DE LOS MUERTOS Y HERIDOS\n=================================\n"
        juego += azul + "¿LISTO PARA ENCONTRAR EL NÚMERO DE 4 CIFRAS?\n"
        juego += "¡Cuidado que ninguna cifra se repite!\n\n" + default
        juego += verde + "#\t\tNUMERO\t\tMUERTOS\t\tHERIDOS\n-\t\t------\t\t-------\t\t-------\n" + default
        if len(self.__numerosIntroducidos) == 0:
            juego += "\t\t\tCOMENZAMOS"
        else:
            pos = 1
            for num in self.__numerosIntroducidos:
                if isinstance(num, Numeros):
                    juego += f"{pos}\t\t{num.numero}\t\t{num.muertos}\t\t{num.heridos}\n"
                    pos += 1
        return juego