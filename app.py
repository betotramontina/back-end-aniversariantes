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


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Produto removido", "id": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id  = form.produto_id
    logger.debug(f"Adicionando comentários ao produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao produto
    produto.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{produto_id}")

    # retorna a representação de produto
    return apresenta_produto(produto), 200
