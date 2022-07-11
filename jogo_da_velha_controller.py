   
from agente_inteligente import AgenteInteligente
from grade import Grade
from usuario import Usuario


class JogoDaVelhaController:
    
    def __init__(self):
        self._usuario = Usuario('')
        self._agente_inteligente = AgenteInteligente('')
        self._grade_atual = Grade()
        self._combinacoes_vencedoras = self.get_combinacoes_vencedoras()
        self._ha_vencedor = False
        self._flag_rodada = 'usuario'
        self._pontuacao_jogador = 0
        self._pontuacao_agente_inteligente = 0
        self._contador_empate = 0
    


    def ha_espacos_vazios(self):
        posicoes_grade = self._grade_atual.posicoes
        for linha in posicoes_grade:
            for coluna in linha:
                if coluna == []:
                    return True
        return False

    def checa_empate(self):
        if self.ha_espacos_vazios() == False and self.checa_vencedores() == '':
            return True
        return False

    # Retorna se "X" ou "O" venceram
    def checa_vencedores(self):

        orientacoes = ['Horizontal', 'Vertical', 'Diagonal']

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
    
    def atualiza_pontuacao(self):
        if self.checa_vencedores() == self._usuario.simbolo:
            self._pontuacao_jogador += 1
        elif self.checa_vencedores() == self._agente_inteligente.simbolo:
            self._pontuacao_agente_inteligente += 1
        elif self.checa_empate():
            self._contador_empate += 1

    def reset_controller(self):
        self._grade_atual = Grade()
        self._ha_vencedor = False
        self._flag_rodada = 'usuario'