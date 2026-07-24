from fastapi import FastAPI
from app.core.database import init_db

#importación limpia y directa:
from app.api.v1.routes import products as products_route

from app.api.v1.routes import categories as categories_route
from app.api.v1.routes import product_images as product_images_route  # Importa el router de imágenes de productos
from app.api.v1.routes import staff as staff_route  # Importa el router de staff
from app.api.v1.routes import customers as customers_route
from app.api.v1.routes import orders as orders_route
from app.api.v1.routes import order_items as order_items_route
from app.api.v1.routes import transactions as transactions_route
from app.api.v1.routes import inventory as inventory_route

app = FastAPI(title="Web Store API")

app.include_router(products_route.router, prefix="/api/v1")
app.include_router(categories_route.router, prefix="/api/v1")
app.include_router(product_images_route.router, prefix="/api/v1")  # Agrega el router de imágenes de productos
app.include_router(staff_route.router, prefix="/api/v1")  # Agrega el router de staff
app.include_router(customers_route.router, prefix="/api/v1")
app.include_router(orders_route.router, prefix="/api/v1")
app.include_router(order_items_route.router, prefix="/api/v1")
app.include_router(transactions_route.router, prefix="/api/v1")
app.include_router(inventory_route.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    print("Connecting to PostgreSQL...")
    init_db()

@app.get("/")
def home():
    return {"mensaje": "¡Backend ready!"}
