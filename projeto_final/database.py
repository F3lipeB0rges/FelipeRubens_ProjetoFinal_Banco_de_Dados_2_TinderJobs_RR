from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Dev(Base):
    __tablename__ = 'devs'
    name = Column(String, primary_key=True)
    email = Column(String)
    cel = Column(String)
    habilidades = Column(String)
    password = Column(String)

class Empresa(Base):
    __tablename__ = 'empresas'
    name = Column(String, primary_key=True)
    email = Column(String)
    cel = Column(String)
    habilidades = Column(String)
    password = Column(String)

# Configurando o banco de dados
engine = create_engine('sqlite:///projeto_final.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
