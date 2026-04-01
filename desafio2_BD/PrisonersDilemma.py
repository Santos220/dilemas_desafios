from tournament_core import GameEngine, Action

class Combate:
    def __init__(self, algortimo1, algortimo2, ruido, num_rodadas):
        self.algortimo1 = algortimo1
        self.algortimo2 = algortimo2
        self.ruido = ruido
        self.num_rodadas = num_rodadas
        self.dados_rodada = []
    
    def jogar(self):   
        hist1 = []
        hist2 = []
        pontos1 = 0
        pontos2 = 0
        
        for rodada in range(self.num_rodadas):
            acao1 = self.algortimo1.play(hist1, hist2)
            acao2 = self.algortimo2.play(hist2, hist1)
            
            acao1_ruidosa = GameEngine.apply_noise(acao1, self.ruido)
            acao2_ruidosa = GameEngine.apply_noise(acao2, self.ruido)
            
            hist1.append(acao1_ruidosa)
            hist2.append(acao2_ruidosa)
            
            payoff_matrix = {
                (Action.COOPERATE, Action.COOPERATE): (3, 3),
                (Action.COOPERATE, Action.DEFECT): (0, 5),
                (Action.DEFECT, Action.COOPERATE): (5, 0),
                (Action.DEFECT, Action.DEFECT): (1, 1)
            }
            
            pontos_rodada1, pontos_rodada2 = payoff_matrix[(acao1_ruidosa, acao2_ruidosa)]
            pontos1 += pontos_rodada1
            pontos2 += pontos_rodada2
            
            registro = {
                "num_rodada": rodada + 1,
                "j1_escolha_real": acao1.value,
                "j1_escolha_pos_ruido": acao1_ruidosa.value,
                "j1_pontos": pontos_rodada1,
                "j2_escolha_real": acao2.value,
                "j2_escolha_pos_ruido": acao2_ruidosa.value,
                "j2_pontos": pontos_rodada2
            }
            
            self.dados_rodada.append(registro)
            
        return self.dados_rodada