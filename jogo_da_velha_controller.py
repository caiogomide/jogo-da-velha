from minimax import Minimax
import simulated_annealing
from grade import Grade
from usuario import Usuario

class JogoDaVelhaController:
    
    def __init__(self):

        self._usuario = Usuario('')
        self._agente_inteligente = self.cria_agente_inteligente()
        self._flag_rodada = 'usuario'
        self._grade_atual = Grade()

        self._numero_de_jogadas = 0
        
        self._combinacoes_vencedoras = self.get_combinacoes_vencedoras()
        self._ha_vencedor = False
        
        self._pontuacao_jogador = 0
        self._pontuacao_agente_inteligente = 0
        self._contador_empate = 0
    
    '''
    Método responsável por criar um Agente Inteligente
    ao receber um parâmetro que o determina, retorna
    alguma classe herdeira de Agente Inteligente,
    SimulatedAnnealing ou Minimax
    '''
    def cria_agente_inteligente(self):

        entrada_valida = False

        while entrada_valida != True:
       
            print('[1] Para jogar com o Agente Inteligente Minimax \n[2] Para jogar com o Agente Inteligente Simulated Annealing')
            
            agente_inteligente = int(input('Digite o código do Agente Inteligente Desejado: '))

            if agente_inteligente == 1:

                entrada_valida = True
                return Minimax('')

            elif agente_inteligente == 2:

                entrada_valida = True
                return simulated_annealing.SimulatedAnnealing('')

            else:

                print("Entrada Inválida, tente novamente.")

    '''
    Método responsável por calcular e retornar
    a quantidade de espaços já ocupados na
    grade do jogo.
    '''
    def quantidade_espacos_posicionados(self):

        quantidade_espacos_posicionados = 0
        posicoes_grade = self._grade_atual.posicoes

        for linha in posicoes_grade:
            for coluna in linha:
                if coluna == 'X' or coluna == 'O':
                    quantidade_espacos_posicionados+=1

        return quantidade_espacos_posicionados

    '''
    Método responsável por cálcular e retornar
    se há espaços não ocupados em uma grade 
    determinada
    '''
    def ha_espacos_vazios(self):

        posicoes_grade = self._grade_atual.posicoes

        for linha in posicoes_grade:
            for coluna in linha:
                if coluna == []:
                    return True

        return False

    '''
    Método responsável por checar se houve um empate
    no Jogo, dado uma grade, retorna um valor booleano
    '''
    def checa_empate(self):

        if self.ha_espacos_vazios() == False and self.checa_vencedores() == '':
            return True

        return False

    '''
    Método responsável por checa se há vencedores dado uma grade
    caso haja, retorna o simbolo do vencedor, caso não,
    retorna uma string vazia
    '''
    def checa_vencedores(self):

        orientacoes = ['Horizontal', 'Vertical', 'Diagonal']

        # Checa se para cada orientação houve um vencedor
        for orientacao in orientacoes:

            # Checa se há vencedores na orientacao dada
            combinacoes_vencedoras_por_orientacao = self._combinacoes_vencedoras[orientacao]
            posicoes_simbolos = self._grade_atual.posicoes

            for combinacao_vencedora_orientada in combinacoes_vencedoras_por_orientacao:

                combinacao_x = 0
                combinacao_o = 0

                # Checa se cada combinação ocorre
                for i in range(3):
                    linha, coluna = combinacao_vencedora_orientada[i]
                    # Caso um elemento de uma combinação não tenha sido preenchido, pula para próxima combinação
                    if posicoes_simbolos[linha][coluna] == '[]':
                        break
                    # Checa se o elemento na posicao dada é X ou O
                    if posicoes_simbolos[linha][coluna] == 'X':
                        combinacao_x+=1
                    if posicoes_simbolos[linha][coluna] == 'O':
                        combinacao_o+=1
                # Caso haja uma combinacao de 3 elementos na horizontal de X ou O, este é o vencedor
                if combinacao_x == 3:
                    return 'X'
                if combinacao_o == 3:
                    return 'O'
        return ''

    '''
    Método responsável por determinar quais combinações
    são vencedoras para cada orientação, retorna um 
    dicionário contendo as combinações de vitórias
    para cada orientação
    '''
    def get_combinacoes_vencedoras(self):
        # Para haver um vencedor, deve haver 3 símbolos consecutivos na horizontal, diagonal ou vertical   
        
        # 3 Combinações possíveis para vencer na vertical
        combinacao_vencedora_vertical = [[(x,y) for x in range (3)] for y in range(3)]

        # 3 Combinações possíveis para vencer na horizontal
        combinacao_vencedora_horizontal = [[(x,y) for y in range (3)] for x in range(3)]

        # 2 Combinações possíveis para vencer na diagonal
        combinacao_vencedora_diagonal = [[(0,0),(1,1),(2,2)],[(2,0),(1,1),(0,2)]]

        # As 8 combinações possíveis para vencer
        combinacoes_vencedoras_possiveis = {
            'Vertical':combinacao_vencedora_vertical,
            'Horizontal':combinacao_vencedora_horizontal,
            'Diagonal':combinacao_vencedora_diagonal
        }
        
        return combinacoes_vencedoras_possiveis
    
    '''
    Método responsável por determinar, caso haja um vencedor no jogo
    qual foi a sequência que fez o jogador ganhar, retorna uma lista
    contendo as posições dos símbolos que levaram a vitória
    '''
    def sequencia_vencedora(self):

        orientacoes = ['Horizontal', 'Vertical', 'Diagonal']
        vencedor = self.checa_vencedores()

        for orientacao in orientacoes:
            
            # Checa se há vencedores na orientacao dada
            combinacoes_vencedoras_por_orientacao = self._combinacoes_vencedoras[orientacao]
            posicoes_simbolos = self._grade_atual.posicoes

            for combinacao_vencedora_orientada in combinacoes_vencedoras_por_orientacao:

                combinacao_vencedora = 0
                # Checa se cada combinação ocorre
                for i in range(3):
                    linha, coluna = combinacao_vencedora_orientada[i]
                    # Caso um elemento de uma combinação não tenha sido preenchido, pula para próxima combinação
                    if posicoes_simbolos[linha][coluna] == []:
                        break
                    # Checa se o elemento na posicao dada é X ou O
                    if posicoes_simbolos[linha][coluna] == vencedor:
                        combinacao_vencedora+=1
    
                # Caso haja uma combinacao de 3 elementos na horizontal do vencedor, devolve as posicoes desta
                if combinacao_vencedora == 3:
                    return combinacao_vencedora_orientada
                
    '''
    Método responsável por aumentar a pontuação do jogador 
    ou agente inteligente ao ele ganhar, ou aumentar o 
    contador de empate ao ocorrer um empate, não retorna
    valores
    '''
    def atualiza_pontuacao(self):

        if self.checa_vencedores() == self._usuario.simbolo:
            self._pontuacao_jogador += 1

        elif self.checa_vencedores() == self._agente_inteligente.simbolo:
            self._pontuacao_agente_inteligente += 1

        elif self.checa_empate():
            self._contador_empate += 1

    '''
    Método responsável por resetar o controller do jogo
    para o estado inicial, não retorna valores
    '''
    def reset_controller(self):

        self._grade_atual = Grade()
        self._ha_vencedor = False
        self._flag_rodada = 'usuario'
        self._numero_de_jogadas = 0
