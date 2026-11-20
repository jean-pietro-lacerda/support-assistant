import json

FORMATS = {
    "diagnosis": {
        "hypotheses": [],
        "evidence": [],
        "missing_information": [],
        "conclusion": ""
    },

    "resolution": {
        "title": "",
        "steps": [],
        "additional_guidance": ""
    },

    "clarification": {
        "questions": []
    },

    "flowchart": {
        "format": "",
        "flow": ""
    }
}


CHANNEL_FORMATS = {
    "chat": """
Organize as informações em mensagens conversacionais,
parágrafos curtos e tópicos de fácil leitura.
""",

    "email": """
Organize as informações em seções, utilizando saudação
e encerramento quando apropriado.
""",

    "telefone": """
Organize as informações como um roteiro de atendimento,
utilizando linguagem oral e orientações sequenciais.
Para o resumo do fluxo, prefira uma descrição estruturada
de decisão em vez de fluxograma ASCII.
"""
}


def obter_formato(tipo, cliente, versao):

    schema = json.dumps(
        FORMATS[tipo],
        indent=4,
        ensure_ascii=False
    )

    formato_base = f"""
FORMATO DE SAÍDA

Retorne exclusivamente um JSON válido seguindo
a estrutura abaixo:

{schema}

Não adicione campos extras.
Não inclua textos fora do JSON.
Não utilize blocos de código Markdown.
Gere somente o tipo de conteúdo solicitado.
Preencha os campos de acordo com suas finalidades.
"""

    if versao == "v1":
        return formato_base + """
Adapte a apresentação ao canal de atendimento do cliente.
"""

    if versao == "v2":
        return formato_base + CHANNEL_FORMATS[cliente["channel"]]