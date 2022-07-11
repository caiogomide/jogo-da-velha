from abc import ABC, abstractmethod

class Jogador(ABC):

    def __init__(self,simbolo):
        self.simbolo = simbolo

    @abstractmethod
    def posicionar_simbolo(self, linha, coluna, grade):
        pass
