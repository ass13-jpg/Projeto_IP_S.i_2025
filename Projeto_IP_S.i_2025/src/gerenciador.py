import pygame
import random
import os
from src.configuracoes import *

# IMPORTAÇÕES DE CLASSES (MODULOS)
from src.atores.jogador import Jogador
from src.atores.obstaculo import Obstaculo
from src.itens.coletavel import Item

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
        """Carrega as imagens dos cenários"""
        # Pega o diretório raiz do projeto (sobe duas pastas a partir deste arquivo)
        dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        try:
            # CAMINHO CORRIGIDO PARA A PASTA 'CENARIO'
            path_bg1 = os.path.join(dir_raiz, 'assets', 'cenario', 'cidade.png')
            path_bg2 = os.path.join(dir_raiz, 'assets', 'cenario', 'invertido.png')
            
            self.img_fundo_normal = pygame.transform.scale(pygame.image.load(path_bg1).convert(), (LARGURA_TELA, ALTURA_TELA))
            self.img_fundo_invertido = pygame.transform.scale(pygame.image.load(path_bg2).convert(), (LARGURA_TELA, ALTURA_TELA))
            self.tem_fundo = True
            print("Sucesso: Cenários carregados!")
        except Exception as e:
            print(f"ERRO: Não foi possível carregar os cenários. {e}")
            self.tem_fundo = False

    def alternar_mundo(self):
        """Troca a dificuldade e o visual entre Normal e Invertido"""
        self.mundo_invertido = not self.mundo_invertido
        if self.mundo_invertido:
            self.velocidade_atual = VELOCIDADE_RAPIDA
            self.momento_entrada_invertido = pygame.time.get_ticks()
        else:
            self.velocidade_atual = VELOCIDADE_NORMAL
            
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

        # Regras de Mudança de Mundo (10 luzes)
        if self.conta_luzes >= 10 and not self.mundo_invertido: 
            self.alternar_mundo()
        
        # Tempo limite no mundo invertido
        if self.mundo_invertido:
            agora = pygame.time.get_ticks()
            if agora - self.momento_entrada_invertido > TEMPO_MUNDO_INVERTIDO:
                self.alternar_mundo()

        self.verificar_colisoes()

        # Movimento do Fundo (Parallax simples)
        self.posicao_fundo -= self.velocidade_atual * 0.5 
        if self.posicao_fundo <= -LARGURA_TELA: self.posicao_fundo = 0

    def verificar_colisoes(self):
        """Gerencia colisão com Inimigos e Itens"""
        
        # 1. Colisão com Obstáculos
        if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True):
            if not self.jogador.tem_escudo:
                # Sem escudo: Perde vida
                self.jogador.vidas -= 1
                if self.jogador.vidas <= 0: self.game_over = True
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

    def desenhar(self, tela):
        # 1. Fundo
        if self.tem_fundo:
            fundo = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
            tela.blit(fundo, (self.posicao_fundo, 0))
            tela.blit(fundo, (self.posicao_fundo + LARGURA_TELA, 0))
        else:
            tela.fill(VERMELHO_MUNDO if self.mundo_invertido else VERDE_CIN)

        # 2. Sprites
        self.grupo_jogador.draw(tela)
        self.grupo_obstaculos.draw(tela)
        self.grupo_itens.draw(tela)

        # Só desenha o círculo se o escudo estiver ATIVO
        if self.jogador.tem_escudo:
            centro = self.jogador.rect.center
            pygame.draw.circle(tela, MARROM, centro, 90, 5)

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