from pydantic import BaseModel
from typing import Optional, List
from model.contato import Contato


class ContatoSchema(BaseModel):
    """ Define como um novo contato a ser inserido deve ser representado
    """
    nome: str = "Carlos Araujo"
    celular: str = "61990070205"
    email: str = "carlinhos@gmail.com"
    data_nascimento: str = "DD-MM-AAAA" 


class ContatoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do contato.
    """
    nome: str = "Carlos Araujo"


class ListagemContatoSchema(BaseModel):
    """ Define como uma listagem de contatos será retornada.
    """
    contatos:List[ContatoSchema]


def apresenta_contatos(contatos: List[Contato]):
    """ Retorna uma representação do contato seguindo o schema definido em
        ContatoViewSchema.
    """
    result = []
    for contato in contatos:
        result.append({
            "nome": contato.nome,
            "celular": contato.celular,
            "email": contato.email,
            "data_nascimento": contato.data_nascimento,          
        })

    return {"contatos": result}


class ContatoViewSchema(BaseModel):
    """ Define como um contato será retornado: contato.
    """
    id: int = 1
    nome: str = "Carlos Araujo"
    celular: str = "61990070205"
    email: str = "carlinhos@gmail.com"
    data_nascimento: str = "DD-MM-AAAA" 


class ContatoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

def apresenta_contato(contato: Contato):
    """ Retorna uma representação do contato seguindo o schema definido em
        ContatoViewSchema.
    """
    return {
        "id": contato.id,
        "nome": contato.nome,
        "celular": contato.celular,
        "email": contato.email,
        "data_nascimento": contato.data_nascimento,
    }
