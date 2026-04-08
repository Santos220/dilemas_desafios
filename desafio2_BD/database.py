from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Jogador, Partida, Rodada, Serie

DATABASE_URL = "postgresql://admin:senha123@localhost:5433/torneio_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def iniciar_banco():
    """Cria todas as tabelas no banco de dados se elas não existirem."""
    Base.metadata.create_all(bind=engine)
    print("Banco de dados sincronizado!")

def obter_ou_criar_jogador(session, nome_jogador):
    """Busca o jogador pelo nome. Se não achar, cria e já devolve com o ID."""
    jogador = session.query(Jogador).filter_by(nome=nome_jogador).first()
    
    if not jogador:
        jogador = Jogador(nome=nome_jogador)
        session.add(jogador)
        session.commit()
        session.refresh(jogador)
        print(f"Novo jogador '{nome_jogador}' cadastrado com ID: {jogador.id_jogador}")
        
    return jogador.id_jogador

def salvar_rodadas_em_massa(session, id_serie, lista_resultados):
    """Recebe a lista de dicionários do Combate e salva tudo via ORM"""
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
    
# ---

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
    print("Vencedor registrado com sucesso no banco de dados!")