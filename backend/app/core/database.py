import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# 1. Cargamos las variables del archivo .env (En AWS, la nube provee esto automáticamente)
load_dotenv()

# 2. Obtenemos la URL de la base de datos.
# Si estás en tu PC, usará localhost. Si estás en AWS, leerá el endpoint de RDS.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("ERROR:La variable de entorno DATABASE_URL no está configurada.")

# 3. El 'Engine' (Motor) es el encargado de administrar las conexiones con PostgreSQL.
# Usamos psycopg2 por debajo de forma automática.
engine = create_engine(DATABASE_URL, echo=True)  # echo=True muestra los comandos SQL en la terminal (ideal para desarrollo)


# 4. Esta función crea las tablas en PostgreSQL basándose en tus modelos de Python (Productos, Usuarios, etc.)
def init_db():
    # SQLModel busca todos los modelos que hayas creado y genera las tablas en la BD si no existen
    SQLModel.metadata.create_all(engine)


# 5. Esta función crea una sesión temporal para cada petición que haga el cliente.
# Usamos un generador ('yield') para que la sesión se abra al iniciar la petición y se cierre automáticamente al terminar.
def get_session():
    with Session(engine) as session:
        yield session