
import tkinter as tk
from tkinter import font
from tkinter import Button
from tkinter import PhotoImage
from simulated_annealing import SimulatedAnnealing

from threading import Thread

from time import sleep
from grade import Grade
from jogo_da_velha_controller import JogoDaVelhaController
from usuario import Usuario

class JogoDaVelhaView(tk.Tk):

    def __init__(self):
        # Define as posições da grade
        self.posicoes = {}

        # Representação lógica do jogo
        self.jogo = JogoDaVelhaController()

        super().__init__()
       
        # Define as telas possiveis do jogo
        self._tela_inicial = self.cria_tela_inicial()
        self._tela_de_jogo = self.cria_grade()


        # Define a tela que está sendo mostrada
        self._tela = None

        # Define o titulo do jogo
        self.title("Jogo da Velha")

        # Define o simbolo escolhido pelo usuário, "X" ou "O"
        self.simbolo_escolhido = ""
        
        # Mostra a tela inicial
        self.muda_tela(self._tela_inicial)

        Thread(target=self.mudanca_listener).start()
    
       
        
    # Checa se houve mudanca no scoring do jogo
    def mudanca_listener(self):
        while True:
          
            numero_de_jogadas = self.jogo._numero_de_jogadas

            numero_de_posicoes_ocupadas = self.jogo.quantidade_espacos_posicionados()

            if numero_de_jogadas == numero_de_posicoes_ocupadas:
                if self.jogo.checa_vencedores() == 'X' or self.jogo.checa_vencedores() == 'O' or self.jogo.checa_empate() == True:
                    sleep(3)
                    self.jogo.reset_controller()
                    self._reset_view()
                    
            sleep(1)
            

    def muda_tela(self, tela, msg=""):
        # Verifica se foi escolhido algum simbolo para jogar
        if msg == "O" or msg == "X":
            self.simbolo_escolhido = msg
            self.jogo._usuario = Usuario(self.simbolo_escolhido)
            
            if msg == "O":
                self.jogo._agente_inteligente.simbolo = "X"
            else:
                self.jogo._agente_inteligente.simbolo = "O"

        nova_tela = tela

        if self._tela is not None:
            self._tela.destroy()

        self._tela = nova_tela
        self._tela.pack(fill=tk.X,expand=10000)

      
        

    def cria_tela_inicial(self):
      
      # Cria a tela inicial do jogo 
      tela_inicial = tk.Frame(master=self, bg="#F5F5F5",pady=20)


      # Cria o texto de iniciação do jogo
      texto_inicial = tk.Label(

            master=tela_inicial,

            text="BEM VINDO AO JOGO DA VELHA! \n \n ESCOLHA O SÍMBOLO \"X\" ou \"O\" PARA JOGAR",

            pady = 100,

            bg="#F5F5F5",

            fg = "#121212",

            font=font.Font(size=12, weight="bold"),

        )
      
      # Cria um botão para tela inicial representando o ícone X
      icone_x = PhotoImage(file = r"assets/icones/icone-x.png") 

      botao_x = Button(tela_inicial, text = "X", image = icone_x, bg = "#F5F5F5", borderwidth=0, command=lambda: self.muda_tela(self._tela_de_jogo,msg="X"))
      botao_x.image = icone_x

      # Cria um botão para tela inicial representando o ícone O
      icone_o = PhotoImage(file = r"assets/icones/icone-o.png") 
      botao_o = Button(tela_inicial, text = "O", image = icone_o, bg = "#F5F5F5", borderwidth=0, command=lambda: self.muda_tela(self._tela_de_jogo,msg="O"))
      botao_o.image = icone_o

      # Configura a tela inicial para aparecer no começo do jogo
      texto_inicial.pack()
      botao_x.pack()
      botao_o.pack(pady=100)

      return tela_inicial

    # Cria a grade na qual o corre o jogo
    def cria_grade(self):

        # Capta a pontuação dos jogadores
        pontuacao_usuario = self.jogo._pontuacao_jogador
        pontuacao_agente_inteligente = self.jogo._pontuacao_agente_inteligente
        contador_empates = self.jogo._contador_empate

        # Cria a tela de jogo
        tela_de_jogo = tk.Frame(master=self, bg="#F5F5F5",pady=100,padx=200)
                        

        # Indica se venceu, empatou ou perdeu
        self.status = tk.Label(
            bg = "#F5F5F5",
            master = tela_de_jogo,
            text = "",
            font=font.Font(size=12, weight="bold"),
            pady=50
        )
        self.status.grid(row=8,column=1)


        # Cria o placar do jogo
        self.placar = tk.Label(
            bg = "#F5F5F5",

            master=tela_de_jogo,

            text=  f"| Usuário: {pontuacao_usuario} | \n |  Computador: {pontuacao_agente_inteligente} | \n | Empates: {contador_empates} |",

            padx=100
        )

        self.placar.grid(row=1,column=5)

        for linha in range(3):
            
            # Configura a grade, as linhas e as colunas
            self.rowconfigure(linha, weight=2, minsize=100)
            self.columnconfigure(linha, weight=2, minsize=125)

            for coluna in range(3):

                espaco = tk.Button(
                    bg = "#F5F5F5",
                    
                    master=tela_de_jogo,

                    image = PhotoImage(file = f"assets/background/background-cor.png") ,

                    font=font.Font(size=48, weight="bold"),

                    fg="black",

                    width=150,

                    height=150,

                    highlightbackground="#121212",

                    highlightthickness = 3,


                )

                self.posicoes[espaco] = (linha, coluna)
               
                espaco.bind("<ButtonPress-1>", self.clique_posicao)

                espaco.grid(
                
                    row=linha,

                    column=coluna,

                    padx=0,

                    pady=0,

                    sticky="nsew"
                )
        
        return tela_de_jogo

    # Atualiza imagem de posicao ao ser escolhida
    def atualiza_imagem_posicao(self, posicao_clicada, simbolo):
        
        simbolo = PhotoImage(file = f"assets/simbolos/simbolo-{simbolo.lower()}.png") 
        posicao_clicada.config(image = simbolo)
        posicao_clicada.image = simbolo
        

    def atualiza_acao_computador(self):
        
  
        if self.jogo.checa_vencedores() == 'X' or self.jogo.checa_vencedores() == 'O' or self.jogo.checa_empate():
                self.atualiza_view()
        else:
            if self.jogo._flag_rodada == 'agente_inteligente':

                melhor_posicao = self.jogo._agente_inteligente.posicionar_simbolo(self.jogo._grade_atual, self.jogo)
                    
                for botao, posicao in self.posicoes.items():                
                    if posicao == melhor_posicao:
                        posicao_clicada = botao
                        self.atualiza_imagem_posicao(posicao_clicada, self.jogo._agente_inteligente.simbolo)

                if self.jogo.checa_vencedores() != '' or self.jogo.checa_empate():
                    self.atualiza_view()

            self.jogo._flag_rodada = 'usuario'

    # Checa se a posicao dada já não foi clicada
    def posicao_selecionada(self, posicao):

     

        # Encontra a coordenada selecionada
        for botao, coordenada in self.posicoes.items():     
            if botao == posicao:
                coordenada_selecionada = coordenada    
                # Checa se a coordenada selecionada está vazia
                simbolo_na_coordenada_selecionada = self.jogo._grade_atual.posicoes[coordenada_selecionada[0]][coordenada_selecionada[1]] 
                
                # Checa se a posicao selecionada contem algum valor
                if simbolo_na_coordenada_selecionada != []:
                    return True

                return False



    # Evento ativado ao jogador clicar em posicao
    def clique_posicao(self, event):
  
        if self.jogo.checa_vencedores() == 'X' or self.jogo.checa_vencedores() == 'O' or self.jogo.checa_empate():
                self.atualiza_view()

        else: 
            if self.jogo._flag_rodada == 'usuario':
                posicao_clicada = event.widget    

                # Checa se a posicao dada já não foi clicada
                if not self.posicao_selecionada(posicao_clicada):

                    linha, coluna = self.posicoes[posicao_clicada]

                    # Posiciona o simbolo escolhido e atualiza a view
                   
                    self.jogo._usuario.posicionar_simbolo(linha, coluna, self.jogo._grade_atual, self.jogo)
                    self.atualiza_imagem_posicao(posicao_clicada, self.jogo._usuario.simbolo)           
                
                    self.jogo._flag_rodada = 'agente_inteligente'
                    self.atualiza_acao_computador()
        
    
    def atualiza_pontuacao(self):
        
        self.jogo.atualiza_pontuacao()
        # Capta a pontuação dos jogadores
        pontuacao_usuario = self.jogo._pontuacao_jogador
        pontuacao_agente_inteligente = self.jogo._pontuacao_agente_inteligente
        contador_empates = self.jogo._contador_empate

        dados_placar=f"| Usuário: {pontuacao_usuario} | \n | Computador: {pontuacao_agente_inteligente} | \n | Empates: {contador_empates} |"
        self.placar.config(text=dados_placar)
        
   
    
    def _reset_view(self):
        
        # Encontra a coordenada selecionada
        for posicao in self.posicoes.keys():   
            posicao.config(highlightbackground="#121212", image=PhotoImage(master=self._tela, file = f"assets/background/background-cor.png"), highlightthickness=3)     
            
        self.status.config(text="")
           


    def _personaliza_empate(self):

        for posicao in self.posicoes.keys():     
            posicao.config(highlightbackground="#F24F00")
            posicao.config(highlightthickness=5)
            self.status.config(text="EMPATE")
            self.status.config(fg="#F24F00")

    def _personaliza_usuario_ganhou(self):
        for posicao, coordenada in self.posicoes.items():

            if coordenada in self.jogo.sequencia_vencedora():
                posicao.config(highlightbackground="#32CD32")
                posicao.config(highlightthickness=5)
                self.status.config(text="VOCÊ VENCEU!")
                self.status.config(fg="#32CD32")

        
    def _personaliza_agente_ganhou(self):
        for posicao, coordenada in self.posicoes.items():

            if coordenada in self.jogo.sequencia_vencedora():
                posicao.config(highlightbackground="#ff0800")
                posicao.config(highlightthickness=5)
                self.status.config(text="VOCÊ PERDEU!")
                self.status.config(fg="#ff0800")


    def atualiza_view(self):
        
        self.jogo._ha_vencedor = self.jogo.checa_vencedores() 
        self.atualiza_pontuacao()

        usuario_ganhou = self.jogo.checa_vencedores() == self.jogo._usuario.simbolo
        agente_ganhou = self.jogo.checa_vencedores() == self.jogo._agente_inteligente.simbolo

        # View de empate
        if self.jogo.checa_empate():
            self._personaliza_empate()
        
        elif usuario_ganhou:
            self._personaliza_usuario_ganhou()
        
        elif agente_ganhou:
            self._personaliza_agente_ganhou()

        

        

            

                

      

