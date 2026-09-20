from pathlib import Path
from urllib.request import urlretrieve
from zipfile import is_zipfile, ZipFile
import shutil

SOURCE_URL      = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2026-01.zip"
DESTINATION     = Path("data/bronze/anp/ca-2026-01.zip")
CSV_DESTINATION = Path("data/bronze/anp/csv")



def download_anp_data() -> None:
    destination_directory = DESTINATION.parent
    destination_directory.mkdir(parents=True, exist_ok=True)
    if DESTINATION.exists():
        print("arquivo já existente")
        return
    print("Baixando arquivo!")
    urlretrieve(SOURCE_URL, DESTINATION)
    print("Arquivo baixado com sucesso!")


def validate_download(path: Path) -> list[str] | None:
    #verifica se é um zip válido.
    if not is_zipfile(path):
        print("Arquivo não é um ZIP")
        return

    #Abre o arquivo zip.
    with ZipFile(path) as zip_file:

        #testa integridade do arquivo ZIP.
        tested_zip = zip_file.testzip()
        if tested_zip:
            print(f"O arquivo {tested_zip}, não é valido pode estar corrompido.")
            return
        #verifica se o conteúdo do ZIP contem arquivo CSV.
        zip_file_content = zip_file.namelist()
        csv_files = [item for item in zip_file_content if item.lower().endswith(".csv")]

        if not csv_files:
            print("Nenhum arquivo .csv encontrado.")
            return 
    return csv_files

def extract_csv(path: Path, csv_files: list[str]) -> None:

    CSV_DESTINATION.mkdir(parents=True, exist_ok=True)

    with ZipFile(path) as zip_file:

        for csv_file in csv_files:

            # Pega somente o nome do arquivo
            file_name = Path(csv_file).name

            destination = CSV_DESTINATION / file_name

            # Abre o CSV que está dentro do ZIP
            with zip_file.open(csv_file) as source:

                # "wb" sobrescreve caso o arquivo já exista
                with destination.open("wb") as target:
                    shutil.copyfileobj(source, target)

            print(f"CSV salvo em: {destination}")


if __name__ == "__main__":
    download_anp_data()
    csv_files = validate_download(DESTINATION)

    if csv_files:
        extract_csv(DESTINATION, csv_files)