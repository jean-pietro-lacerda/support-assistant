# A função montar_contexto é responsável por criar um contexto detalhado para o 
# modelo de linguagem, fornecendo informações sobre o cliente e o problema relatado. 
# ( as informações sobre o cliente estão em JSON inicialmente)


def montar_contexto(cliente, ticket):
    return f"""
CONTEXTO

Nome do cliente: {cliente['name']}
Nível técnico: {cliente['technical_level']}
Estilo de comunicação: {cliente['communication_style']}
Canal de atendimento: {cliente['channel']}

Problema relatado: {ticket}
"""