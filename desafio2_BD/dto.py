from dataclasses import dataclass
from typing import List

# Imutáveis e Pequenos

@dataclass
class CadastroJogadoresDTO:
    nome_j1: str
    nome_j2: str

@dataclass
class EscolhaCarta:
    nome_jogador: str
    cartas: List[str]