# CLAUDE.md — WebStore

Contexto para Claude Code / Codex al trabajar en este repo. Las decisiones de
diseño se toman en Claude.ai (Projects); este archivo es el resumen que debe
mantenerse actualizado cada vez que se cierre una decisión nueva.

## Qué es este proyecto

App single-tenant (un deploy por cliente) para que negocios pequeños
(librerías, tiendas de ropa) en una ciudad pequeña de Guatemala vendan online.
No es SaaS multi-tenant.

**Objetivo del dev:** aprender buenas prácticas fullstack reales, no vibe
coding. BS en Computer Science, conoce teoría, poca práctica. Quiere entender
el "por qué" de cada decisión.

## Stack

- **Backend:** FastAPI + SQLModel + PostgreSQL (Neon/Supabase) → deploy en
  Railway o Render
- **Frontend:** React + Vite + Tailwind CSS → deploy en Vercel
- **Auth:** Firebase Authentication (stateless — el backend solo verifica el
  ID token en cada request con el Firebase Admin SDK, no hay sesiones en la DB)
- **Storage:** AWS S3 (lo único que se queda en AWS)
- **Pagos:** Stripe (nunca tocar datos de tarjeta directamente)
- **Package manager backend:** `uv` (NO pip). Instalar deps con
  `uv add <paquete>`, dev deps con `uv add --dev <paquete>`.

## Reglas de código

- Todo en inglés: variables, nombres de archivo, tablas, endpoints.
- Comentarios ocasionales pueden ir en español si se pide explícitamente.
- No generar código completo sin explicar el patrón primero.
- Patrón fijo a seguir: **Model → Schema (Create/Update/Response) → Route →
  axios service (frontend)**.

## Convenciones de API

- Todas las rutas bajo `/api/v1/`.
- Response envelope (`{"data": [...], "meta": {...}}`) solo en listas con
  paginación/filtros reales (ej. `GET /products`). Catálogos simples sin
  paginar (ej. `GET /categories`) devuelven el array directo.
- Errores: formato default de FastAPI (`{"detail": "..."}`).
- Auth: `Authorization: Bearer <firebase_id_token>`, verificado por request,
  sin sesiones server-side.
- Query style preferido: `session.exec(select(...))`, no `session.query()`
  (ambos funcionan con SQLModel, pero `.exec(select())` es el idiomático y el
  que migra a async si algún día se necesita).

## Patrón de schemas (Pydantic)

Por cada recurso, 3 schemas separados — nunca reusar uno para otro propósito:

- **Create**: lo que el cliente manda en `POST`. Excluye todo lo que genera
  el servidor (`id`, timestamps, slugs).
- **Update**: igual que Create pero todo `Optional`, para `PATCH` parcial.
  **Nunca reusar `Create` aquí** — si un campo es obligatorio en Create y el
  PATCH no lo manda, Pydantic rechaza el request con 422.
- **Response**: lo que devuelve el servidor. Incluye `id`, timestamps, y
  cualquier campo del modelo que el frontend necesite (fácil olvidarse de
  alguno, ej. `sku` en `products`).

## Decisiones de scope ya tomadas

- Sin direcciones estructuradas — `delivery_note` como texto libre en orders.
- Tablas separadas: `staff` vs `customers` (no un solo `users`).
- `unit_price` se congela en `order_items` al momento de la compra.
- Slugs (`categories.slug`) se generan en el backend con `python-slugify` a
  partir de `name` — nunca los manda el cliente.
- `price` siempre `Decimal` en Python / `NUMERIC(10,2)` en Postgres. Nunca
  `float` (los floats no representan bien decimales — importante con dinero).
- `products.sku` tiene `UNIQUE`.
- `products.stock_quantity` **nunca** se edita vía `PATCH /products/{id}` —
  ese campo está deliberadamente fuera de `ProductUpdate`. Todo cambio de
  stock pasa por `POST /inventory`, que internamente actualiza el producto y
  deja rastro de auditoría (`reason`, `staff_id`).
- Soft-delete (`is_active`) en `products` y `staff` — nunca `DELETE` real en
  estas tablas ni en `orders`/`customers`, porque otras tablas los referencian
  por FK (`order_items.product_id`, `inventory.staff_id`, `orders.customer_id`)
  y borrarlos rompería el historial de ventas.
- `orders`, `order_items`, `transactions`, `inventory` son insert-only /
  append-only desde la perspectiva de la API: no tienen `DELETE`, y
  `transactions`/`inventory` tampoco tienen `PATCH` (son logs inmutables de
  auditoría/financieros).
- `order_items` no tiene endpoints propios — se crea atómicamente dentro de
  `POST /orders` y se devuelve anidado en `GET /orders/{id}`.
- `transactions` se crean vía webhook de Stripe, no por un POST expuesto al
  cliente.

## Endpoints por tabla (resumen)

| Tabla | Endpoints | Notas |
|---|---|---|
| categories | GET, GET/{id}, POST, PATCH | sin DELETE hasta resolver qué pasa si tiene productos asociados |
| products | GET (paginado/filtrable), GET/{id}, POST, PATCH | sin DELETE; `stock_quantity` fuera de Update |
| product_images | POST, PATCH (sort_order), DELETE | sin GET propio, anidado en products |
| staff | GET /me, GET, POST, PATCH | sin registro público; alta la hace un admin |
| customers | POST, GET /me, PATCH /me, GET (staff) | sin DELETE |
| orders | POST, GET, GET/{id}, PATCH (solo status) | sin DELETE |
| order_items | — | sin endpoints propios |
| transactions | GET | creación vía webhook, inmutable |
| inventory | POST, GET | inmutable, actualiza stock_quantity del producto |

## Inconsistencia conocida (a propósito, no tocar)

`categories` usa `categories_id` como nombre real de columna PK (tanto en
Python como en la DB). Todas las tablas siguientes (`products`, `staff`,
`customers`, `orders`, etc.) usan simplemente `id`. Esto es inconsistente
pero **intencional**: `categories` ya estaba probada y en uso cuando se
detectó la inconsistencia, y no vale la pena el riesgo de refactorizarla
(schema + route + frontend service) solo por naming. No "corregir"
`categories_id` a `id` sin que se pida explícitamente.

## Errores ya cazados durante implementación (para no repetirlos)

- Mismatch de verbo HTTP entre axios y el decorador de FastAPI (`api.put`
  contra una route `@router.patch` → 405). El verbo en axios debe ser
  idéntico al decorador de la route.
- Reuso de `XCreate` en el endpoint de `PATCH` en vez de `XUpdate` — deja
  código muerto (`if x is not None` que nunca puede ser `None` porque el
  campo era obligatorio en Create).
- `session.query()` vs `session.exec(select(...))` en SQLModel — ambos
  funcionan, pero se decidió estandarizar en `.exec(select())`.
- `model_dump()` sin `exclude_unset=True` en updates parciales — sobreescribe
  con `None` todos los campos que el cliente no mandó. Siempre usar
  `model_dump(exclude_unset=True)` en PATCH.
- `IntegrityError` importado de `psycopg2` en vez de `sqlalchemy.exc` — el
  `except` no atrapa nada porque SQLAlchemy envuelve el error en su propia
  clase antes de propagarlo. Import correcto:
  `from sqlalchemy.exc import IntegrityError`.
- `onupdate` en `updated_at` con un valor ya evaluado
  (`datetime.now(timezone.utc)`) en vez de un callable
  (`lambda: datetime.now(timezone.utc)`) — el timestamp queda congelado en el
  momento en que Python cargó la clase, no se actualiza en cada UPDATE real.
- Campos del modelo que no se exponen en `Response` sin querer (ej. `sku`
  olvidado en `ProductResponse`) — revisar que el schema de salida tenga
  todos los campos que el frontend necesita.
- SQLModel vs SQLAlchemy `Base` — el proyecto usa SQLModel
  (`class X(SQLModel, table=True)`), no `declarative_base()`. No mezclar
  imports de `sqlalchemy.orm.Mapped` con modelos SQLModel.

## Naming convention (frontend services)

Verbo + recurso singular: `createCategory`, `getAllCategories`,
`getCategoryById`, `updateCategory`. Mismo patrón para cada recurso nuevo —
el nombre del export describe la acción (`update`), no el método HTTP
(`patch`).

## Estado actual

- ✅ `categories`: model, schema (Create/Update/Response), routes (GET, GET/{id}
  pendiente de confirmar, POST, PATCH), service — completo y revisado.
- ✅ `products`: model, schema, routes (GET, GET/{id}, POST, PATCH), service —
  completo y revisado.
- ⏳ `product_images`: siguiente en la fila.
- ⏳ `staff`, `customers`, `orders`, `order_items`, `transactions`,
  `inventory`: pendientes.

## Flujo de trabajo

1. Diseño y decisiones en Claude.ai (Projects): arquitectura, payloads,
   tradeoffs.
2. Cuando algo queda decidido, se refleja en este archivo.
3. Claude Code / Codex lee este archivo al trabajar en el repo, para operar
   con las mismas reglas sin tener que repetir el contexto.
4. Patrón de aprendizaje: Claude da un ejemplo completo de un recurso: el dev
   implementa el siguiente recurso solo y entrega los 4 archivos
   (model, schema, route, service) juntos para revisión.