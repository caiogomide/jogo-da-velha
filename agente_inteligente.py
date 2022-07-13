from jogador import Jogador

from abc import abstractmethod


class AgenteInteligente(Jogador):

    def __init__(self,simbolo):
        self.simbolo = simbolo

    @abstractmethod
    def posicionar_simbolo(self, grade, jogo):
        pass

    # Recria jogo para não alterar localmente o jogo real
    def _recria_jogo_hipotetico(self, jogo, grade):
        jogo_hipotetico = jogo
        jogo_hipotetico.grade = grade
        return jogo_hipotetico
