from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Algoritmo(Base):
    __tablename__ = 'algoritmo'
    id_algoritmo = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)

class Jogador(Base):
    __tablename__ = 'jogador'
    id_jogador = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)

class Partida(Base):
    __tablename__ = 'partida'
    id_partida = Column(Integer, primary_key=True)
    id_jogador1 = Column(Integer, ForeignKey('jogador.id_jogador'))
    id_jogador2 = Column(Integer, ForeignKey('jogador.id_jogador'))
    ruido_sorteado = Column(Numeric(5, 2))
    id_vencedor = Column(Integer, ForeignKey('jogador.id_jogador'), nullable=True)

class Serie(Base):
    __tablename__ = 'serie'
    id_serie = Column(Integer, primary_key=True)
    id_partida = Column(Integer, ForeignKey('partida.id_partida'))
    num_serie = Column(Integer)
    id_algoritmo_j1 = Column(Integer, ForeignKey('algoritmo.id_algoritmo'))
    id_algoritmo_j2 = Column(Integer, ForeignKey('algoritmo.id_algoritmo'))
    pontos_j1 = Column(Integer)
    pontos_j2 = Column(Integer)

class Rodada(Base):
    __tablename__ = 'rodada'
    id_rodada = Column(Integer, primary_key=True)
    id_serie = Column(Integer, ForeignKey('serie.id_serie'))
    num_rodada = Column(Integer)
    j1_escolha_real = Column(String(1))
    j1_escolha_pos_ruido = Column(String(1), nullable=True)
    j1_pontos = Column(Integer)
    j2_escolha_real = Column(String(1))
    j2_escolha_pos_ruido = Column(String(1), nullable=True)
    j2_pontos = Column(Integer)