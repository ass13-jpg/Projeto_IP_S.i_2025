import pygame
import os
from src.configuracoes import *
from src.assets_paths import * # ==============================================================================
# CLASSE ENTIDADE (MÃE DE TODOS OS OBJETOS)
# ==============================================================================
class Entidade(pygame.sprite.Sprite):
    """
    Classe Mãe. Todas as classes visuais (Jogador, Inimigo, Item) herdam daqui.
    Responsável por carregar a imagem correta e criar o retângulo de colisão (hitbox).
    """
    def __init__(self, x, y, largura, altura, nome_imagem):
        super().__init__()
        
        # --- 1. CONFIGURAÇÃO DE CAMINHOS ---
        # Calcula onde está a pasta raiz do projeto de forma automática
        dir_atual = os.path.dirname(os.path.abspath(__file__))
        dir_src = os.path.dirname(dir_atual)
        dir_raiz = os.path.dirname(dir_src)
        
        # --- 2. CLASSIFICAÇÃO DOS OBJETOS ---
        # Define quais imagens pertencem a qual pasta
        
        coletaveis = [IMAGEM_WAFFLE, IMAGEM_CAFE, IMAGEM_PISCA_PISCA]
        
        # Lista de obstáculos (Inimigos)
        obstaculos = [IMAGEM_DEMODOG, IMAGEM_CADEIRA, IMAGEM_DEMOGORGON] 
        
        # --- 3. SELEÇÃO DA PASTA CORRETA ---
        if nome_imagem in coletaveis:
            pasta = 'coletaveis' 
        elif nome_imagem in obstaculos: 
            pasta = 'obstaculos' # O Demogorgon cairá aqui agora!
        elif nome_imagem.lower() in ['wilque.png', 'ellen.png']:
            pasta = 'personagens' 
        else:
            pasta = 'imagens' # Pasta padrão para o que não foi classificado
            
        # Monta o caminho final: ex: C:/Jogo/assets/obstaculos/demogorgon.png
        caminho_completo = os.path.join(dir_raiz, 'assets', pasta, nome_imagem)
        
        # --- 4. CARREGAMENTO DA IMAGEM ---
        try:
            # Tenta carregar a imagem
            img_original = pygame.image.load(caminho_completo).convert_alpha()
            self.image = pygame.transform.scale(img_original, (largura, altura))
            
        except Exception as e:
            # --- DEBUG: Só aparece se der erro ---
            print(f"-"*30)
            print(f"ERRO: Não encontrei '{nome_imagem}'")
            print(f"Procurei em: {caminho_completo}")
            print(f"-"*30)
            
            # Cria um quadrado colorido de emergência (Fallback)
            self.image = pygame.Surface((largura, altura))
            
            # Define cores baseadas no nome para facilitar identificação visual
            if 'wilque' in nome_imagem: cor = AZUL
            elif 'ellen' in nome_imagem: cor = (255, 105, 180) 
            elif 'demodog' in nome_imagem or 'demogorgon' in nome_imagem: cor = PRETO # Preto para monstros
            elif 'cadeira' in nome_imagem: cor = (100, 100, 100)
            elif 'cafe' in nome_imagem: cor = MARROM
            elif 'luzes' in nome_imagem: cor = VERDE_LUZ
            else: cor = AMARELO # Amarelo = Erro genérico
            
            self.image.fill(cor)

        # --- 5. FÍSICA E COLISÃO ---
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Cria máscara para colisão pixel-perfect (opcional)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Método abstrato a ser sobrescrito pelos filhos"""
        pass