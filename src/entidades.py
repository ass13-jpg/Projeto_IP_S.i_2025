import pygame
import random
import os

try:
    from src.configuracoes import *
except ModuleNotFoundError:
    from configuracoes import *

class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, nome_imagem):
        super().__init__()
        
        # --- LÓGICA DE PASTAS (CORRIGIDA) ---
        dir_atual = os.path.dirname(os.path.abspath(__file__))
        dir_raiz = os.path.dirname(dir_atual)
        
        # Se for um dos personagens, busca na pasta 'personagens'
        if nome_imagem.lower() in ['wilque.png', 'ellen.png']:
            pasta = 'personagens'
        else:
            # Itens e Inimigos ficam na pasta 'imagens'
            pasta = 'imagens'
            
        caminho_completo = os.path.join(dir_raiz, 'assets', pasta, nome_imagem)
        # ------------------------------------
        
        try:
            imagem_original = pygame.image.load(caminho_completo).convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (largura, altura))
        except Exception:
            # Fallback de cor se falhar
            self.image = pygame.Surface((largura, altura))
            if 'wilque' in nome_imagem: cor = (0, 0, 255)
            elif 'ellen' in nome_imagem: cor = (255, 105, 180)
            elif 'demodog' in nome_imagem or 'cadeira' in nome_imagem: cor = (0, 0, 0)
            elif 'cafe' in nome_imagem: cor = (100, 50, 0)
            elif 'luzes' in nome_imagem: cor = (0, 255, 0)
            else: cor = (255, 255, 0)
            self.image.fill(cor)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

# --- Classes Filhas (Sem alterações necessárias) ---
class Jogador(Entidade):
    def __init__(self, nome_personagem="wilque"):
        if nome_personagem == "wilque": nome_arquivo = "wilque.png"
        else: nome_arquivo = "ellen.png"
        super().__init__(100, NIVEL_CHAO - 160, 100, 160, nome_arquivo) 
        self.velocidade_y = 0
        self.esta_pulando = False
        self.vidas = 3
        self.tem_escudo = False
        self.nome = nome_personagem

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
        if self.rect.right < 0: self.kill()

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
        if self.rect.right < 0: self.kill()