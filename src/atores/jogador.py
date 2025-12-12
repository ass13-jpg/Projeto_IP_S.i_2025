from src.configuracoes import *
from src.base.entidade import Entidade

class Jogador(Entidade):
    """
    Controla o aluno. Gerencia Pulo Duplo, Gravidade e Vidas.
    """
    def __init__(self, nome_personagem="wilque"):
        # Define qual arquivo PNG carregar
        arquivo = "wilque.png" if nome_personagem == "wilque" else "ellen.png"
        
        super().__init__(100, NIVEL_CHAO - 160, 100, 160, arquivo)
        
        self.velocidade_y = 0
        self.vidas = VIDAS_INICIAIS 
        self.tem_escudo = False
        self.nome = nome_personagem
        
        # LÓGICA DO PULO DUPLO 
        self.pulos_dados = 0 # Contador de pulos (0, 1 ou 2)

    def pular(self):
        """Permite pular se tiver dado menos de 2 pulos"""
        if self.pulos_dados < 2:
            self.velocidade_y = FORCA_PULO
            self.pulos_dados += 1 # Conta +1 pulo

    def update(self):
        # Aplica gravidade constante
        self.velocidade_y += GRAVIDADE
        self.rect.y += self.velocidade_y
        
        # Colisão com o chão (Reset do pulo duplo)
        if self.rect.bottom >= NIVEL_CHAO:
            self.rect.bottom = NIVEL_CHAO
            self.velocidade_y = 0
            self.pulos_dados = 0 # Zera o contador ao tocar no chão