import PrisonersDilemma
import database
from interface import obter_escolha_segura

class TorneioManager:
    def __init__(self, db_session, partida_db, p1, p2, ruido, num_rodadas):
        self.session = db_session
        self.partida_db = partida_db
        self.p1 = p1
        self.p2 = p2
        self.ruido = ruido
        self.num_rodadas = num_rodadas

    def executar_torneio(self):
        print("\n" + "="*30 + "\n   INÍCIO DO TORNEIO!\n" + "="*30)
        vitorias1, vitorias2 = 0, 0
        
        while vitorias1 < 3 and vitorias2 < 3:
            # Escolha das Cartas
            if vitorias1 == 2 and vitorias2 == 2:
                alg1 = obter_escolha_segura(self.p1.discard_pile, f"[!] EMPATE 2x2! TUDO OU NADA!\n>>> {self.p1.name}, resgate do descarte:")
                alg2 = obter_escolha_segura(self.p2.discard_pile, f"[!] EMPATE 2x2! TUDO OU NADA!\n>>> {self.p2.name}, resgate do descarte:")
            else:
                alg1 = obter_escolha_segura(self.p1.hand, f">>> BATALHA: {self.p1.name}, escolha sua carta:")
                alg2 = obter_escolha_segura(self.p2.hand, f">>> BATALHA: {self.p2.name}, escolha sua carta:")
            
            combate = PrisonersDilemma.Combate(alg1, alg2, self.ruido, self.num_rodadas)
            resultado = combate.jogar()
            pontos1 = sum(item['j1_pontos'] for item in resultado)
            pontos2 = sum(item['j2_pontos'] for item in resultado)
            
            # Salva no Banco
            nova_serie = database.salvar_serie(
                self.session, self.partida_db.id_partida, vitorias1 + vitorias2 + 1, 
                alg1.id, alg2.id, pontos1, pontos2
            )
            database.salvar_rodadas_em_massa(self.session, nova_serie.id_serie, resultado)
            
            if pontos1 > pontos2:
                vitorias1 += 1
                self.anunciar_turno(self.p1, alg1, pontos1, alg2, pontos2)
            elif pontos2 > pontos1:
                vitorias2 += 1
                self.anunciar_turno(self.p2, alg2, pontos2, alg1, pontos1)
            else:
                print(f"\n-> Empate na série: {pontos1} pontos cada. | {alg1.name} vs {alg2.name}")
                self.p1.hand.append(alg1)
                self.p2.hand.append(alg2)
                
            self.p1.discard_pile.append(alg1)
            self.p2.discard_pile.append(alg2)
            print(f"Placar Atual: {self.p1.name} {vitorias1} x {vitorias2} {self.p2.name}\n")

        self._declarar_vencedor_final(vitorias1)

    def anunciar_turno(self, vencedor, alg_v, pts_v, alg_p, pts_p):
        print(f"\n-> Vitória de {vencedor.name}! ({alg_v.name} - {pts_v} x {pts_p} - {alg_p.name})")

    def _declarar_vencedor_final(self, vitorias1):
        print("\n" + "-"*30)
        # Corrigido o bug onde o id_vencedor era sempre id_p1 no seu código original
        if vitorias1 == 3:
            vencedor, id_vencedor = self.p1.name, self.p1.id_db
        else:
            vencedor, id_vencedor = self.p2.name, self.p2.id_db
            
        print(f"🏆 VENCEDOR: {vencedor.upper()}!")
        database.registrar_vencedor(self.session, self.partida_db, id_vencedor)
        print("-" * 30)