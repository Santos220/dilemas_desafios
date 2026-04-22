import tournament_core
import database
import player_hand
import interface.interface as Interface
from manager import TorneioManager
from dto import PartidaConfigDTO 

def main():
    database.iniciar_banco()
    db_session = database.SessionLocal()
    
    db_repo = database.DatabaseRepository(db_session)
    
    ruido = tournament_core.GameEngine.generate_noise_level()
    num_rodadas = tournament_core.GameEngine.generate_rounds_count()
    
    Interface.SystemMessages.dados_iniciais(ruido, num_rodadas)

    dados_nomes = Interface.DataInterface.configurar_jogadores()    
    p1 = tournament_core.Player(dados_nomes.nome_j1)
    p2 = tournament_core.Player(dados_nomes.nome_j2)    
    p1.id_db = database.obter_ou_criar_jogador(db_session, p1.name)
    p2.id_db = database.obter_ou_criar_jogador(db_session, p2.name)
    player_hand.realizar_draft(p1, p2, tournament_core.avaiable_algorithms.copy())

    partida_db = database.criar_partida(db_session, p1.id_db, p2.id_db, ruido)
    Interface.SystemMessages.partida_iniciada(partida_db.id_partida)
    
    config_dto = PartidaConfigDTO(
        id_partida=partida_db.id_partida,
        ruido=ruido,
        num_rodadas=num_rodadas
    )
    
    torneio = TorneioManager(config_dto, p1, p2, Interface, db_repo)
    torneio.executar_torneio()

if __name__ == "__main__":
    main()