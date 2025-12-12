import pygame
import os
from src.configuracoes import *

class TelaSelecao:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = pygame.font.SysFont("arial", 40, bold=True)
        self.fonte_nome = pygame.font.SysFont("arial", 30)
        
        # Hitboxes para clique
        self.rect_wilque = pygame.Rect(largura//4 - 75, altura//2 - 100, 150, 200)
        self.rect_ellen = pygame.Rect(3*largura//4 - 75, altura//2 - 100, 150, 200)

        self.preview_wilque = None
        self.preview_ellen = None
        self.tem_imagens = False

        # Caminhos dos Assets 
        dir_atual = os.path.dirname(os.path.abspath(__file__)) 
        dir_raiz = os.path.dirname(os.path.dirname(dir_atual))
        
        caminho_w = os.path.join(dir_raiz, 'assets', 'personagens', 'wilque.png')
        caminho_e = os.path.join(dir_raiz, 'assets', 'personagens', 'ellen.png')

        try:
            img_w = pygame.image.load(caminho_w).convert_alpha()
            self.preview_wilque = pygame.transform.scale(img_w, (150, 200))
            
            img_e = pygame.image.load(caminho_e).convert_alpha()
            self.preview_ellen = pygame.transform.scale(img_e, (150, 200))
            self.tem_imagens = True
        except:
            self.tem_imagens = False

    def update(self, eventos):
        """Retorna string 'wilque' ou 'ellen' se clicado"""
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.rect_wilque.collidepoint(pos): return "wilque"
                if self.rect_ellen.collidepoint(pos): return "ellen"
        return None 

    def desenhar(self, tela):
        tela.fill(PRETO) 
        
        titulo = self.fonte_titulo.render("ESCOLHA SEU PERSONAGEM", True, BRANCO)
        tela.blit(titulo, (self.largura//2 - titulo.get_width()//2, 50))

        # Desenha previews
        if self.tem_imagens:
            tela.blit(self.preview_wilque, self.rect_wilque)
            tela.blit(self.preview_ellen, self.rect_ellen)
        else:
            # Fallback (Retângulos coloridos)
            pygame.draw.rect(tela, AZUL, self.rect_wilque) 
            pygame.draw.rect(tela, (255, 105, 180), self.rect_ellen)

        # Bordas de seleção
        pygame.draw.rect(tela, BRANCO, self.rect_wilque, 3)
        pygame.draw.rect(tela, BRANCO, self.rect_ellen, 3)
        
        # Nomes
        tela.blit(self.fonte_nome.render("WILQUE", True, BRANCO), (self.rect_wilque.centerx - 50, self.rect_wilque.bottom + 10))
        tela.blit(self.fonte_nome.render("ELLEN", True, BRANCO), (self.rect_ellen.centerx - 40, self.rect_ellen.bottom + 10))