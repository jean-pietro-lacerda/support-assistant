import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

from psycopg.types.json import Jsonb

from services.database import conectar

# Agora a validação se ta em cache é feita por um Banco de Dados PostgreSQL

VALIDATION_VERSION = 2

def identificar_prompt(mensagens):
    configuracao = {
        "messages": mensagens,
        "validation_version": VALIDATION_VERSION
    }

    texto = json.dumps(configuracao, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def salvar_execucao(cliente, ticket, tipo, versao, output, modelo, temperatura, mensagens):
    registro_id = uuid4()

    registro = {
        "id": str(registro_id),
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
        "validation_version": VALIDATION_VERSION
    }

    with conectar() as conexao:
        conexao.execute(
            """
            INSERT INTO executions (
                id,
                prompt_hash,
                provider,
                model,
                temperature,
                validation_version,
                record
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                registro_id,
                registro["prompt_hash"],
                registro["provider"],
                modelo,
                temperatura,
                VALIDATION_VERSION,
                Jsonb(registro)
            )
        )

    return registro


def buscar_cache(mensagens, modelo, temperatura):
    chave = identificar_prompt(mensagens)

    with conectar() as conexao:
        resultado = conexao.execute(
            """
            SELECT record
            FROM executions
            WHERE prompt_hash = %s
              AND validation_version = %s
              AND model = %s
              AND provider = %s
              AND temperature = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (
                chave,
                VALIDATION_VERSION,
                modelo,
                "groq",
                temperatura
            )
        ).fetchone()

    if resultado is None:
        return None

    return resultado[0]["output"]