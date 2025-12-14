import pygame
import random
import os
from src.configuracoes import *
from src.assets_paths import *

# IMPORTAÇÕES DE CLASSES (MODULOS)
from src.atores.jogador import Jogador
from src.atores.obstaculo import Obstaculo
from src.itens.coletavel import Item

DIR_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(DIR_RAIZ, 'assets')

import pygame.mixer


if not pygame.mixer.get_init():
    pygame.mixer.init()

try:
    # Definindo 44100Hz (qualidade CD) e buffer pequeno para baixa latência
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Mixer Pygame inicializado com sucesso.")
except pygame.error as e:
    print(f"Erro ao inicializar o Mixer: {e}") 

# 2. Carrega o som do pulo de forma GLOBAL (acessível pelo Jogador.py)
# Isso deve funcionar agora que o mixer está inicializado corretamente
try:
    SOM_PULO_OBJETO = pygame.mixer.Sound(
        os.path.join(ASSETS_DIR, 'sons', SOM_PULO)
    )
except pygame.error as e:
    print(f"Erro ao carregar SOM_PULO. Verifique o formato do arquivo (tente .wav): {e}")
    # Cria um som mudo para evitar falha se o arquivo estiver corrompido
    SOM_PULO_OBJETO = pygame.mixer.Sound(buffer=128)

SOM_PULO_OBJETO = pygame.mixer.Sound(
    os.path.join(ASSETS_DIR, 'sons', SOM_PULO))

class GerenciadorJogo:
    """
    Classe MÃE.
    Gerencia Score, Vidas, Regras de Café (5x) e Mudança de Mundo.
    """
    def __init__(self):
        self.fonte = pygame.font.SysFont('Arial', 30, bold=True)
        self.fonte_go = pygame.font.SysFont('Arial', 60, bold=True)
        
        self.personagem_selecionado = "wilque" 
        self.carregar_fundos()
        self.iniciar_musicas()
        self.resetar_jogo()

    def resetar_jogo(self, personagem=None):
        """Reinicia todas as variáveis para uma nova partida"""
        if personagem:
            self.personagem_selecionado = personagem

        self.pontos_score = 0           
        self.ultimo_score_lanterna = 0  
        
        self.vidas = VIDAS_INICIAIS     
        self.game_over = False
        
        self.conta_cafe = 0    # Conta total de cafés pegos
        self.conta_luzes = 0   
        
        self.mundo_invertido = False 
        self.velocidade_atual = VELOCIDADE_NORMAL
        self.posicao_fundo = 0 
        self.momento_entrada_invertido = 0 
        self.cooldown_spawn = 0         
        
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
    
    def iniciar_musicas(self):
        """Carrega caminhos, carrega o som de Game Over e toca a música de fundo inicial."""
        
        # 1. Carrega CAMINHOS (Lógica Padrão)
        self.musica_real_path = os.path.join(ASSETS_DIR, 'sons', SOM_MUNDO_REAL)
        self.musica_invertida_path = os.path.join(ASSETS_DIR, 'sons', SOM_MUNDO_INVERTIDO)
        
        # 2. Carrega Efeito de Game Over
        try:
            self.som_game_over_objeto = pygame.mixer.Sound(
                os.path.join(ASSETS_DIR, 'sons', SOM_GAME_OVER)
            )
        except pygame.error as e:
            print(f"Erro ao carregar SOM_GAME_OVER: {e}")
            self.som_game_over_objeto = pygame.mixer.Sound(buffer=128) 
            
        # 3. Configura Volume
        pygame.mixer.music.set_volume(1.0) 
        print(f"Volume da Música: {pygame.mixer.music.get_volume()}")

        # 4. Carrega e Toca a Música Inicial (Mundo Real)
        try:
            pygame.mixer.music.load(self.musica_real_path)
            pygame.mixer.music.play(-1) 
        except pygame.error as e:
            print(f"ERRO ao carregar a MÚSICA INICIAL: {e}") 
            print(f"Caminho tentado: {self.musica_real_path}")
    def alternar_mundo(self):
        """Troca a dificuldade, o visual e a música."""
        
        # 1. Inverte o estado
        self.mundo_invertido = not self.mundo_invertido
        
        try:
            # 2. Define o caminho da música baseado no NOVO estado
            if self.mundo_invertido:
                # MUNDO INVERTIDO
                caminho_musica = self.musica_invertida_path 
                
                self.velocidade_atual = VELOCIDADE_RAPIDA
                self.momento_entrada_invertido = pygame.time.get_ticks()
            else:
                # MUNDO REAL
                caminho_musica = self.musica_real_path 
                
                self.velocidade_atual = VELOCIDADE_NORMAL
            
            # 3. Carrega e Toca a Música
            pygame.mixer.music.load(caminho_musica) 
            pygame.mixer.music.play(-1)
            
        except pygame.error as e:
             print(f"Erro ao tentar trocar a música no alternar_mundo: {e}")
            
        self.conta_luzes = 0
        
    def atualizar(self):
        """Loop lógico (60 FPS)"""
        if self.game_over: return
        
        self.grupo_jogador.update()
        self.grupo_obstaculos.update()
        self.grupo_itens.update()

        # DIFICULDADE DINÂMICA
        # Mais inimigos no mundo invertido
        if self.mundo_invertido:
            chance_inimigo = 4   # 4%
            tempo_espera = 40    # Rápido
        else:
            chance_inimigo = 1   # 1%
            tempo_espera = 60    # Normal

        # Geração de Obstáculos
        if self.cooldown_spawn > 0: self.cooldown_spawn -= 1
        
        if self.cooldown_spawn == 0:
            if random.randint(0, 100) < chance_inimigo: 
                self.grupo_obstaculos.add(Obstaculo(self.velocidade_atual))
                self.cooldown_spawn = tempo_espera

        # Geração de Itens 
        # 1. Aleatória
        if random.randint(0, 100) < 2: 
            tipo = random.choice(["waffle", "waffle", "cafe", "luzes"])
            self.grupo_itens.add(Item(self.velocidade_atual, tipo))

        # 2. Bônus por Score (Lanterna extra a cada 30 pontos)
        if self.pontos_score >= self.ultimo_score_lanterna + 30:
            self.grupo_itens.add(Item(self.velocidade_atual, "luzes"))
            self.ultimo_score_lanterna = self.pontos_score 

        # Regras de Mudança de Mundo
        if self.conta_luzes >= 10 and not self.mundo_invertido: 
            self.alternar_mundo()
        
        if self.mundo_invertido:
            agora = pygame.time.get_ticks()
            if agora - self.momento_entrada_invertido > TEMPO_MUNDO_INVERTIDO:
                self.alternar_mundo()

        self.verificar_colisoes()

        self.posicao_fundo -= self.velocidade_atual * 0.5 
        if self.posicao_fundo <= -LARGURA_TELA: self.posicao_fundo = 0

    def verificar_colisoes(self):
        """Gerencia colisão com Inimigos e Itens"""
        
        # 1. Colisão com Obstáculos
        if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True):
            if not self.jogador.tem_escudo:
                # Sem escudo: Perde vida
                self.jogador.vidas -= 1
                if self.jogador.vidas <= 0: 
                    
                    pygame.mixer.music.stop()
                    self.som_game_over_objeto.play()

                    self.game_over = True
            else: 
                # Com escudo: Perde o escudo, mas salva a vida
                self.jogador.tem_escudo = False
                print("Escudo QUEBRADO! (Protegeu 1 vida)") 
        
        # 2. Colisão com Itens
        itens_coletados = pygame.sprite.spritecollide(self.jogador, self.grupo_itens, True)
        for item in itens_coletados:
            if item.tipo == "waffle": 
                self.pontos_score += 1 
            
            elif item.tipo == "cafe": 
                self.conta_cafe += 1
                # NOVA LÓGICA DO CAFÉ 
                # Só ativa o escudo se o total de cafés for múltiplo de 5 (5, 10, 15...)
                if self.conta_cafe > 0 and self.conta_cafe % 5 == 0:
                    self.jogador.tem_escudo = True
                    print(f"ESCUDO ATIVADO! (Pegou {self.conta_cafe} cafés)")
            
            elif item.tipo == "luzes": 
                self.conta_luzes += 1 

    def desenhar_fundo(self, tela):
        """Desenha apenas o fundo/cenário (Normal ou Invertido). Deve ser o primeiro a ser chamado."""
        # 1. Fundo
        if self.tem_fundo:
            fundo = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
            # Desenha o fundo normal (ou invertido)
            tela.blit(fundo, (self.posicao_fundo, 0))
            tela.blit(fundo, (self.posicao_fundo + LARGURA_TELA, 0))
        else:
            # Fallback para cor sólida (usando as constantes de configuração)
            tela.fill(VERMELHO_MUNDO if self.mundo_invertido else VERDE_CIN)
            
    def desenhar_sprites(self, tela):
        """Desenha o jogador, obstáculos e itens."""
        # 2. Sprites
        self.grupo_jogador.draw(tela)
        self.grupo_obstaculos.draw(tela)
        self.grupo_itens.draw(tela)

        # Só desenha o círculo se o escudo estiver ATIVO
        if self.jogador.tem_escudo:
            centro = self.jogador.rect.center
            pygame.draw.circle(tela, MARROM, centro, 90, 5)

    def desenhar_hud_e_game_over(self, tela):
        """Desenha o HUD, Timer e a tela de Game Over (deve ser o último a ser chamado)."""
        # 3. HUD (Texto)
        texto = f"SCORE: {self.pontos_score} | VIDAS: {self.jogador.vidas} | LUZES: {self.conta_luzes}/10"
        
        sombra = self.fonte.render(texto, True, PRETO)
        frente = self.fonte.render(texto, True, BRANCO)
        
        tela.blit(sombra, (23, 23))
        tela.blit(frente, (20, 20))
        
        # 4. Timer Central (Só no mundo invertido)
        if self.mundo_invertido:
            tempo = (TEMPO_MUNDO_INVERTIDO - (pygame.time.get_ticks() - self.momento_entrada_invertido)) // 1000
            txt_timer = self.fonte.render(f"RETORNO EM: {tempo}s", True, BRANCO)
            tela.blit(txt_timer, (LARGURA_TELA//2-100, 100))

        # 5. Game Over
        if self.game_over:
            s = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            s.set_alpha(200); s.fill(PRETO); tela.blit(s, (0,0))
            
            t1 = self.fonte_go.render("GAME OVER", True, VERMELHO_MUNDO)
            t2 = self.fonte.render(f"Score Final: {self.pontos_score}", True, AMARELO)
            t3 = self.fonte.render("ESC para Menu | R para Reiniciar", True, BRANCO)
            
            tela.blit(t1, (LARGURA_TELA//2 - t1.get_width()//2, ALTURA_TELA//2 - 100))
            tela.blit(t2, (LARGURA_TELA//2 - t2.get_width()//2, ALTURA_TELA//2))
            tela.blit(t3, (LARGURA_TELA//2 - t3.get_width()//2, ALTURA_TELA//2 + 80))