# 🎮 Stranger CINgs

Este projeto consiste no desenvolvimento de um jogo 2D do gênero *Endless Runner*, criado utilizando a linguagem **Python** e a biblioteca **Pygame**.

O jogo foi desenvolvido como parte da avaliação da disciplina de **Introdução à Programação (IP)**, ofertada no Centro de Informática (**CIn**) da Universidade Federal de Pernambuco (**UFPE**).

## 🚀 Sobre o Jogo

Ambientado em uma atmosfera inspirada na série *Stranger Things*, o jogador deve desviar de obstáculos e coletar itens para pontuar. O diferencial do projeto é a mecânica de **troca de mundos**: ao coletar luzes suficientes, o cenário e a dificuldade se alteram, transportando o jogador para o "Mundo Invertido".

## 👨‍🦰 Membros

- [Albert Santos de Santana](https://github.com/ass13-jpg)
- [Erlon Matheus Felix de Santana](https://github.com/emfs2-byte)
- [Juan William da Silva Bezerra](https://github.com/SouoWill)
- [Luiz Miguel de Oliveira Siqueira](https://github.com/oliveiraluizmiguel57-blip)
- [Samuel Renan Mendes Umbelino do Monte](https://github.com/Samukarn)
- [Vicente Ancelmo de Oliveira Morais](http://github.com/vancelmo)

## ⛏ Divisão do Trabalho

| Membro | Função Principal | Contribuições Especificias  |
| --- | --- | --- |
| Albert | Game Designer & Dev | Criação do roteiro, desenvolvimento e aprimoramento das mecânicas. |
| Erlon | Project Manager & Dev | Divisão de tarefas, criação dos Menus (Início/Seleção) e correção de bugs (QA). |
| Luiz | Character Artist | Design e criação dos personagens e seus respectivos sprites. |
| Juan | Gameplay Developer | Criação dos vilões e implementação/melhoria do Mundo Invertido. |
| Samuel | Audio & UI Designer | Implementação da tela de Game Over e design de som (SFX/Música). |
| Vicente | Tech Lead & Artist | Criação dos cenários e organização/arquitetura do código. |

## 🛠️**Ferramentas, Frameworks e Bibliotecas**

- **Pygame**

> O **Pygame** serviu como o motor principal do projeto, sendo a biblioteca responsável por toda a infraestrutura multimídia. No contexto deste jogo, ele foi utilizado para gerenciar a janela gráfica (alternância entre resoluções virtual e real), renderizar *sprites* e superfícies (como o efeito de *parallax* no cenário e as animações dos personagens), além de capturar eventos de entrada (teclado e mouse) para controlar o pulo do personagem e a navegação nos menus.
> 
- **OS**

> O módulo **os** foi fundamental para garantir a portabilidade e a organização do projeto. No código, ele é utilizado extensivamente através de `os.path` para construir caminhos dinâmicos e absolutos para os arquivos de *assets* (imagens e sons). Isso assegura que o jogo consiga localizar e carregar recursos corretamente (como as músicas "Separate Ways" e "Master of Puppets"), independentemente do sistema operacional ou do diretório em que o jogo foi instalado.
> 
- **Random**

> O módulo **random** atua como o núcleo da lógica procedural do jogo, sendo essencial para o gênero *Endless Runner*. Ele foi empregado para determinar a aleatoriedade na geração de obstáculos e itens colecionáveis (decidindo se aparecerá um Waffle, Café ou Luzes), além de controlar a "chance" de aparição de inimigos (variando entre 1% no mundo normal e 4% no mundo invertido), garantindo que nenhuma partida seja idêntica à outra.
> 
- **Sys**

> O módulo **sys** foi utilizado para o gerenciamento de saída do sistema. Em conjunto com os eventos do Pygame, a função `sys.exit()` garante que, ao fechar a janela ou clicar em "Sair" no menu, o interpretador Python encerre todos os processos de forma limpa e segura, liberando a memória utilizada pelo jogo.
> 
- **Pygame.mixer**

> Embora parte do pacote Pygame, o submódulo **mixer** merece destaque pela implementação da trilha sonora dinâmica. Ele foi programado para gerenciar canais de áudio estéreo, permitindo a transição suave (*fadeout/fadein*) entre a música tema do mundo normal e a do mundo invertido, criando a atmosfera imersiva exigida pela temática da série.
> 

## 💡Fundamentação e Metas

A ideia central do projeto foi desenvolver um jogo de plataforma infinita (*endless runner*) com progressão lateral, no qual o cenário se desloca continuamente para criar a ilusão de movimento, enquanto a arquitetura do código foi organizada modularmente para separar a lógica de controle, os atores e os itens. O fluxo do jogo inicia-se em um menu interativo que permite a navegação entre telas, passando pela seleção de personagens — onde o jogador escolhe entre os protagonistas disponíveis — e culminando na partida em si. Durante a jogabilidade, o personagem é submetido a uma física de gravidade constante e deve utilizar a mecânica de "Pulo Duplo" para desviar de obstáculos gerados proceduralmente; essa geração aleatória é balanceada por um sistema de tempo de recarga, impedindo que inimigos surjam em sequência impossível de ser desviada.

O sistema de progressão e sobrevivência é baseado na coleta estratégica de itens: enquanto os "Waffles" incrementam a pontuação, o "Café" possui uma mecânica acumulativa que concede um escudo de invulnerabilidade a cada cinco unidades coletadas, protegendo o jogador contra danos. O grande diferencial da experiência é a alternância dinâmica entre dimensões: ao acumular uma quantidade específica de "Luzes", o jogo transporta o personagem para o "Mundo Invertido". Neste estado, a atmosfera visual torna-se sombria, a velocidade do jogo aumenta drasticamente e a frequência de inimigos é quadruplicada, criando um desafio intenso de sobrevivência que dura trinta segundos antes de o portal se fechar e retornar à normalidade. O ciclo se encerra quando os pontos de vida do jogador chegam a zero, acionando a tela de derrota com a pontuação final.

## 🏛Arquitetura do Projeto

O código foi estruturado de forma modular e hierárquica, separando responsabilidades para garantir um desenvolvimento escalável e inteligível:

- **Assets**

> Diretório central onde residem todos os recursos multimídia utilizados na aplicação. Nele encontram-se as subpastas de áudio e imagem, contendo os *sprites* dos personagens (Wilque e Ellen), as camadas de fundo para o efeito de *parallax* (tanto do mundo normal quanto do invertido), os elementos de interface (HUD) e a trilha sonora dinâmica que alterna entre as dimensões.
> 
- **Src (Source)**

> Pasta raiz do código-fonte, a qual organiza a lógica do jogo em módulos específicos baseados em Programação Orientada a Objetos (POO). Dentro dela, temos divisões claras como `atores` (para entidades vivas como o Jogador e Obstáculos), `itens` (para objetos coletáveis como Café e Waffles) e `base`, que contém a superclasse "Entidade", responsável por padronizar o carregamento de imagens e o posicionamento de todos os objetos visuais.
> 
- **Configurações**

> Arquivo (`configuracoes.py`) onde todas as constantes globais do sistema são definidas. É aqui que parâmetros cruciais são centralizados, como as dimensões da tela, paletas de cores, variáveis de física (gravidade e força do pulo), além das configurações de balanceamento de dificuldade, como a velocidade de deslocamento dos mundos e as taxas de aparecimento de inimigos.
> 
- **Gerenciador**

> O "cérebro" do jogo (`gerenciador.py`), equivalente à *engine* lógica. Esta classe é responsável por processar as regras de negócio a cada quadro (*frame*). Nela ocorrem os cálculos de colisão, a atualização da pontuação e vidas, a lógica de ativação do escudo acumulativo e, principalmente, o controle do temporizador e das condições necessárias para a transição dinâmica entre o Mundo Normal e o Mundo Invertido.
> 
- **Main**

> O ponto de entrada da aplicação (`main.py`). Este arquivo implementa o *loop* principal e uma Máquina de Estados que orquestra o fluxo de navegação do usuário. Ele é responsável por inicializar a biblioteca gráfica, configurar a janela de exibição e alternar o controle entre as diferentes interfaces do sistema: Menu Principal, Tela de Seleção de Personagens, o Jogo em si (instanciando o Gerenciador) e a Tela de Créditos.
> 

## Conceitos na pratica

**Estruturas Condicionais:**
As condicionais foram fundamentais para a lógica de estado do jogo e para as regras de gameplay. O uso mais evidente ocorre na verificação de colisões e na mecânica de troca de mundos. Utilizamos `if` e `else` para determinar se o jogador possui um escudo ativo ao colidir com um obstáculo (decidindo se ele perde uma vida ou apenas o escudo) e para verificar se a contagem de "luzes" atingiu o critério necessário para alternar entre o Mundo Normal e o Invertido. Além disso, o fluxo principal do jogo (Menu -> Jogo -> Game Over) é controlado inteiramente por checagens condicionais. Exemplo da lógica de troca de mundo e colisão:

```python
# Trecho de src/gerenciador.py
if self.conta_luzes >= 10 and not self.mundo_invertido: 
    self.alternar_mundo()

if pygame.sprite.spritecollide(self.jogador, self.grupo_obstaculos, True):
    if not self.jogador.tem_escudo:
        self.jogador.vidas -= 1
        if self.jogador.vidas <= 0: 
            self.game_over = True
    else: 
        self.jogador.tem_escudo = False
```

**Laços de Repetição:**
Os laços são a base do "Game Loop", responsável por manter a janela aberta e atualizar os quadros a 60 FPS. O `while` principal gerencia a execução contínua do jogo, enquanto laços `for` são extensivamente utilizados para iterar sobre eventos do sistema (como cliques e teclas) e para atualizar e desenhar grupos de objetos (sprites). Um uso específico e criativo dos laços neste projeto foi na atualização dos textos flutuantes (pop-ups) e das partículas do Mundo Invertido, onde iteramos sobre cada item da lista para ajustar sua posição frame a frame. Exemplo da iteração sobre a lista de pop-ups:

```python
# Trecho de src/gerenciador.py
def atualizar_popups(self):
    # Itera sobre uma cópia da lista para permitir remoção segura
    for popup in self.textos_flutuantes[:]:
        popup['y'] -= 1.5 # Faz o texto subir
        popup['tempo'] -= 1
        if popup['tempo'] <= 0:
            self.textos_flutuantes.remove(popup)
```

**Listas:**
As listas foram essenciais para o gerenciamento de múltiplos objetos dinâmicos. O Pygame utiliza o conceito de `Group` (que funciona como uma lista avançada) para gerenciar o jogador, obstáculos e itens coletáveis. Além disso, utilizamos listas nativas do Python para criar o sistema de partículas e os textos flutuantes de feedback. Isso permitiu adicionar e remover elementos da tela dinamicamente sem precisar criar variáveis individuais para cada um. Exemplo da lista usada para armazenar dicionários de texto:

```python
# Trecho de src/gerenciador.py
self.textos_flutuantes = [] 

def criar_popup(self, texto, cor):
    self.textos_flutuantes.append({
        'texto': texto,
        'x': self.jogador.rect.centerx,
        'y': self.jogador.rect.top,
        'tempo': 60,
        'cor': cor
    })
```

**Funções:**
Para manter o código limpo, modular e de fácil manutenção, encapsulamos lógicas específicas em funções (métodos). Criamos funções dedicadas para tarefas distintas, como `resetar_jogo()` (que restaura as variáveis iniciais), `carregar_fundos()` (que lida com I/O de imagens), `verificar_colisoes()` e `alternar_mundo()`. Isso evita a repetição de código e torna o desenvolvimento mais ágil. Exemplo da função que isola a lógica de desenhar o cenário:

```python
# Trecho de src/gerenciador.py
def desenhar_fundo(self, tela):
    if self.tem_fundo:
        fundo = self.img_fundo_invertido if self.mundo_invertido else self.img_fundo_normal
        tela.blit(fundo, (self.posicao_fundo, 0))
        tela.blit(fundo, (self.posicao_fundo + LARGURA_TELA, 0))
    else:
        tela.fill((20, 20, 20))
```

**Dicionários e Tuplas:**
As tuplas foram amplamente utilizadas para representar dados imutáveis, como as coordenadas `(x, y)` de desenho na tela e as definições de cores RGB no arquivo de configurações (ex: `(255, 255, 255)` para branco). Já os dicionários foram cruciais para armazenar dados estruturados dos textos flutuantes, permitindo agrupar propriedades heterogêneas (texto, posição numérica, cor e tempo de vida) em um único objeto acessível por chaves. Exemplo de uso de tuplas para cores e dicionário para estrutura de dados:

```python
# Trecho de src/configuracoes.py e src/gerenciador.py
BRANCO = (255, 255, 255) # Tupla
VERMELHO_MUNDO = (139, 0, 0) # Tupla

# Dicionário armazenando estado do popup
{
    'texto': texto,
    'x': self.jogador.rect.centerx, # Coordenada
    'cor': cor # Tupla de cor
}
```

**Programação Orientada a Objetos (POO):**
Este foi o paradigma central do projeto. O jogo foi arquitetado em torno de classes que representam as entidades do sistema. A classe `GerenciadorJogo` atua como o cérebro, controlando o fluxo global. As classes `Jogador`, `Obstaculo` e `Item` herdam da classe `pygame.sprite.Sprite`, aproveitando funcionalidades nativas de física e renderização. O encapsulamento permitiu que cada objeto cuidasse de sua própria lógica (como o movimento autônomo dos obstáculos), enquanto o gerenciador apenas coordena as interações. Exemplo da estrutura da classe principal:

```python
# Trecho de src/gerenciador.py
class GerenciadorJogo:
    def __init__(self):
        self.personagem_selecionado = "wilque"
        self.carregar_fundos()
        self.iniciar_musicas()
        
        # Instanciação de objetos
        self.jogador = Jogador(self.personagem_selecionado)
        self.grupo_obstaculos = pygame.sprite.Group()
        
    def atualizar(self):
        # Polimorfismo: chamando update() de objetos diferentes
        self.grupo_jogador.update()
        self.grupo_obstaculos.update()
```

## 📁 Estrutura de Pastas

### Arquitetura de pastas do projeto

O projeto está organizado de forma modular, separando responsabilidades e facilitando a leitura, manutenção e evolução do código.

```
Projeto_IP_S.i_2025/
├── assets/
├──src/
│   ├── atores/
│   ├── base/
│   ├── itens/
│   └── telas/
├──main.py
├── requirements.txt
├── README.md
└──.gitignore

```

---

## 📁 src

Pasta principal do **código-fonte do projeto**, contendo toda a lógica do jogo.

### 📂 Estrutura interna de `src/`

```
src/
├── atores/
│   ├── player.py
│   ├── enemy.py
│   └── ...
├── base/
│   ├── base_game.py
│   └── utilities.py
├── itens/
│   ├── health_pack.py
│   └── speed_boost.py
└── telas/
    ├──menu.py
    └── game_over.py

```

---

## 📂 atores

Contém os **atores do jogo**, ou seja, entidades que possuem comportamento ativo.

➡️ Responsabilidades comuns:

- Movimentação
- Interações
- Colisões
- Estados do personagem

Arquivos típicos:

- `player.py` — lógica do jogador
- `enemy.py` — lógica dos inimigos

---

## 📂 base

Contém **classes base e utilitárias**, usadas por diferentes partes do projeto.

➡️ Funções principais:

- Estruturas genéricas
- Código reutilizável
- Base para herança ou composição

Arquivos típicos:

- `base_game.py` — estrutura principal do jogo
- `utilities.py` — funções auxiliares

---

## 📂 itens

Reúne os **itens do jogo**, geralmente objetos coletáveis ou utilizáveis.

➡️ Exemplos:

- `health_pack.py` — item de recuperação de vida
- `speed_boost.py` — item de aumento de velocidade

Essa separação facilita o controle de efeitos e inventário.

---

## 📂 telas

Responsável pelas **telas e estados visuais do jogo**.

➡️ Exemplos:

- `menu.py` — tela inicial
- `game_over.py` — tela de fim de jogo

Cada tela costuma gerenciar:

- Renderização
- Entrada do usuário
- Transição entre estados

---

## 📁 assets

Pasta destinada aos **recursos do jogo** (imagens, sons, músicas, etc.).

```
assets/
├── imagens
├── sons
└── outros recursos

```

---

## 🟢 main.py

Arquivo principal que **inicializa o jogo**, cria a janela e inicia o loop principal.

## **Capturas de tela**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/24b18874-b016-400d-b898-ee32c90828db" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/380018fb-98c9-4e75-b1f8-f39063471d5c" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/bab8849f-0933-484b-bb9f-b20b25fa1b2d" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/941a968a-ba87-4a0e-8821-2d93021fa202" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ebaa6617-cdd7-4355-a5c2-464bd25ee0dc" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4b932090-a604-4750-abea-8611ff7fffad" />



## 💪Desafios:

**Maior Erro:** 

- Escopo vs. Prazo

> O Problema: Subestimamos a complexidade do jogo frente ao tempo curto, tentando criar mecânicas demais.
A Solução: Adotamos a estratégia de MVP (Produto Viável Mínimo). Cortamos funcionalidades secundárias e focamos em garantir que o núcleo do jogo (mapa, câmera align_camera e colisões) funcionasse sem bugs.
> 

**Maior Desafio:** 

- Versionamento (Git)

> O Problema: Dificuldades técnicas em manter o código sincronizado entre a equipe, gerando conflitos de merge e erros de configuração (user.email).
A Solução: Capacitação da equipe. Estabelecemos boas práticas de commits e divisão de tarefas (ex: um cuida do Mago, outro dos Inimigos) para evitar conflitos.
> 

**Lições Aprendidas:**

- Organização e Modularização

> O Aprendizado: Em grupo, código organizado é sobrevivência.
Na Prática: A aplicação de Orientação a Objetos (POO) e estruturas de dados (Listas/Dicionários) permitiu o trabalho simultâneo e provou a versatilidade do Python/Pygame para prototipagem rápida.
>

