from pathlib import Path
import polars as pl
import polars.selectors as cs

OUTPUT = Path("data/silver/anp/fuel_prices_2026_01.parquet")
BRONZE_DIR = Path("data/bronze/anp/csv")

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

def find_csv(dir: Path) -> Path:
    csv_files = list(dir.glob("*.csv"))

    if len(csv_files) == 0:
        raise FileNotFoundError("Nenhum  arquivo encontrado")

    if len(csv_files) > 1:
        raise RuntimeError("Mais de um arquivo informado para operação")

    return csv_files[0]

def transform_silver_df(df: pl.DataFrame) -> pl.DataFrame:
    silver_df = (
        df
        .rename(COLUMN_NAMES)
        .with_columns(
            pl.col("data_da_coleta").str.strptime(pl.Date,"%d/%m/%Y"),
            pl.col("valor_de_venda").str.replace(",",".").cast(pl.Decimal(10,3)),
            pl.col("valor_de_compra").str.replace(",",".").cast(pl.Decimal(10,3))
                      )
        )
    return silver_df

def clear_silver_df(df: pl.DataFrame) -> pl.DataFrame:
    clean_silver_df = (
        df
        .with_columns(
            cs.string()                                 # todas as colunas String
            .str.replace_all(r"[\s\u200B]+", " ")       # colapsa espaços, tabs, NBSP
            .str.strip_chars()                          # remove bordas
            .replace("", None)                          # vazio vira null
        )
        .unique(maintain_order=True)                    # retira resgistros duplicados                  
    )
    return clean_silver_df

def main():
    csv_path = find_csv(BRONZE_DIR)

    raw_df = pl.read_csv(
        csv_path,
        separator=";",
    )

    silver_df = transform_silver_df(raw_df)
    clean_silver_df = clear_silver_df(silver_df)

    removed_rows = silver_df.height - clean_silver_df.height

    print(f"Linhas removidas: {removed_rows}")
    print(f"Linhas finais: {clean_silver_df.height}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    clean_silver_df.write_parquet(OUTPUT)

if __name__ == "__main__":
    main()