from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Contato
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
contato_tag = Tag(name="Contato", description="Adição, visualização e remoção de contato da base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/contato', tags=[contato_tag],
          responses={"200": ContatoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_contato(form: ContatoSchema):
    """Adiciona um novo contato à base de dados

    Retorna uma representação dos contatos.
    """
    contato = Contato(
        nome=form.nome,
        celular=form.celular,
        email=form.email,
        data_nascimento=form.data_nascimento)
    logger.debug(f"Adicionando contato de nome: '{contato.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(contato)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado contato de nome: '{contato.nome}'")
        return apresenta_contato(contato), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Contato de mesmo nome já cadastrado :/"
        logger.warning(f"Erro ao adicionar contato '{contato.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível adicionar esse novo contato :/"
        logger.warning(f"Erro ao adicionar contato '{contato.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/contatos', tags=[contato_tag],
         responses={"200": ListagemContatosSchema, "404": ErrorSchema})
def get_contatos():
    """Faz a busca por todos os contatos cadastrados

    Retorna uma representação da listagem de contatos.
    """
    logger.debug(f"Coletando contatos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    contatos = session.query(Contato).all()

    if not contatos:
        # se não há contatos cadastrados
        return {"contatos": []}, 200
    else:
        logger.debug(f"%d contatos encontrados" % len(contatos))
        # retorna a representação de contato
        print(contatos)
        return apresenta_contatos(contatos), 200


@app.get('/contato', tags=[contato_tag],
         responses={"200": ContatoViewSchema, "404": ErrorSchema})
def get_contato(query: ContatoBuscaSchema):
    """Faz a busca por um contato a partir do seu nome

    Retorna uma representação dos contatos.
    """
    contato_nome = query.nome
    logger.debug(f"Coletando dados sobre contato #{contato_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    contato = session.query(Contato).filter(Contato.nome == contato_nome).first()

    if not contato:
        # se o contato não foi encontrado
        error_msg = "Contato não encontrado :/"
        logger.warning(f"Erro ao buscar contato '{contato_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Contato econtrado: '{contato.nome}'")
        # retorna a representação de contato
        return apresenta_contato(contato), 200


@app.delete('/contato', tags=[contato_tag],
            responses={"200": ContatoDelSchema, "404": ErrorSchema})
def del_contato(query: ContatoBuscaSchema):
    """Deleta um contato a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    contato_nome = unquote(unquote(query.nome))
    print(contato_nome)
    logger.debug(f"Deletando dados sobre o contato #{contato_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Contato).filter(Contato.nome == contato_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Contato deletado #{contato_nome}")
        return {"message": "Contato removido", "id": contato_nome}
    else:
        # se o contato não foi encontrado
        error_msg = "Contato não encontrado :/"
        logger.warning(f"Erro ao deletar contato #'{contato_nome}', {error_msg}")
        return {"message": error_msg}, 404


