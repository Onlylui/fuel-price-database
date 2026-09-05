from pathlib import Path
from urllib.request import urlretrieve
from zipfile import is_zipfile, ZipFile

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


def validate_download(path: Path) -> None:
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
        csv_files = [item for item in zip_file_content if file.lower().endswith(".csv")]

        if not csv_files:
            print("Nenhum arquivo .csv encontrado.")
            return 
    return csv_files

if __name__ == "__main__":
    download_anp_data()
    validate_download(DESTINATION)