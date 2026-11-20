import json
from services.llm import chamar_llm
from prompts.persona import obter_persona
from prompts.context import montar_contexto
from prompts.objectives import obter_objetivo
from prompts.instructions import obter_instrucoes
from prompts.restrictions import obter_restricoes
from prompts.formats import obter_formato

with open("data/customers.json", encoding="utf-8") as arquivo:
    clientes = json.load(arquivo)

cliente = clientes[0]

ticket = "Meu computador não conecta ao Wi-Fi."
versao = "v2"
tipo = "diagnosis"

persona = obter_persona(versao)
contexto = montar_contexto(cliente, ticket)
objetivo = obter_objetivo(tipo, versao)
instrucoes = obter_instrucoes(cliente, versao)
restricoes = obter_restricoes()
formato = obter_formato(tipo, cliente, versao)
prompt = (persona 
          + contexto 
          + objetivo 
          + instrucoes 
          + restricoes 
          + formato)

print("PROMPT ENVIADO:")
print(prompt)

resposta = chamar_llm(prompt)

print("\nRESPOSTA:")
print(resposta)