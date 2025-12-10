import pygame
import sys
from src.configuracoes import *
from src.gerenciador import GerenciadorJogo

def main():
    # Inicializa o Pygame
    pygame.init()
    
    # Configura Tela 
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.FULLSCREEN | pygame.SCALED)
    
    # Esconde o cursor do mouse para ficar mais bonito
    pygame.mouse.set_visible(False)
    
    pygame.display.set_caption("Stranger CIn: O Loop Infinito")
    relogio = pygame.time.Clock()

    # Cria o gerenciador do jogo
    jogo = GerenciadorJogo()

    rodando = True
    while rodando:
        # 1. Eventos (Teclado/Mouse)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.KEYDOWN:
                # Tecla ESC para sair do jogo
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                
                # Pulo (Espaço ou Seta Cima)
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                    jogo.jogador.pular()

        # 2. Atualização Lógica ---
        jogo.atualizar()

        # 3. Desenho na Tela ---
        jogo.desenhar(tela)

        # Atualiza o display e segura o FPS
        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()