from pydantic import BaseModel

# Define como uma mensagem de erro será representada.
class ErrorSchema(BaseModel):
    message: str
