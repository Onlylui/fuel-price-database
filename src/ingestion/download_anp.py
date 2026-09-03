from pathlib import Path
from urllib.request import urlretrieve


SOURCE_URL = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2026-01.zip"
DESTINATION = Path("data/bronze/anp/ca-2026-01.zip")



def download_anp_data() -> None:
    destination_directory = DESTINATION.parent
    destination_directory.mkdir(parents=True, exist_ok=True)
    if DESTINATION.exists():
        print("arquivo já existente")
        return
    print("Baixando arquivo!")
    urlretrieve(SOURCE_URL, DESTINATION)
    print("Arquivo baixado com sucesso!")

if __name__ == "__main__":
    download_anp_data()