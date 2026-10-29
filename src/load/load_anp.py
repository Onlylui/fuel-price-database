'''
Subir .parquet no banco de dados
'''

from pathlib import Path
import polars as pl
from sqlalchemy import Engine
from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import select

from load.database import create_tables
from load.database import get_engine
from load.models import AnpData
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


def load_periodo(engine: Engine, df: pl.DataFrame, periodo: str) -> tuple[int, int]:
    # garante que o DataFrame só tem colunas do modelo (o id é gerado pelo banco).
    model_columns = set(AnpData.__table__.columns.keys()) - {"id"}
    unknown_columns = set(df.columns) - model_columns

    if unknown_columns:
        raise RuntimeError(f"Colunas fora do modelo: {sorted(unknown_columns)}")

    columns = ", ".join(df.columns)
    copy_sql = f"COPY {AnpData.__tablename__} ({columns}) FROM STDIN WITH (FORMAT csv, HEADER true)"

    # DELETE, COPY e conferência na mesma transação: qualquer erro desfaz tudo.
    with engine.begin() as conn:
        deleted = conn.execute(delete(AnpData).where(AnpData.periodo == periodo)).rowcount

        # COPY usa o cursor do psycopg, na mesma conexão (e transação) do DELETE.
        with conn.connection.dbapi_connection.cursor() as cursor:
            with cursor.copy(copy_sql) as copy:
                copy.write(df.write_csv())

        inserted = conn.execute(
            select(func.count()).select_from(AnpData).where(AnpData.periodo == periodo)
        ).scalar_one()

        if inserted != df.height:
            raise RuntimeError(f"Contagem divergente: {inserted} no banco, {df.height} no silver.")

    return deleted, inserted


def main():
    # conecta ao banco e garante que a tabela anp_data existe.
    engine = get_engine()
    create_tables(engine)

    silver_df = read_silver(SILVER_FILE)
    periodo = get_periodo(silver_df)

    deleted, inserted = load_periodo(engine, silver_df, periodo)

    print(f"Período: {periodo}")
    print(f"Linhas removidas da carga anterior: {deleted}")
    print(f"Linhas inseridas: {inserted}")


if __name__ == "__main__":
    main()
