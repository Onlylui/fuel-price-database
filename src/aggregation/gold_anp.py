from pathlib import Path
import polars as pl


OUTPUT = Path("data/gold/anp/fuel_prices_2026_01.parquet")
SILVER_INPUT = Path("data/silver/anp/silver_fuel_prices_2026_01.parquet")

def transform_to_gold(silver_df:pl.DataFrame) -> pl.DataFrame:
    gold_df = (
        silver_df.filter(pl.col("unidade_de_medida") == "R$ / litro")
    )
