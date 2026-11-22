import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Minha Avaliação"])

ROOT = Path(__file__).resolve().parents[2]
NOTES_PATH = ROOT / "PROMPT_ENGINEERING_NOTES.md"
HISTORY_PATH = ROOT / "data" / "history.json"

#Criando a rota para consultar a avaliação obrigatoria do Desafio
@router.get("/evaluation")
def consultar_avaliacao():
    if not NOTES_PATH.exists() or not HISTORY_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Documentação ou histórico não encontrado."
        )

    with open(NOTES_PATH, encoding="utf-8") as arquivo:
        notas = arquivo.read()

    with open(HISTORY_PATH, encoding="utf-8") as arquivo:
        historico = json.load(arquivo)

    avaliacoes = [
        registro
        for registro in historico
        if registro.get("evaluation") is not None
    ]

    return {
        "notes_markdown": notas,
        "history_cli": avaliacoes
    }