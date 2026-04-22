from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Jogador, Partida, Rodada, Serie
from typing import List
from dataclasses import asdict
from dto import ResumoTurnoDTO, AcaoRodadaDTO

DATABASE_URL = "postgresql://admin:senha123@localhost:5433/torneio_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def iniciar_banco():
    Base.metadata.create_all(bind=engine)
    print("Banco de dados sincronizado!")

def obter_ou_criar_jogador(session, nome_jogador):
    jogador = session.query(Jogador).filter_by(nome=nome_jogador).first()
    
    if not jogador:
        jogador = Jogador(nome=nome_jogador)
        session.add(jogador)
        session.commit()
        session.refresh(jogador)
        
    return jogador.id_jogador

def salvar_rodadas_em_massa(session, id_serie, lista_resultados):
    rodadas_orm = []
    
    for reg in lista_resultados:
        rodada_obj = Rodada(
            id_serie=id_serie,
            num_rodada=reg['num_rodada'],
            j1_escolha_real=reg['j1_escolha_real'],
            j1_escolha_pos_ruido=reg['j1_escolha_pos_ruido'],
            j1_pontos=reg['j1_pontos'],
            j2_escolha_real=reg['j2_escolha_real'],
            j2_escolha_pos_ruido=reg['j2_escolha_pos_ruido'],
            j2_pontos=reg['j2_pontos']
        )
        rodadas_orm.append(rodada_obj)
        
    session.add_all(rodadas_orm)
    session.commit()

def criar_partida(session, id_p1, id_p2, ruido):
    nova_partida = Partida(
        id_jogador1=id_p1, id_jogador2=id_p2, 
        ruido_sorteado=ruido, id_vencedor=None
    )
    session.add(nova_partida)
    session.commit()
    return nova_partida

def salvar_serie(session, id_partida, num_serie, alg1_id, alg2_id, pts1, pts2):
    nova_serie = Serie(
        id_partida=id_partida, num_serie=num_serie,
        id_algoritmo_j1=alg1_id, id_algoritmo_j2=alg2_id,
        pontos_j1=pts1, pontos_j2=pts2
    )
    session.add(nova_serie)
    session.commit()
    return nova_serie

def registrar_vencedor(session, partida, id_vencedor):
    partida.id_vencedor = id_vencedor
    session.commit()


class DatabaseRepository:
    def __init__(self, session):
        self.session = session

    def salvar_resultado_turno(self, id_partida: int, resumo_dto: ResumoTurnoDTO, rodadas_dto: List[AcaoRodadaDTO]):
        pts1 = sum(r.j1_pontos for r in rodadas_dto)
        pts2 = sum(r.j2_pontos for r in rodadas_dto)

        nova_serie = salvar_serie(
            self.session, id_partida, resumo_dto.num_serie, 
            resumo_dto.id_algoritmo_j1, resumo_dto.id_algoritmo_j2, pts1, pts2
        )

        lista_dicts = [asdict(r) for r in rodadas_dto]
        salvar_rodadas_em_massa(self.session, nova_serie.id_serie, lista_dicts)

    def registrar_vencedor_partida(self, id_partida: int, id_vencedor: int):
        partida = self.session.query(Partida).get(id_partida)
        if partida:
            registrar_vencedor(self.session, partida, id_vencedor)