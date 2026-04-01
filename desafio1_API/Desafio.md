# API Dilema do Prisioneiro
Desenvolver um sistema que consome uma lista dinâmica de algoritmos via API e executa um torneio entre eles seguindo as regras clássicas do Dilema do Prisioneiro.

### 1. O que é o Dilema do Prisioneiro?
É um problema clássico da Teoria dos Jogos que demonstra o conflito entre agir de forma egoísta ou cooperar para um bem comum. Em cada rodada, duas estratégias decidem simultaneamente se vão **COOPERAR** ou **TRAIR** (Defect). A pontuação da rodada é definida pelo cruzamento dessas escolhas:

* **Ambos cooperam:** Cada um ganha +3 pontos. (Benefício mútuo)
* **Um trai e o outro coopera:** Quem traiu ganha +5 pontos (Benefício máximo) e quem cooperou ganha 0 (Prejuízo máximo).
* **Ambos traem:** Cada um ganha apenas +1 ponto. (Punição mútua)

### 2. O que é uma Estratégia?
No contexto deste torneio, uma "estratégia" é um algoritmo (um conjunto de regras lógicas) que decide qual será a ação na rodada atual.
- Onde encontrar as estratégias para codificá-las? Nas respostas da API; explore a documentação dela antes de tudo.

### 3. Como funciona o Torneio?
Para que estratégias complexas (que analisam o histórico do oponente) possam brilhar, o torneio não é decidido em apenas uma jogada. Ele funciona da seguinte forma:

* **Todos contra Todos:** Cada algoritmo participante deve enfrentar todos os outros algoritmos da lista.
* **Múltiplas Rodadas:** Cada confronto entre dois algoritmos consiste em $N$ rodadas consecutivas (neste desafio, considere **50 rodadas** por confronto). 
* **Memória de Jogo:** Durante essas 50 rodadas, as estratégias podem consultar o histórico de jogadas anteriores daquele confronto específico para decidir sua próxima ação. Ao iniciar um confronto contra um *novo* oponente, o histórico é zerado.
* **Acúmulo de Pontos:** Os pontos obtidos em cada rodada são somados ao longo de todo o torneio.
* **O Vencedor:** Ao final de todos os confrontos possíveis, o algoritmo que tiver a maior soma total de pontos é declarado o grande vencedor.

## Setup
1. A API está compilada em um único arquivo. Para rodá-la, abra um terminal e execute:
* `./api.exe`

2. Acesse **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** no navegador para entender os endpoints, o sistema de paginação por hashes e a política de latência.

## Requisitos de Entrega

* **Ingestão:** O código deve buscar todos os algoritmos automaticamente (o número de competidores pode mudar).
* **Torneio:** Executar 50 rodadas para cada confronto (Todos contra Todos).
* **Ranking:** Exibir no terminal o ranking final somando os pontos de cada estratégia.



# Manifesto Guia de Projeto
> *"The hardest single part of building a software system is deciding precisely what to build."*
> — **Fred Brooks** (The Mythical Man-Month)
## 1. Definição de Algoritmo
Um algoritmo pode ser definido como um procedimento que leva em consideração dados de entrada (inputs) e produz dados de saída (outputs). Logo, algoritmo é uma sequência de passos computacionais que transformam inputs em outputs. Conjunto de instruções lógicas, finitas e bem definidas, que têm o objetivo de executar tarefas específicas.
## 2. Classificação de Problemas: Negócio e Técnico
Há dois tipos de problemas: problemas de negócio e problemas técnicos, que em estudos póstumos serão descritos como requisitos funcionais e não funcionais. Mas, por agora, serão descritos em seus respectivos escopos como negócio e técnico.
### Problemas de Negócio (O "O Quê"):
Um problema de negócio é onde mora a lógica que o seu problema técnico precisa entregar: quais são as minhas saídas, quais são minhas entradas, quais são minhas restrições, quais são as características que modelam meu sistema (conjunto de etapas finitas) que irão resolver o escopo do problema passado. Esses, muitas vezes, são os mais desafiadores de se resolver em um projeto, são a primeira barreira que é necessário derrubar. Raras são as vezes que um projeto novo terá seu escopo totalmente resolvido; sempre haverá mudanças e nuances invisíveis à primeira vista. A etapa de resolver os problemas de negócio é a mais cara e onde mais se deve investir em um projeto, pois se houver um equívoco e a mudança ocorrer de forma tardia, isso irá resultar em uma bola de neve e em um possível fracasso do projeto. É onde são feitos diagramas de fluxo (não técnicos) e reuniões multidisciplinares (você raramente vai saber do domínio onde seu problema mora, você depende de outras pessoas para entender o domínio de sua aplicação). Aqui você nunca vai ter algo pronto, sempre dependerá de suas anotações; você precisa saber exatamente o que precisa entender sobre o mundo do problema para ser capaz de resolvê-lo.
### Problemas Técnicos (O "Como"):
Um problema técnico é onde você literalmente pensa nas ferramentas a baixo nível, versões, aplicações, integrações, pacotes, tipos de algoritmos, arquitetura do sistema... Essa etapa de decifrar as técnicas/tecnologias que serão utilizadas é a segunda mais custosa do projeto, é saber o que usar, quando usar, onde usar e saber onde não usar, quando não usar e onde não usar. Essa é a etapa onde são construídos diagramas de classe, entidade-relacionamento, de uso...
## 3. O Foco no Problema Central e o Raciocínio Macro-Micro
A coisa mais importante de todas: lembrar qual problema está resolvendo, qual o objetivo do seu raciocínio. Essa é a chave para decifrar qualquer etapa do projeto, do nível macro até o micro. O raciocínio deve ser quebrado e adequado para cada etapa; quanto mais de perto você olha para o seu projeto, mais seu raciocínio deve ser detalhado. O seu foco sempre vai ser o escopo que você está tentando alcançar. Se você está resolvendo um problema de comunicação entre duas ferramentas (Monday e Qlik), você sempre deve ter isso em mente ao decifrar as próximas etapas: qual é o intermédio? O que uma produz que a outra consegue usar? Todos esses raciocínios, por mais que algum dia você esqueça deles, são alcançados pela reflexão do problema, todos eles são abrangidos por isso. Essa é a razão do seu trabalho: resolver problemas. Você deve enxergar o problema por meio de um binóculo invertido: o seu maior entendimento deve ser do problema como um todo, e as respostas desse problema macro irão te mostrar como deverão ser os próximos passos.

# Questionário de Resolução de Projetos
Antes de escrever a primeira linha de código, pergunte a si mesma:

**Fase 1: O Binóculo Invertido (O Macro)**

1. Qual é o problema central que estou tentando resolver? (Descreva em uma frase simples).
2. Eu entendo o domínio desse problema? (Se não, com quem preciso conversar ou o que preciso pesquisar antes de começar?)

**Fase 2: O Problema de Negócio (O Quê)**
3. Quais são exatamente as minhas entradas (inputs) neste sistema?
4. Quais são as saídas (outputs) exatas que eu preciso entregar?
5. Quais são as restrições ou regras de negócio que eu **não posso** quebrar? (Ex: tempo, limite de memória, regras de um jogo).
6. Quais são os cenários de exceção? (O que acontece se a entrada vier vazia, corrompida ou demorar?)

**Fase 3: O Problema Técnico (O Como)**
7. Como vou quebrar esse grande problema de negócio em etapas técnicas finitas? (Desenhe um fluxo ou escreva os passos em português antes de programar).
8. Quais ferramentas e estruturas de dados são as mais adequadas para lidar com as entradas e saídas que mapeei?
9. Como vou separar a lógica de negócio (as regras) da infraestrutura (chamadas de rede, banco de dados)?

**Fase 4: Ponto de Controle (Durante a Execução)**
10. A linha de código ou função que estou escrevendo agora está me aproximando de resolver o problema central, ou estou me distraindo com detalhes desnecessários?
