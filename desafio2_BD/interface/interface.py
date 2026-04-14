from dto import CadastroJogadoresDTO

def configurar_jogadores() -> CadastroJogadoresDTO:
    print("--- Cadastro de Jogadores ---")    
    nome1 = input("Digite o nome do Jogador 1: ")
    nome2 = input("Digite o nome do Jogador 2: ")    
    print(f"\n--- Jogadores: {nome1} vs {nome2} ---")
    
    return CadastroJogadoresDTO(nome_j1=nome1, nome_j2=nome2)