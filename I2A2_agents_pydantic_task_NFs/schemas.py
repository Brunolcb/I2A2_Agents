from pydantic import BaseModel

class Pergunta(BaseModel):
    pergunta: str

class Resposta(BaseModel):
    resposta: str
