import pygame

# Configurações da Tela 1920x1080
LARGURA_TELA = 1920
ALTURA_TELA = 1080
FPS = 60


# O chão visual fica a 150px da base da tela
NIVEL_CHAO = ALTURA_TELA - 150

# --- Cores (R, G, B) ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_CIN = (0, 150, 0)      # Cor do CIn Normal
VERMELHO_MUNDO = (100, 0, 0) # Cor do Mundo Invertido
AZUL = (0, 0, 255)           # Cor do Jogador
AMARELO = (255, 255, 0)      # Cor do Waffle
MARROM = (139, 69, 19)       # Cor do Café
VERDE_LUZ = (0, 255, 0)      # Cor das Luzes (Neon)

# Física do Jogo
GRAVIDADE = 2.0
FORCA_PULO = -40
VELOCIDADE_NORMAL = 12
VELOCIDADE_RAPIDA = 20