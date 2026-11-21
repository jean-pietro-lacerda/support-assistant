import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
import hashlib


HISTORY_PATH = Path(__file__).resolve().parent.parent / "data" / "history.json"
VALIDATION_VERSION = 2


def identificar_prompt(mensagens):
    configuracao = {"messages": mensagens, "validation_version": VALIDATION_VERSION}
    texto = json.dumps(configuracao, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def salvar_execucao(cliente, ticket, tipo, versao, output, modelo, temperatura, mensagens):

    registro = {
        "id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "customer_id": cliente["customer_id"],
        "customer_profile": cliente,
        "ticket": ticket,
        "prompt_version": versao,
        "content_type": tipo,
        "provider": "groq",
        "model": modelo,
        "settings": {"temperature": temperatura},
        "output": output,
        "evaluation": None,
        "prompt_hash": identificar_prompt(mensagens),
        "messages": mensagens,
        "validation_version": VALIDATION_VERSION,
    }

    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, encoding="utf-8") as arquivo:
            historico = json.load(arquivo)
    else:
        historico = []

    historico.append(registro)

    with open(HISTORY_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)

    return registro

def buscar_cache(mensagens, modelo, temperatura):

    if not HISTORY_PATH.exists():
        return None

    with open(HISTORY_PATH, encoding="utf-8") as arquivo:
        historico = json.load(arquivo)

    chave = identificar_prompt(mensagens)

    for registro in reversed(historico):
        if (
            registro.get("prompt_hash") == chave
            and registro.get("validation_version") == VALIDATION_VERSION
            and registro.get("model") == modelo
            and registro.get("provider") == "groq"
            and registro.get("settings", {}).get("temperature") == temperatura
        ):
            return registro["output"]

    return None
