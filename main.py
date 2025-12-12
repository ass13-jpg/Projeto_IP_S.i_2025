import pygame
import sys
from src.configuracoes import *
from src.menu import MenuPrincipal
from src.gerenciador import GerenciadorJogo 
from src.selecao import TelaSelecao # <--- IMPORT NOVO

def main():
    pygame.init()
    pygame.mixer.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Stranger CIn: O Loop Infinito")
    relogio = pygame.time.Clock()

    menu = MenuPrincipal(LARGURA_TELA, ALTURA_TELA)
    selecao = TelaSelecao(LARGURA_TELA, ALTURA_TELA) # <--- CRIA A TELA DE SELEÇÃO
    
    try: menu.tocar_musica()
    except: pass
    
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

        # --- MÁQUINA DE ESTADOS ---

        if estado_atual == "MENU":
            pygame.mouse.set_visible(True)
            acao = menu.update(eventos)
            
            if acao == "INICIAR_JOGO":
                # Mudança: Vai para a seleção em vez do jogo direto
                estado_atual = "SELECAO" 
                
            elif acao == "CREDITOS":
                estado_atual = "CREDITOS"
            elif acao == "SAIR":
                rodando = False
            
            menu.draw(tela)

        # === ESTADO NOVO: SELEÇÃO ===
        elif estado_atual == "SELECAO":
            pygame.mouse.set_visible(True)
            
            # Atualiza a tela de seleção e vê se alguém foi clicado
            personagem_escolhido = selecao.update(eventos)
            
            if personagem_escolhido: # Se retornou "wilque" ou "ellen"
                pygame.mixer.music.fadeout(500)
                # Inicia o jogo com o personagem escolhido
                jogo.resetar_jogo(personagem_escolhido) 
                estado_atual = "JOGO"

            selecao.desenhar(tela)
        # ============================

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
                # Se apertar ESC no game over, volta pro menu
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    estado_atual = "MENU"
                    try: menu.tocar_musica()
                    except: pass

        elif estado_atual == "CREDITOS":
            pygame.mouse.set_visible(True)
            tela.fill((0, 0, 0))
            fonte = pygame.font.SysFont("arial", 40, bold=True)
            tela.blit(fonte.render("Desenvolvido por Alunos do CIn", True, (255, 255, 0)), (LARGURA_TELA//2 - 250, ALTURA_TELA//2))
            tela.blit(fonte.render("Pressione ESC para voltar", True, (255, 255, 255)), (LARGURA_TELA//2 - 180, ALTURA_TELA//2 + 60))
            
            for evento in eventos:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    estado_atual = "MENU"

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()