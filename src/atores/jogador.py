from src.configuracoes import *
from src.base.entidade import Entidade

class Jogador(Entidade):
    """
    Controla o aluno. Gerencia Pulo, Gravidade e Vidas.
    """
    def __init__(self, nome_personagem="wilque"):
        # Define qual arquivo PNG carregar
        arquivo = "wilque.png" if nome_personagem == "wilque" else "ellen.png"
        
        # Chama a classe mãe
        super().__init__(100, NIVEL_CHAO - 160, 100, 160, arquivo)
        
        self.velocidade_y = 0
        self.esta_pulando = False
        self.vidas = VIDAS_INICIAIS # Configurado para 10
        self.tem_escudo = False
        self.nome = nome_personagem

    def pular(self):
        """Aplica força para cima se não estiver no ar"""
        if not self.esta_pulando:
            self.velocidade_y = FORCA_PULO
            self.esta_pulando = True

    def update(self):
        # Aplica gravidade constante
        self.velocidade_y += GRAVIDADE
        self.rect.y += self.velocidade_y
        
        # Colisão com o chão (impede de cair infinito)
        if self.rect.bottom >= NIVEL_CHAO:
            self.rect.bottom = NIVEL_CHAO
            self.esta_pulando = False
            self.velocidade_y = 0