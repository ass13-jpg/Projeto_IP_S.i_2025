import pygame
import os
from src.configuracoes import *
from src.assets_paths import * # IMPORTAÇÃO DAS CONSTANTES DE IMAGEM

class Entidade(pygame.sprite.Sprite):
    """
    Classe Mãe. Todas as classes visuais (Jogador, Inimigo, Item) herdam daqui.
    Responsável por carregar a imagem correta e criar o retângulo de colisão (hitbox).
    """
    def __init__(self, x, y, largura, altura, nome_imagem):
        super().__init__()
        
        # Lógica de Caminhos Dinâmica
        dir_atual = os.path.dirname(os.path.abspath(__file__))
        dir_src = os.path.dirname(dir_atual)
        dir_raiz = os.path.dirname(dir_src)
        
        # ==========================================================
        # LÓGICA DE PASTAS INTELIGENTE (CORREÇÃO FINAL)
        # ==========================================================
        
        coletaveis = [IMAGEM_WAFFLE, IMAGEM_CAFE, IMAGEM_PISCA_PISCA]
        # NOVO: Lista de Obstáculos
        obstaculos = [IMAGEM_DEMODOG, IMAGEM_CADEIRA] 
        
        if nome_imagem in coletaveis:
            pasta = 'coletaveis' 
        elif nome_imagem in obstaculos: # <--- NOVO: Verifica se o nome é um obstáculo
            pasta = 'obstaculos' # <--- Envia para a pasta 'obstaculos'
        elif nome_imagem.lower() in ['wilque.png', 'ellen.png']:
            pasta = 'personagens' 
        else:
            pasta = 'imagens' # Para outros sprites gerais
            
        caminho_completo = os.path.join(dir_raiz, 'assets', pasta, nome_imagem)
        # = MANUTENÇÃO: Deixe o bloco try/except com os prints de diagnóstico! =
        # ==========================================================
        
        try:
            # Tenta carregar e otimizar a imagem
            img_original = pygame.image.load(caminho_completo).convert_alpha()
            self.image = pygame.transform.scale(img_original, (largura, altura))
        except Exception as e:
            
            
            # Se a imagem falhar (fallback), cria um quadrado colorido
            self.image = pygame.Surface((largura, altura))
            if 'wilque' in nome_imagem: cor = AZUL
            elif 'ellen' in nome_imagem: cor = (255, 105, 180) 
            elif 'demodog' in nome_imagem or 'cadeira' in nome_imagem: cor = PRETO
            elif 'cafe' in nome_imagem: cor = MARROM
            elif 'luzes' in nome_imagem or 'pisca' in nome_imagem: cor = VERDE_LUZ # Adicionado pisca
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