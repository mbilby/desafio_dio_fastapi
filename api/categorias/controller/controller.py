from fastapi import APIRouter, HTTPException, Body, status
from uuid import uuid4
from typing import List
from api.contrib.dependencies import DatabaseDependency
from api.categorias.models import CategoriaModel  # Assuming this model is defined in models.py
from api.categorias.schemas import CategoriaIn, CategoriaOut  # Assuming this schema is defined in schemas.py
from sqlalchemy.future import select
from pydantic import UUID4

router = APIRouter()

@router.post("/", 
             summary="Cria uma nova categoria",
             response_description="Categoria created successfully",
             status_code=status.HTTP_201_CREATED,
             response_model=CategoriaOut)  # Assuming CategoriaIn is the output schema
async def create_categoria(db_session: DatabaseDependency, 
                        categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    """
    Endpoint to create a new atleta.
    """
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()
    breakpoint  # Debugging breakpoint
    return categoria_out
 
@router.get("/", 
             summary="Consultar todas as categorias",
             status_code=status.HTTP_200_OK,
             response_model=List[CategoriaOut])  # Assuming CategoriaIn is the output schema
async def busca_categorias(db_session: DatabaseDependency) -> List[CategoriaOut]:
    """
    Endpoint to get a categoria.
    """
    categorias: List[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()

    return categorias

@router.get("/{id}", 
             summary="Consulta categoria por ID",
             status_code=status.HTTP_200_OK,
             response_model=CategoriaOut)  # Assuming CategoriaIn is the output schema
async def busca_categoria_por_id(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    """
    Endpoint to get a categoria.
    """
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
        ).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id {id}")
    
    return categoria
