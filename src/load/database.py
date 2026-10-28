import os

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine

from load.models import Base


def get_engine() -> Engine:
    # lê o .env local, sem sobrescrever variáveis já definidas.
    load_dotenv()
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Variável DATABASE_URL não definida.")

    return create_engine(database_url)


def create_tables(engine: Engine) -> None:
    # cria apenas as tabelas que ainda não existem, não altera as existentes.
    Base.metadata.create_all(engine)

def main():
    engine = get_engine()
    create_tables(engine)

if __name__ == "__main__":
    main()