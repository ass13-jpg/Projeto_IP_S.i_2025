import pygame
import os
import random
import sys
from src.configuracoes import *

# Definição de cores caso não existam no config
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

class Button:
    """Classe para botões interativos"""
    def __init__(self, text, x, y, width, height, font_size=40):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        
        # Tenta carregar fonte personalizada
        dir_atual = os.path.dirname(os.path.abspath(__file__)) 
        dir_raiz = os.path.dirname(dir_atual)
        caminho_fonte = os.path.join(dir_raiz, "assets", "fontes", "8-bit-pusab.ttf")
        
        if os.path.exists(caminho_fonte):
            self.font = pygame.font.Font(caminho_fonte, font_size)
        else:
            self.font = pygame.font.SysFont("arial", font_size, bold=True)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Cor muda se o mouse estiver em cima
        color = (255, 255, 200) if self.is_hovered else (255, 235, 0)
        
        text_surf = self.font.render(self.text, True, color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Outline (borda preta)
        outline = self.font.render(self.text, True, PRETO)
        surface.blit(outline, (text_rect.x+3, text_rect.y))
        surface.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                return True
        return False

class MenuPrincipal:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.carregar_assets()
        
        # Posicionamento dos botões
        cx = w // 2
        self.btn_start = Button("INICIAR", cx - 200, h - 380, 400, 80)
        self.btn_credits = Button("CREDITOS", cx - 150, h - 260, 300, 60, 35)
        self.btn_quit = Button("SAIR", cx - 100, h - 150, 200, 50, 30)
        
        self.particles = [{'x':random.randint(0,w), 'y':random.randint(0,h), 'speed':random.uniform(0.5,2), 'size':random.randint(2,5)} for _ in range(100)]

    def carregar_assets(self):
        dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_bg = os.path.join(dir_raiz, "assets", "imagens", "image_0.png")
        caminho_logo = os.path.join(dir_raiz, "assets", "imagens", "image_1.png")
        self.caminho_musica = os.path.join(dir_raiz, "assets", "sons", "theme.mp3")
        
        try:
            self.bg = pygame.transform.scale(pygame.image.load(caminho_bg).convert(), (self.w, self.h))
            logo = pygame.image.load(caminho_logo).convert_alpha()
            fator = 800 / logo.get_width()
            self.logo = pygame.transform.scale(logo, (800, int(logo.get_height()*fator)))
        except:
            self.bg = None
            self.logo = None

    def tocar_musica(self):
        try:
            pygame.mixer.music.load(self.caminho_musica)
            pygame.mixer.music.play(-1)
        except: pass

    def update(self, eventos):
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > self.h: p['y'] = -10
            
        for e in eventos:
            if self.btn_start.check_click(e): return "INICIAR_JOGO"
            if self.btn_credits.check_click(e): return "CREDITOS"
            if self.btn_quit.check_click(e): return "SAIR"
        return None

    def draw(self, tela):
        if self.bg: tela.blit(self.bg, (0,0))
        else: tela.fill(PRETO)
        
        for p in self.particles:
            s = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200,200,200,100), (p['size'], p['size']), p['size'])
            tela.blit(s, (p['x'], p['y']))
            
        if self.logo: tela.blit(self.logo, (self.w//2 - self.logo.get_width()//2, 50))
        
        self.btn_start.draw(tela)
        self.btn_credits.draw(tela)
        self.btn_quit.draw(tela)

# ---------------------------------------------------------
# CLASSE TELA DE SELEÇÃO (COM RETROBYTE E AJUSTE MANUAL)
# ---------------------------------------------------------
class TelaSelecao:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.selecionado = None # Ninguém selecionado no início (None, "WILQUE" ou "ELLEN")
        
        # --- CARREGAR FONTES (RETROBYTE) ---
        dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_retro = os.path.join(dir_raiz, "assets", "fontes", "RetroByte.ttf")
        
        if os.path.exists(caminho_retro):
            self.fonte_titulo = pygame.font.Font(caminho_retro, 50)
            self.fonte_nome = pygame.font.Font(caminho_retro, 35)
        else:
            print("Aviso: Fonte RetroByte não encontrada. Usando Arial.")
            self.fonte_titulo = pygame.font.SysFont('arial', 40, bold=True)
            self.fonte_nome = pygame.font.SysFont('arial', 30, bold=True) 
        
        # Botão confirmar
        self.btn_confirmar = Button("CONFIRMAR", w//2 - 125, h - 100, 250, 60, 30)

        # --- Carregar Imagens ---
        caminho_wilque = os.path.join(dir_raiz, "assets", "personagens", "wilque.png")
        caminho_ellen = os.path.join(dir_raiz, "assets", "personagens", "ellen.png")
        novo_tamanho = (600, 600) 
        
        try:
            img_w = pygame.image.load(caminho_wilque).convert_alpha()
            self.img_wilque_grande = pygame.transform.scale(img_w, novo_tamanho)
        except:
            self.img_wilque_grande = pygame.Surface(novo_tamanho); self.img_wilque_grande.fill((0, 0, 255))

        try:
            img_e = pygame.image.load(caminho_ellen).convert_alpha()
            self.img_ellen_grande = pygame.transform.scale(img_e, novo_tamanho)
        except:
            self.img_ellen_grande = pygame.Surface(novo_tamanho); self.img_ellen_grande.fill((255, 0, 0))

        # --- Definir Posições ---
        cy, cx = h // 2, w // 2
        self.rect_wilque = self.img_wilque_grande.get_rect(center=(cx - 300, cy))
        self.rect_ellen = self.img_ellen_grande.get_rect(center=(cx + 300, cy))

    def update(self, eventos):
        for e in eventos:
            # Se já tem alguém selecionado, verifica o botão confirmar
            if self.selecionado and self.btn_confirmar.check_click(e):
                return self.selecionado

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # Se clicar no Wilque
                if self.rect_wilque.collidepoint(mouse_pos):
                    self.selecionado = "WILQUE"
                
                # Se clicar na Ellen
                elif self.rect_ellen.collidepoint(mouse_pos):
                    self.selecionado = "ELLEN"
        return None

    def draw(self, tela):
        tela.fill(PRETO) 
        
        # Título
        titulo = self.fonte_titulo.render("ESCOLHA SEU PERSONAGEM", True, BRANCO)
        rect_titulo = titulo.get_rect(center=(self.w//2, 80)) 
        tela.blit(titulo, rect_titulo)
        
        # --- Desenha Imagens ---
        tela.blit(self.img_wilque_grande, self.rect_wilque)
        tela.blit(self.img_ellen_grande, self.rect_ellen)
        
        # --- 1. WILQUE (Nome e Centralização) ---
        cor_w = AMARELO if self.selecionado == "WILQUE" else BRANCO
        nome_w = self.fonte_nome.render("WILQUE", True, cor_w)
        rect_nome_w = nome_w.get_rect()
        
        # LÓGICA DO WILQUE (COM AJUSTE -55)
        rect_nome_w.centerx = self.rect_wilque.centerx - 55
        rect_nome_w.top = self.rect_wilque.bottom + 10
        
        tela.blit(nome_w, rect_nome_w)

        # --- 2. ELLEN (Nome e Centralização) ---
        cor_e = AMARELO if self.selecionado == "ELLEN" else BRANCO
        nome_e = self.fonte_nome.render("ELLEN", True, cor_e)
        rect_nome_e = nome_e.get_rect()
        
        # LÓGICA DA ELLEN (COM AJUSTE -40)
        rect_nome_e.centerx = self.rect_ellen.centerx - 40
        rect_nome_e.top = self.rect_ellen.bottom + 10
        
        tela.blit(nome_e, rect_nome_e)

        # Botão Confirmar (Só desenha se alguém estiver selecionado)
        if self.selecionado:
            self.btn_confirmar.draw(tela)