class Juiz:
    @staticmethod
    def devolver_cartas(p1, p2, alg1, alg2):
        p1.hand.append(alg1)
        p2.hand.append(alg2)

    @staticmethod
    def declarar_vencedor_final(vitorias1, p1, p2):
        if vitorias1 == 3:
            vencedor_nome, id_vencedor = p1.name, p1.id_db
            return vencedor_nome, id_vencedor
        else:
            vencedor_nome, id_vencedor = p2.name, p2.id_db
            return vencedor_nome, id_vencedor
        
    @staticmethod
    def empate(vitorias1, vitorias2):
        return vitorias1 == 2 and vitorias2 == 2

    @staticmethod
    def vitoria(vitorias1, vitorias2):
        return vitorias1 == 3 or vitorias2 == 3


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
