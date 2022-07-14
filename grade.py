class Grade:

    def __init__(self):   

        self.posicoes = self.forma_grade_inicial()

    def forma_grade_inicial(self):

        grade = []

        for linha in range(3):
            linha = [[],[],[]]
            grade.append(linha)
            
        return grade

    def atualiza_grade(self, linha, coluna, simbolo, jogo):

        self.posicoes[linha][coluna] = simbolo
        jogo._numero_de_jogadas += 1
    
    
