# O dicionário OBJECTIVES contém os objetivos de atendimento, cada um com duas versões (v1 e v2).
# A função obter_objetivo recebe o tipo de objetivo e a versão desejada, retornando o objetivo correspondente.

OBJECTIVES = {
    "diagnosis": {
        "v1": """
Gere um diagnóstico do problema relatado pelo cliente,
considerando seu perfil.

Apresente hipóteses, evidências disponíveis,
informações faltantes e conclusão provável.
""",
        "v2": """
Gere um diagnóstico do problema relatado pelo cliente,
considerando as evidências disponíveis e respeitando
as características do seu perfil.

Organize as hipóteses de acordo com sua plausibilidade,
identifique as evidências que sustentam cada hipótese
e destaque as informações faltantes.

Apresente uma conclusão provável, respeitando
as limitações das informações disponíveis.
"""
    },

    "resolution": {
        "v1": """
Gere um passo a passo para a resolução do problema
relatado pelo cliente, considerando seu perfil.
""",
        "v2": """
Gere um passo a passo para a resolução do problema
relatado pelo cliente, adaptando a linguagem, a
complexidade técnica e o nível de detalhamento
às características do seu perfil.
"""
    },

    "clarification": {
        "v1": """
Gere perguntas de esclarecimento priorizadas para obter
informações necessárias sobre o problema relatado pelo
cliente, considerando seu perfil.
""",
        "v2": """
Gere perguntas de esclarecimento que permitam reduzir
as incertezas sobre o problema relatado pelo cliente.

Priorize as perguntas mais relevantes para avançar
no atendimento, evitando informações redundantes
e adaptando a linguagem ao perfil do cliente.
"""
    },

    "flowchart": {
        "v1": """
Gere um resumo visual do atendimento em formato de
fluxograma ASCII ou descrição estruturada de decisão.

Escolha o formato mais adequado ao perfil do cliente.
""",
        "v2": """
Gere um resumo visual do atendimento em formato de
fluxograma ASCII ou descrição estruturada de decisão.

Escolha o formato mais adequado ao perfil do cliente.

Priorize as informações relevantes do atendimento,
organizando as etapas, condições e possíveis caminhos
de decisão em uma sequência lógica.

Adapte a linguagem e a complexidade ao perfil do cliente.
"""
    }
}


def obter_objetivo(tipo, versao):
    return OBJECTIVES[tipo][versao]