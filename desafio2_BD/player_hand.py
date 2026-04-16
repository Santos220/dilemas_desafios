import tournament_core
import interface.interface as Interface

def realizar_draft(player1, player2, avaiable_algorithms):    
    while len(player1.hand) < 4 or len(player2.hand) < 4:    
        moeda = tournament_core.GameEngine.coin_toss()
        
        if moeda == 'Player 1' and len(player1.hand) < 4:
            Interface.MatchMessages.draft_escolha_carta(player1)
            idx = Interface.DataInterface.menu_escolha_segura(avaiable_algorithms)
            carta = avaiable_algorithms.pop(idx)
            player1.hand.append(carta)
                 
        elif moeda == 'Player 2' and len(player2.hand) < 4:
            Interface.MatchMessages.draft_escolha_carta(player2)
            idx = Interface.DataInterface.menu_escolha_segura(avaiable_algorithms)
            carta = avaiable_algorithms.pop(idx)
            player2.hand.append(carta) 
            
    player1.hand = tournament_core.criar_algoritmos(player1.hand)
    player2.hand = tournament_core.criar_algoritmos(player2.hand)
    
    Interface.SystemMessages.mostrar_estrategias(player1, player2)
    