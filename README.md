# Cyberdeck Retro - Revisor de Reviews de Livros

![Banner pixel art neon do Cyberdeck Retro](assets/readme-banner.svg)

Projeto autoral criado e assinado por **Marcus Guedes**.

Projeto desenvolvido **for fun** para explorar dados de livros e reviews em um painel visual inspirado em cyberdecks, arcade retrofuturista e Night City.

A ideia original era evoluir para um revisor/analista de reviews de livros com dados atualizados em tempo real. Como a prioridade atual é manter o projeto gratuito, seguro e sem gasto com tokens ou APIs pagas, esta versão trabalha com CSVs locais, upload manual de dados e amostras públicas anonimizadas.

Por segurança e privacidade, os CSVs brutos não são versionados por padrão. Bases de reviews podem conter nomes de revisores, textos com informações pessoais e conteúdo sujeito aos termos de uso da fonte original. Para manter o projeto testável no GitHub, o repositório inclui amostras anonimizadas.

## Status

Em desenvolvimento, mas já funcional para testes públicos.

A versão atual inclui UI revisada, upload de CSV, dados de exemplo, score local de confiança, radar de compra, comparador de livros e exportação segura dos resultados filtrados.

## Funcionalidades

- Upload de CSVs de livros e reviews direto pela interface.
- Fallback automático para CSV local ou amostras públicas anonimizadas.
- Filtros por gênero, título, preço máximo e nota mínima.
- Filtro de reviews verificadas.
- Filtro de reviews que merecem revisão manual.
- Busca textual literal em reviews, títulos e nomes de livros.
- Score local de confiança das reviews.
- Explicação dos motivos que impactaram o score de cada review.
- Radar de compra com destaques automáticos.
- Comparador de até 4 livros.
- Aba de qualidade dos dados com origem, colunas, vazios e duplicatas.
- Gráficos interativos com Plotly.
- Exportação de CSVs filtrados.
- Proteção simples contra CSV formula injection nos arquivos exportados.
- Interface em pixel art neon com foco em leitura rápida e navegação fácil.

## Score de confiança

O score de confiança é uma heurística local, sem IA paga e sem consumo de tokens.

Ele reduz pontos quando uma review apresenta sinais como:

- review não verificada;
- texto muito curto;
- título genérico;
- nota extrema combinada com ausência de verificação;
- pontuação repetida em excesso.

O score não é uma detecção definitiva de fraude. Ele serve para priorizar revisão humana.

Cada review exibe também os motivos do alerta, como `não verificada`, `texto curto`, `título genérico` ou `nota extrema sem verificação`.

## Radar de compra

O radar destaca automaticamente:

- melhor custo-benefício;
- livro mais confiável;
- livro mais comentado;
- livro mais controverso.

Esses destaques usam preço, nota, volume de reviews, percentual de reviews verificadas e score médio de confiança.

## Escolha de design

Cyberpunk sempre. Hahaha.

A interface foi criada para parecer um painel arcade de ficção urbana: fundo escuro, luzes neon, contraste alto, botões coloridos, chips de status, painéis de métricas e um banner em pixel art com skyline, sol neon e grade retrofuturista. A intenção é que a pessoa entenda rapidamente os filtros e gráficos, mas ainda sinta que está entrando em um console visual memorável.

O design prioriza:

- leitura simples;
- filtros claros;
- métricas visíveis logo no topo;
- gráficos com cores fortes;
- ações diretas para upload, comparação e download;
- visual expressivo sem tornar a interface confusa.

## Tecnologias

- Python
- Streamlit
- Pandas
- Plotly

## Estrutura atual

```text
.
├── .streamlit/
│   └── config.toml
├── assets/
│   └── readme-banner.svg
├── datasets/
│   ├── app.py
│   ├── cyberdeck/
│   │   ├── __init__.py
│   │   ├── analysis.py
│   │   ├── data_loader.py
│   │   └── ui.py
│   ├── sample_books.csv
│   ├── sample_reviews.csv
│   └── README.md
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

## Como rodar localmente

O projeto já inclui dados de exemplo anonimizados, então pode ser executado logo após a instalação.

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o app:

```bash
streamlit run datasets/app.py
```

Depois de abrir o app, você pode:

- usar os dados de exemplo;
- enviar seus próprios CSVs pela barra lateral;
- buscar termos específicos dentro das reviews;
- comparar livros;
- baixar os resultados filtrados;
- trocar filtros sem depender de qualquer API externa.

## Testes

Execute os testes locais das heurísticas com:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Usando dados locais completos

Para usar uma base local completa, coloque estes arquivos dentro da pasta `datasets/`:

- `Top-100 Trending Books.csv`
- `customer reviews.csv`

Esses arquivos estão no `.gitignore` e não devem ser publicados no GitHub.

## Deploy gratuito

O projeto está preparado para Streamlit Community Cloud.

Configuração sugerida:

- Repositório: `marcusguedess/projeto_retro`
- Branch: `main`
- Main file path: `datasets/app.py`

Não é necessário cadastrar secrets para a versão pública com samples.

## Segurança e dados

- Não há chaves de API, tokens ou credenciais no código.
- Arquivos `.env`, logs, cache Python e `secrets.toml` estão ignorados no Git.
- CSVs brutos estão ignorados para evitar publicar dados de terceiros ou conteúdo pessoal de reviews.
- Amostras anonimizadas permitem testes públicos sem expor dados reais.
- Uploads são limitados a 50 MB pela configuração do Streamlit.
- A busca por título é tratada como texto literal, não como expressão regular.
- A busca nas reviews também é literal, evitando execução de padrões regex fornecidos pelo usuário.
- O HTML permitido via `unsafe_allow_html=True` é usado apenas com conteúdo estático ou valores controlados pelo app.
- Exportações CSV neutralizam células iniciadas por `=`, `+`, `-` ou `@`.

## Custo

Esta versão foi pensada para custo zero:

- não usa API paga;
- não usa LLM;
- não consome tokens;
- não faz scraping da Amazon;
- roda localmente com Streamlit, Pandas e Plotly.

Para dados mais atuais, o caminho recomendado é usar CSVs próprios, datasets públicos permitidos ou, futuramente, integrações oficiais quando houver credenciais e autorização adequadas.

## Autoria e licença

Este projeto é autoral de **Marcus Guedes**.

O código está público para visualização, estudo e teste do projeto, mas não está liberado como licença open-source permissiva. Todos os direitos estão reservados, salvo autorização expressa do autor.

## Próximos passos

- Adicionar testes automatizados para as heurísticas.
- Criar conectores seguros para fontes públicas permitidas.
- Melhorar o modelo local de score com mais sinais estatísticos.
- Adicionar busca textual nas reviews.
- Adicionar versão em inglês.
- Criar screenshots oficiais para o README após o deploy.

## Observação

Este projeto ainda está em conclusão e foi criado como experimento pessoal. A versão atual é um protótipo funcional para testes, demonstração de UI e validação da ideia.
