from jogador import Jogador

from abc import abstractmethod

class AgenteInteligente(Jogador):

    def __init__(self,simbolo):

        self.simbolo = simbolo

    '''
    Método responsável pelo Agente Inteligente
    posicionar um símbolo dado uma grade,
    retorna o melhor posicionamento, no formato
    (linha, coluna)
    '''
    @abstractmethod
    def posicionar_simbolo(self, grade, jogo):

        pass

