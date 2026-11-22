import json

from services.llm import chamar_llm, MODEL, TEMPERATURE
from services.prompt_engine import montar_prompt
from services.storage import buscar_cache, salvar_execucao
from prompts.formats import FORMATS


def validar_resposta(output, tipo):
    schema = FORMATS[tipo]

    if (
        not isinstance(output, dict)
        or set(output) != set(schema)
        or any(
            not isinstance(output[campo], type(valor))
            for campo, valor in schema.items()
        )
    ):
        raise ValueError("Estrutura JSON inválida.")

    for campo, valor in output.items():
        if isinstance(valor, list) and any(not isinstance(item, str) for item in valor):
            raise ValueError(f"O campo {campo} deve conter somente textos.")

        textos = valor if isinstance(valor, list) else [valor]

        if not textos or any(not texto.strip() for texto in textos):
            raise ValueError(f"O campo obrigatório {campo} está vazio.")

    if tipo == "flowchart":
        if output["format"] != "decision_tree":
            raise ValueError("O formato do fluxo deve ser decision_tree.")

        if "\\n" in output["flow"]:
            raise ValueError("O fluxo contém escapes de linha duplicados (\\n literal).")


def gerar_resposta(cliente, ticket, tipo, versao):
    mensagens = montar_prompt(cliente, ticket, tipo, versao)

    output = buscar_cache(mensagens, MODEL, TEMPERATURE)
    resposta_nova = output is None

    if resposta_nova:
        resposta = chamar_llm(mensagens)

        try:
            output = json.loads(resposta)
        except (json.JSONDecodeError, TypeError) as erro:
            raise ValueError("A LLM não retornou um JSON válido.") from erro

    validar_resposta(output, tipo)

    if resposta_nova:
        salvar_execucao(
            cliente, ticket, tipo, versao,
            output, MODEL, TEMPERATURE, mensagens
        )

    return output