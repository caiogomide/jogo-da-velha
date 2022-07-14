from abc import ABC, abstractmethod

class Jogador(ABC):

    def __init__(self,simbolo):

        self.simbolo = simbolo

    '''
    Método responsável pelo posicionamento de um 
    símbolo, por parte do usuário ou agente
    inteligente
    '''
    @abstractmethod
    def posicionar_simbolo(self, linha, coluna, grade):

        pass


