from jogador import Jogador

class Usuario(Jogador):

    def __init__(self,simbolo):

        self.simbolo = simbolo

 
    '''
    Método responsável pelo Usuário
    posicionar um símbolo dado uma grade,
    retorna o melhor posicionamento, no formato
    (linha, coluna)
    '''
    def posicionar_simbolo(self, linha, coluna, grade,jogo):
        grade.atualiza_grade(linha, coluna, self.simbolo, jogo) 
        return (linha, coluna)
