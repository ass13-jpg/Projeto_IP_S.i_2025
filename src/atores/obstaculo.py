import random
from src.configuracoes import *
from src.assets_paths import *
from src.base.entidade import Entidade

class Obstaculo(Entidade):
    """
    Inimigos que se movem da direita para a esquerda.
    Agora suporta o DEMOGORGON (mais rápido) e filtra objetos por mundo.
    """
    # 1. Adicionamos o parametro 'mundo_invertido' aqui no final
    def __init__(self, velocidade_atual, eh_demogorgon=False, mundo_invertido=False):
        
        if eh_demogorgon:
            # --- DEMOGORGON (BOSS) ---
            # Ele é mais rápido que o cenário (1.5x) para dar susto
            self.velocidade = velocidade_atual * 1.5
            
            super().__init__(
                LARGURA_TELA + random.randint(0, 200), 
                NIVEL_CHAO - 320, 
                280, 400, 
                IMAGEM_DEMOGORGON
            )
            
        else:
            # --- INIMIGOS NORMAIS ---
            self.velocidade = velocidade_atual
            
            # 2. LÓGICA DE FILTRO DO MUNDO
            if mundo_invertido:
                # No mundo invertido, NÃO existe cadeira, apenas monstros.
                tipo = 'demodog'
            else:
                # No mundo normal, sorteia entre Demodog e Cadeira
                tipo = random.choice(['demodog', 'cadeira'])
            
            # --- CRIAÇÃO DO SPRITE BASEADO NO TIPO ---
            if tipo == 'demodog':
                # Demodog: Baixo e Largo
                super().__init__(LARGURA_TELA + random.randint(0, 400), NIVEL_CHAO - 180, 220, 320, IMAGEM_DEMODOG)
            else:
                # Cadeira: Alta e Estreita
                super().__init__(LARGURA_TELA + random.randint(0, 400), NIVEL_CHAO - 150, 180, 200, IMAGEM_CADEIRA)

    def update(self):
        # Move para a esquerda
        self.rect.x -= self.velocidade
        
        # Limpeza de memória: Destrói se sair da tela
        if self.rect.right < 0: 
            self.kill()