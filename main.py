import pygame
import sys
from src.configuracoes import *
from src.menu import MenuPrincipal
from src.gerenciador import GerenciadorJogo
from src.telas.selecao import TelaSelecao

def main():
    pygame.init()
    pygame.mixer.init()
    
    # Configura tela cheia
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Stranger CIn: O Loop Infinito")
    relogio = pygame.time.Clock()

    # Instancia as telas
    menu = MenuPrincipal(LARGURA_TELA, ALTURA_TELA)
    selecao = TelaSelecao(LARGURA_TELA, ALTURA_TELA)
    jogo = GerenciadorJogo()
    
    try: menu.tocar_musica()
    except: pass
    
    estado_atual = "MENU" 
    rodando = True

    while rodando:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT: rodando = False
            # Atalho Alt+F4
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F4 and (pygame.key.get_mods() & pygame.KMOD_ALT): 
                rodando = False

        # --- MÁQUINA DE ESTADOS ---
        if estado_atual == "MENU":
            pygame.mouse.set_visible(True)
            acao = menu.update(eventos)
            if acao == "INICIAR_JOGO": estado_atual = "SELECAO" 
            elif acao == "CREDITOS": estado_atual = "CREDITOS"
            elif acao == "SAIR": rodando = False
            menu.draw(tela)

        elif estado_atual == "SELECAO":
            pygame.mouse.set_visible(True)
            personagem = selecao.update(eventos)
            if personagem: 
                pygame.mixer.music.fadeout(500)
                jogo.resetar_jogo(personagem) 
                estado_atual = "JOGO"
            selecao.desenhar(tela)

        elif estado_atual == "JOGO":
            pygame.mouse.set_visible(False)
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    # ESC durante o jogo volta ao menu
                    if evento.key == pygame.K_ESCAPE and not jogo.game_over:
                        estado_atual = "MENU"
                        try: menu.tocar_musica()
                        except: pass
                    
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                        jogo.jogador.pular()
                    
                    # Comandos de Game Over
                    if jogo.game_over:
                        if evento.key == pygame.K_r: 
                            jogo.resetar_jogo(jogo.personagem_selecionado)
                        if evento.key == pygame.K_ESCAPE: 
                            estado_atual = "MENU"
                            try: menu.tocar_musica()
                            except: pass

            jogo.atualizar()
            jogo.desenhar(tela)

        elif estado_atual == "CREDITOS":
            pygame.mouse.set_visible(True)
            tela.fill(PRETO)
            fonte = pygame.font.SysFont("arial", 40, bold=True)
            
            t1 = fonte.render("Desenvolvido por Alunos do CIn - UFPE", True, AMARELO)
            t2 = fonte.render("Disciplina: Introdução à Programação", True, BRANCO)
            t3 = fonte.render("Pressione ESC para voltar", True, (200, 200, 200))
            
            tela.blit(t1, (LARGURA_TELA//2 - t1.get_width()//2, ALTURA_TELA//2 - 50))
            tela.blit(t2, (LARGURA_TELA//2 - t2.get_width()//2, ALTURA_TELA//2 + 10))
            tela.blit(t3, (LARGURA_TELA//2 - t3.get_width()//2, ALTURA_TELA//2 + 100))
            
            for e in eventos:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: 
                    estado_atual = "MENU"

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()  