# Dados locais

Os arquivos CSV brutos usados no desenvolvimento local podem ficar nesta pasta, mas nao devem ser publicados no GitHub por padrao.

Arquivos esperados pelo app:

- `Top-100 Trending Books.csv`
- `customer reviews.csv`

Motivo: a base de reviews pode conter nomes de revisores, textos longos com informacoes pessoais e conteudo sujeito a termos de uso da fonte original. Para publicar o projeto, mantenha os CSVs fora do repositorio ou substitua por uma amostra anonimizada.

O repositorio inclui os arquivos `sample_books.csv` e `sample_reviews.csv` para que outras pessoas consigam clonar, gerar o JSON analitico e testar o dashboard sem acessar os dados brutos.

## Colunas esperadas

`Top-100 Trending Books.csv`:

```text
Rank,book title,book price,rating,author,year of publication,genre,url
```

`customer reviews.csv`:

```text
Sno,book name,review title,reviewer,reviewer rating,review description,is_verified,date,timestamp,ASIN
```
