import pygame
import os
import random
from src.configuracoes import *

class Button:
    """Classe para botões interativos"""
    def __init__(self, text, x, y, width, height, font_size=40):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        
        # Tenta carregar fonte personalizada
        dir_atual = os.path.dirname(os.path.abspath(__file__)) # src
        dir_raiz = os.path.dirname(dir_atual) # Raiz
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
        
        # Efeito de borda no texto
        outline = self.font.render(self.text, True, PRETO)
        surface.blit(outline, (text_rect.x+3, text_rect.y))
        surface.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered: return True
        return False

class MenuPrincipal:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.carregar_assets()
        
        # Posicionamento dos botões
        cx = w // 2
        self.btn_start = Button("INICIAR", cx - 200, 710, 400, 80)
        self.btn_credits = Button("CREDITOS", cx - 150, 820, 300, 60, 35)
        self.btn_quit = Button("SAIR", cx - 100, 900, 200, 50, 30)
        
        # Partículas decorativas
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
        # Atualiza partículas
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > self.h: p['y'] = -10
            
        # Verifica cliques
        for e in eventos:
            if self.btn_start.check_click(e): return "INICIAR_JOGO"
            if self.btn_credits.check_click(e): return "CREDITOS"
            if self.btn_quit.check_click(e): return "SAIR"
        return None

    def draw(self, tela):
        if self.bg: tela.blit(self.bg, (0,0))
        else: tela.fill(PRETO)
        
        # Desenha partículas
        for p in self.particles:
            s = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200,200,200,100), (p['size'], p['size']), p['size'])
            tela.blit(s, (p['x'], p['y']))
            
        if self.logo: tela.blit(self.logo, (self.w//2 - self.logo.get_width()//2, 100))
        
        self.btn_start.draw(tela)
        self.btn_credits.draw(tela)
        self.btn_quit.draw(tela)