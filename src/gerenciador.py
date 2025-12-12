import pygame
import random
import os
from src.configuracoes import *

# IMPORTAÇÕES DE MODULOS 
from src.atores.jogador import Jogador
from src.atores.obstaculo import Obstaculo
from src.itens.coletavel import Item

class GerenciadorJogo:
    def __init__(self):
        self.fonte = pygame.font.SysFont('Arial', 30, bold=True)
        self.fonte_go = pygame.font.SysFont('Arial', 60, bold=True)
        self.personagem_selecionado = "wilque"
        self.carregar_fundos()
        # Inicia o jogo zerado
        self.resetar_jogo()

    def resetar_jogo(self, personagem=None):
        """Reinicia todas as variáveis para uma nova partida"""
        if personagem:
            self.personagem_selecionado = personagem

        self.pontos_score = 0       # Score Principal 
        self.pontos_waffles = 0     # Contador interno
        self.vidas = VIDAS_INICIAIS # 10 Vidas
        self.game_over = False
        
        self.conta_cafe = 0
        self.conta_luzes = 0
        self.mundo_invertido = False 
        self.velocidade_atual = VELOCIDADE_NORMAL
        self.posicao_fundo = 0 
        self.momento_entrada_invertido = 0
        self.cooldown_spawn = 0
        
        # Recria os grupos de sprites
        self.jogador = Jogador(self.personagem_selecionado)
        self.grupo_jogador = pygame.sprite.GroupSingle(self.jogador)
        self.grupo_obstaculos = pygame.sprite.Group()
        self.grupo_itens = pygame.sprite.Group()

    def carregar_fundos(self):
        dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
        if self.mundo_invertido:
            self.velocidade_atual = VELOCIDADE_RAPIDA
            self.momento_entrada_invertido = pygame.time.get_ticks()
        else:
            self.velocidade_atual = VELOCIDADE_NORMAL
        self.conta_luzes = 0 

    def atualizar(self):
        if self.game_over: return
        
        self.grupo_jogador.update()
        self.grupo_obstaculos.update()
        self.grupo_itens.update()

        # Espaçamento entre Inimigos
        if self.cooldown_spawn > 0: self.cooldown_spawn -= 1
        
        if self.cooldown_spawn == 0:
            if random.randint(0, 100) < 1: 
                self.grupo_obstaculos.add(Obstaculo(self.velocidade_atual))
                self.cooldown_spawn = 60 # Bloqueia novos monstros por 1s

        if random.randint(0, 100) < 2: 
            tipo = random.choice(["waffle", "waffle", "cafe", "luzes"])
            self.grupo_itens.add(Item(self.velocidade_atual, tipo))

        # Ida para o Invertido (10 Luzes)
        if self.conta_luzes >= 10 and not self.mundo_invertido: self.alternar_mundo()
        
        # Volta do Invertido (30 Segundos)
        if self.mundo_invertido:
            agora = pygame.time.get_ticks()
            if agora - self.momento_entrada_invertido > TEMPO_MUNDO_INVERTIDO:
                self.alternar_mundo()

        self.verificar_colisoes()

        # Scroll do Fundo
        self.posicao_fundo -= self.velocidade_atual * 0.5 
        if self.posicao_fundo <= -LARGURA_TELA: self.posicao_fundo = 0

    def verificar_colisoes(self):
        # Colisão com Inimigos
        if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True):
            if not self.jogador.tem_escudo:
                self.jogador.vidas -= 1
                if self.jogador.vidas <= 0: self.game_over = True
            else: self.jogador.tem_escudo = False 
        
        # Colisão com Itens
        itens = pygame.sprite.spritecollide(self.jogador, self.grupo_itens, True)
        for item in itens:
            if item.tipo == "waffle": 
                # Score aumenta ao pegar waffles
                self.pontos_score += (20 if self.mundo_invertido else 10)
            elif item.tipo == "cafe": self.jogador.tem_escudo = True
            elif item.tipo == "luzes": self.conta_luzes += 1

    def desenhar(self, tela):
        # 1. Fundo
        if self.tem_fundo:
            fundo = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
            tela.blit(fundo, (self.posicao_fundo, 0))
            tela.blit(fundo, (self.posicao_fundo + LARGURA_TELA, 0))
        else:
            tela.fill(VERMELHO_MUNDO if self.mundo_invertido else VERDE_CIN)

        # 2. Objetos
        self.grupo_jogador.draw(tela)
        self.grupo_obstaculos.draw(tela)
        self.grupo_itens.draw(tela)

        # 3. HUD (Texto Superior Esquerdo)
        texto = f"SCORE: {self.pontos_score} | VIDAS: {self.jogador.vidas}"
        sombra = self.fonte.render(texto, True, PRETO)
        frente = self.fonte.render(texto, True, BRANCO)
        
        tela.blit(sombra, (23, 23)) # Sombra
        tela.blit(frente, (20, 20)) # Texto
        
        # 4. Timer Central (Só no invertido)
        if self.mundo_invertido:
            tempo = (TEMPO_MUNDO_INVERTIDO - (pygame.time.get_ticks() - self.momento_entrada_invertido)) // 1000
            txt_timer = self.fonte.render(f"RETORNO EM: {tempo}s", True, BRANCO)
            tela.blit(txt_timer, (LARGURA_TELA//2-100, 100))

        # 5. Tela de Game Over
        if self.game_over:
            s = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            s.set_alpha(200); s.fill(PRETO); tela.blit(s, (0,0))
            
            t1 = self.fonte_go.render("GAME OVER", True, VERMELHO_MUNDO)
            t2 = self.fonte.render(f"Score Final: {self.pontos_score}", True, AMARELO)
            t3 = self.fonte.render("ESC para Menu | R para Reiniciar", True, BRANCO)
            
            tela.blit(t1, (LARGURA_TELA//2 - t1.get_width()//2, ALTURA_TELA//2 - 100))
            tela.blit(t2, (LARGURA_TELA//2 - t2.get_width()//2, ALTURA_TELA//2))
            tela.blit(t3, (LARGURA_TELA//2 - t3.get_width()//2, ALTURA_TELA//2 + 80))