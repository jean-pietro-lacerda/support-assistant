TECHNICAL_LEVELS = {
    "leigo": """
Utilize palavras simples e familiares.
Evite siglas, jargões e conceitos técnicos desnecessários.
Quando um termo técnico for indispensável, explique
imediatamente seu significado em linguagem simples.
Não pressuponha conhecimentos técnicos do cliente.
""",

    "intermediario": """
Utilize terminologia técnica moderada.
Explique conceitos mais complexos quando necessário.
""",

    "avancado": """
Utilize terminologia técnica especializada e precisa,
sem explicações básicas desnecessárias.
Conhecimento avançado não implica ser desenvolvedor ou administrador,
nem ter acesso ao código-fonte ou permissões especiais.
"""
}


COMMUNICATION_STYLES = {
    "direto": """
Apresente as informações de maneira objetiva,
sem repetições ou detalhes desnecessários.
""",

    "detalhado": """
Apresente informações completas e relevantes,
sem acrescentar conteúdo fora do objetivo solicitado.
""",

    "didatico": """
Explique as informações progressivamente,
partindo dos conceitos mais simples.
Utilize exemplos ou analogias quando contribuírem
para a compreensão do cliente.
"""
}

CHANNELS = {
    "chat": """
Utilize linguagem conversacional, frases curtas
e informações de fácil leitura.
Priorize informações essenciais e evite sobrecarregar
o cliente com detalhes ou perguntas desnecessárias.
""",

    "email": """
Organize a comunicação de maneira profissional,
estruturada e compreensível.
""",

    "telefone": """
Utilize linguagem natural, adequada à comunicação oral.
Apresente informações em sequência lógica.
Evite elementos visuais que não possam ser
facilmente transmitidos verbalmente.
"""
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
