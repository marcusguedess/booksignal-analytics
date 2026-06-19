# Cyberdeck Retro - Amazon Books Review Dashboard

Projeto desenvolvido **for fun** para explorar dados de livros e reviews da Amazon em um painel visual inspirado em interfaces cyberpunk.

A ideia do projeto é evoluir para um revisor/analista de reviews de livros com dados atualizados em tempo real. Por enquanto, esta primeira versão de testes trabalha com bases locais em CSV e serve como protótipo inicial da experiência, dos filtros e das visualizações.

Por segurança e privacidade, os CSVs brutos não são versionados por padrão. A base de reviews pode conter nomes de revisores, textos com informações pessoais e conteúdo sujeito aos termos de uso da fonte original.

## Status

Em desenvolvimento.

Esta é uma primeira versão de teste. Ainda há melhorias planejadas, especialmente para integrar dados em tempo real, refinar a análise das reviews e organizar melhor a arquitetura do projeto conforme ele crescer.

## O que o projeto faz

- Carrega dados de livros e reviews a partir de arquivos CSV.
- Permite filtrar livros por gênero, título, preço máximo e avaliação mínima.
- Permite visualizar apenas reviews verificadas.
- Exibe métricas gerais sobre livros, avaliações e reviews.
- Gera gráficos interativos com Plotly.
- Mostra livros mais comentados e reviews recentes.
- Inclui um "Modo Hacker" visual para reforçar a proposta estética do projeto.

## Escolha de design

Cyberpunk sempre. Hahaha.

A interface foi criada com uma estética retrofuturista, usando cores neon, fundo escuro, fontes inspiradas em terminal/arcade e uma atmosfera de "cyberdeck". A ideia é transformar uma análise simples de dados em uma experiência visual mais divertida, com cara de painel saído de Night City.

## Tecnologias

- Python
- Streamlit
- Pandas
- Plotly

## Estrutura atual

```text
.
├── datasets/
│   ├── app.py
│   └── README.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Como rodar localmente

Antes de executar, coloque os arquivos CSV locais dentro da pasta `datasets/`:

- `Top-100 Trending Books.csv`
- `customer reviews.csv`

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o app:

```bash
streamlit run datasets/app.py
```

## Segurança e dados

- Não há chaves de API, tokens ou credenciais no código.
- Arquivos `.env`, logs, cache Python e `secrets.toml` estão ignorados no Git.
- Os CSVs brutos estão ignorados para evitar publicar dados de terceiros ou conteúdo pessoal de reviews.
- A busca por título é tratada como texto literal, não como expressão regular.
- O HTML permitido via `unsafe_allow_html=True` é usado apenas com conteúdo estático do próprio app.

## Próximos passos

- Integrar uma fonte de dados atualizada em tempo real.
- Melhorar a organização do código e separar responsabilidades.
- Refinar as análises de reviews.
- Adicionar tratamento de erros para arquivos ausentes ou dados incompletos.
- Evoluir a experiência visual mantendo a identidade cyberpunk.

## Observação

Este projeto ainda está em conclusão e foi criado como experimento pessoal. A versão atual é um protótipo funcional para testes e validação da ideia.
