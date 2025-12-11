import pygame
import os
import random
# Importa as configurações globais
from src.configuracoes import * # --- CONFIGURAÇÕES VISUAIS DO MENU ---
YELLOW_SUB = (255, 235, 0)
YELLOW_HOVER = (255, 255, 200)
BLACK = (0, 0, 0)
ASH_COLOR = (200, 210, 220)

class Button:
    def __init__(self, text, x, y, width, height, font_size=40):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        
        # Tenta carregar a fonte (ajuste o caminho se necessário)
        # Assumindo que a pasta 'fontes' está na raiz do projeto
        caminho_fonte = os.path.join("fontes", "8-bit-pusab.ttf") 
        if os.path.exists(caminho_fonte):
            self.font = pygame.font.Font(caminho_fonte, font_size)
        else:
            self.font = pygame.font.SysFont("arial", font_size, bold=True)

    def draw(self, surface):
        # Verifica hover
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        primary_color = YELLOW_HOVER if self.is_hovered else YELLOW_SUB
        
        # Renderiza texto
        text_surf = self.font.render(self.text, True, primary_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Borda (Outline)
        outline_surf = self.font.render(self.text, True, BLACK)
        offset = 3
        for dx, dy in [(-offset,0), (offset,0), (0,-offset), (0,offset)]:
            surface.blit(outline_surf, (text_rect.x + dx, text_rect.y + dy))
             
        surface.blit(text_surf, text_rect)

    def check_click(self, event):
        """Verifica se houve clique do mouse neste botão"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

class MenuPrincipal:
    def __init__(self, largura_tela, altura_tela):
        self.largura = largura_tela
        self.altura = altura_tela
        
        # --- Carregar Assets ---
        self.carregar_assets()
        
        # --- Criar Botões ---
        cx = self.largura // 2
        # Posições dos botões
        self.btn_start = Button("INICIAR", cx - 200, 710, 400, 80, font_size=45)
        self.btn_credits = Button("CREDITOS", cx - 150, 820, 300, 60, font_size=35)
        self.btn_quit = Button("SAIR", cx - 100, 900, 200, 50, font_size=30)
        
        # --- Partículas ---
        self.particles = []
        for _ in range(100):
            self.criar_particula(inicio=True)

    def carregar_assets(self):
        # Caminhos baseados na raiz do projeto
        caminho_bg = os.path.join("imagens", "image_0.png")
        if os.path.exists(caminho_bg):
            self.bg = pygame.image.load(caminho_bg).convert()
            self.bg = pygame.transform.scale(self.bg, (self.largura, self.altura))
        else:
            # print(f"AVISO: Background não encontrado em {caminho_bg}")
            self.bg = None
            
        caminho_logo = os.path.join("imagens", "image_1.png")
        if os.path.exists(caminho_logo):
            self.logo = pygame.image.load(caminho_logo).convert_alpha()
            fator = 800 / self.logo.get_width()
            nova_altura = int(self.logo.get_height() * fator)
            self.logo = pygame.transform.scale(self.logo, (800, nova_altura))
        else:
            self.logo = None

        self.caminho_musica = os.path.join("sons", "theme.mp3")

    def tocar_musica(self):
        if os.path.exists(self.caminho_musica):
            pygame.mixer.music.load(self.caminho_musica)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def criar_particula(self, inicio=False):
        p = {
            'x': random.randint(0, self.largura),
            'y': random.randint(0, self.altura) if inicio else random.randint(-50, -10),
            'speed_y': random.uniform(0.5, 2.0),
            'size': random.randint(2, 5),
            'alpha': random.randint(50, 200)
        }
        self.particles.append(p)

    def update_particulas(self):
        for p in self.particles:
            p['y'] += p['speed_y']
            if p['y'] > self.altura:
                self.particles.remove(p)
                self.criar_particula()

    def update(self, eventos):
        """Retorna uma AÇÃO (String) se um botão for clicado."""
        self.update_particulas()
        
        for event in eventos:
            if self.btn_start.check_click(event):
                return "INICIAR_JOGO"
            if self.btn_credits.check_click(event):
                return "CREDITOS"
            if self.btn_quit.check_click(event):
                return "SAIR"
        return None

    def draw(self, tela):
        # 1. Fundo
        if self.bg:
            tela.blit(self.bg, (0, 0))
        else:
            tela.fill(BLACK)
        
        # 2. Partículas
        for p in self.particles:
            temp_surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*ASH_COLOR, p['alpha']), (p['size'], p['size']), p['size'])
            tela.blit(temp_surf, (p['x'], p['y']))
            
        # 3. Logo
        if self.logo:
            logo_x = self.largura // 2 - self.logo.get_width() // 2
            tela.blit(self.logo, (logo_x, 100))
            
        # 4. Botões
        self.btn_start.draw(tela)
        self.btn_credits.draw(tela)
        self.btn_quit.draw(tela)