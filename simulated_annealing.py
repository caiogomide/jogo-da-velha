import random
from random import uniform
from numpy.random import randn, rand, seed
import math
from copy import deepcopy

from agente_inteligente import AgenteInteligente

class SimulatedAnnealing(AgenteInteligente):

    def __init__(self, simbolo):
        
        self.simbolo = simbolo

    # Executa recursivamente a têmpera simulada até encontrar a melhor alternativa
    def execute(self, grade, jogo):

        # Posição inicial de análise - Simulação de jogada
        posicao_atual = (0,0)

        # Define o número de iterações inicial
        numero_de_iteracoes = 1

        while True:

            temperatura = self._temperatura(numero_de_iteracoes)

            if temperatura == 0:
                return posicao_atual

            # Analisa uma proxima posicao, vizinha da posicao atual, e que seja válida (não esteja ocupada)         
            proxima_posicao = self.posicao_aleatoria_valida_vizinha(grade, posicao_atual)
              
            # Faz análise da diferença da qualidade dos movimentos
            qualidade_atual = self.calcula_qualidade_movimento(posicao_atual, jogo) 
            proxima_qualidade = self.calcula_qualidade_movimento(proxima_posicao, jogo) 

            diferenca_qualidade = proxima_qualidade - qualidade_atual

            # Caso a qualidade da próxima ação seja maior que a qualidade da ação analisada atualmente
            if diferenca_qualidade > 0:
                posicao_atual = proxima_posicao
  
            # Analisa probabilidade de a ação dada ser boa no futuro
            elif(random.uniform(0,1)<(math.e)**(diferenca_qualidade/temperatura)):
                posicao_atual = proxima_posicao
            
            numero_de_iteracoes+=1

    # Cacula a temperatura da Simulated Annealing
    def _temperatura(self, numero_de_iteracoes):
  
        return int(200/numero_de_iteracoes)

    # Analisa se uma posição está definida nos lados da grade
    def _lados(self, posicao):
  
        lados = [(0,1),(1,2),(2,1),(1,0)]
        return posicao in lados

    # Analisa se uma posição está definida nos cantados da grade
    def _cantos(self, posicao):
  
        cantos = [(0,0),(0,2),(2,0),(2,2)]
        return posicao in cantos
    
    # Analisa se uma posição está definida no centro da grade
    def _ponto_central(self, posicao):
  
        return posicao == (1,1)


    

    # Analisa se uma posição está bloqueando o ganho do oponente
    def _bloqueia_oponente(self, posicao, jogo):

        linha, coluna = posicao

        # Recria o jogo na situação hipotética do movimento dado
        jogo_hipotetico = deepcopy(jogo)

        # Recria o movimento hipotético
        jogo_hipotetico._grade_atual.posicoes[linha][coluna] = jogo_hipotetico._usuario.simbolo

        # Analisa se o oponente colocar um simbolo na posicao dada ele bloqueia o movimento
        if jogo_hipotetico.checa_vencedores() == jogo_hipotetico._usuario.simbolo:
            return True
        else:
            return False

    def _ganha_o_jogo(self, posicao, jogo):

        linha, coluna = posicao

        # Recria o jogo na situação hipotética do movimento dado
        jogo_hipotetico = deepcopy(jogo)

        # Recria o movimento hipotético
        jogo_hipotetico._grade_atual.posicoes[linha][coluna] = jogo_hipotetico._agente_inteligente.simbolo

        # Analisa se o agente inteligente colocar um simbolo na posicao dada ele ganha
        if jogo_hipotetico.checa_vencedores() == jogo_hipotetico._agente_inteligente.simbolo:
            return True
        else:
            return False
    
    # Calcula um valor para a qualidade do movimento dado - de 2 a 10
    def calcula_qualidade_movimento(self, posicao, jogo):

        if self._ganha_o_jogo(posicao, jogo):            
            return 10

        elif self._bloqueia_oponente(posicao, jogo):
            return 6

        if self._ponto_central(posicao):
            return 5

        elif self._cantos(posicao):
            return 4

        elif self._lados(posicao):
            return 3

        else:
            return 2


    def get_vizinhos_da_posicao(self, posicao):

        vizinhos_por_posicao = {
            (0,0) : [(0,1), (1,0)],
            (0,1) : [(0,0), (0,2), (1,1)],
            (0,2) : [(1,2),(0,1)],
            (1,0) : [(0,0),(1,1)],
            (1,1) : [(0,1),(1,2),(2,1),(1,0)],
            (1,2) : [(0,2),(1,1),(2,2)],
            (2,0) : [(1,0),(2,1)],
            (2,1) : [(1,1),(2,2),(2,0)],
            (2,2) : [(1,2),(2,1)]
        }

        return vizinhos_por_posicao[posicao]

    def posicao_aleatoria_valida_vizinha(self, grade, posicao):

        vizinhos_da_posicao = self.get_vizinhos_da_posicao(posicao)
        posicoes_validas = self.get_posicoes_validas(grade)
        posicoes_vizinhas_validas = [vizinho_da_posicao for vizinho_da_posicao in vizinhos_da_posicao if vizinho_da_posicao in posicoes_validas]

        # Caso haja vizinhos, escolhe um, caso não, muda para outra posição valida sequencial
        if len(posicoes_vizinhas_validas) > 0:  

            posicao_aleatoria_valida_vizinha = random.choice(posicoes_vizinhas_validas)
            return posicao_aleatoria_valida_vizinha

        else:

            linha, coluna = posicao
            if coluna < 2:
                quantidade_de_vizinhos = len(self.posicao_aleatoria_valida_vizinha(grade,(linha, coluna+1)))
                if quantidade_de_vizinhos > 1:
                    return self.posicao_aleatoria_valida_vizinha(grade,(linha, coluna+1))
            elif coluna == 2 and linha < 2:
                quantidade_de_vizinhos = len(self.posicao_aleatoria_valida_vizinha(grade,(linha+1, coluna)))
                if quantidade_de_vizinhos > 1:
                    return self.posicao_aleatoria_valida_vizinha(grade,(linha+1, coluna))
            else:
                return self.posicao_aleatoria_valida(grade)

    def posicao_aleatoria_valida(self, grade):

        posicoes_validas = self.get_posicoes_validas(grade)
        posicao_aleatoria_valida = random.choice(posicoes_validas)
        return posicao_aleatoria_valida

    def get_posicoes_validas(self, grade):

        posicoes_validas = []

        for linha in range(3):
            for coluna in range(3):
                # Caso o espaço da grade esteja vazio
                if grade.posicoes[linha][coluna] == []:
                    posicoes_validas.append((linha, coluna))
                    
        return posicoes_validas


    def posicionar_simbolo(self, grade, jogo):

        melhor_posicionamento = self.execute(grade, jogo)

        grade.atualiza_grade(melhor_posicionamento[0], melhor_posicionamento[1], self.simbolo, jogo)

        return melhor_posicionamento
