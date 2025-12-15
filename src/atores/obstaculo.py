import random
from src.configuracoes import *
from src.assets_paths import *
from src.base.entidade import Entidade

class Obstaculo(Entidade):
    """
    Inimigos que se movem da direita para a esquerda.
    """
    def __init__(self, velocidade_atual):
        # Sorteia o tipo de inimigo
        tipo = random.choice(['demodog', 'cadeira'])
        
        if tipo == 'demodog':
            # Demodog: Baixo e Largo
            super().__init__(LARGURA_TELA + random.randint(0, 400), NIVEL_CHAO - 88, 120, 180, IMAGEM_DEMODOG)
        else:
            # Cadeira: Alta e Estreita
            super().__init__(LARGURA_TELA + random.randint(0, 400), NIVEL_CHAO - 95, 80, 130, IMAGEM_CADEIRA)
            
        self.velocidade = velocidade_atual

    def update(self):
        # Move para a esquerda
        self.rect.x -= self.velocidade
        
        # Limpeza de memória: Destrói se sair da tela
        if self.rect.right < 0: 
            self.kill()