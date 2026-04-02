import random
import tournament_core
import PrisonersDilemma


# Métricas Iniciais
ruido = tournament_core.GameEngine.generate_noise_level()
num_rodadas = tournament_core.GameEngine.generate_rounds_count()
print(f"\n---Dados da Partida---\nNível de Ruído: {ruido*100:.1f}%\nNúmero de Rodadas: {num_rodadas}\n")


# Jogadores
player1 = tournament_core.Player("Walter")
player2 = tournament_core.Player("Jesse")
print(f"[Jogadores: {player1.name} vs {player2.name}]\n")


# Escolha das Estratégias
AVAILABLE_ALGORITHMS = [
    'AlwaysCooperate', 'AlwaysDefect', 'RandomChoice', 'TitForTat', 'GrimTrigger',
    'SuspiciousTitForTat', 'Pavlov', 'TitForTwoTats', 'HardMajority', 'Alternator'
]

while len(player1.hand) < 4 or len(player2.hand) < 4:    
    moeda = tournament_core.GameEngine.coin_toss()
    if moeda == 'Player 1' and len(player1.hand) < 4:
        indice = random.randint(0, len(AVAILABLE_ALGORITHMS) - 1)
        player1.hand.append(AVAILABLE_ALGORITHMS.pop(indice))        
    elif moeda == 'Player 2' and len(player2.hand) < 4:
        indice = random.randint(0, len(AVAILABLE_ALGORITHMS) - 1)
        player2.hand.append(AVAILABLE_ALGORITHMS.pop(indice))
    
print("---Estratégias escolhidas:---")
print(f"{player1.name}: {player1.hand}")
print(f"{player2.name}: {player2.hand}")


# Tratamento de Objetos
player1.hand = tournament_core.criar_algoritmos(player1.hand)
player2.hand = tournament_core.criar_algoritmos(player2.hand)


# Inicio da Partida
vitorias1 = 0
vitorias2 = 0
print("\n--- Início do Torneio! ---\n")

while vitorias1 < 3 and vitorias2 < 3:
    # Em caso de empate (2X2):
    if vitorias1 == 2 and vitorias2 == 2:
        print("\n--- EMPATE 2x2! Resgatando uma carta do descarte ---")
        player1.hand.append(player1.discard_pile.pop(random.randint(0, len(player1.discard_pile) - 1)))
        player2.hand.append(player2.discard_pile.pop(random.randint(0, len(player2.discard_pile) - 1)))

    alg1 = player1.hand.pop(random.randint(0, len(player1.hand) - 1))
    alg2 = player2.hand.pop(random.randint(0, len(player2.hand) - 1))
    
    combate = PrisonersDilemma.Combate(alg1, alg2, ruido, num_rodadas)
    resultado = combate.jogar()
    
    pontos1 = sum(item['j1_pontos'] for item in resultado)
    pontos2 = sum(item['j2_pontos'] for item in resultado)
    
    if pontos1 > pontos2:
        vitorias1 += 1
        print(f"-> Vitória de {player1.name}! ({alg1.name} - {pontos1} x {pontos2} - {alg2.name})")
    elif pontos2 > pontos1:
        vitorias2 += 1
        print(f"-> Vitória de {player2.name}! ({alg1.name} - {pontos1} x {pontos2} - {alg2.name})")
    else:
        print(f"Empate na série: {pontos1} pontos cada. | {alg1.name} vs {alg2.name}")
        player1.hand.append(alg1)
        player2.hand.append(alg2)
        
    player1.discard_pile.append(alg1)
    player2.discard_pile.append(alg2)


# Declarando o Vencedor Final
print("\n" + "-"*30)
if vitorias1 == 3:
    print(f"🏆 {player1.name.upper()} É O VENCEDOR FINAL!")
else:
    print(f"🏆 {player2.name.upper()} É O VENCEDOR FINAL!")
print("-"*30)

