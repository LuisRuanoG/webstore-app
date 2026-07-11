# Backend - Web Store API

Backend de la tienda web creado con FastAPI, SQLModel, PostgreSQL y uv.

## Requisitos

- Python 3.14 o superior: https://www.python.org/downloads/
- uv: https://docs.astral.sh/uv/getting-started/installation/
- PostgreSQL instalado y ejecutandose

Para verificar las instalaciones:

```bash
python --version
uv --version
```

En macOS puede que el comando sea:

```bash
python3 --version
uv --version
```

## Instalar uv

Windows, desde PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS, desde Terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Despues de instalar uv, cierra y abre la terminal si el comando `uv` no aparece inmediatamente.

## Configurar base de datos

1. Crea una base de datos en PostgreSQL, por ejemplo:

```sql
CREATE DATABASE webstore_db;
```

2. Crea o edita el archivo `.env` dentro de la carpeta `backend`.

Ejemplo:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/webstore_db
```

Reemplaza `usuario`, `password` y `webstore_db` por los datos reales de tu PostgreSQL.

## Instalacion en Windows

Desde PowerShell o la terminal de VS Code:

```powershell
cd backend
uv sync
.venv\Scripts\activate
uv run uvicorn app.main:app --reload
```

La API normalmente queda disponible en:

```text
http://localhost:8000
```

Documentacion interactiva de FastAPI:

```text
http://localhost:8000/docs
```

## Instalacion en macOS

Desde Terminal:

```bash
cd backend
uv sync
source .venv/bin/activate
uv run uvicorn app.main:app --reload
```

La API normalmente queda disponible en:

```text
http://localhost:8000
```

Documentacion interactiva de FastAPI:

```text
http://localhost:8000/docs
```

## Comandos utiles

Instalar o sincronizar dependencias:

```bash
uv sync
```

Ejecutar el servidor:

```bash
uv run uvicorn app.main:app --reload
```

Ejecutar el servidor en otro puerto:

```bash
uv run uvicorn app.main:app --reload --port 8001
```

Salir del entorno virtual:

```bash
deactivate
```

## Notas

- El proyecto lee la variable `DATABASE_URL` desde el archivo `.env`.
- Al iniciar el backend, FastAPI crea las tablas usando los modelos de SQLModel si todavia no existen.
- Si PostgreSQL no esta encendido o la URL de conexion esta mal, el backend no podra arrancar correctamente.
