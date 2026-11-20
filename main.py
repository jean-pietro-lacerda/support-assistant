from services.llm import chamar_llm

prompt = "Explique brevemente o que é suporte técnico."

resposta = chamar_llm(prompt)

print(resposta)