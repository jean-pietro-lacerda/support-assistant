import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()

CUSTOMERS_PATH = Path(__file__).resolve().parents[2] / "data" / "customers.json"


def carregar_clientes():
    # r = read , ler
    with open(CUSTOMERS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# Criação da rota para listar clientes
@router.get("/customers")
def listar_clientes():
    return carregar_clientes()