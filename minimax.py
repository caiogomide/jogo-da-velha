from agente_inteligente import AgenteInteligente


class Minimax(AgenteInteligente):

    def __init__(self,simbolo):

        self.simbolo = simbolo

    '''
    Método responsável por realizar a lógica recursiva
    do algorítimo minimax, retorna a melhor opção de
    jogada dado uma grade
    '''
    def minimax(self, grade, maximizando, jogo, profundidade):

        pontuacao = self.avaliador(jogo)

        # Caso o Agente Inteligente tenha sido bem sucedido e vencido

        if(pontuacao == 10):
            return pontuacao 

        # Caso o Agente Inteligente tenha sido mal sucedido e perdido

        if(pontuacao == -10):
            return pontuacao

        # Caso o Agente Inteligente tenha empatado com o Usuário

        if (jogo.checa_empate()):
            return 2

        # Caso seja o turno do Agente Inteligente
        if maximizando:

            melhor_opcao = -100

            for linha in range(3):
                for coluna in range(3):
                    # Caso o espaço da grade esteja vazio
                    if grade.posicoes[linha][coluna] == []:

                        # Faz o movimento com o simbolo do Agente Inteligente
                        grade.posicoes[linha][coluna] = self.simbolo
                        
                        # Escolhe o máximo valor para determinação do movimento do jogo
                        melhor_opcao = max(melhor_opcao, self.minimax(grade, False, jogo, profundidade+1))
                        # Remove o movimento hipotético feito para análise
                        grade.posicoes[linha][coluna] = []

            return melhor_opcao

        # Caso seja o turno do Usuário
        if not maximizando:
            melhor_opcao = 100

            for linha in range(3):
                for coluna in range(3):
                    # Caso o espaço da grade esteja vazio
                    if grade.posicoes[linha][coluna] == []:
                        # Faz o movimento com o simbolo do Usuário
                        grade.posicoes[linha][coluna] = jogo._usuario.simbolo
                        # Escolhe o máximo valor para determinação do movimento do jogo
                        melhor_opcao = min(melhor_opcao, self.minimax(grade, True, jogo, profundidade+1))
                        # Remove o movimento hipotético feito para análise
                        grade.posicoes[linha][coluna] = []

            return melhor_opcao

    '''
    Método responsável por avaliar, se dado um jogo,
    o usuário ou o agente inteligente ganhou, ou, ainda,
    se houve empate, e atribui um valor para cada caso,
    que representa o interesse do Agente Inteligente
    por essa escolha
    '''
    def avaliador(self, jogo):
       
        # Analisa vitoria do Usuario
        if jogo.checa_vencedores() == jogo._usuario.simbolo:
            return -10

        # Analisa vitoria do Agente Inteligente
        if jogo.checa_vencedores() == self.simbolo:
            return 10

        # Caso ninguem tenha ganhado o jogo
        return 0

    '''
    Método responsável por posicionar o simbolo, 
    considerando a melhor opção, dado pelo algorítimo
    Minimax
    '''
    def posicionar_simbolo(self, grade, jogo):

        melhor_opcao = -1000
        melhor_posicionamento = (0,0)
        
        for linha in range(3):
            for coluna in range(3):
                # Caso o espaço da grade esteja vazio
                if grade.posicoes[linha][coluna] == []:
                    # Faz o movimento com o simbolo do Agente Inteligente
                    grade.posicoes[linha][coluna] = self.simbolo
                    # Calcula o quão bom esse movimento dado é
                    avaliacao = self.minimax(grade, False, jogo, 0)
                    # Remove o movimento hipotético feito para análise
                    grade.posicoes[linha][coluna] = []
                    # Caso o movimento avaliado seja melhor que o melhor movimento, este é o melhor
                    if(avaliacao > melhor_opcao):
                        melhor_posicionamento = (linha, coluna)
                        melhor_opcao = avaliacao
        # Atualiza a grade com o melhor posicionamento escolhido pelo Minimax
        grade.atualiza_grade(melhor_posicionamento[0], melhor_posicionamento[1], self.simbolo,jogo)
        return melhor_posicionamento

