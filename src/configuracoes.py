import pygame
# CONSTANTES DO GAME
# Tela (Resolução Full HD)
LARGURA_TELA = 1920
ALTURA_TELA = 1080
FPS = 60

# Mecânicas dO JOGO
VIDAS_INICIAIS = 10            # Começa com 10 vidas (Pedido no requisito)
TEMPO_MUNDO_INVERTIDO = 30000  # Tempo em ms (30 segundos)
NIVEL_CHAO = ALTURA_TELA - 150 # Altura visual do chão em relação ao fundo

# Estados do Jogo (Máquina de Estados interna) 
ESTADO_JOGANDO = 0
ESTADO_GAME_OVER = 1

# Paleta de Cores (RGB) 
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_CIN = (0, 150, 0)      # Fundo do CIn Normal
VERMELHO_MUNDO = (100, 0, 0) # Fundo do Mundo Invertido
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)      # Usado para Score e Destaques


# Cores de Fallback (Usadas se a imagem não carregar)
MARROM = (139, 69, 19)       # Café
VERDE_LUZ = (0, 255, 0)      # Luzes

# Física e Dificuldade 
GRAVIDADE = 2.0           # Força que puxa para baixo
FORCA_PULO = -40          # Força negativa (para cima) ao pular
VELOCIDADE_NORMAL = 12    # Velocidade de scroll no mundo normal
VELOCIDADE_RAPIDA = 16    # Velocidade no mundo invertido

