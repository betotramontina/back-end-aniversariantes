from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Contato(Base):
    __tablename__ = 'contato'

    id = Column("pk_contato", Integer, primary_key=True)
    nome = Column(String(50), unique=True)
    celular = Column(String(11))
    email = Column(String(50))
    data_nascimento = Column(String(10))
    data_insercao = Column(DateTime, default=datetime.now())

    
    def __init__(self, nome:str, celular:str, email:str, data_nascimento:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Contato

        Arguments:
            nome: nome do contato.
            celular: número do celular do contato
            email: email do contato
            data_nascimento: data de nascimento/ aniversário do contato
            data_insercao: data de inserção do contato na base de dados
        """
        self.nome = nome
        self.celular = celular
        self.email = email
        self.data_nascimento = data_nascimento

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao


