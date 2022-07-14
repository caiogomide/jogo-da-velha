from jogador import Jogador

class Usuario(Jogador):

    def __init__(self,simbolo):

        self.simbolo = simbolo

    def posicionar_simbolo(self, linha, coluna, grade,jogo):

        grade.atualiza_grade(linha, coluna, self.simbolo, jogo)
