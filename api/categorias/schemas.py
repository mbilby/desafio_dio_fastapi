from api.contrib.schemas import BaseSchema
from datetime import datetime
from pydantic import UUID4, Field
from typing import Annotated
from api.contrib.schemas import OutMixin

class Categorias(BaseSchema):
    """
    Schema for the Categorias model.
    """
    nome: Annotated[str, Field(description="Nome da categoria", examples=["Scale"], max_length=10)]

class CategoriaIn(Categorias):
    """
    Schema for creating a new Categoria.
    """
    pass

class CategoriaOut(CategoriaIn, OutMixin):
    """
    Schema for outputting a Categoria.
    """
    id: Annotated[UUID4, Field(description="Identificador de categoria", examples=["123e4567-e89b-12d3-a456-426614174000"])]
    #created_at: Annotated[datetime, Field(description="Data de criação", exemples=["2023-10-01T12:00:00Z"])]