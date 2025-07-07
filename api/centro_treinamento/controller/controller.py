from fastapi import APIRouter, Body, status
from uuid import uuid4
from typing import List
from api.contrib.dependencies import DatabaseDependency
from api.centro_treinamento.models import CentroTreinamentoModel  # Assuming this model is defined in models.py
from api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut  # Assuming this schema is defined in schemas.py
from sqlalchemy.future import select
from pydantic import UUID4

router = APIRouter()

@router.post("/", 
             summary="Cria um novo centro de treinamento",
             response_description="Centro de treinamento created successfully",
             status_code=status.HTTP_201_CREATED,
             response_model=CentroTreinamentoOut)  # Assuming CategoriaIn is the output schema
async def create_centro_treinamento(db_session: DatabaseDependency, 
                        centro_treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    """
    Endpoint to create a new atleta.
    """
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()
    breakpoint  # Debugging breakpoint
    return centro_treinamento_model
 
@router.get("/", 
             summary="Consultar todos os centros de treinamento",
             status_code=status.HTTP_200_OK,
             response_model=List[CentroTreinamentoOut])  # Assuming CategoriaIn is the output schema
async def busca_centro_treinamento(db_session: DatabaseDependency) -> List[CentroTreinamentoOut]:
    """
    Endpoint to get a categoria.
    """
    centros_treinamento: List[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()

    return centros_treinamento

@router.get("/{id}", 
             summary="Consulta centro de treinamento por ID",
             status_code=status.HTTP_200_OK,
             response_model=CentroTreinamentoOut)  # Assuming CentroTreinamentoIn is the output schema
async def busca_centro_treinamento_por_id(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    """
    Endpoint to get a categoria.
    """
    centro_treinamento: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
        ).scalars().first()
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrada no id {id}")
    
    return centro_treinamento
