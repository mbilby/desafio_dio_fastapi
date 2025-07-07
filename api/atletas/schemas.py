from pydantic import Field, PositiveFloat, UUID4
from api.contrib.schemas import BaseSchema
from api.contrib.schemas import OutMixin
from typing import Annotated, Optional
from datetime import datetime

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", examples=["João", "Maria"], max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", examples=["12345678900"], max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", examples=[70.5])]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", examples=[1.75])]
    sexo: Annotated[str, Field(description="Sexo do atleta", examples=["M", "F"], max_length=1)]
    categoria: Annotated[str, Field(alias="categoria", description="Categoria do atleta", examples=["Scale"])]
    centro_treinamento: Annotated[str, Field(alias="centro_treinamento",description="Centro de treinamento do atleta", examples=["CT King"])]                    

class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    id: Annotated[UUID4, Field(description="Identificador do Atleta", examples=["123e4567-e89b-12d3-a456-426614174000"])]
    nome: Annotated[str, Field(description="Nome do atleta", examples=["João", "Maria"], max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", examples=["12345678900"], max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", examples=[70.5])]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", examples=[1.75])]
    sexo: Annotated[str, Field(description="Sexo do atleta", examples=["M", "F"], max_length=1)]
    categoria: Annotated[str, Field(alias="categoria", description="Categoria do atleta", examples=["Scale"])]
    centro_treinamento: Annotated[str, Field(alias="centro_treinamento",description="Centro de treinamento do atleta", examples=["CT King"])] 
    created_at: Annotated[datetime, Field(description="Data da criação do atleta")]

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]

class AtletaOutParams(BaseSchema):

    page: int = Field(0, ge=0, description="Page number (0-indexed).")
    size: int = Field(50, ge=1, le=100, description="Number of items per page (max 100).")