from fastapi import FastAPI
from app.core.database import init_db

# 💡 Aseguramos la importación limpia y directa:
from app.api.routes import products as products_route
from app.api.routes import users as users_route

app = FastAPI(title="Web Store API")

app.include_router(products_route.router)
app.include_router(users_route.router)

@app.on_event("startup")
def on_startup():
    print("Connecting to PostgreSQL...")
    init_db()

@app.get("/")
def home():
    return {"mensaje": "¡Backend ready!"}