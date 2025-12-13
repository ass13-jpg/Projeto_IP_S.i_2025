import pygame
from src.configuracoes import *

class TelaGameOver:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        
        # Cria uma superfície preta semi-transparente para escurecer o jogo ao fundo
        self.overlay = pygame.Surface((largura, altura))
        self.overlay.set_alpha(100) # Transparência (0-255)
        self.overlay.fill(PRETO)

        # Fontes (ajuste os nomes das fontes conforme seu projeto)
        self.fonte_titulo = pygame.font.SysFont("arial", 80, bold=True)
        self.fonte_texto = pygame.font.SysFont("arial", 30)

    def desenhar(self, tela, pontuacao_final=0):
        # Desenha o overlay escuro sobre o frame atual do jogo
        tela.blit(self.overlay, (0, 0))

        # Renderiza os textos
        texto_titulo = self.fonte_titulo.render("GAME OVER", True, VERMELHO_MUNDO)
        texto_score = self.fonte_texto.render(f"Pontuação Final: {int(pontuacao_final)}", True, AMARELO)
        texto_reset = self.fonte_texto.render("Pressione [R] para Tentar Novamente", True, AMARELO)
        texto_menu = self.fonte_texto.render("Pressione [ESC] para Menu Principal", True, AMARELO)

        #  Centraliza e desenha na tela
        rect_titulo = texto_titulo.get_rect(center=(self.largura//2, self.altura//2 - 80))
        rect_score = texto_score.get_rect(center=(self.largura//2, self.altura//2))
        rect_reset = texto_reset.get_rect(center=(self.largura//2, self.altura//2 + 80))
        rect_menu = texto_menu.get_rect(center=(self.largura//2, self.altura//2 + 130))

        tela.blit(texto_titulo, rect_titulo)
        tela.blit(texto_score, rect_score)
        tela.blit(texto_reset, rect_reset)
        tela.blit(texto_menu, rect_menu)