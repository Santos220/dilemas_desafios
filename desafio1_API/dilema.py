import requests
from itertools import combinations
from classes import AlwaysDefect, AlwaysCooperate, Random, GrimTrigger, TitForTat, Combate, Tabela

# Conexão com a API
url = 'http://127.0.0.1:8000/api/tournament/start'
response_init = requests.post(url)
print(f"Status Code: {response_init.status_code}\n")

# Início do Torneio
torneio = response_init.json()
sessao_id = torneio['session_id']
sessao = {
    'session_id': sessao_id,
    'cursor': torneio['next_cursor'],
}

# Início da ingestão dos algoritmos
ingestao = requests.get('http://127.0.0.1:8000/api/tournament/strategies', params=sessao)
algoritmo = ingestao.json()
lista_algoritmos = []
next_cursor = algoritmo['pagination']['next_cursor']
lista_algoritmos.append(algoritmo)

while next_cursor is not None:
    busca = {
        'session_id': sessao_id,
        'cursor': next_cursor,
    }
    ingestao = requests.get('http://127.0.0.1:8000/api/tournament/strategies', params=busca)
    algoritmo = ingestao.json()
    next_cursor = algoritmo['pagination']['next_cursor']
    lista_algoritmos.append(algoritmo)


# Tratamento de dicionários para criação de objetos
lista_jogadores = [] 
for i in lista_algoritmos:
    if i['algorithm']['slug'] == 'always_defect':
        always_defect = AlwaysDefect(**i['algorithm'])
        lista_jogadores.append(always_defect)
    elif i['algorithm']['slug'] == 'always_cooperate':
        always_cooperate = AlwaysCooperate(**i['algorithm'])
        lista_jogadores.append(always_cooperate)
    elif i['algorithm']['slug'] == 'random':
        random_player = Random(**i['algorithm'])
        lista_jogadores.append(random_player)
    elif i['algorithm']['slug'] == 'grim_trigger':
        grim_trigger = GrimTrigger(**i['algorithm'])
        lista_jogadores.append(grim_trigger)
    elif i['algorithm']['slug'] == 'tit_for_tat':
        tit_for_tat = TitForTat(**i['algorithm'])
        lista_jogadores.append(tit_for_tat)


# Execução do Dilema do Prisioneiro
combates = combinations(lista_jogadores, 2)
num = 0
for jogador1, jogador2 in combates:
    luta = Combate(jogador1, jogador2)
    num += 1
    
    pontuacao_total1 = jogador1.pontos
    pontuacao_total2 = jogador2.pontos
    
    for rodada in range(50):
        luta.executar_rodada()
        
    pontos_do_combate1 = jogador1.pontos - pontuacao_total1
    pontos_do_combate2 = jogador2.pontos - pontuacao_total2
    
    print(f"[Combate {num}: {jogador1.name} vs {jogador2.name}]")
    print(f"O jogador '{jogador1.name}' fez {pontos_do_combate1}.")
    print(f"O jogador '{jogador2.name}' fez {pontos_do_combate2}.\n")
    jogador1.historico_op.clear()
    jogador2.historico_op.clear()

# Tabela Final de Pontos:
tabela = Tabela(lista_jogadores)
tabela.exibir()

    
# print(len(lista_algoritmos))
# for i in lista_jogadores:
#     print(i.name)
    