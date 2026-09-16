from pathlib import Path
import polars as pl

OUTPUT = Path("data/silver/anp/fuel_prices_2026_01.parquet")
BRONZE_DIR = Path("data/bronze/anp")

def find_csv(dir: Path) -> Path:
    csv_files = list(dir.glob("*.csv"))

    if len(csv_files) == 0:
        raise FileNotFoundError("Nenhum  arquivo encontrado")

    if len(csv_files) > 1:
        raise RuntimeError("Mais de um arquivo informado para operação")

    return csv_files[0]

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

csv_path = find_csv(BRONZE_DIR)

raw_df = pl.read_csv(
    csv_path,
    separator=";",
)

silver_df = (
    raw_df
    .rename(COLUMN_NAMES)
    .with_columns(
        pl.col("data_da_coleta").str.strptime(pl.Date,"%d/%m/%Y"),
        pl.col("valor_de_venda").str.replace(",",".").cast(pl.Decimal(10,3)),
        pl.col("valor_de_compra").str.replace(",",".").cast(pl.Decimal(10,3))
                  )
    )

clean_silver_df = silver_df.unique(
    maintain_order=True
)

removed_rows = silver_df.height - clean_silver_df.height

print(f"Linhas removidas: {removed_rows}")
print(f"Linhas finais: {clean_silver_df.height}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
clean_silver_df.write_parquet(OUTPUT)