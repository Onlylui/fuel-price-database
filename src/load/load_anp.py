'''
Subir .parquet no banco de dados
'''

from pathlib import Path
import polars as pl

from load.database import create_tables
from load.database import get_engine
from transformation.transform_anp import OUTPUT

SILVER_FILE = OUTPUT


def read_silver(path: Path) -> pl.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo silver não encontrado: {path}")

    return pl.read_parquet(path)


def get_periodo(df: pl.DataFrame) -> str:
    # o período vem dos próprios dados, garantindo que o DELETE corresponde ao que será inserido.
    if "periodo" not in df.columns:
        raise RuntimeError("Coluna periodo ausente no silver. Execute a transformação novamente.")

    periodos = df["periodo"].unique().to_list()

    if len(periodos) != 1:
        raise RuntimeError(f"O silver deve conter exatamente um período, encontrados: {periodos}")

    return periodos[0]


def main():
    # conecta ao banco e garante que a tabela anp_data existe.
    engine = get_engine()
    create_tables(engine)

    silver_df = read_silver(SILVER_FILE)
    periodo = get_periodo(silver_df)

    print(f"Linhas lidas do silver: {silver_df.height} (período {periodo})")


if __name__ == "__main__":
    main()
