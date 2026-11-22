from fastapi import FastAPI

from backend.routes.generation import router as generation_router
from backend.routes.customers import router as customers_router
from backend.routes.comparison import router as comparison_router

app = FastAPI(title="Support Assistant API")

# Adicionando os routers ao  FastAPI
app.include_router(generation_router)
app.include_router(customers_router)
app.include_router(comparison_router)