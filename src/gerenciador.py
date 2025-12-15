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
    # Definindo 44100Hz e buffer pequeno para baixa latência
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Mixer Pygame inicializado com sucesso.")
except pygame.error as e:
    print(f"Erro ao inicializar o Mixer: {e}") 

# Carrega o som do pulo de forma GLOBAL
try:
    SOM_PULO_OBJETO = pygame.mixer.Sound(
        os.path.join(ASSETS_DIR, 'sons', SOM_PULO)
    )
    # --- VOLUME DO PULO: 30% ---
    SOM_PULO_OBJETO.set_volume(0.30) 
    
except pygame.error as e:
    print(f"Erro ao carregar SOM_PULO: {e}")
    SOM_PULO_OBJETO = pygame.mixer.Sound(buffer=128) # Som mudo de segurança

class GerenciadorJogo:
    """
    Classe MÃE.
    Gerencia Score, Vidas, Regras de Café (5x) e Mudança de Mundo.
    """
    def __init__(self):
        # --- CARREGAMENTO DA FONTE BLOCKCRAFT ---
        caminho_fonte = os.path.join(DIR_RAIZ, 'assets', 'fontes', 'BlockCraft.ttf')
        
        tamanho_hud = 40 
        tamanho_popups = 30
        tamanho_game_over = 70

        if os.path.exists(caminho_fonte):
            self.fonte = pygame.font.Font(caminho_fonte, tamanho_hud)
            self.fonte_popup = pygame.font.Font(caminho_fonte, tamanho_popups) 
            self.fonte_go = pygame.font.Font(caminho_fonte, tamanho_game_over)
        else:
            print(f"AVISO: Fonte BlockCraft não encontrada em {caminho_fonte}. Usando Arial.")
            self.fonte = pygame.font.SysFont('Arial', 30, bold=True)
            self.fonte_popup = pygame.font.SysFont('Arial', 20, bold=True)
            self.fonte_go = pygame.font.SysFont('Arial', 60, bold=True)
        
        # Padrão em minúsculo
        self.personagem_selecionado = "wilque" 
        
        # Carrega os cenários novos
        self.carregar_fundos()
        
        # Carrega os caminhos das músicas
        self.iniciar_musicas()
        
        # Reseta o jogo (Isso vai dar o play na música agora)
        self.resetar_jogo()

    def resetar_jogo(self, personagem=None):
        """Reinicia todas as variáveis para uma nova partida"""
        if personagem:
            self.personagem_selecionado = personagem.lower()

        self.pontos_score = 0          
        self.ultimo_score_lanterna = 0  
        
        self.vidas = VIDAS_INICIAIS     
        self.game_over = False
        
        self.conta_cafe = 0    
        self.conta_luzes = 0   
        
        self.mundo_invertido = False 
        self.velocidade_atual = VELOCIDADE_NORMAL
        self.posicao_fundo = 0 
        self.momento_entrada_invertido = 0 
        self.cooldown_spawn = 0         
        
        self.textos_flutuantes = [] 

        self.jogador = Jogador(self.personagem_selecionado)
        self.grupo_jogador = pygame.sprite.GroupSingle(self.jogador)
        self.grupo_obstaculos = pygame.sprite.Group()
        self.grupo_itens = pygame.sprite.Group()

        # Garante que começa com a música do mundo normal tocando
        try:
            pygame.mixer.music.load(self.musica_real_path)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao iniciar música no reset: {e}")

    def carregar_fundos(self):
        dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # cenario_n = Normal (Início)
        # cenario_i = Invertido
        path_bg_normal = os.path.join(dir_raiz, 'assets', 'cenarios', 'cenario_n.png') 
        path_bg_invertido = os.path.join(dir_raiz, 'assets', 'cenarios', 'cenario_i.png')
        
        try:
            bg_normal_bruto = pygame.image.load(path_bg_normal).convert()
            bg_invertido_bruto = pygame.image.load(path_bg_invertido).convert()

            self.img_fundo_normal = pygame.transform.scale(bg_normal_bruto, (LARGURA_TELA, ALTURA_TELA))
            self.img_fundo_invertido = pygame.transform.scale(bg_invertido_bruto, (LARGURA_TELA, ALTURA_TELA))
            
            self.tem_fundo = True
            print("Cenários carregados e redimensionados com sucesso!")
        except Exception as e:
            print(f"ERRO AO CARREGAR CENÁRIOS: {e}")
            self.tem_fundo = False
    
    def iniciar_musicas(self):
        """Define os caminhos das músicas e sons."""
        
        # 1. Carrega CAMINHOS
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
            
        # --- VOLUME DA MÚSICA: 25% ---
        pygame.mixer.music.set_volume(0.25) 

    def alternar_mundo(self):
        """Troca a dificuldade, o visual e a música."""
        self.mundo_invertido = not self.mundo_invertido
        
        try:
            if self.mundo_invertido:
                # MUNDO INVERTIDO
                caminho_musica = self.musica_invertida_path 
                self.velocidade_atual = VELOCIDADE_RAPIDA
                self.momento_entrada_invertido = pygame.time.get_ticks()
                self.criar_popup("MUNDO INVERTIDO!", (255, 0, 0)) # Esse aviso grande mantive
            else:
                # MUNDO REAL
                caminho_musica = self.musica_real_path 
                self.velocidade_atual = VELOCIDADE_NORMAL
                self.criar_popup("MUNDO REAL", (0, 255, 0)) # Esse aviso grande mantive
            
            pygame.mixer.music.load(caminho_musica) 
            pygame.mixer.music.play(-1)
            
        except pygame.error as e:
             print(f"Erro ao tentar trocar a música no alternar_mundo: {e}")
            
        self.conta_luzes = 0
        
    def criar_popup(self, texto, cor):
        """Cria um texto que aparece em cima do jogador e sobe."""
        self.textos_flutuantes.append({
            'texto': texto,
            'x': self.jogador.rect.centerx,
            'y': self.jogador.rect.top,
            'tempo': 60, # O texto dura 60 frames (1 segundo)
            'cor': cor
        })

    def atualizar_popups(self):
        """Atualiza a posição e remove popups antigos."""
        for popup in self.textos_flutuantes[:]:
            popup['y'] -= 1.5 # Faz o texto subir
            popup['tempo'] -= 1
            if popup['tempo'] <= 0:
                self.textos_flutuantes.remove(popup)

    def atualizar(self):
        """Loop lógico (60 FPS)"""
        if self.game_over: return
        
        self.grupo_jogador.update()
        self.grupo_obstaculos.update()
        self.grupo_itens.update()
        
        # Atualiza os textos flutuantes
        self.atualizar_popups()

        # DIFICULDADE DINÂMICA
        if self.mundo_invertido:
            chance_inimigo = 4 
            tempo_espera = 40 
        else:
            chance_inimigo = 1 
            tempo_espera = 60 

        # Geração de Obstáculos
        if self.cooldown_spawn > 0: self.cooldown_spawn -= 1
        
        if self.cooldown_spawn == 0:
            if random.randint(0, 100) < chance_inimigo: 
                self.grupo_obstaculos.add(Obstaculo(self.velocidade_atual))
                self.cooldown_spawn = tempo_espera

        # Geração de Itens 
        if random.randint(0, 100) < 2: 
            tipo = random.choice(["waffle", "waffle", "cafe", "luzes"])
            self.grupo_itens.add(Item(self.velocidade_atual, tipo))

        # Bônus por Score
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
                self.jogador.vidas -= 1
                # REMOVIDO: self.criar_popup("-1 VIDA", (255, 0, 0)) 
                
                if self.jogador.vidas <= 0: 
                    pygame.mixer.music.stop()
                    self.som_game_over_objeto.play()
                    self.game_over = True
            else: 
                self.jogador.tem_escudo = False
                # REMOVIDO: self.criar_popup("ESCUDO QUEBRADO!", (255, 255, 255)) 
        
        # 2. Colisão com Itens
        itens_coletados = pygame.sprite.spritecollide(self.jogador, self.grupo_itens, True)
        for item in itens_coletados:
            if item.tipo == "waffle": 
                self.pontos_score += 1 
                # REMOVIDO: self.criar_popup("+10 PONTOS", (255, 255, 0)) 
            
            elif item.tipo == "cafe": 
                self.conta_cafe += 1
                # REMOVIDO: self.criar_popup("+1 CAFE", (139, 69, 19)) 
                
                if self.conta_cafe > 0 and self.conta_cafe % 5 == 0:
                    self.jogador.tem_escudo = True
                    # REMOVIDO: self.criar_popup("ESCUDO ATIVO!", (0, 0, 255)) 
            
            elif item.tipo == "luzes": 
                self.conta_luzes += 1 
                # REMOVIDO: self.criar_popup("+1 LUZ", (255, 255, 255)) 

    def desenhar_fundo(self, tela):
        if self.tem_fundo:
            fundo = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
            tela.blit(fundo, (self.posicao_fundo, 0))
            tela.blit(fundo, (self.posicao_fundo + LARGURA_TELA, 0))
        else:
            tela.fill(VERMELHO_MUNDO if self.mundo_invertido else VERDE_CIN)
            
    def desenhar_sprites(self, tela):
        self.grupo_jogador.draw(tela)
        self.grupo_obstaculos.draw(tela)
        self.grupo_itens.draw(tela)

        if self.jogador.tem_escudo:
            centro = self.jogador.rect.center
            pygame.draw.circle(tela, MARROM, centro, 90, 5)

    def desenhar_hud_e_game_over(self, tela):
        texto = f"SCORE: {self.pontos_score}  |  VIDAS: {self.jogador.vidas}  |  LUZES: {self.conta_luzes}/10"
        
        sombra = self.fonte.render(texto, True, PRETO)
        frente = self.fonte.render(texto, True, BRANCO)
        
        tela.blit(sombra, (23, 23))
        tela.blit(frente, (20, 20))
        
        for popup in self.textos_flutuantes:
            surf = self.fonte_popup.render(popup['texto'], True, popup['cor'])
            sombra_p = self.fonte_popup.render(popup['texto'], True, PRETO)
            rect = surf.get_rect(center=(popup['x'], int(popup['y'])))
            tela.blit(sombra_p, (rect.x + 2, rect.y + 2))
            tela.blit(surf, rect)

        if self.mundo_invertido:
            tempo = (TEMPO_MUNDO_INVERTIDO - (pygame.time.get_ticks() - self.momento_entrada_invertido)) // 1000
            txt_timer = self.fonte.render(f"RETORNO EM: {tempo}s", True, (255, 0, 0))
            tela.blit(txt_timer, (LARGURA_TELA//2 - txt_timer.get_width()//2, 100))

        if self.game_over:
            s = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            s.set_alpha(200); s.fill(PRETO); tela.blit(s, (0,0))
            
            t1 = self.fonte_go.render("GAME OVER", True, VERMELHO_MUNDO)
            t2 = self.fonte.render(f"Score Final: {self.pontos_score}", True, AMARELO)
            t3 = self.fonte.render("ESC para Menu | R para Reiniciar", True, BRANCO)
            
            tela.blit(t1, (LARGURA_TELA//2 - t1.get_width()//2, ALTURA_TELA//2 - 100))
            tela.blit(t2, (LARGURA_TELA//2 - t2.get_width()//2, ALTURA_TELA//2))
            tela.blit(t3, (LARGURA_TELA//2 - t3.get_width()//2, ALTURA_TELA//2 + 80))