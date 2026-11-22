from fastapi import FastAPI

from backend.routes.generation import router as generation_router
from backend.routes.customers import router as customers_router
from backend.routes.comparison import router as comparison_router
from backend.routes.evaluetion import router as evaluation_router
from fastapi import Request
from fastapi.responses import JSONResponse
from groq import APIError
from psycopg import Error as DatabaseError

app = FastAPI(title="Support Assistant API")

# Adicionando manipuladores de exceção para erros específicos
@app.exception_handler(APIError)
def tratar_erro_groq(request: Request, erro: APIError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Serviço de IA temporariamente indisponível."}
    )


@app.exception_handler(DatabaseError)
def tratar_erro_banco(request: Request, erro: DatabaseError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Erro ao acessar o banco de dados."}
    )

# Adicionando os routers ao  FastAPI
app.include_router(generation_router)
app.include_router(customers_router)
app.include_router(comparison_router)
app.include_router(evaluation_router)
