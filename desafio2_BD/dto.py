from dataclasses import dataclass

@dataclass
class CadastroJogadoresDTO:
    nome_j1: str
    nome_j2: str

@dataclass(frozen=True)
class AcaoRodadaDTO:
    num_rodada: int
    j1_escolha_real: str
    j1_escolha_pos_ruido: str
    j1_pontos: int
    j2_escolha_real: str
    j2_escolha_pos_ruido: str
    j2_pontos: int

@dataclass(frozen=True)
class ResumoTurnoDTO:
    num_serie: int
    id_algoritmo_j1: int
    id_algoritmo_j2: int
    vencedor_turno: int