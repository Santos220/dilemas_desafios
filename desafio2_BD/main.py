import tournament_core
import database
import player_hand
from interface import interface
from manager import TorneioManager

def main():
    # 1. Configurações Iniciais e Banco
    database.iniciar_banco()
    db_session = database.SessionLocal()
    
    ruido = tournament_core.GameEngine.generate_noise_level()
    num_rodadas = tournament_core.GameEngine.generate_rounds_count()
    
    print(f"\n--- Dados da Partida ---\nNível de Ruído: {ruido*100:.1f}%\nNúmero de Rodadas: {num_rodadas}\n")

    # 2. Setup (Interface)
    dados_nomes = interface.configurar_jogadores()    
    p1 = tournament_core.Player(dados_nomes.nome_j1)
    p2 = tournament_core.Player(dados_nomes.nome_j2)    
    p1.id_db = database.obter_ou_criar_jogador(db_session, p1.name)
    p2.id_db = database.obter_ou_criar_jogador(db_session, p2.name)
    
    # Versão Antiga (sem DTO)
    # p1, p2 = interface_bkp.configurar_jogadores(db_session, database)
    player_hand.realizar_draft(p1, p2)

    # 3. Abre Partida no Banco (Database)
    partida_db = database.criar_partida(db_session, p1.id_db, p2.id_db, ruido)
    print(f"Partida iniciada no banco de dados. ID: {partida_db.id_partida}")

    # 4. Executa o Jogo (Gerenciador)
    torneio = TorneioManager(db_session, partida_db, p1, p2, ruido, num_rodadas)
    torneio.executar_torneio()

if __name__ == "__main__":
    main()