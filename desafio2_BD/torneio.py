import random
import tournament_core
import PrisonersDilemma
from tournament_core import Player

# Métricas Iniciais
ruido = tournament_core.GameEngine.generate_noise_level()
num_rodadas = tournament_core.GameEngine.generate_rounds_count()


# Jogadores
player1 = Player("Walter")
player2 = Player("Jesse")


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
    
print(f"Estratégias {player1.name}: {player1.hand}")
print(f"Estratégias {player2.name}: {player2.hand}")


# Tratamento de Objetos
player1.hand = tournament_core.criar_algoritmos(player1.hand)
player2.hand = tournament_core.criar_algoritmos(player2.hand)


# Inicio da Partida
# (implementar...)

# Teste de Torneio
# always_defect = tournament_core.AlwaysDefect()
# always_cooperate = tournament_core.AlwaysCooperate()

# resultado = tournament_core.Combate(always_defect, always_cooperate, ruido, num_rodadas=30).jogar()

# pontos1 = sum(item['j1_pontos'] for item in resultado)
# pontos2 = sum(item['j2_pontos'] for item in resultado)

# for item in resultado:
#     print(f"Rodada {item['num_rodada']}:")
#     print(f"- Always Defect    - Escolha: {item['j1_escolha_real']} | Ruído: {item['j1_escolha_pos_ruido']} | Pontos: {item['j1_pontos']}")
#     print(f"- Always Cooperate - Escolha: {item['j2_escolha_real']} | Ruído: {item['j2_escolha_pos_ruido']} | Pontos: {item['j2_pontos']}\n")

# print(f"Pontuação total do Always Defect: {pontos1}")
# print(f"Pontuação total do Always Cooperate: {pontos2}")
