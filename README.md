# Fuel Price Database

## Pergunta de negócio
Com base nos dados fornecidos, qual a variação de preço por município, UF e tempo?

## Fonte de dados
Arquivos CSV coletados semanalmente pela ANP.(https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis). O pipeline deve baixar um CSV e salvá-lo em `data/bronze/`, sem alterar seu conteúdo.

## Arquitetura inicial
```
fuel-price-database/
├── data/
│   ├── bronze/       # CSV original da ANP
│   ├── silver/       # dados limpos e padronizados
│   └── gold/         # tabelas analíticas
├── src/
│   └── ingestion/    # código para obter e salvar a fonte
├── docs/             # decisões, dicionário de dados e diagramas
├── README.md
└── .gitignore

```

## Primeira entrega
O pipeline deve baixar um CSV e o guarda em data/bronze/ sem alterar seu conteúdo.

## Escopo da primeira versão
- PostgreSQL e pipeline executados via Docker Compose.
- Sem testes automatizados; a verificação é feita executando o pipeline e conferindo as contagens de linhas e os arquivos gerados.


## Executando com Docker
Pré-requisitos: Docker e Docker Compose.

```bash
cp .env.example .env        # ajuste as credenciais
docker compose build
docker compose up -d db     # sobe o PostgreSQL (porta 5433 no host)

docker compose run --rm app python src/ingestion/download_anp.py
docker compose run --rm app python src/transformation/transform_anp.py
```

A pasta `data/` é montada no container, então os arquivos gerados ficam disponíveis no host.
Para derrubar o banco: `docker compose down` (adicione `-v` para apagar também os dados).
