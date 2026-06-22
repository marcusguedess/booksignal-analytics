# Metodologia

O dashboard foi desenhado para análise comparativa. Os scores ajudam a priorizar livros para curadoria, promoção ou leitura manual mais cuidadosa.

## Ranking Dos Livros

O ranking principal usa um score de oportunidade derivado de:

- rating do livro;
- preço;
- volume de reviews;
- proporção de reviews verificadas;
- qualidade média das reviews.

A interface também oferece modos de decisão para promoção, auditoria, busca de barganhas e exploração por categoria. Cada modo altera a ênfase do ranking sem alterar a base analisada.

## Qualidade Das Reviews

A qualidade da review é uma heurística local. O score reduz confiança quando encontra sinais como:

- review não verificada;
- texto muito curto;
- título genérico;
- nota extrema com pouco contexto;
- pontuação repetida.

O score não classifica uma review como falsa. Ele apenas indica registros que merecem leitura manual.

## Normalização De Gêneros

As bases de livros costumam trazer várias categorias em uma única célula. O pipeline agrupa esses rótulos em categorias mais estáveis, como `Fiction`, `Romance`, `Business`, `Children` e `Young Adult`.

O gênero normalizado é usado em filtros, ranking e benchmarks. O rótulo original continua disponível no painel do livro selecionado.

## Qualidade Da Base

O dashboard mostra:

- número de linhas;
- número de colunas;
- células vazias;
- linhas duplicadas;
- completude geral;
- cobertura dos gêneros normalizados.

Essas checagens são simples de propósito. O objetivo é deixar claro se a base tem qualidade mínima antes de interpretar o score.

## Limitações

Os dados de amostra demonstram o fluxo do produto, mas não representam um feed de mercado em tempo real.

Em uso operacional, preço, rating e reviews devem carregar origem, data de coleta, permissão de uso e política de atualização. A versão pública no GitHub Pages não armazena secrets, não chama APIs pagas e não executa ingestão server-side.
