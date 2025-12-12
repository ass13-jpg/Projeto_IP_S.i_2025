import pygame
import os
from src.configuracoes import *

class Entidade(pygame.sprite.Sprite):
    """
    Classe Mãe. Todas as classes visuais (Jogador, Inimigo, Item) herdam daqui.
    Responsável por carregar a imagem correta e criar o retângulo de colisão (hitbox).
    """
    def __init__(self, x, y, largura, altura, nome_imagem):
        super().__init__()
        
        # Lógica de Caminhos Dinâmica
        # Garante que o jogo ache as imagens independente do computador
        dir_atual = os.path.dirname(os.path.abspath(__file__)) # src/base
        dir_src = os.path.dirname(dir_atual)                   # src/
        dir_raiz = os.path.dirname(dir_src)                    # PROJETO_IP.../
        
        # Decide se busca na pasta de personagens ou imagens gerais
        if nome_imagem.lower() in ['wilque.png', 'ellen.png']:
            pasta = 'personagens'
        else:
            pasta = 'imagens'
            
        caminho_completo = os.path.join(dir_raiz, 'assets', pasta, nome_imagem)
        
        try:
            # Tenta carregar e otimizar a imagem
            img_original = pygame.image.load(caminho_completo).convert_alpha()
            self.image = pygame.transform.scale(img_original, (largura, altura))
        except Exception:
            # Se a imagem falhar, cria um quadrado colorido
            self.image = pygame.Surface((largura, altura))
            if 'wilque' in nome_imagem: cor = AZUL
            elif 'ellen' in nome_imagem: cor = (255, 105, 180) # Rosa
            elif 'demodog' in nome_imagem or 'cadeira' in nome_imagem: cor = PRETO
            elif 'cafe' in nome_imagem: cor = MARROM
            elif 'luzes' in nome_imagem: cor = VERDE_LUZ
            else: cor = AMARELO
            self.image.fill(cor)

        # Configura posição e máscara de colisão
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Método abstrato a ser sobrescrito pelos filhos"""
        pass