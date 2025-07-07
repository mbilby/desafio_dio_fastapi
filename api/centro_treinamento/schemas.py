from api.contrib.schemas import BaseSchema
from pydantic import Field, UUID4
from typing import Annotated

class CentroTreinamento(BaseSchema):
    """
    Schema for the Categorias model.
    """
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="CT King", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example="Rua das Flores, 123", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="João Silva", max_length=30)]


class CentroTreinamentoIn(CentroTreinamento):
    """
    Schema for creating a new Categoria.
    """
    pass

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]

class CentroTreinamentoOut(CentroTreinamento, BaseSchema):
    """
    Schema for outputting a Categoria.
    """
    id: Annotated[UUID4, Field(description="Identificador de centro de treinamento", example="123e4567-e89b-12d3-a456-426614174000")]
    # created_at: Annotated[datetime, Field(description="Data de criação", examples=["2023-10-01T12:00:00Z"])]