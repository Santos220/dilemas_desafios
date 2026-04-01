import random

class Algoritmo:
    def __init__(self, id, slug, name, behavior_type, description):
        self.id = id
        self.slug = slug
        self.name = name
        self.behavior_type = behavior_type
        self.description = description
        self.pontos = 0
        self.historico_op = []
        
    def pontuar(self, pontos):
        self.pontos += pontos
        
    def registrar_jogada_op(self, acao):
        self.historico_op.append(acao)


class AlwaysDefect(Algoritmo):
    def escolher_acao(self):
        return 'DEFECT'

    
class AlwaysCooperate(Algoritmo):
    def escolher_acao(self):
        return 'COOPERATE'

    
class Random(Algoritmo):
    def escolher_acao(self):
        return random.choice(['COOPERATE', 'DEFECT'])

    
class GrimTrigger(Algoritmo):            
    def escolher_acao(self):
        if 'DEFECT' in self.historico_op:
            return 'DEFECT'
        else:
            return 'COOPERATE'

        
class TitForTat(Algoritmo):
    def escolher_acao(self):
        if not self.historico_op:
            return 'COOPERATE'
        else:
            return self.historico_op[-1]
        

class Combate:
    def __init__(self, jogador1, jogador2):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        
    def executar_rodada(self):
        acao1 = self.jogador1.escolher_acao()
        acao2 = self.jogador2.escolher_acao()
        
        self.jogador1.registrar_jogada_op(acao2)
        self.jogador2.registrar_jogada_op(acao1)
        
        payoff_matrix = {
            ('COOPERATE', 'COOPERATE'): (3, 3),
            ('COOPERATE', 'DEFECT'): (0, 5),
            ('DEFECT', 'COOPERATE'): (5, 0),
            ('DEFECT', 'DEFECT'): (1, 1)
        }
        
        pontos1, pontos2 = payoff_matrix[(acao1, acao2)]
        self.jogador1.pontuar(pontos1)
        self.jogador2.pontuar(pontos2)
        
        
class Tabela:
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.jogadores.sort(key=lambda x: x.pontos, reverse=True)
    def exibir(self):
        print("--- Ranking de Pontuação: ---")
        for jogador in self.jogadores:
            print(f"{jogador.name}: {jogador.pontos} pontos")
        print(f"\nO algoritmo vencedor é '{self.jogadores[0].name}' com {self.jogadores[0].pontos} pontos!\n")
