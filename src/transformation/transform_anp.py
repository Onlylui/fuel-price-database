from pathlib import Path
import polars as pl
import polars.selectors as cs

OUTPUT = Path("data/silver/anp/silver_fuel_prices_2026_01.parquet")
REJECTED_OUTPUT = Path("data/silver/anp/rejected_data/rejected.csv")
BRONZE_DIR = Path("data/bronze/anp/csv")

COLUMN_NAMES = {
    "Regiao - Sigla": "regiao_sigla",
    "Estado - Sigla": "estado_sigla",
    "Municipio": "municipio",
    "Revenda": "revenda",
    "CNPJ da Revenda": "cnpj_revenda",
    "Nome da Rua": "nome_rua",
    "Numero Rua": "numero_rua",
    "Complemento": "complemento",
    "Bairro": "bairro",
    "Cep": "cep",
    "Produto": "produto",
    "Data da Coleta": "data_coleta",
    "Valor de Venda": "valor_venda",
    "Valor de Compra": "valor_compra",
    "Unidade de Medida": "unidade_medida",
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
            pl.col("data_coleta").str.strptime(pl.Date,"%d/%m/%Y"),
            pl.col("valor_venda").str.replace(",",".").cast(pl.Decimal(10,2)),
            pl.col("valor_compra").str.replace(",",".").cast(pl.Decimal(10,2))
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

def clean_doc_fields(df:pl.DataFrame)-> pl.DataFrame:
    return df.with_columns(
        pl.col("cnpj_revenda")
        .str.replace_all(r"[^A-Za-z0-9]", "")           # mantém só letras e números
        .str.to_uppercase(),                            # CNPJ alfanumérico usa maiúsculas
        pl.col("cep")
        .str.replace_all(r"\D", "")                     # mantém só dígitos
    )

def validate_docs(unvalited_df:pl.DataFrame)-> tuple[pl.DataFrame,pl.DataFrame]:
    cleaned_doc = clean_doc_fields(unvalited_df)
    cnpj_ok = (
                pl.col("cnpj_revenda").is_not_null()
                &
                (pl.col("cnpj_revenda").str.len_chars() == 14) 
                & 
                (pl.col("cnpj_revenda").str.contains(r"\d{2}$")))
    cep_ok = (
                pl.col("cep").is_not_null()
                &
                (pl.col("cep").str.len_chars() == 8)
    )
    validated_docs = cleaned_doc.filter(cnpj_ok & cep_ok)
    rejected_docs = cleaned_doc.filter(~cnpj_ok | ~cep_ok)
    return validated_docs, rejected_docs
     


def main():
    csv_path = find_csv(BRONZE_DIR)

    raw_df = pl.read_csv(
        csv_path,
        separator=";",
    )

    silver_df = transform_silver_df(raw_df)

    clean_silver_df = clear_silver_df(silver_df)

    check_docs_fields = clean_doc_fields(clean_silver_df)

    validated_docs = validate_docs(check_docs_fields)

    removed_rows = silver_df.height - clean_silver_df.height

    print(f"Linhas removidas: {removed_rows}")
    print(f"Linhas finais: {clean_silver_df.height}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    validated_docs[0].write_parquet(OUTPUT)
    validated_docs[1].write_csv(REJECTED_OUTPUT)

if __name__ == "__main__":
    main()