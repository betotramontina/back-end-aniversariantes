from pydantic import BaseModel
from typing import Optional, List
from model.contato import Contato

class ContatoSchema(BaseModel):
    """ Define como um novo contato deve ser representado ao ser inserido.
    """
    nome: str = "Carlos Araujo"
    celular: str = "61990070205"
    data_nascimento: str = "DD-MM-AAAA" 

 class ContatoBuscaSchema(BaseModel):
     """ Define a estrutura da busca de um contato, que será realizada apenas com base no nome.
     """
     nome: str = "Carlos Araujo"

class ListagemContatosSchema(BaseModel):
    """ Define como uma lista de contatos será retornada na resposta da API.
    """
    contatos:List[ContatoSchema]

def apresenta_contatos(contatos: List[Contato]):
    """ Converte uma lista de objetos do modelo Contato para uma estrutura de dicionário que segue o formato definido pelo esquema ListagemContatosSchema.
    """
    result = []
    for contato in contatos:
        result.append({
            "nome": contato.nome,
            "celular": contato.celular,
            "data_nascimento": contato.data_nascimento,          
        })

    return {"contatos": result}

class ContatoViewSchema(BaseModel):
""" Define como os detalhes de um contato específico serão retornados na API.
"""
    id: int = 1
    nome: str = "Carlos Araujo"
    celular: str = "61990070205"
    data_nascimento: str = "DD-MM-AAAA" 

class ContatoDelSchema(BaseModel):
""" Define a estrutura do dado retornado após a remoção de um contato.
"""
    message: str
    nome: str

def apresenta_contato(contato: Contato):
""" Converte um objeto do modelo Contato para uma representação compatível com o esquema definido em ContatoViewSchema.
"""
    return {
        "id": contato.id,
        "nome": contato.nome,
        "celular": contato.celular,
        "data_nascimento": contato.data_nascimento,
    }
