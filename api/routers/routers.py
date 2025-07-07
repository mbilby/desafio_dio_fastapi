from fastapi import APIRouter
from api.atletas.controller.controller import router as atletas_router
from api.categorias.controller.controller import router as categorias_router
from api.centro_treinamento.controller.controller import router as centro_treinamento_router

api_router = APIRouter()
api_router.include_router(atletas_router, prefix="/v1/atletas", tags=["Atletas"])
api_router.include_router(categorias_router, prefix="/v1/categorias", tags=["Categorias"])
api_router.include_router(centro_treinamento_router, prefix="/v1/centros-treinamento", tags=["Centros de Treinamento"])