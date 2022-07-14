from jogador import Jogador

from abc import abstractmethod

class AgenteInteligente(Jogador):

    def __init__(self,simbolo):

        self.simbolo = simbolo

    @abstractmethod
    def posicionar_simbolo(self, grade, jogo):
        
        pass


