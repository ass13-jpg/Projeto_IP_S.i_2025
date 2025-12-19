import pygame
import random
import os
from src.configuracoes import *
from src.assets_paths import *

# ==============================================================================
# IMPORTAÇÕES DOS ATORES (PERSONAGENS E OBJETOS)
# ==============================================================================
from src.atores.jogador import Jogador
from src.atores.obstaculo import Obstaculo
from src.itens.coletavel import Item

# Define o diretório raiz para que o Python encontre os arquivos em qualquer PC
DIR_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(DIR_RAIZ, 'assets')

# ==============================================================================
# CONFIGURAÇÃO DE ÁUDIO GLOBAL (ANTI-DELAY)
# ==============================================================================
import pygame.mixer

if not pygame.mixer.get_init():
    pygame.mixer.init()

try:
    # buffer=512 é crucial: diminui o atraso entre o comando e o som sair
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except pygame.error as e:
    print(f"Erro ao inicializar Mixer: {e}") 

# Carregamento antecipado do som de pulo para evitar travadinhas durante o jogo
try:
    SOM_PULO_OBJETO = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sons', SOM_PULO))
    SOM_PULO_OBJETO.set_volume(0.30) 
except Exception:
    SOM_PULO_OBJETO = pygame.mixer.Sound(buffer=128) # Cria som mudo se falhar

# ==============================================================================
# CLASSE GERENCIADOR: O CÉREBRO DO JOGO
# ==============================================================================
class GerenciadorJogo:
    def __init__(self):
        """Inicializa configurações globais, fontes e carrega arquivos."""
        
        # --- 1. CONFIGURAÇÃO DE FONTES ---
        caminho_fonte = os.path.join(DIR_RAIZ, 'assets', 'fontes', 'BlockCraft.ttf')
        
        # Tenta carregar a fonte estilo Stranger Things/Minecraft
        if os.path.exists(caminho_fonte):
            self.fonte = pygame.font.Font(caminho_fonte, 40)       # Texto normal
            self.fonte_popup = pygame.font.Font(caminho_fonte, 30) # Textos flutuantes
            self.fonte_go = pygame.font.Font(caminho_fonte, 70)    # Game Over
        else:
            # Fallback (Plano B) caso a fonte não exista
            self.fonte = pygame.font.SysFont('Arial', 30, bold=True)
            self.fonte_popup = pygame.font.SysFont('Arial', 20, bold=True)
            self.fonte_go = pygame.font.SysFont('Arial', 60, bold=True)
        
        self.personagem_selecionado = "wilque" 
        
        # --- 2. EXECUÇÃO INICIAL ---
        self.carregar_fundos()    # Carrega imagens de cenário
        self.iniciar_musicas()    # Prepara playlists
        self.resetar_jogo()       # Zera pontuação e vidas

    def resetar_jogo(self, personagem=None):
        """Reinicia todas as variáveis para começar uma nova partida."""
        if personagem:
            self.personagem_selecionado = personagem.lower()

        # Placar e Mecânicas
        self.pontos_score = 0          
        self.ultimo_score_lanterna = 0  
        self.vidas = VIDAS_INICIAIS     
        self.game_over = False
        
        # Inventário
        self.conta_cafe = 0    
        self.conta_luzes = 0   
        
        # Controle de Mundo (Normal vs Invertido)
        self.mundo_invertido = False 
        self.velocidade_atual = VELOCIDADE_NORMAL
        self.posicao_fundo = 0 
        self.momento_entrada_invertido = 0
        
        # Controle de Geração de Inimigos (Spawning)
        self.cooldown_spawn = 0         
        self.textos_flutuantes = [] 

        # Recria os Grupos de Sprites (limpa os antigos)
        self.jogador = Jogador(self.personagem_selecionado)
        self.grupo_jogador = pygame.sprite.GroupSingle(self.jogador)
        self.grupo_obstaculos = pygame.sprite.Group()
        self.grupo_itens = pygame.sprite.Group()

        # Toca a música do mundo normal
        try:
            pygame.mixer.music.load(self.musica_real_path)
            pygame.mixer.music.play(-1) # Loop infinito
        except Exception:
            pass

    def carregar_fundos(self):
        """Carrega as imagens de fundo e trata erros se não existirem."""
        path_bg_normal = os.path.join(DIR_RAIZ, 'assets', 'cenarios', 'cenario_n.png') 
        path_bg_invertido = os.path.join(DIR_RAIZ, 'assets', 'cenarios', 'cenario_i.png')
        
        try:
            bg_n = pygame.image.load(path_bg_normal).convert()
            bg_i = pygame.image.load(path_bg_invertido).convert()
            # Redimensiona para caber perfeitamente na janela
            self.img_fundo_normal = pygame.transform.scale(bg_n, (LARGURA_TELA, ALTURA_TELA))
            self.img_fundo_invertido = pygame.transform.scale(bg_i, (LARGURA_TELA, ALTURA_TELA))
            self.tem_fundo = True
        except:
            print("ERRO: Imagens de cenário não encontradas. Usando cor sólida.")
            self.tem_fundo = False
    
    def iniciar_musicas(self):
        """Define os caminhos dos arquivos de áudio."""
        self.musica_real_path = os.path.join(ASSETS_DIR, 'sons', SOM_MUNDO_REAL)
        self.musica_invertida_path = os.path.join(ASSETS_DIR, 'sons', SOM_MUNDO_INVERTIDO)
        try:
            self.som_game_over_objeto = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sons', SOM_GAME_OVER))
        except:
            self.som_game_over_objeto = pygame.mixer.Sound(buffer=128) 
            
        pygame.mixer.music.set_volume(0.25) 

    def alternar_mundo(self):
        """
        Lógica Central de Troca de Dimensão.
        Alterna entre Mundo Real e Mundo Invertido, mudando música e velocidade.
        """
        self.mundo_invertido = not self.mundo_invertido
        
        try:
            if self.mundo_invertido:
                # --- INDO PARA O MUNDO INVERTIDO ---
                caminho = self.musica_invertida_path 
                self.velocidade_atual = VELOCIDADE_RAPIDA # Jogo acelera
                self.momento_entrada_invertido = pygame.time.get_ticks() # Marca hora de entrada
                self.criar_popup("MUNDO INVERTIDO!", (255, 0, 0)) 
            else:
                # --- VOLTANDO PARA O MUNDO REAL ---
                caminho = self.musica_real_path 
                self.velocidade_atual = VELOCIDADE_NORMAL
                self.criar_popup("MUNDO REAL", (0, 255, 0)) 
            
            # Troca a trilha sonora
            pygame.mixer.music.load(caminho) 
            pygame.mixer.music.play(-1)
        except:
             pass
            
        self.conta_luzes = 0 # Reseta contador para exigir nova coleta
        
    def criar_popup(self, texto, cor):
        """Cria um texto que sobe e desaparece (ex: +10 pontos)."""
        self.textos_flutuantes.append({
            'texto': texto, 'x': self.jogador.rect.centerx,
            'y': self.jogador.rect.top, 'tempo': 60, 'cor': cor
        })

    def atualizar_popups(self):
        """Animação dos textos flutuantes."""
        for popup in self.textos_flutuantes[:]:
            popup['y'] -= 1.5   # Sobe 1.5 pixels
            popup['tempo'] -= 1 # Reduz tempo de vida
            if popup['tempo'] <= 0: self.textos_flutuantes.remove(popup)

    def atualizar(self):
        """
        GAME LOOP PRINCIPAL:
        Executado 60 vezes por segundo. Controla toda a lógica do jogo.
        """
        if self.game_over: return
        
        # Atualiza posição de todos os sprites
        self.grupo_jogador.update()
        self.grupo_obstaculos.update()
        self.grupo_itens.update()
        self.atualizar_popups()

        # --- DIFICULDADE DINÂMICA ---
        if self.mundo_invertido:
            chance_inimigo = 4  # 4% de chance por frame (Muitos inimigos)
            tempo_espera = 40   # Cooldown menor
        else:
            chance_inimigo = 1.5  # 1.5% de chance (Normal)
            tempo_espera = 60     # Cooldown maior

        # --- GERADOR DE INIMIGOS (SPAWN) ---
        if self.cooldown_spawn > 0: self.cooldown_spawn -= 1
        
        if self.cooldown_spawn == 0:
            # Sorteio para ver se cria inimigo agora
            if random.randint(0, 100) < chance_inimigo: 
                
                # =====================================================
                # LÓGICA DE SORTEIO DO INIMIGO (DEMODOG VS DEMOGORGON)
                # =====================================================
                eh_boss = False
                
                if self.mundo_invertido:
                    # No Mundo Invertido, jogamos uma moeda:
                    # 60% de chance de ser o CHEFE (Demogorgon) - Rápido e Grande
                    if random.randint(0, 100) < 60:
                        eh_boss = True
                    # 40% de chance de ser um Demodog/Cadeira - Comum
                    else:
                        eh_boss = False
                else:
                    # Mundo normal nunca tem o Chefe Demogorgon
                    eh_boss = False
                
                # --- ATENÇÃO: AQUI ESTÁ A CORREÇÃO PARA A CADEIRA ---
                # Passamos "mundo_invertido=self.mundo_invertido"
                novo_obstaculo = Obstaculo(
                    self.velocidade_atual, 
                    eh_demogorgon=eh_boss,
                    mundo_invertido=self.mundo_invertido 
                )
                self.grupo_obstaculos.add(novo_obstaculo)
                
                self.cooldown_spawn = tempo_espera

        # --- GERADOR DE ITENS ---
        if random.randint(0, 100) < 2: # 2% de chance
            tipo = random.choice(["waffle", "waffle", "cafe", "luzes"])
            self.grupo_itens.add(Item(self.velocidade_atual, tipo))

        # --- SISTEMA DE AJUDA (LANTERNA GARANTIDA) ---
        # Se o jogador fez muitos pontos sem ver lanterna, força o aparecimento de uma
        if self.pontos_score >= self.ultimo_score_lanterna + 30:
            self.grupo_itens.add(Item(self.velocidade_atual, "luzes"))
            self.ultimo_score_lanterna = self.pontos_score 

        # --- CHECAGEM DE TROCA DE MUNDO ---
        
        # 1. Ida para o Invertido (Pegou 5 luzes)
        if self.conta_luzes >= 5 and not self.mundo_invertido: 
            self.alternar_mundo()
        
        # 2. Volta para o Real (Acabou o tempo)
        if self.mundo_invertido:
            agora = pygame.time.get_ticks()
            if agora - self.momento_entrada_invertido > TEMPO_MUNDO_INVERTIDO:
                self.alternar_mundo()

        # Verifica se alguém bateu em alguém
        self.verificar_colisoes()

        # --- MOVIMENTO DO FUNDO (PARALLAX SIMPLES) ---
        self.posicao_fundo -= self.velocidade_atual * 0.5 
        if self.posicao_fundo <= -LARGURA_TELA: self.posicao_fundo = 0

    def verificar_colisoes(self):
        """
        Lógica de Colisão 'Pixel-Perfect' (Hitbox Melhorada).
        Usa collide_mask para ignorar as partes transparentes da imagem.
        """
        
        # 1. COLISÃO COM INIMIGOS (Usando collide_mask)
        # O parâmetro 'collided=pygame.sprite.collide_mask' faz a mágica:
        # Ele verifica o contorno real do desenho, não o quadrado em volta.
        if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True, collided=pygame.sprite.collide_mask):
            
            if not self.jogador.tem_escudo:
                # Sem escudo: Perde vida
                self.jogador.vidas -= 1
                
                if self.jogador.vidas <= 0: 
                    # Morreu de vez
                    pygame.mixer.music.stop()
                    self.som_game_over_objeto.play()
                    self.game_over = True
            else: 
                # Com escudo: Perde o escudo, mas continua vivo
                self.jogador.tem_escudo = False
        
        # 2. COLISÃO COM ITENS (Também Pixel-Perfect)
        itens_coletados = pygame.sprite.spritecollide(self.jogador, self.grupo_itens, True, collided=pygame.sprite.collide_mask)
        
        for item in itens_coletados:
            if item.tipo == "waffle": 
                self.pontos_score += 1 
                
            elif item.tipo == "cafe": 
                self.conta_cafe += 1
                # Regra: A cada 5 cafés = Ganha Escudo
                if self.conta_cafe > 0 and self.conta_cafe % 5 == 0:
                    self.jogador.tem_escudo = True
                    
            elif item.tipo == "luzes": 
                self.conta_luzes += 1

    def desenhar_fundo(self, tela):
        """Desenha o cenário em loop (efeito infinito)."""
        if self.tem_fundo:
            fundo = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
            # Desenha duas vezes para cobrir o buraco quando a imagem anda
            tela.blit(fundo, (self.posicao_fundo, 0))
            tela.blit(fundo, (self.posicao_fundo + LARGURA_TELA, 0))
        else:
            tela.fill(VERMELHO_MUNDO if self.mundo_invertido else VERDE_CIN)
            
    def desenhar_sprites(self, tela):
        """Desenha todos os grupos na tela."""
        self.grupo_jogador.draw(tela)
        self.grupo_obstaculos.draw(tela)
        self.grupo_itens.draw(tela)
        
        # Desenha o escudo visualmente se o jogador tiver
        if self.jogador.tem_escudo:
            pygame.draw.circle(tela, MARROM, self.jogador.rect.center, 120, 5)

    def desenhar_hud_e_game_over(self, tela):
        """Desenha a interface do usuário (HUD) e tela de fim de jogo."""
        
        # --- HUD (PLACAR) ---
        texto = f"SCORE: {self.pontos_score}   |   VIDAS: {self.jogador.vidas}   |   LUZES: {self.conta_luzes}/5"
        
        sombra = self.fonte.render(texto, True, PRETO)
        frente = self.fonte.render(texto, True, BRANCO)
        tela.blit(sombra, (23, 23)) # Sombra deslocada
        tela.blit(frente, (20, 20))
        
        # --- POPUPS FLUTUANTES ---
        for popup in self.textos_flutuantes:
            surf = self.fonte_popup.render(popup['texto'], True, popup['cor'])
            sombra_p = self.fonte_popup.render(popup['texto'], True, PRETO)
            rect = surf.get_rect(center=(popup['x'], int(popup['y'])))
            tela.blit(sombra_p, (rect.x + 2, rect.y + 2))
            tela.blit(surf, rect)

        # --- TIMER DO MUNDO INVERTIDO ---
        if self.mundo_invertido:
            # Calcula quantos segundos faltam
            tempo = (TEMPO_MUNDO_INVERTIDO - (pygame.time.get_ticks() - self.momento_entrada_invertido)) // 1000
            txt_timer = self.fonte.render(f"RETORNO EM: {tempo}s", True, (255, 0, 0))
            tela.blit(txt_timer, (LARGURA_TELA//2 - txt_timer.get_width()//2, 100))

        # --- TELA DE GAME OVER ---
        if self.game_over:
            # Fundo escuro transparente
            s = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            s.set_alpha(200); s.fill(PRETO); tela.blit(s, (0,0))
            
            t1 = self.fonte_go.render("GAME OVER", True, VERMELHO_MUNDO)
            t2 = self.fonte.render(f"Score Final: {self.pontos_score}", True, AMARELO)
            t3 = self.fonte.render("ESC para Menu | R para Reiniciar", True, BRANCO)
            
            # Centraliza textos
            tela.blit(t1, (LARGURA_TELA//2 - t1.get_width()//2, ALTURA_TELA//2 - 100))
            tela.blit(t2, (LARGURA_TELA//2 - t2.get_width()//2, ALTURA_TELA//2))
            tela.blit(t3, (LARGURA_TELA//2 - t3.get_width()//2, ALTURA_TELA//2 + 80))