import pygame
import sys
import random

from src.configuracoes import *
from src.menu import MenuPrincipal, TelaSelecao 
from src.gerenciador import GerenciadorJogo
from src.telas.game_over import TelaGameOver

class Particula:
    # Representa uma partícula para o efeito visual da neve/poeira no Mundo Invertido.
    
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        # Posição inicial aleatória
        self.x = random.randint(0, largura_tela)
        self.y = random.randint(0, altura_tela)
        self.radius = random.randint(1, 3) 
        self.velocidade_y = random.uniform(1.0, 3.5)
        self.velocidade_x = random.uniform(-0.5, 0.5) 
        self.cor = BRANCO 

    def mover(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        
        # Reinicia a partícula no topo
        if self.y > self.altura_tela:
            self.y = 0  
            self.x = random.randint(0, self.largura_tela)

    def desenhar(self, tela, cor_particula):
        pygame.draw.circle(tela, cor_particula, (int(self.x), int(self.y)), self.radius)

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
    tela_game_over = TelaGameOver(LARGURA_TELA, ALTURA_TELA)  
    
    global particulas 
    particulas = []
    NUMERO_PARTICULAS = 150 
    
    # Cores fixas para o efeito invertido
    COR_PARTICULA_INVERTIDA = (255, 100, 100) 
    
    for _ in range(NUMERO_PARTICULAS):
        particulas.append(Particula(LARGURA_TELA, ALTURA_TELA))

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
            # Verifica se o jogador confirmou a seleção
            personagem = selecao.update(eventos)
            
            # Se personagem retornou um nome (ex: "WILQUE"), inicia o jogo
            if personagem: 
                pygame.mixer.music.fadeout(500)
                jogo.resetar_jogo(personagem) 
                estado_atual = "JOGO"
            
            selecao.draw(tela)

        elif estado_atual == "JOGO":
            pygame.mouse.set_visible(False)
            
            # 1. TRANSIÇÃO PARA GAME OVER
            if jogo.game_over:
                jogo.desenhar_fundo(tela) 
                jogo.desenhar_sprites(tela) # Mantém os sprites para o fundo do GO
                estado_atual = "GAME_OVER"
                continue

            # 2. Lógica de Input 
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        estado_atual = "MENU"
                        try: menu.tocar_musica()
                        except: pass
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                        jogo.jogador.pular()
            
            # 3. Atualização de Lógica
            jogo.atualizar()

            # CAMADA 1: FUNDO
            jogo.desenhar_fundo(tela)
            
            # CAMADA 2: SPRITES (Jogador, Obstáculos, Itens)
            jogo.desenhar_sprites(tela) 

            # CAMADA 3: PARTÍCULAS (Por cima do cenário e dos sprites, mas por baixo do HUD)
            if jogo.mundo_invertido: 
                for particula in particulas:
                    particula.mover()
                    particula.desenhar(tela, COR_PARTICULA_INVERTIDA) 

            # CAMADA 4: HUD e TIMER (Por cima de TUDO)
            jogo.desenhar_hud_e_game_over(tela)
        
        elif estado_atual == "GAME_OVER":
            pygame.mouse.set_visible(True) # Mostra o cursor
    
            # Desenha a nova tela de Game Over (overlay + texto)
            tela_game_over.desenhar(tela, jogo.pontos_score)

            # Processa os inputs específicos para Game Over
            for evento in eventos:
                if evento.type == pygame.KEYDOWN:
                    # Reiniciar (R)
                    if evento.key == pygame.K_r: 
                        jogo.resetar_jogo(jogo.personagem_selecionado)
                        estado_atual = "JOGO" # Volta para o jogo
                    
                    # Voltar ao Menu (ESC)
                    elif evento.key == pygame.K_ESCAPE: 
                        estado_atual = "MENU" # Volta ao Menu
                        try: menu.tocar_musica()
                        except: pass
                        
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