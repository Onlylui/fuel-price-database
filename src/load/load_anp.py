'''
Subir .parquet no banco de dados
'''

from load.database import create_tables
from load.database import get_engine


def main():
    # conecta ao banco e garante que a tabela anp_data existe.
    engine = get_engine()
    create_tables(engine)


if __name__ == "__main__":
    main()
