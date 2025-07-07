from typing import List, Optional
from fastapi import APIRouter, Body, Query, HTTPException, status, Depends
from uuid import uuid4
from pydantic import UUID4
from datetime import datetime
from api.contrib.dependencies import DatabaseDependency
from api.atletas.models import AtletaModel  # Assuming this model is defined in models.py
from api.atletas.schemas import AtletaIn, AtletaOut, AtletaUpdate # Assuming this schema is defined in schemas.py
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.categorias.models import CategoriaModel # Assuming this schema is defined in schemas.py
from api.centro_treinamento.models import CentroTreinamentoModel  # Assuming this schema is defined in schemas.py
from api.error.error import HTTPError
from api.error.messages import CPF_DUPLICADO_MSG, CATEGORIA_NAO_ENCONTRADA
from fastapi_pagination import Page, paginate, add_pagination, Params

router = APIRouter()

add_pagination(router)

@router.post("/", 
             summary="Cria um novo atleta",
             response_description="Atleta created successfully",
             response_model=AtletaOut,  # Assuming AtletaIn is the output schema
             status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_409_CONFLICT: {
                 "model": HTTPError,
                 "description": "Error: Conflict",
                 "examples": {
                     "cpf_duplicado" : {
                         "summary" : "CPF Duplicado",
                         "value" : {
                             "detail" : CPF_DUPLICADO_MSG.format(cpf="12345678900")
                         }
                     }
                 }
             },
             })
async def create_atleta(db_session: DatabaseDependency, 
                        atleta_in: AtletaIn = Body(...)) -> AtletaOut:
    """
    Endpoint to create a new atleta.
    """
    categoria_name = atleta_in.categoria
    centro_treinamento_name = atleta_in.centro_treinamento
    
    

    atleta_existe = (await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_in.cpf))).scalars().first()
    
    if atleta_existe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=CPF_DUPLICADO_MSG.format(cpf=atleta_in.cpf))
    
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=CATEGORIA_NAO_ENCONTRADA.format(nome=categoria))
    
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_name))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Centro de treinamento {centro_treinamento_name} não encontrada.")
            
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Erro ao criar o atleta. Verifique os dados informados. {e}")
    return atleta_out


@router.get("/", 
             summary="Consultar todos os atletas",
             status_code=status.HTTP_200_OK,
             response_model=Page[AtletaOut])  # Assuming CategoriaIn is the output schema
async def busca_atletas(db_session: DatabaseDependency,
                        params: Params = Depends()) -> Page[AtletaOut]:
    """
    Endpoint to get a categoria.
    """
    atletas: Page[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()

    retorno = [AtletaOut(
                            id=atleta.id,
                            nome=atleta.nome,
                            cpf=atleta.cpf,
                            idade=atleta.idade,
                            peso=atleta.peso,
                            altura = atleta.altura,
                            sexo=atleta.sexo,
                            categoria=atleta.categoria.nome,
                            centro_treinamento=atleta.centro_treinamento.nome,
                            created_at=atleta.created_at
                        )
                        for atleta in atletas
              ]


    return paginate(retorno, params)

@router.get("/atleta", 
             summary="Consulta atleta pelo cpf ou nome",
             status_code=status.HTTP_200_OK,
             response_model=AtletaOut)  # Assuming CategoriaIn is the output schema
async def busca_atleta_por_nome_ou_cpf(db_session: DatabaseDependency,
                              nome: Optional[str] = Query(None, description="Filtrar atletas pelo nome"),
                              cpf: Optional[str] = Query(None, description="Filtrar atletas pelo cpf")) -> AtletaOut:
    """
    Endpoint para consultar atletas.
    Retorna atletas que possuam o nome OU o CPF idêntico ao informado.
    Pelo menos um dos parâmetros (nome ou cpf) deve ser fornecido.
    """
    # atleta: AtletaOut = (
    #     await db_session.execute(select(AtletaModel).filter_by(id=id))
    #     ).scalars().first()
    # if not atleta:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta com {id} não encontrado.")
    query_conditions = []
    criterios_buscados = [] 

    if not nome and not cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pelo menos um dos parâmetros 'nome' ou 'cpf' deve ser fornecido para a busca."
        )
    if nome:
        query_conditions.append(AtletaModel.nome == nome)
        criterios_buscados.append(f"nome '{nome}'")
    if cpf:    
        query_conditions.append(AtletaModel.cpf == cpf)
        criterios_buscados.append(f"cpf '{cpf}'")

    query = (select(AtletaModel)
             .where(*query_conditions)
             .options(selectinload(AtletaModel.categoria))
             .options(selectinload(AtletaModel.centro_treinamento)))

    
    atleta = (await db_session.execute(query)).scalars().first()

    if not atleta:
        criterios_str = " e ".join(criterios_buscados)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Atleta com {criterios_str} informado não localizado." )
    
    retorno = AtletaOut(
                    id=atleta.id,
                    nome=atleta.nome,
                    cpf=atleta.cpf,
                    idade=atleta.idade,
                    peso=atleta.peso,
                    altura = atleta.altura,
                    sexo=atleta.sexo,
                    categoria=atleta.categoria.nome,
                    centro_treinamento=atleta.centro_treinamento.nome,
                    created_at=atleta.created_at
    )

    #atleta = [AtletaOut.model_validate(atleta) for atleta in atleta_db]

    return retorno
        

@router.patch("/{id}", 
             summary="Editar atleta por ID",
             status_code=status.HTTP_200_OK,
             response_model=AtletaOut)  # Assuming CategoriaIn is the output schema
async def busca_atleta_por_id(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    """
    Endpoint to get a categoria.
    """
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta com {id} não encontrado.")
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    
    await db_session.commit()
    await db_session.refresh(atleta)

    retorno = AtletaOut(
                        id=atleta.id,
                        nome=atleta_up.nome,
                        cpf=atleta.cpf,
                        idade=atleta_up.idade,
                        peso=atleta.peso,
                        altura = atleta.altura,
                        sexo=atleta.sexo,
                        categoria=atleta.categoria.nome,
                        centro_treinamento=atleta.centro_treinamento.nome,
                        created_at=atleta.created_at
                    )
    
    return retorno

@router.delete("/{id}", 
             summary="Consulta atleta por ID",
             status_code=status.HTTP_204_NO_CONTENT,
             response_model=None)  # Assuming CategoriaIn is the output schema
async def deleta_atleta_por_id(id: UUID4, db_session: DatabaseDependency) -> None:
    """
    Endpoint to get a categoria.
    """
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta com {id} não encontrado.")
    
    await db_session.delete(atleta)
    await db_session.commit()
    