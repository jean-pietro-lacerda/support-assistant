
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
Utilize linguagem profissional e seções claras dentro dos campos,
preservando a estrutura JSON.
""",

    "telefone": """
Fale diretamente com o cliente em linguagem oral,
com perguntas e orientações sequenciais fáceis de ler em voz alta.
"""
}


EMAIL_FORMATS = {
    "diagnosis": """
Não inclua saudações, despedidas ou assinaturas nos campos
hypotheses, evidence ou missing_information.

O campo conclusion representa a resposta final que será
enviada diretamente ao cliente por e-mail.

Nesse campo, escreva uma mensagem completa contendo:
- Saudação personalizada com o nome do cliente.
- Conclusão técnica fundamentada nas evidências.
- Informações necessárias para continuar o atendimento,
  quando o diagnóstico for inconclusivo.
- Encerramento com "Atenciosamente, Equipe de Suporte".

Não apresente hipóteses como causas confirmadas.
Não invente informações ou diagnósticos.
Não mencione os nomes dos campos JSON na mensagem.
""",

    "resolution": """
O campo title deve conter apenas o título do problema.

No primeiro item de steps, inicie com uma saudação
personalizada usando o nome do cliente e apresente
a primeira orientação de resolução.

Mantenha os demais itens como etapas práticas,
organizadas em sequência lógica.

No campo additional_guidance, apresente as orientações
complementares necessárias e finalize com
"Atenciosamente, Equipe de Suporte".

Não coloque a assinatura nas etapas de resolução.
Não invente procedimentos ou resultados.
""",

    "clarification": """
No primeiro item de questions, inicie com uma saudação
personalizada usando o nome do cliente, seguida
da primeira pergunta de esclarecimento.

Mantenha os demais itens como perguntas objetivas
e necessárias para avançar no atendimento.

No último item de questions, após a última pergunta,
inclua uma breve despedida e finalize com
"Atenciosamente, Equipe de Suporte".

Cada item deve conter uma pergunta relevante.
Não acrescente perguntas apenas para acomodar
a saudação ou o encerramento.
""",

    "flowchart": """
O campo format deve conter somente decision_tree.

No campo flow, inicie com uma saudação personalizada
usando o nome do cliente e uma breve introdução.

Em seguida, apresente a árvore de decisão completa,
com etapas identificadas, condições e destinos explícitos.

Após a árvore de decisão, finalize com
"Atenciosamente, Equipe de Suporte".

Não transforme a saudação ou a assinatura em etapas
de decisão. Preserve a estrutura lógica do fluxo.
Não invente procedimentos ou resultados.
"""
}


def obter_formato(tipo, cliente, versao):

    schema = json.dumps(
        FORMATS[tipo],
        indent=4,
        ensure_ascii=False
    )

    regra_saudacao = "Não inclua saudações, despedidas ou assinaturas nos campos técnicos."

    if versao == "v2" and cliente["channel"] == "email":
        regra_saudacao = EMAIL_FORMATS[tipo]

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
Respeite os tipos de dados definidos na estrutura.
Preencha listas com elementos textuais individuais.
Não deixe campos obrigatórios vazios. Quando não houver itens em
uma lista, use um item textual curto explicando a ausência.
{regra_saudacao}
A adaptação ao canal deve preservar este contrato JSON.

Não mencione os nomes internos dos campos JSON
na comunicação direcionada ao cliente.
"""

    if tipo == "flowchart":
        formato_base += """
O campo format deve conter somente decision_tree.

O campo flow deve conter a representação completa do fluxo.
Use uma árvore textual simples em português, com etapas identificadas
e destinos explícitos para cada resultado, sem caixas ASCII.

Preserve as quebras de linha utilizando o escape JSON \\n,
sem duplicar o caractere de escape.
"""

    if versao == "v1":
        return formato_base + """
Adapte a apresentação ao canal de atendimento do cliente.
"""

    if versao == "v2":
        return formato_base + CHANNEL_FORMATS[cliente["channel"]]
