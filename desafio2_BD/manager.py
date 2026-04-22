import PrisonersDilemma
from dto import ResumoTurnoDTO, AcaoRodadaDTO

class Juiz:
    def __init__(self, p1, p2, repo, ui):
        self.p1 = p1
        self.p2 = p2
        self.repo = repo
        self.ui = ui

    def devolver_cartas(self, alg1, alg2):
        self.p1.hand.append(alg1)
        self.p2.hand.append(alg2)

    def declarar_vencedor_final(self, vitorias1):
        if vitorias1 == 3:
            vencedor_nome, id_vencedor = self.p1.name, self.p1.id_db
            return vencedor_nome, id_vencedor
        else:
            vencedor_nome, id_vencedor = self.p2.name, self.p2.id_db
            return vencedor_nome, id_vencedor


class Pontuador:
    @staticmethod
    def somar_pontos(rodadas_dto):
        pontos1 = sum(item.j1_pontos for item in rodadas_dto)
        pontos2 = sum(item.j2_pontos for item in rodadas_dto)
        return pontos1, pontos2
    
    @staticmethod
    def atualizar_vitorias(pontos1, vitorias1, pontos2, vitorias2):
        if pontos1 > pontos2:
            return vitorias1 + 1, vitorias2, 1
        elif pontos2 > pontos1:
            return vitorias1, vitorias2 + 1, 2
        else:
            return vitorias1, vitorias2, 0


class TorneioManager:
    def __init__(self, config_dto, p1, p2, ui, db_repo):
        self.config = config_dto
        self.p1 = p1
        self.p2 = p2
        self.ui = ui
        self.repo = db_repo
        self.juiz = Juiz(p1, p2, db_repo, ui, config_dto.id_partida)
    
    def executar_torneio(self):
        self.ui.SystemMessages.torneio_inicio()
        vitorias1, vitorias2 = 0, 0
        turno_atual = 1
        
        # Deixar as funções mais legíveis
        # Determinar o máximo de rodadas, utilizando o for por exemplo
        # Lista de tipo de rodadas
        # for rodada tipo...
        while vitorias1 < 3 and vitorias2 < 3:
            # Tranformar em Funções
            if vitorias1 == 2 and vitorias2 == 2:
                self.ui.MatchMessages.resgaste_descarte(self.p1)
                idx1 = self.ui.DataInterface.menu_escolha_segura(self.p1.discard_pile)
                alg1 = self.p1.discard_pile.pop(idx1)
                
                self.ui.MatchMessages.resgaste_descarte(self.p2)
                idx2 = self.ui.DataInterface.menu_escolha_segura(self.p2.discard_pile)
                alg2 = self.p2.discard_pile.pop(idx2)
            else:
                self.ui.MatchMessages.escolha_carta_batalha(self.p1)
                idx1 = self.ui.DataInterface.menu_escolha_segura(self.p1.hand)
                alg1 = self.p1.hand.pop(idx1)
                
                self.ui.MatchMessages.escolha_carta_batalha(self.p2)
                idx2 = self.ui.DataInterface.menu_escolha_segura(self.p2.hand)
                alg2 = self.p2.hand.pop(idx2)
            
            combate = PrisonersDilemma.Combate(alg1, alg2, self.config.ruido, self.config.num_rodadas)
            resultado_raw = combate.jogar()
            
            rodadas_dto = [AcaoRodadaDTO(**reg) for reg in resultado_raw]
            
            pontos1, pontos2 = Pontuador.somar_pontos(rodadas_dto)
            vitorias1, vitorias2, status = Pontuador.atualizar_vitorias(pontos1, vitorias1, pontos2, vitorias2)
            
            resumo_dto = ResumoTurnoDTO(
                num_serie=turno_atual,
                id_algoritmo_j1=alg1.id,
                id_algoritmo_j2=alg2.id,
                vencedor_turno=status
            )
            
            self.repo.salvar_resultado_turno(self.config.id_partida, resumo_dto, rodadas_dto)
            
            if status == 0:
                self.ui.MatchMessages.empate_rodada(pontos1, alg1, alg2)
                self.juiz.devolver_cartas(alg1, alg2)
            else:
                self.ui.MatchMessages.resultado_rodada(self.p1, self.p2, pontos1, pontos2, alg1, alg2)
                self.p1.discard_pile.append(alg1)
                self.p2.discard_pile.append(alg2)
            
            self.ui.MatchMessages.placar_atual(self.p1, self.p2, vitorias1, vitorias2)
            turno_atual += 1

        self.juiz.declarar_vencedor_final(vitorias1)
        vencedor_nome, id_vencedor = self.juiz.declarar_vencedor_final(vitorias1)
        self.ui.MatchMessages.mostrar_vencedor_final(vencedor_nome)
        self.repo.registrar_vencedor_partida(self.config.id_partida, id_vencedor)
