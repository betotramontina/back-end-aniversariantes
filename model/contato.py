# Importa parâmetros, ferramentas e módulos
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

# Importa classe Base
from  model import Base

# Define a classe Contato como uma representação ORM da tabela 'contato'
class Contato(Base):
    __tablename__ = 'contato'

    # Define as colunas da tabela e seus respectivos tipos e propriedades
    id = Column("pk_contato", Integer, primary_key=True)
    nome = Column(String(50), unique=True)
    celular = Column(String(11))
    data_nascimento = Column(String(10))
    data_insercao = Column(DateTime, default=datetime.now())

    
    def __init__(self, nome:str, celular:str, data_nascimento:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Contato
        Arguments:
            nome: nome do contato.
            celular: número do celular (whatsapp) do contato
            data_nascimento: data de nascimento/ aniversário do contato
            data_insercao: data de inserção do contato na base de dados
        """
        self.nome = nome
        self.celular = celular
        self.data_nascimento = data_nascimento

        # Define a data de criação do contato. Se não informada, define como a data exata da inserção no banco de dados
        if data_insercao:
            self.data_insercao = data_insercao


