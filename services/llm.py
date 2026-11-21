import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("CHAVE_API_LLM"))
MODEL = os.getenv("GROQ_MODEL")
TEMPERATURE = 0.2

def chamar_llm(mensagens):
    response = client.chat.completions.create(
        model=MODEL,
        messages=mensagens,
        temperature=TEMPERATURE
    )

    return response.choices[0].message.content
