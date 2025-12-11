import pygame
import sys
from src.configuracoes import *
from src.menu import MenuPrincipal
# AQUI ESTÁ A MÁGICA: Importando do arquivo separado
from src.gerenciador import GerenciadorJogo 

def main():
    pygame.init()
    pygame.mixer.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Stranger CIn: O Loop Infinito")
    relogio = pygame.time.Clock()

    menu = MenuPrincipal(LARGURA_TELA, ALTURA_TELA)
    try: menu.tocar_musica()
    except: pass
    
    # Cria o jogo usando a classe importada
    jogo = GerenciadorJogo()

    estado_atual = "MENU" 
    rodando = True

    while rodando:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                 if evento.key == pygame.K_F4 and (pygame.key.get_mods() & pygame.KMOD_ALT):
                     rodando = False

        if estado_atual == "MENU":
            pygame.mouse.set_visible(True)
            acao = menu.update(eventos)
            
            if acao == "INICIAR_JOGO":
                pygame.mixer.music.fadeout(500)
                jogo.resetar_jogo() # Agora vai funcionar direto do arquivo src/gerenciador.py
                estado_atual = "JOGO"
                
            elif acao == "CREDITOS":
                estado_atual = "CREDITOS"
            elif acao == "SAIR":
                rodando = False
            
            menu.draw(tela)

        elif estado_atual == "JOGO":
            pygame.mouse.set_visible(False)
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        estado_atual = "MENU"
                        try: menu.tocar_musica()
                        except: pass
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                        jogo.jogador.pular()

            jogo.atualizar()
            jogo.desenhar(tela)
            
            if jogo.game_over:
                # Se quiser reiniciar automático ou mostrar tela de game over
                pass

        elif estado_atual == "CREDITOS":
            pygame.mouse.set_visible(True)
            tela.fill((0, 0, 0))
            fonte = pygame.font.SysFont("arial", 40, bold=True)
            tela.blit(fonte.render("Desenvolvido por Alunos do CIn", True, (255, 255, 0)), (LARGURA_TELA//2 - 200, ALTURA_TELA//2))
            
            for evento in eventos:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    estado_atual = "MENU"

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()