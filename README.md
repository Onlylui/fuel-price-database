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
├── tests/
├── docs/             # decisões, dicionário de dados e diagramas
├── README.md
└── .gitignore

```

## Primeira entrega
O pipeline deve baixar um CSV e o guarda em data/bronze/ sem alterar seu conteúdo.