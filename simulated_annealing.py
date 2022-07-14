import random
import math

from random import uniform
from numpy.random import randn, rand, seed
from agente_inteligente import AgenteInteligente
from copy import deepcopy

class SimulatedAnnealing(AgenteInteligente):

    def __init__(self, simbolo):
        
        self.simbolo = simbolo

    '''
    Método responsável por realizar recursivamente
    o algorítimo de Simulated Annealing, até encontrar
    a melhor escolha para o jogo
    '''
    def execute(self, grade, jogo):

        # Posição inicial de análise - Simulação de jogada
        posicao_atual = (0,0)

        # Inicializa o número de iterações
        numero_de_iteracoes = 1

        while True:

            # Calcula a temperatura, dado o número de iterações
            temperatura = self._temperatura(numero_de_iteracoes)

            # Caso a temperatura tenha atingido o valor mínimo, retorna a melhor posição
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

    '''
    Método responsável por cálcular a temperatura, baseado no Simulated
    Annealing, que diminui conforme o número de iterações
    '''
    def _temperatura(self, numero_de_iteracoes):
  
        return int(200/numero_de_iteracoes)

    '''
    Método que retorna um valor booleano indicando
    se uma posição está nos lados da grade do 
    Jogo da Velha
    '''
    def _lados(self, posicao):
  
        lados = [(0,1),(1,2),(2,1),(1,0)]
        return posicao in lados

    '''
    Método que retorna um valor booleano indicando
    se uma posição está nos cantos da grade do
    Jogo da Velha
    '''
    def _cantos(self, posicao):
  
        cantos = [(0,0),(0,2),(2,0),(2,2)]
        return posicao in cantos
    
    '''
    Método que retorna um valor booleano indicando
    se uma posição está no centro da grade do
    Jogo da Velha
    '''
    def _ponto_central(self, posicao):
  
        return posicao == (1,1)

    '''
    Método que retorna um valor booleano indicando 
    se ao posicionar um símbolo do Agente Inteligente
    em determinada posição, está bloqueando a vitória
    do oponente
    '''
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

    '''
    Método que retorna um valor booleano indicando 
    se ao posicionar um símbolo do Agente Inteligente
    em determinada posição, está ganhando o jogo
    '''
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
    
    '''
    Método responsável por análisar uma posição
    e calcular o quão bom este movimento é,
    numa escala de 2 a 10
    '''
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


    '''
    Método responsável por receber uma posição
    como parâmetro e devolver quais são os vizinhos
    desta posição
    '''
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

    '''
    Método responsável por retornar uma posição aleatória
    que não esteja ocupada, e seja vizinha de uma posição
    fornecida como parâmetro
    '''
    def posicao_aleatoria_valida_vizinha(self, grade, posicao):


        vizinhos_da_posicao = self.get_vizinhos_da_posicao(posicao)
        posicoes_validas = self.get_posicoes_validas(grade)

        # Calcula as posições vizinhas de uma posição, que não estejam ocupadas
        posicoes_vizinhas_validas = [vizinho_da_posicao for vizinho_da_posicao in vizinhos_da_posicao if vizinho_da_posicao in posicoes_validas]

        # Caso haja vizinhos, escolhe um, caso não, muda para outra posição valida sequencial
        if len(posicoes_vizinhas_validas) > 0:  
            posicao_aleatoria_valida_vizinha = random.choice(posicoes_vizinhas_validas)
            return posicao_aleatoria_valida_vizinha
        # Caso não haja vizinhos da posição dada, que sejam válidos
        else:
            linha, coluna = posicao
            # Caso ainda haja um espaço na coluna da direita, e que contenha vizinhos, escolhe-a
            if coluna < 2:
                quantidade_de_vizinhos = len(self.posicao_aleatoria_valida_vizinha(grade,(linha, coluna+1)))
                if quantidade_de_vizinhos > 1:
                    return self.posicao_aleatoria_valida_vizinha(grade,(linha, coluna+1))
            # Caso não haja um espaço na coluna da direita, mas há linhas abaixo, escolhe-a
            elif coluna == 2 and linha < 2:
                quantidade_de_vizinhos = len(self.posicao_aleatoria_valida_vizinha(grade,(linha+1, coluna)))
                if quantidade_de_vizinhos > 1:
                    return self.posicao_aleatoria_valida_vizinha(grade,(linha+1, coluna))
            # Caso não haja espaços vizinhos correspondetes, escolhe uma posição aleatória da grade
            else:
                return self.posicao_aleatoria_valida(grade)

    '''
    Método responsável por escolher uma posição
    de forma aleatória, desde que não esteja 
    ocupada por um símbolo
    '''
    def posicao_aleatoria_valida(self, grade):

        posicoes_validas = self.get_posicoes_validas(grade)
        posicao_aleatoria_valida = random.choice(posicoes_validas)
        return posicao_aleatoria_valida

    '''
    Método responsável por encontrar todas as posições
    não ocupadas na grade, retorna-as em forma de lsita
    '''
    def get_posicoes_validas(self, grade):

        posicoes_validas = []

        for linha in range(3):
            for coluna in range(3):
                # Caso o espaço da grade esteja vazio
                if grade.posicoes[linha][coluna] == []:
                    posicoes_validas.append((linha, coluna))

        return posicoes_validas

    '''
    Método responsável por posicionar o simbolo, 
    considerando a melhor opção, dado pelo algorítimo
    Simulated Annealing
    '''
    def posicionar_simbolo(self, grade, jogo):

        melhor_posicionamento = self.execute(grade, jogo)

        # Atualiza a grade com o melhor posicionamento escolhido pelo Simulated Annealing
        grade.atualiza_grade(melhor_posicionamento[0], melhor_posicionamento[1], self.simbolo, jogo)
        return melhor_posicionamento
