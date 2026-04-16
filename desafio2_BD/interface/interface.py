from dto import CadastroJogadoresDTO

class DataInterface:
    @staticmethod
    def configurar_jogadores() -> CadastroJogadoresDTO:
        print("--- Cadastro de Jogadores ---")    
        nome1 = input("Digite o nome do Jogador 1: ")
        nome2 = input("Digite o nome do Jogador 2: ")    
        print(f"\n--- Jogadores: {nome1} vs {nome2} ---")
        return CadastroJogadoresDTO(nome_j1=nome1, nome_j2=nome2)
    
    @staticmethod
    def menu_escolha_segura(lista_opcoes) -> int:
        """Exibe o menu e retorna APENAS O NÚMERO escolhido pelo usuário."""
        for i, opcao in enumerate(lista_opcoes):
            nome = opcao.name if hasattr(opcao, 'name') else opcao
            print(f"[{i + 1}] {nome}")
            
        while True:
            try:
                escolha = int(input(f"Digite o número (1-{len(lista_opcoes)}): ")) - 1
                if 0 <= escolha < len(lista_opcoes):
                    return escolha
                print("Número inválido! Escolha uma das opções acima.")
            except ValueError:
                print("Por favor, digite apenas números.")
    

class SystemMessages:
    @staticmethod
    def dados_iniciais(ruido, num_rodadas):
        print(f"\n--- Dados da Partida ---\nNível de Ruído: {ruido*100:.1f}%\nNúmero de Rodadas: {num_rodadas}\n")
    
    @staticmethod
    def partida_iniciada(partida_id):
        print(f"Partida iniciada no banco de dados. ID: {partida_id}")
        
    @staticmethod
    def mostrar_estrategias(player1, player2):
        print("\n--- Estratégias escolhidas: ---")
        print(f"{player1.name}: {[c.name for c in player1.hand]}")
        print(f"{player2.name}: {[c.name for c in player2.hand]}\n")
        
    @staticmethod
    def torneio_inicio():
        print("\n" + "="*30 + "\n   INÍCIO DO TORNEIO!\n" + "="*30)
        

class MatchMessages:
    @staticmethod
    def draft_escolha_carta(player):
        print(f"\n>>> DRAFT: {player.name}, escolha uma carta:")
    
    @staticmethod
    def escolha_carta_batalha(player):
        print(f"\n>>> BATALHA: {player.name}, escolha sua carta:")
    
    @staticmethod
    def resgaste_descarte(player):
        print(f"\n[!] EMPATE 2x2! TUDO OU NADA!\n>>> {player.name}, resgate do descarte:")
    
    @staticmethod
    def placar_atual(p1, p2, vitorias1, vitorias2):
        print(f"Placar Atual: {p1.name} {vitorias1} x {vitorias2} {p2.name}\n")
    
    @staticmethod
    def empate_rodada(pontos1, alg1, alg2):
        print(f"\n-> Empate na série: {pontos1} pontos cada. | {alg1.name} vs {alg2.name}")
    
    @staticmethod
    def resultado_rodada(p1, p2, pontos1, pontos2, alg1, alg2):
        if pontos1 > pontos2:
            print(f"\n-> Vitória de {p1.name}! ({alg1.name} - {pontos1} x {pontos2} - {alg2.name})")
        elif pontos2 > pontos1:
            print(f"\n-> Vitória de {p2.name}! ({alg2.name} - {pontos2} x {pontos1} - {alg1.name})")
        
    @staticmethod
    def mostrar_vencedor_final(vencedor):
        print("\n" + "-"*30)
        print(f"    🏆 VENCEDOR: {vencedor.upper()}!")
        print("-" * 30)


        