from pathlib import Path
import polars as pl

bronze_dir = Path("data/bronze/anp")
OUTPUT = Path("data/silver/anp/fuel_prices_2026_01.parquet")

csv_archive = list(bronze_dir.glob("*.csv"))

raw_df = pl.read_csv(
    csv_archive[0],
    separator = ";"
    )

COLUMN_NAMES = {
    "Regiao - Sigla": "regiao_sigla",
    "Estado - Sigla": "estado_sigla",
    "Municipio": "municipio",
    "Revenda": "revenda",
    "CNPJ da Revenda": "cnpj_da_revenda",
    "Nome da Rua": "nome_da_rua",
    "Numero Rua": "numero_da_rua",
    "Complemento": "complemento",
    "Bairro": "bairro",
    "Cep": "cep",
    "Produto": "produto",
    "Data da Coleta": "data_da_coleta",
    "Valor de Venda": "valor_de_venda",
    "Valor de Compra": "valor_de_compra",
    "Unidade de Medida": "unidade_de_medida",
    "Bandeira": "bandeira",
}


silver_df = (
    raw_df
    .rename(COLUMN_NAMES)
    .with_columns(
        pl.col("data_da_coleta").str.strptime(pl.Date,"%d/%m/%Y"),
        pl.col("valor_de_venda").str.replace(",",".").cast(pl.Decimal(10,3)),
        pl.col("valor_de_compra").str.replace(",",".").cast(pl.Decimal(10,3))
                  )
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
silver_df.write_parquet(OUTPUT)