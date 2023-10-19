# Clase que define la estructura de los Usuarios
class Usuario:
    def __init__(self, nombre=None, contrasena=None, intentos=None, tiempo=None):
        # Constructor de usuarios con atributos a None para no tener que definirlos al crear un objeto
        self.__nombre = nombre
        self.__contrasena = contrasena
        self.__intentos = intentos
        self.__tiempo = tiempo

    # Getters y setters de nombre
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    # Getters y setters de contraseña
    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, contrasena):
        self.__contrasena = contrasena

    # Getters y setters de puntos
    @property
    def puntos(self):
        return self.__intentos

    @puntos.setter
    def puntos(self, intentos):
        self.__intentos = intentos

    # Getters y setters de tiempo
    @property
    def tiempo(self):
        return self.__tiempo

    @tiempo.setter
    def tiempo(self, tiempo):
        self.__tiempo = tiempo

    def __str__(self):
        # Método especial que convierte un objeto Usuario en una cadena para ser agregada al fichero
        return f"{self.__nombre}*{self.__contrasena}*{self.__intentos}*{self.__tiempo}"

    def __eq__(self, otroUsuario):
        # Método especial para verificar si un usuario es igual a otro usuario
        if isinstance(otroUsuario, Usuario):
            return self.nombre.lower() == otroUsuario.nombre.lower()
        return False
