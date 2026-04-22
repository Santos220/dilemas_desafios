import tournament_core
import database
import player_hand
import PrisonersDilemma
import interface.interface as Interface
import manager as manager
import dto as dto

# Funções Auxiliares [temporárias...]
def obter_escolha_mao(player, Interface):
    Interface.MatchMessages.escolha_carta_batalha(player)
    idx = Interface.DataInterface.menu_escolha_segura(player.hand)
    return player.hand.pop(idx)

def obter_resgate_descarte(player, Interface):
    Interface.MatchMessages.resgaste_descarte(player)
    idx = Interface.DataInterface.menu_escolha_segura(player.discard_pile)
    return player.discard_pile.pop(idx)

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
        
    Interface.SystemMessages.torneio_inicio()
    vitorias1, vitorias2 = 0, 0
    
    for turno in range(1, 6):
        if manager.Juiz.vitoria(vitorias1, vitorias2):
            break

        if manager.Juiz.empate(vitorias1, vitorias2):
            alg1 = obter_resgate_descarte(p1, Interface)
            alg2 = obter_resgate_descarte(p2, Interface)
        else:
            alg1 = obter_escolha_mao(p1, Interface)
            alg2 = obter_escolha_mao(p2, Interface)

        combate = PrisonersDilemma.Combate(alg1, alg2, ruido, num_rodadas)
        resultados_raw = combate.jogar()
        rodadas_dto = [dto.AcaoRodadaDTO(**reg) for reg in resultados_raw]

        pontos1, pontos2 = manager.Pontuador.somar_pontos(rodadas_dto)
        vitorias1, vitorias2, status = manager.Pontuador.atualizar_vitorias(pontos1, vitorias1, pontos2, vitorias2)
        resumo_dto = dto.ResumoTurnoDTO(turno, alg1.id, alg2.id, status)

        db_repo.salvar_resultado_turno(partida_db.id_partida, resumo_dto, rodadas_dto)

        if status == 0:
            Interface.MatchMessages.empate_rodada(pontos1, alg1, alg2)
            manager.Juiz.devolver_cartas(p1, p2, alg1, alg2)
        else:
            Interface.MatchMessages.resultado_rodada(p1, p2, pontos1, pontos2, alg1, alg2)
            p1.discard_pile.append(alg1)
            p2.discard_pile.append(alg2)

        Interface.MatchMessages.placar_atual(p1, p2, vitorias1, vitorias2)

    vencedor_nome, id_vencedor = manager.Juiz.declarar_vencedor_final(vitorias1, p1, p2)
    Interface.MatchMessages.mostrar_vencedor_final(vencedor_nome)
    db_repo.registrar_vencedor_partida(partida_db.id_partida, id_vencedor)
    

if __name__ == "__main__":
    main()