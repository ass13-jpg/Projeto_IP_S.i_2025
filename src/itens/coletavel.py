import random
from src.configuracoes import *
from src.base.entidade import Entidade

class Item(Entidade):
    """
    Itens: Waffle (Score), Café (Escudo), Luzes (Mudança de Mundo).
    """
    def __init__(self, velocidade_atual, tipo_item):
        self.tipo = tipo_item
        self.velocidade = velocidade_atual
        
        # Seleciona a imagem correta
        if tipo_item == "cafe": nome = 'cafe.png'
        elif tipo_item == "luzes": nome = 'luzes.png'
        else: nome = 'waffle.png'
        
        # Posição Y aleatória para variar o pulo
        pos_y = random.choice([NIVEL_CHAO - 150, NIVEL_CHAO - 300]) 
        
        super().__init__(LARGURA_TELA + random.randint(0, 200), pos_y, 60, 60, nome)

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0: 
            self.kill()