import PrisonersDilemma
import database
import interface.interface as Interface


class Juiz:
    def __init__(self, p1, p2, session, partida_db):
        self.p1 = p1
        self.p2 = p2
        self.session = session
        self.partida_db = partida_db

    def devolver_cartas(self, alg1, alg2):
        self.p1.hand.append(alg1)
        self.p2.hand.append(alg2)

    def declarar_vencedor_final(self, vitorias1):
        if vitorias1 == 3:
            vencedor, id_vencedor = self.p1.name, self.p1.id_db
        else:
            vencedor, id_vencedor = self.p2.name, self.p2.id_db
        
        Interface.MatchMessages.mostrar_vencedor_final(vencedor)
        database.registrar_vencedor(self.session, self.partida_db, id_vencedor)
        


class Pontuador:
    @staticmethod
    def somar_pontos(resultado):
        pontos1 = sum(item['j1_pontos'] for item in resultado)
        pontos2 = sum(item['j2_pontos'] for item in resultado)
        return pontos1, pontos2
    
    @staticmethod
    def atualizar_vitorias(pontos1, vitorias1, pontos2, vitorias2):
        """Retorna o novo placar e o status do turno (1=Vitória P1, 2=Vitória P2, 0=Empate)"""
        if pontos1 > pontos2:
            return vitorias1 + 1, vitorias2, 1
        elif pontos2 > pontos1:
            return vitorias1, vitorias2 + 1, 2
        else:
            return vitorias1, vitorias2, 0


class BancoDados:   
    @staticmethod
    def salvar_resultados(session, partida_db, vitorias1, vitorias2, alg1, alg2, resultado, pontos1, pontos2):
        nova_serie = database.salvar_serie(
            session, partida_db.id_partida, vitorias1 + vitorias2 + 1, 
            alg1.id, alg2.id, pontos1, pontos2
        )
        database.salvar_rodadas_em_massa(session, nova_serie.id_serie, resultado)
    

class TorneioManager:
    def __init__(self, session, partida_db, p1, p2, ruido, num_rodadas):
        self.session = session
        self.partida_db = partida_db
        self.p1 = p1
        self.p2 = p2
        self.ruido = ruido
        self.num_rodadas = num_rodadas        
        self.juiz = Juiz(p1, p2, session, partida_db)
    
    def executar_torneio(self):
        Interface.SystemMessages.torneio_inicio()
        vitorias1, vitorias2 = 0, 0
        
        while vitorias1 < 3 and vitorias2 < 3:
            if vitorias1 == 2 and vitorias2 == 2:
                # Player 1
                Interface.MatchMessages.resgaste_descarte(self.p1)
                escolha1 = Interface.DataInterface.menu_escolha_segura(self.p1.discard_pile)
                alg1 = self.p1.discard_pile.pop(escolha1)
                # Player 2
                Interface.MatchMessages.resgaste_descarte(self.p2)
                escolha2 = Interface.DataInterface.menu_escolha_segura(self.p1.discard_pile)
                alg2 = self.p1.discard_pile.pop(escolha2)
                
            else:
                # Player 1
                Interface.MatchMessages.escolha_carta_batalha(self.p1)
                escolha1 = Interface.DataInterface.menu_escolha_segura(self.p1.hand)
                alg1 = self.p1.hand.pop(escolha1)
                # Player 2
                Interface.MatchMessages.escolha_carta_batalha(self.p2)
                escolha2 = Interface.DataInterface.menu_escolha_segura(self.p2.hand)
                alg2 = self.p2.hand.pop(escolha2)
                
            
            combate = PrisonersDilemma.Combate(alg1, alg2, self.ruido, self.num_rodadas)
            resultado = combate.jogar()
            
            pontos1, pontos2 = Pontuador.somar_pontos(resultado)
            BancoDados.salvar_resultados(self.session, self.partida_db, vitorias1, vitorias2, alg1, alg2, resultado, pontos1, pontos2)
            vitorias1, vitorias2, status = Pontuador.atualizar_vitorias(pontos1, vitorias1, pontos2, vitorias2)
            
            if status == 0:
                self.juiz.devolver_cartas(alg1, alg2)
                Interface.MatchMessages.empate_rodada(pontos1, alg1, alg2)
            else:
                Interface.MatchMessages.resultado_rodada(self.p1, self.p2, pontos1, pontos2, alg1, alg2)
            
            self.p1.discard_pile.append(alg1)
            self.p2.discard_pile.append(alg2)
            Interface.MatchMessages.placar_atual(self.p1, self.p2, vitorias1, vitorias2)

        self.juiz.declarar_vencedor_final(vitorias1)