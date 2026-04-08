import random
import tournament_core
import PrisonersDilemma
import database
from models import Partida, Serie, Rodada

database.iniciar_banco()
db_session = database.SessionLocal()

# --- Funções de Interação com o Usuário ---
def escolher_draft(jogador, algoritmos_disponiveis):
    print(f"\n>>> DRAFT: {jogador.name}, escolha uma carta para a sua mão:")
    for i, algo in enumerate(algoritmos_disponiveis):
        print(f"[{i + 1}] {algo}")
    while True:
        try:
            escolha = int(input(f"Digite o número da carta (1-{len(algoritmos_disponiveis)}): ")) - 1
            if 0 <= escolha < len(algoritmos_disponiveis):
                carta = algoritmos_disponiveis.pop(escolha)
                print(f"-> {jogador.name} adicionou '{carta}' na mão!")
                return carta
            print("Número inválido! Escolha uma das opções acima.")
        except ValueError:
            print("Por favor, digite apenas números.")


def escolher_mao(jogador, contexto):
    print(f"\n>>> {contexto.upper()}: {jogador.name}, escolha sua carta:")
    lista_opcoes = jogador.hand if contexto == "batalha" else jogador.discard_pile
    for i, algo in enumerate(lista_opcoes):
        nome = algo.name if hasattr(algo, 'name') else algo
        print(f"[{i + 1}] {nome}")    
    while True:
        try:
            escolha = int(input(f"Digite o número da carta (1-{len(lista_opcoes)}): ")) - 1
            if 0 <= escolha < len(lista_opcoes):
                return lista_opcoes.pop(escolha)
            print("Número inválido! Escolha uma das opções acima.")
        except ValueError:
            print("Por favor, digite apenas números.")


# Métricas Iniciais
ruido = tournament_core.GameEngine.generate_noise_level()
num_rodadas = tournament_core.GameEngine.generate_rounds_count()
print(f"\n---Dados da Partida---\nNível de Ruído: {ruido*100:.1f}%\nNúmero de Rodadas: {num_rodadas}\n")


# Jogadores
print("--- Cadastro de Jogadores ---")
nome_p1 = input("Digite o nome do Jogador 1: ")
nome_p2 = input("Digite o nome do Jogador 2: ")
player1 = tournament_core.Player(nome_p1)
player2 = tournament_core.Player(nome_p2)
# Cadastro via ORM
id_p1 = database.obter_ou_criar_jogador(db_session, player1.name)
id_p2 = database.obter_ou_criar_jogador(db_session, player2.name)

print(f"\n[Jogadores: {player1.name} vs {player2.name}]\n")


# Criando a Partida no Banco
nova_partida = Partida(
    id_jogador1=id_p1, 
    id_jogador2=id_p2, 
    ruido_sorteado=0.15,
    id_vencedor=None
)
db_session.add(nova_partida)
db_session.commit()
print(f"Partida aberta! O ID gerado foi: {nova_partida.id_partida}")


# Escolha das Estratégias
AVAILABLE_ALGORITHMS = [
    'AlwaysCooperate', 'AlwaysDefect', 'RandomChoice', 'TitForTat', 'GrimTrigger',
    'SuspiciousTitForTat', 'Pavlov', 'TitForTwoTats', 'HardMajority', 'Alternator'
]
# Coin Toss para Escolha de Cartas
while len(player1.hand) < 4 or len(player2.hand) < 4:    
    moeda = tournament_core.GameEngine.coin_toss()
    if moeda == 'Player 1' and len(player1.hand) < 4:
        carta_escolhida = escolher_draft(player1, AVAILABLE_ALGORITHMS)
        player1.hand.append(carta_escolhida)     
    elif moeda == 'Player 2' and len(player2.hand) < 4:
        carta_escolhida = escolher_draft(player2, AVAILABLE_ALGORITHMS)
        player2.hand.append(carta_escolhida)   
    
print("---Estratégias escolhidas:---")
print(f"{player1.name}: {player1.hand}")
print(f"{player2.name}: {player2.hand}")

# Tratamento de Objetos
player1.hand = tournament_core.criar_algoritmos(player1.hand)
player2.hand = tournament_core.criar_algoritmos(player2.hand)


# Inicio da Partida
vitorias1 = 0
vitorias2 = 0
print("\n--- Início do Torneio! ---")

while vitorias1 < 3 and vitorias2 < 3:
    # Em caso de empate (2X2):
    if vitorias1 == 2 and vitorias2 == 2:
        print("\n--- EMPATE 2x2! Resgatando uma carta do descarte ---")
        alg1 = escolher_mao(player1, contexto="resgate")
        alg2 = escolher_mao(player2, contexto="resgate")
    else:
        alg1 = escolher_mao(player1, contexto="batalha")
        alg2 = escolher_mao(player2, contexto="batalha")
    
    combate = PrisonersDilemma.Combate(alg1, alg2, ruido, num_rodadas)
    resultado = combate.jogar()
    
    pontos1 = sum(item['j1_pontos'] for item in resultado)
    pontos2 = sum(item['j2_pontos'] for item in resultado)
    
    # Salva a Série (Turno)
    nova_serie = Serie(
        id_partida=nova_partida.id_partida,
        num_serie=vitorias1 + vitorias2 + 1,
        id_algoritmo_j1=alg1.id,
        id_algoritmo_j2=alg2.id,
        pontos_j1=pontos1,
        pontos_j2=pontos2
    )
    db_session.add(nova_serie)
    db_session.commit()
    
    # Salva as Rodadas (Jogadas)
    database.salvar_rodadas_em_massa(db_session, nova_serie.id_serie, resultado)
    
    if pontos1 > pontos2:
        vitorias1 += 1
        print(f"-> Vitória de {player1.name}! ({alg1.name} - {pontos1} x {pontos2} - {alg2.name})")
        print(f"Placar Atual: {player1.name} {vitorias1} x {vitorias2} {player2.name}\n")
    elif pontos2 > pontos1:
        vitorias2 += 1
        print(f"-> Vitória de {player2.name}! ({alg1.name} - {pontos1} x {pontos2} - {alg2.name})")
        print(f"Placar Atual: {player1.name} {vitorias1} x {vitorias2} {player2.name}\n")
    else:
        print(f"-> Empate na série: {pontos1} pontos cada. | {alg1.name} vs {alg2.name}")
        player1.hand.append(alg1)
        player2.hand.append(alg2)
        
    player1.discard_pile.append(alg1)
    player2.discard_pile.append(alg2)


# Declarando o Vencedor Final
print("\n" + "-"*30)
if vitorias1 == 3:
    print(f"🏆 {player1.name.upper()} É O VENCEDOR FINAL!")
    nova_partida.id_vencedor = id_p1
    db_session.commit()
    print("Vencedor registrado com sucesso!")
else:
    print(f"🏆 {player2.name.upper()} É O VENCEDOR FINAL!")
    nova_partida.id_vencedor = id_p1
    db_session.commit()
    print("Vencedor registrado com sucesso!")
print("-"*30)
