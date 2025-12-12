import pygame
import random
import os

try:
    from src.configuracoes import *
    from src.entidades import Jogador, Obstaculo, Item
except ModuleNotFoundError:
    from configuracoes import *
    from entidades import Jogador, Obstaculo, Item

class GerenciadorJogo:
    def __init__(self):
        self.fonte = pygame.font.SysFont('Arial', 30)
        self.personagem_selecionado = "wilque"
        self.carregar_fundos()
        # Inicia sem argumentos na primeira vez
        self.resetar_jogo()

    # --- CORREÇÃO IMPORTANTE AQUI ---
    def resetar_jogo(self, personagem=None):
        """Aceita o nome do personagem para não dar TypeError"""
        
        if personagem:
            self.personagem_selecionado = personagem

        # Reseta variáveis
        self.pontuacao = 0
        self.vidas = 3
        self.game_over = False
        self.pontos_waffles = 0
        self.conta_cafe = 0
        self.conta_luzes = 0
        self.mundo_invertido = False 
        self.velocidade_atual = VELOCIDADE_NORMAL
        self.posicao_fundo = 0 
        
        # Cria o jogador com o nome certo
        self.jogador = Jogador(self.personagem_selecionado)
        self.grupo_jogador = pygame.sprite.GroupSingle(self.jogador)
        
        self.grupo_obstaculos = pygame.sprite.Group()
        self.grupo_itens = pygame.sprite.Group()

    def carregar_fundos(self):
        # Garante que acha os fundos na pasta imagens
        dir_atual = os.path.dirname(os.path.abspath(__file__))
        dir_raiz = os.path.dirname(dir_atual)
        try:
            path_bg1 = os.path.join(dir_raiz, 'assets', 'imagens', 'bg_normal.png')
            path_bg2 = os.path.join(dir_raiz, 'assets', 'imagens', 'bg_invertido.png')
            
            self.img_fundo_normal = pygame.transform.scale(pygame.image.load(path_bg1).convert(), (LARGURA_TELA, ALTURA_TELA))
            self.img_fundo_invertido = pygame.transform.scale(pygame.image.load(path_bg2).convert(), (LARGURA_TELA, ALTURA_TELA))
            self.tem_fundo = True
        except:
            self.tem_fundo = False

    def alternar_mundo(self):
        self.mundo_invertido = not self.mundo_invertido
        self.velocidade_atual = VELOCIDADE_RAPIDA if self.mundo_invertido else VELOCIDADE_NORMAL
        self.conta_luzes = 0 

    def atualizar(self):
        if self.game_over: return
        self.grupo_jogador.update()
        self.grupo_obstaculos.update()
        self.grupo_itens.update()

        if random.randint(0, 100) < 2: self.grupo_obstaculos.add(Obstaculo(self.velocidade_atual))
        if random.randint(0, 100) < 3: 
            tipo = random.choice(["waffle", "waffle", "cafe", "luzes"])
            self.grupo_itens.add(Item(self.velocidade_atual, tipo))

        if self.conta_luzes >= 10 and not self.mundo_invertido: self.alternar_mundo()
        if self.mundo_invertido and self.conta_luzes >= 5: self.alternar_mundo()
        self.verificar_colisoes()

        velocidade_fundo = self.velocidade_atual * 0.5 
        self.posicao_fundo -= velocidade_fundo
        if self.posicao_fundo <= -LARGURA_TELA: self.posicao_fundo = 0

    def verificar_colisoes(self):
        if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True):
            if not self.jogador.tem_escudo:
                self.jogador.vidas -= 1
                if self.jogador.vidas <= 0: self.game_over = True
            else: self.jogador.tem_escudo = False 
        
        itens = pygame.sprite.spritecollide(self.jogador, self.grupo_itens, True)
        for item in itens:
            if item.tipo == "waffle": self.pontos_waffles += (20 if self.mundo_invertido else 10)
            elif item.tipo == "cafe": self.jogador.tem_escudo = True
            elif item.tipo == "luzes": self.conta_luzes += 1

    def desenhar(self, tela):
        if self.tem_fundo:
            fundo = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
            tela.blit(fundo, (self.posicao_fundo, 0))
            tela.blit(fundo, (self.posicao_fundo + LARGURA_TELA, 0))
        else:
            tela.fill(VERMELHO_MUNDO if self.mundo_invertido else VERDE_CIN)

        self.grupo_jogador.draw(tela)
        self.grupo_obstaculos.draw(tela)
        self.grupo_itens.draw(tela)

        texto = f"Waffles: {self.pontos_waffles} | Vidas: {self.jogador.vidas}"
        tela.blit(self.fonte.render(texto, True, BRANCO), (20, 20))

        if self.game_over:
            msg = self.fonte.render("GAME OVER - ESC para Menu", True, (255, 0, 0))
            tela.blit(msg, (LARGURA_TELA//2 - 200, ALTURA_TELA//2))