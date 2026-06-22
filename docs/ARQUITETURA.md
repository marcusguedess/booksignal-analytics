# Arquitetura

O BookSignal separa preparação de dados e apresentação visual.

```text
CSVs de amostra
  -> preparação em Python
  -> contrato JSON normalizado
  -> dashboard estático em Next.js
  -> GitHub Pages
```

## Camada Python

`analytics/export_booksignal.py` carrega as bases de amostra, aplica as funções de preparo em `datasets/booksignal/` e grava `web/src/data/booksignal.json`.

O export contém:

- origem dos dados e cobertura temporal das reviews;
- métricas gerais;
- livros ranqueados;
- agregações por gênero;
- distribuições de rating e confiança;
- amostras recentes de reviews;
- indicadores de qualidade da base.

## Camada Web

A interface fica em `web/` e usa Next.js App Router.

O dashboard é estático por escolha de arquitetura. Isso mantém o projeto barato de hospedar, simples de revisar e seguro para GitHub Pages, já que nenhuma chave de API ou serviço privado é necessário em runtime.

## CI E Publicação

O workflow do GitHub Actions executa a mesma sequência esperada localmente:

1. Instala dependências Python.
2. Exporta o JSON analítico.
3. Roda testes Python.
4. Verifica sintaxe Python.
5. Instala dependências do frontend.
6. Roda ESLint.
7. Roda typecheck TypeScript.
8. Gera o site estático.
9. Publica `web/out`.

## Por Que Export Estático

GitHub Pages não executa backend nem protege secrets. O export estático é o limite correto para a versão pública do projeto. Uma implantação privada poderia adicionar banco, ingestão sob demanda e conectores externos, mas isso fica fora do escopo da versão de portfólio.
