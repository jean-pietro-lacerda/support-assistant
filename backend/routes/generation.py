from threading import Lock
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.routes.customers import carregar_clientes
from services.generation import gerar_resposta

router = APIRouter()
generation_lock = Lock()


class GenerateRequest(BaseModel):
    customer_id: str
    ticket: str = Field(min_length=1)
    # Literal é usado para restringir os valores possíveis de um campo a um conjunto específico de strings.
    content_type: Literal["diagnosis", "resolution", "clarification", "flowchart"]
    prompt_version: Literal["v1", "v2"]


# Criação da rota
@router.post("/generate")
def generate(request: GenerateRequest):
    clientes = carregar_clientes()

    cliente = next(
        (item for item in clientes if item["customer_id"] == request.customer_id),
        None
    )

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    if not request.ticket.strip():
        raise HTTPException(status_code=422, detail="O ticket não pode estar vazio.")

    with generation_lock:
        try:
            resposta = gerar_resposta(
                cliente,
                request.ticket,
                request.content_type,
                request.prompt_version
            )
        except ValueError as erro:
            raise HTTPException(status_code=422, detail=str(erro))

    return resposta