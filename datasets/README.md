# Dados locais

Os arquivos CSV brutos usados pelo app ficam nesta pasta durante o desenvolvimento local, mas nao devem ser publicados no GitHub por padrao.

Arquivos esperados pelo app:

- `Top-100 Trending Books.csv`
- `customer reviews.csv`

Motivo: a base de reviews pode conter nomes de revisores, textos longos com informacoes pessoais e conteudo sujeito a termos de uso da fonte original. Para publicar o projeto, mantenha os CSVs fora do repositorio ou substitua por uma amostra anonimizada.

## Colunas esperadas

`Top-100 Trending Books.csv`:

```text
Rank,book title,book price,rating,author,year of publication,genre,url
```

`customer reviews.csv`:

```text
Sno,book name,review title,reviewer,reviewer rating,review description,is_verified,date,timestamp,ASIN
```
