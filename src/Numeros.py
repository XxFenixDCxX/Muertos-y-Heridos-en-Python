# Clase que define los atributos de los números
class Numeros:
    def __init__(self, numero, muertos, heridos):
        # Constructor de números con los atributos número, muertos y heridos
        self.__numero = numero
        self.__muertos = muertos
        self.__heridos = heridos
    
    # Getter y setter del atributo 'numero'
    @property
    def numero(self):
        return self.__numero
    
    @numero.setter
    def numero(self, numero):
        self.__numero = numero

    # Getter y setter del atributo 'muertos'
    @property
    def muertos(self):
        return self.__muertos
    
    @muertos.setter
    def muertos(self, muertos):
        self.__muertos = muertos

    # Getter y setter del atributo 'heridos'
    @property
    def heridos(self):
        return self.__heridos
    
    @heridos.setter
    def heridos(self, heridos):
        self.__heridos = heridos
