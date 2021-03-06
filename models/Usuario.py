from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.orm import relationship

import config
from database.database import Base, engine, metadata


class Usuario(Base):
    __tablename__ = 'usuario'
    metadata

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    email = Column(String(100))
    senha = Column(String(200))
    tarefas = relationship('Tarefa')


if not inspect(engine).has_table('usuario', schema=config.MYSQL_DATABASE):
    Usuario.__table__.create(engine)
