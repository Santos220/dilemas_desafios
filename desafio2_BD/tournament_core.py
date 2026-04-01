import random
import uuid
from enum import Enum
from typing import List

class Action(Enum):
    COOPERATE = "C"
    DEFECT = "D"

class GameEngine:
    @staticmethod
    def coin_toss() -> str:
        return random.choice(["Player 1", "Player 2"])

    # Nível de ruído entre 5% e 15%
    @staticmethod
    def generate_noise_level() -> float:
        return round(random.uniform(0.05, 0.15), 3)

    @staticmethod
    def generate_rounds_count() -> int:
        return random.choice(range(50, 450, 50))

    # Aplicação do Ruído
    @staticmethod
    def apply_noise(intended_action: Action, noise_level: float) -> Action:
        if random.random() < noise_level:
        
            return Action.DEFECT if intended_action == Action.COOPERATE else Action.COOPERATE
        return intended_action

class Player:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.hand = []         
        self.discard_pile = [] 
        self.wins = 0          

    def reset_for_new_match(self):
        self.hand = []
        self.discard_pile = []
        self.wins = 0

class Strategy:
    name = "Base Strategy"
    
    def play(self, my_history: List[Action], opp_history: List[Action]) -> Action:
        raise NotImplementedError("Toda estratégia deve implementar o método play.")

class AlwaysCooperate(Strategy):
    name = "Always Cooperate"
    def play(self, my_history, opp_history):
        return Action.COOPERATE

class AlwaysDefect(Strategy):
    name = "Always Defect"
    def play(self, my_history, opp_history):
        return Action.DEFECT

class RandomChoice(Strategy):
    name = "Random Choice"
    def play(self, my_history, opp_history):
        return random.choice([Action.COOPERATE, Action.DEFECT])

class TitForTat(Strategy):
    name = "Tit For Tat"
    def play(self, my_history, opp_history):
    
        if not opp_history:
            return Action.COOPERATE
        return opp_history[-1]

class GrimTrigger(Strategy):
    name = "Grim Trigger"
    def play(self, my_history, opp_history):
    
        if Action.DEFECT in opp_history:
            return Action.DEFECT
        return Action.COOPERATE

class SuspiciousTitForTat(Strategy):
    name = "Suspicious Tit For Tat"
    def play(self, my_history, opp_history):
    
        if not opp_history:
            return Action.DEFECT
        return opp_history[-1]

class Pavlov(Strategy):
    name = "Pavlov (Win-Stay, Lose-Shift)"
    def play(self, my_history, opp_history):
    
        if not my_history or not opp_history:
            return Action.COOPERATE
        if my_history[-1] == opp_history[-1]:
            return Action.COOPERATE
        return Action.DEFECT

class TitForTwoTats(Strategy):
    name = "Tit For Two Tats"
    def play(self, my_history, opp_history):
    
        if len(opp_history) < 2:
            return Action.COOPERATE
        if opp_history[-1] == Action.DEFECT and opp_history[-2] == Action.DEFECT:
            return Action.DEFECT
        return Action.COOPERATE

class HardMajority(Strategy):
    name = "Hard Majority"
    def play(self, my_history, opp_history):
    
        if not opp_history:
            return Action.COOPERATE
        defects = opp_history.count(Action.DEFECT)
        if defects > len(opp_history) / 2:
            return Action.DEFECT
        return Action.COOPERATE

class Alternator(Strategy):
    name = "Alternator"
    def play(self, my_history, opp_history):
    
        if len(my_history) % 2 == 0:
            return Action.COOPERATE
        return Action.DEFECT

AVAILABLE_ALGORITHMS = [
    AlwaysCooperate, AlwaysDefect, RandomChoice, TitForTat, GrimTrigger,
    SuspiciousTitForTat, Pavlov, TitForTwoTats, HardMajority, Alternator
]

class Combate:
    def __init__(self, algortimo1, algortimo2, ruido, num_rodadas):
        self.algortimo1 = algortimo1
        self.algortimo2 = algortimo2
        self.ruido = ruido
        self.num_rodadas = num_rodadas
        self.dados_rodada = {}
    
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