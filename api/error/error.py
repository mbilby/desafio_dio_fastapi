from pydantic import BaseModel, Field
from api.error.messages import CPF_DUPLICADO_MSG

class HTTPError(BaseModel):
    """
    Schema padrão para o corpo das respostas de erro do FastAPI.
    """
    detail: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "example": {
                        "detail": CPF_DUPLICADO_MSG.format(cpf="12345678900")
            }
        }
    }