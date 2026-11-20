import os
from groq import Groq
from  dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("CHAVE_API_LLM"))
MODEL = os.getenv("GROQ_MODEL")

def chamar_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content