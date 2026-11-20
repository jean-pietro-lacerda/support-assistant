TECHNICAL_LEVELS = {
    "leigo": "Utilize linguagem simples e explique termos técnicos quando necessário.",

    "intermediario": "Utilize terminologia técnica moderada, explicando conceitos mais complexos.",

    "avancado": "Utilize terminologia técnica especializada, sem explicações básicas desnecessárias."
}


COMMUNICATION_STYLES = {
    "direto": "Apresente as informações de maneira objetiva, sem detalhes desnecessários.",

    "detalhado": "Apresente informações completas, com explicações e detalhes relevantes.",

    "didatico": "Explique as informações progressivamente, utilizando exemplos quando necessário."
}


CHANNELS = {
    "chat": "Utilize linguagem conversacional e mensagens de fácil leitura.",

    "email": "Organize a comunicação de maneira profissional, estruturada e compreensível.",

    "telefone": "Utilize linguagem natural e instruções que possam ser transmitidas verbalmente."
}


def obter_instrucoes(cliente, versao):

    if versao == "v1":
        return """
INSTRUÇÕES

Adapte a resposta ao nível técnico, estilo de
comunicação e canal de atendimento do cliente.
"""

    if versao == "v2":
        return f"""
INSTRUÇÕES

Nível técnico:
{TECHNICAL_LEVELS[cliente['technical_level']]}

Estilo de comunicação:
{COMMUNICATION_STYLES[cliente['communication_style']]}

Canal de atendimento:
{CHANNELS[cliente['channel']]}
"""