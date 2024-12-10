from pydantic import BaseModel
from typing import Optional, List
from model.contato import Contato

# Define como um novo contato deve ser representado ao ser inserido.
class ContatoSchema(BaseModel):
    nome: str = "Carlos Araujo"
    celular: str = "61990070205"
    data_nascimento: str = "DD-MM-AAAA" 

# Define a estrutura da busca de um contato, que será realizada apenas com base no nome.
 class ContatoBuscaSchema(BaseModel):
     nome: str = "Carlos Araujo"

# Define como uma lista de contatos será retornada na resposta da API.
class ListagemContatosSchema(BaseModel):
    contatos:List[ContatoSchema]

# Converte uma lista de objetos do modelo Contato para uma estrutura de dicionário que segue o formato definido pelo esquema ListagemContatosSchema.
def apresenta_contatos(contatos: List[Contato]):
    result = []
    for contato in contatos:
        result.append({
            "nome": contato.nome,
            "celular": contato.celular,
            "data_nascimento": contato.data_nascimento,          
        })

    return {"contatos": result}

# Define como os detalhes de um contato específico serão retornados na API.
class ContatoViewSchema(BaseModel):
    id: int = 1
    nome: str = "Carlos Araujo"
    celular: str = "61990070205"
    data_nascimento: str = "DD-MM-AAAA" 

# Define a estrutura do dado retornado após a remoção de um contato.
class ContatoDelSchema(BaseModel):
    message: str
    nome: str

# Converte um objeto do modelo Contato para uma representação compatível com o esquema definido em ContatoViewSchema.
def apresenta_contato(contato: Contato):
    return {
        "id": contato.id,
        "nome": contato.nome,
        "celular": contato.celular,
        "data_nascimento": contato.data_nascimento,
    }
