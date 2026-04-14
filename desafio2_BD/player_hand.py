import tournament_core

# Função de Menu
def obter_escolha_segura(lista_opcoes, mensagem_cabecalho):
    print(f"\n{mensagem_cabecalho}")
    for i, opcao in enumerate(lista_opcoes):
        nome = opcao.name if hasattr(opcao, 'name') else opcao
        print(f"[{i + 1}] {nome}")
        
    while True:
        try:
            escolha = int(input(f"Digite o número (1-{len(lista_opcoes)}): ")) - 1
            if 0 <= escolha < len(lista_opcoes):
                return lista_opcoes.pop(escolha)
            print("Número inválido! Escolha uma das opções acima.")
        except ValueError:
            print("Por favor, digite apenas números.")


# Escolha das Cartas (Draft)
def realizar_draft(player1, player2, avaiable_algorithms):    
    while len(player1.hand) < 4 or len(player2.hand) < 4:    
        moeda = tournament_core.GameEngine.coin_toss()
        if moeda == 'Player 1' and len(player1.hand) < 4:
            carta = obter_escolha_segura(avaiable_algorithms, f">>> DRAFT: {player1.name}, escolha uma carta:")
            player1.hand.append(carta)     
        elif moeda == 'Player 2' and len(player2.hand) < 4:
            carta = obter_escolha_segura(avaiable_algorithms, f">>> DRAFT: {player2.name}, escolha uma carta:")
            player2.hand.append(carta) 
            
    # Tratamento de objetos após o Draft
    player1.hand = tournament_core.criar_algoritmos(player1.hand)
    player2.hand = tournament_core.criar_algoritmos(player2.hand)
    
    print("\n--- Estratégias escolhidas: ---")
    print(f"{player1.name}: {[c.name for c in player1.hand]}")
    print(f"{player2.name}: {[c.name for c in player2.hand]}\n")