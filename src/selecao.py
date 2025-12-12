import pygame
import os

try:
    from src.configuracoes import *
except ModuleNotFoundError:
    from configuracoes import *

class TelaSelecao:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = pygame.font.SysFont("arial", 40, bold=True)
        self.fonte_nome = pygame.font.SysFont("arial", 30)
        
        self.rect_wilque = pygame.Rect(largura//4 - 75, altura//2 - 100, 150, 200)
        self.rect_ellen = pygame.Rect(3*largura//4 - 75, altura//2 - 100, 150, 200)

        self.preview_wilque = None
        self.preview_ellen = None
        self.tem_imagens = False

        # --- CAMINHOS PARA A PASTA PERSONAGENS ---
        dir_atual = os.path.dirname(os.path.abspath(__file__))
        dir_raiz = os.path.dirname(dir_atual)
        
        # Monta o caminho exato para a pasta que você indicou
        caminho_w = os.path.join(dir_raiz, 'assets', 'personagens', 'wilque.png')
        caminho_e = os.path.join(dir_raiz, 'assets', 'personagens', 'ellen.png')

        try:
            img_w = pygame.image.load(caminho_w).convert_alpha()
            self.preview_wilque = pygame.transform.scale(img_w, (150, 200))
            
            img_e = pygame.image.load(caminho_e).convert_alpha()
            self.preview_ellen = pygame.transform.scale(img_e, (150, 200))
            
            self.tem_imagens = True
        except Exception:
            self.tem_imagens = False

    def update(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_wilque.collidepoint(pos_mouse): return "wilque"
                if self.rect_ellen.collidepoint(pos_mouse): return "ellen"
        return None 

    def desenhar(self, tela):
        tela.fill((0, 0, 0)) 
        
        titulo = self.fonte_titulo.render("ESCOLHA SEU PERSONAGEM", True, (255, 255, 255))
        tela.blit(titulo, (self.largura//2 - titulo.get_width()//2, 50))

        if self.tem_imagens:
            tela.blit(self.preview_wilque, self.rect_wilque)
            tela.blit(self.preview_ellen, self.rect_ellen)
        else:
            pygame.draw.rect(tela, (0, 0, 255), self.rect_wilque) 
            pygame.draw.rect(tela, (255, 105, 180), self.rect_ellen)

        pygame.draw.rect(tela, (255, 255, 255), self.rect_wilque, 3)
        pygame.draw.rect(tela, (255, 255, 255), self.rect_ellen, 3)
        
        nome_w = self.fonte_nome.render("WILQUE", True, (255, 255, 255))
        tela.blit(nome_w, (self.rect_wilque.centerx - nome_w.get_width()//2, self.rect_wilque.bottom + 10))

        nome_e = self.fonte_nome.render("ELLEN", True, (255, 255, 255))
        tela.blit(nome_e, (self.rect_ellen.centerx - nome_e.get_width()//2, self.rect_ellen.bottom + 10))

        dica = self.fonte_nome.render("Clique para selecionar", True, (255, 255, 0))
        tela.blit(dica, (self.largura//2 - dica.get_width()//2, self.altura - 80))