import pygame
import random
import os
from src.configuracoes import *
from src.entidades import Jogador, Obstaculo, Item

class GerenciadorJogo:
    def __init__(self):
        # --- Pontuações ---
        self.pontos_waffles = 0
        self.conta_cafe = 0
        self.conta_luzes = 0
        
        # --- Estados do Jogo ---
        self.mundo_invertido = False 
        self.velocidade_atual = VELOCIDADE_NORMAL
        
        # --- Carregando Fundos (Backgrounds) ---
        self.carregar_fundos()
        self.posicao_fundo = 0 
        
        # --- Grupos de Sprites (Pygame) ---
        self.jogador = Jogador()
        self.grupo_jogador = pygame.sprite.GroupSingle(self.jogador)
        self.grupo_obstaculos = pygame.sprite.Group()
        self.grupo_itens = pygame.sprite.Group()
        
        self.fonte = pygame.font.SysFont('Arial', 30) # Fonte maior para HD

    def carregar_fundos(self):
        try:
            caminho_normal = os.path.join('assets', 'imagens', 'bg_normal.png')
            caminho_invertido = os.path.join('assets', 'imagens', 'bg_invertido.png')
            
            # Carrega e ajusta para o tamanho da tela (1920x1080)
            self.img_fundo_normal = pygame.transform.scale(
                pygame.image.load(caminho_normal).convert(), (LARGURA_TELA, ALTURA_TELA)
            )
            self.img_fundo_invertido = pygame.transform.scale(
                pygame.image.load(caminho_invertido).convert(), (LARGURA_TELA, ALTURA_TELA)
            )
            self.tem_fundo = True
        except:
            print("Aviso: Imagens de fundo não encontradas. Usando cores sólidas.")
            self.tem_fundo = False

    def alternar_mundo(self):
        """Muda do CIn Normal para o Invertido e vice-versa"""
        self.mundo_invertido = not self.mundo_invertido
        
        if self.mundo_invertido:
            self.velocidade_atual = VELOCIDADE_RAPIDA
        else:
            self.velocidade_atual = VELOCIDADE_NORMAL
        
        # Reseta as luzes para coletar novamente
        self.conta_luzes = 0 

    def atualizar(self):
        # Atualiza todos os objetos
        self.grupo_jogador.update()
        self.grupo_obstaculos.update()
        self.grupo_itens.update()

        # --- Gerar Inimigos e Itens (Aleatório) ---
        if random.randint(0, 100) < 2: # Chance de criar obstáculo
            self.grupo_obstaculos.add(Obstaculo(self.velocidade_atual))
        
        if random.randint(0, 100) < 3: # Chance de criar item
            tipo = random.choice(["waffle", "waffle", "cafe", "luzes"])
            self.grupo_itens.add(Item(self.velocidade_atual, tipo))

        # --- Lógica Stranger Things ---
        # Se pegar 10 luzes no normal -> Vai pro Invertido
        if self.conta_luzes >= 10 and not self.mundo_invertido:
            self.alternar_mundo()
        
        # Se pegar 5 luzes no invertido -> Volta (Facilita pro jogador)
        if self.mundo_invertido and self.conta_luzes >= 5:
            self.alternar_mundo()

        self.verificar_colisoes()

        # --- Movimento do Fundo (Parallax) ---
        velocidade_fundo = self.velocidade_atual * 0.5 
        self.posicao_fundo -= velocidade_fundo
        if self.posicao_fundo <= -LARGURA_TELA:
            self.posicao_fundo = 0

    def verificar_colisoes(self):
        # Colisão com Inimigos
        if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True):
            if not self.jogador.tem_escudo:
                self.jogador.vidas -= 1
                print(f"Bateu! Vidas restantes: {self.jogador.vidas}")
            else:
                self.jogador.tem_escudo = False # Perde o escudo, mas não a vida
                print("Escudo protegeu!")

        # Colisão com Itens
        itens_pegos = pygame.sprite.spritecollide(self.jogador, self.grupo_itens, True)
        for item in itens_pegos:
            if item.tipo == "waffle":
                self.pontos_waffles += (20 if self.mundo_invertido else 10)
            elif item.tipo == "cafe":
                self.conta_cafe += 1
                self.jogador.tem_escudo = True
            elif item.tipo == "luzes":
                self.conta_luzes += 1

    def desenhar(self, tela):
        # 1. Desenha o Fundo
        if self.tem_fundo:
            fundo_atual = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
            tela.blit(fundo_atual, (self.posicao_fundo, 0))
            tela.blit(fundo_atual, (self.posicao_fundo + LARGURA_TELA, 0))
        else:
            cor = VERMELHO_MUNDO if self.mundo_invertido else VERDE_CIN
            tela.fill(cor)

        # 2. Desenha os Sprites
        self.grupo_jogador.draw(tela)
        self.grupo_obstaculos.draw(tela)
        self.grupo_itens.draw(tela)

        # 3. Desenha o Placar (HUD)
        texto = f"Waffles: {self.pontos_waffles} | Café: {self.conta_cafe} | Luzes: {self.conta_luzes} | Vidas: {self.jogador.vidas}"
        superficie_texto = self.fonte.render(texto, True, BRANCO)
        tela.blit(superficie_texto, (20, 20))