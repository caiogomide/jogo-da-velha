class Grade:

    def __init__(self):   

        self.posicoes = self.forma_grade_inicial()

    '''
    Método responsável por devolver uma grade
    inicial, vazia, que é composta por nove
    células, e pode ser acessada no formato
    grade[linha, coluna]
    '''
    def forma_grade_inicial(self):

        grade = []

        for linha in range(3):
            linha = [[],[],[]]
            grade.append(linha)

        return grade

    '''
    Método responsável por atualizar a grade
    ao posicionar um símbolo em determinada
    posição
    '''
    def atualiza_grade(self, linha, coluna, simbolo, jogo):

        self.posicoes[linha][coluna] = simbolo
        jogo._numero_de_jogadas += 1
