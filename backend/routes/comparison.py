from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.routes.customers import carregar_clientes
from backend.routes.generation import generation_lock
from services.generation import gerar_resposta

router = APIRouter()


class CompareRequest(BaseModel):
    customer_id: str
    ticket: str = Field(min_length=1)
    content_type: Literal["diagnosis", "resolution", "clarification", "flowchart"]

# Criação da rota para comparar respostas
@router.post("/compare")
def compare(request: CompareRequest):
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
            resposta_v1 = gerar_resposta(
                cliente, request.ticket, request.content_type, "v1"
            )

            resposta_v2 = gerar_resposta(
                cliente, request.ticket, request.content_type, "v2"
            )

        except ValueError as erro:
            raise HTTPException(status_code=502, detail=str(erro))

    # Retorna as respostas de ambas as versões pra comparação
    return {
        "v1": resposta_v1,
        "v2": resposta_v2
    }