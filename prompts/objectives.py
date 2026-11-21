# O dicionário OBJECTIVES contém os objetivos de atendimento, cada um com duas versões (v1 e v2).
# A função obter_objetivo recebe o tipo de objetivo e a versão desejada, retornando o objetivo correspondente.

OBJECTIVES = {
    "diagnosis": {
        "v1": """
Gere um diagnóstico do problema relatado pelo cliente,
considerando seu perfil.

Apresente hipóteses, evidências disponíveis,
informações faltantes e conclusão sustentada pelas evidências.
Quando elas forem insuficientes, declare o diagnóstico inconclusivo.
""",
        "v2": """
Gere um diagnóstico do problema relatado pelo cliente,
considerando as evidências disponíveis e seu perfil.

Apresente hipóteses relevantes para o problema.

Ordene as hipóteses por plausibilidade somente quando
existirem evidências que sustentem essa classificação.

Considere como evidências apenas fatos relatados
no ticket, sem confundir características do cliente
com evidências técnicas.

Identifique as informações faltantes necessárias
para confirmar ou descartar as hipóteses.

Quando não houver evidências suficientes para
determinar uma causa provável, declare explicitamente
que o diagnóstico é inconclusivo.

Não gere procedimentos de resolução.
"""
    },

    "resolution": {
        "v1": """
Gere um passo a passo para a resolução do problema
relatado pelo cliente, considerando seu perfil.
""",
        "v2": """
Gere um passo a passo para a resolução do problema
relatado pelo cliente.

Adapte a linguagem, a complexidade técnica e o
nível de detalhamento ao seu perfil.

Priorize procedimentos simples, seguros e reversíveis.

Organize as etapas em uma sequência lógica,
indicando como prosseguir dependendo dos resultados.

Antes de orientar procedimentos dependentes do dispositivo ou sistema,
solicite os dados essenciais que faltam e aguarde a resposta.
Ofereça apenas etapas seguras que não dependam desses dados.

Evite etapas redundantes e procedimentos avançados
que ultrapassem o conhecimento técnico do cliente.

Caso não seja possível resolver o problema com
segurança, indique a necessidade de suporte especializado.
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

Priorize perguntas com maior capacidade de confirmar
ou descartar possíveis causas do problema.

Organize as perguntas por ordem de relevância.

Solicite somente as informações necessárias para
avançar no atendimento.

Evite perguntas redundantes, já respondidas ou
excessivamente técnicas para o perfil do cliente.

Para atendimento por chat, priorize de três a cinco
perguntas quando forem suficientes.

Não solicite que o cliente execute procedimentos
de resolução.
"""
    },

    "flowchart": {
        "v1": """
Gere uma árvore textual simples de decisão em português,
falando diretamente com o cliente e considerando seu perfil.
Identifique as etapas e indique o destino de cada resultado possível.
Todas as etapas devem ser alcançáveis a partir do início e todos
os caminhos devem terminar em resolução, pedido de dados ou suporte.
""",
        "v2": """
Gere uma árvore textual simples de decisão em português,
falando diretamente com o cliente, conforme seu perfil e canal.
Use etapas identificadas, sem desenhos ASCII ou caixas.

Organize as etapas, condições e caminhos de decisão
em uma sequência lógica.

Cada condição deve indicar claramente a próxima ação
para cada resultado possível.

Todas as etapas devem ser alcançáveis a partir do início.
Não inclua etapas sem entrada, caminhos incompletos ou ciclos sem saída.
Cada resposta deve determinar um destino; não repita perguntas já
respondidas no ticket. Após cada teste, indique também o que fazer
se o problema for resolvido.

Utilize o mesmo idioma do atendimento em todas
as etapas e condições.

Adapte a linguagem e a complexidade ao perfil do cliente.

Finalize cada caminho indicando a resolução,
a necessidade de informações adicionais ou o
encaminhamento para suporte especializado.
"""
    }
}


def obter_objetivo(tipo, versao):
    return OBJECTIVES[tipo][versao]
