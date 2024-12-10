# Importa funções, ferramentas e módulos
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importa os elementos definidos no modelo
from model.base import Base
from model.contato import Contato

# Define o caminho para o diretório do banco de dados
db_path = "database/"
# Verifica se o diretório especificado para o banco de dados não existe
if not os.path.exists(db_path):
   # Cria o diretório do banco de dados, caso ele não exista
   os.makedirs(db_path)

# Define a URL de conexão com o banco de dados (SQLite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria a engine de conexão com o banco de dados
engine = create_engine(db_url, echo=False)

# Instancia um criador de sessões para interagir com o banco de dados
Session = sessionmaker(bind=engine)

# Verifica se o banco de dados não existe
if not database_exists(engine.url):
    # Cria o banco de dados, caso ele ainda não tenha sido criado
    create_database(engine.url) 

# Cria as tabelas no banco de dados com base no modelo, caso ainda não existam
Base.metadata.create_all(engine)
