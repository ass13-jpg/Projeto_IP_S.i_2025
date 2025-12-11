import pygame
import random
import os

# --- CORREÇÃO DE IMPORTAÇÃO (Igual ao Gerenciador) ---
try:
    from src.configuracoes import *
except ModuleNotFoundError:
    from configuracoes import *
# -----------------------------------------------------

class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, nome_imagem):
        super().__init__()
        caminho_completo = os.path.join('assets', 'imagens', nome_imagem)
        try:
            imagem_original = pygame.image.load(caminho_completo).convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (largura, altura))
        except Exception:
            self.image = pygame.Surface((largura, altura))
            if 'jogador' in nome_imagem: cor = AZUL
            elif 'demodog' in nome_imagem or 'cadeira' in nome_imagem: cor = PRETO
            elif 'cafe' in nome_imagem: cor = MARROM
            elif 'luzes' in nome_imagem: cor = VERDE_LUZ
            else: cor = AMARELO
            self.image.fill(cor)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

class Jogador(Entidade):
    def __init__(self):
        super().__init__(100, NIVEL_CHAO - 160, 100, 160, 'jogador.png') 
        self.velocidade_y = 0
        self.esta_pulando = False
        self.vidas = 3
        self.tem_escudo = False

    def pular(self):
        if not self.esta_pulando:
            self.velocidade_y = FORCA_PULO
            self.esta_pulando = True

    def update(self):
        self.velocidade_y += GRAVIDADE
        self.rect.y += self.velocidade_y
        if self.rect.bottom >= NIVEL_CHAO:
            self.rect.bottom = NIVEL_CHAO
            self.esta_pulando = False
            self.velocidade_y = 0

class Obstaculo(Entidade):
    def __init__(self, velocidade_atual):
        tipo = random.choice(['demodog', 'cadeira'])
        if tipo == 'demodog':
            super().__init__(LARGURA_TELA + random.randint(0, 400), NIVEL_CHAO - 80, 120, 80, 'demodog.png')
        else:
            super().__init__(LARGURA_TELA + random.randint(0, 400), NIVEL_CHAO - 120, 80, 120, 'cadeira.png')
        self.velocidade = velocidade_atual

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()

class Item(Entidade):
    def __init__(self, velocidade_atual, tipo_item):
        self.tipo = tipo_item
        self.velocidade = velocidade_atual
        if tipo_item == "cafe": nome_arq = 'cafe.png'
        elif tipo_item == "luzes": nome_arq = 'luzes.png'
        else: nome_arq = 'waffle.png'
        pos_y = random.choice([NIVEL_CHAO - 150, NIVEL_CHAO - 300]) 
        super().__init__(LARGURA_TELA + random.randint(0, 200), pos_y, 60, 60, nome_arq)

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()