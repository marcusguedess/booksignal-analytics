# Cyberdeck Retro - Revisor de Reviews de Livros

Projeto desenvolvido **for fun** para explorar dados de livros e reviews em um painel visual inspirado em cyberdecks, arcade retrofuturista e Night City.

A ideia original era evoluir para um revisor/analista de reviews de livros com dados atualizados em tempo real. Como a prioridade atual é manter o projeto gratuito, seguro e sem gasto com tokens ou APIs pagas, esta versão trabalha com CSVs locais, upload manual de dados e amostras públicas anonimizadas.

Por segurança e privacidade, os CSVs brutos não são versionados por padrão. Bases de reviews podem conter nomes de revisores, textos com informações pessoais e conteúdo sujeito aos termos de uso da fonte original. Para manter o projeto testável no GitHub, o repositório inclui amostras anonimizadas.

## Status

Em desenvolvimento.

Esta é uma versão revisada do protótipo inicial. O app já pode ser clonado e executado por qualquer pessoa usando os dados de exemplo, mas ainda há melhorias planejadas para futuras integrações oficiais e análises mais profundas.

## O que o projeto faz

- Carrega dados de livros e reviews a partir de arquivos CSV.
- Permite upload de CSV direto pela interface.
- Usa dados locais quando existirem.
- Usa amostras públicas anonimizadas quando os CSVs reais não estiverem disponíveis.
- Permite filtrar livros por gênero, título, preço máximo e avaliação mínima.
- Permite visualizar apenas reviews verificadas.
- Exibe métricas gerais sobre livros, avaliações e reviews.
- Gera gráficos interativos com Plotly.
- Mostra livros em destaque, reviews recentes e livros mais comentados.
- Sinaliza reviews potencialmente frágeis com uma heurística local simples.
- Permite baixar os livros e reviews filtrados.
- Exibe um console visual do projeto com status da fonte de dados.

## Escolha de design

Cyberpunk sempre. Hahaha.

A interface foi criada para parecer um cyberdeck: fundo escuro, luzes neon, contraste alto, botões coloridos, chips de status, painéis de métricas e uma sensação arcade. A intenção é que a pessoa entenda rapidamente os filtros e gráficos, mas ainda sinta que está navegando em um painel saído de Night City.

O design prioriza:

- leitura simples;
- filtros claros;
- métricas visíveis logo no topo;
- gráficos com cores fortes;
- ações diretas para upload e download;
- visual cyberpunk sem tornar a interface confusa.

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
│   ├── sample_books.csv
│   ├── sample_reviews.csv
│   └── README.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Como rodar localmente

O projeto já inclui dados de exemplo anonimizados, então pode ser executado logo após a instalação.

Para usar a base completa local, coloque os arquivos CSV brutos dentro da pasta `datasets/`:

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

Depois de abrir o app, você pode:

- usar os dados de exemplo;
- enviar seus próprios CSVs pela barra lateral;
- baixar os resultados filtrados;
- trocar filtros sem depender de qualquer API externa.

## Segurança e dados

- Não há chaves de API, tokens ou credenciais no código.
- Arquivos `.env`, logs, cache Python e `secrets.toml` estão ignorados no Git.
- Os CSVs brutos estão ignorados para evitar publicar dados de terceiros ou conteúdo pessoal de reviews.
- Amostras anonimizadas foram incluídas para permitir testes públicos do projeto.
- A busca por título é tratada como texto literal, não como expressão regular.
- O HTML permitido via `unsafe_allow_html=True` é usado apenas com conteúdo estático do próprio app.

## Custo

Esta versão foi pensada para custo zero:

- não usa API paga;
- não usa LLM;
- não consome tokens;
- não faz scraping da Amazon;
- roda localmente com Streamlit, Pandas e Plotly.

Para dados mais atuais, o caminho recomendado é usar CSVs próprios, datasets públicos permitidos ou, futuramente, integrações oficiais quando houver credenciais e autorização adequadas.

## Próximos passos

- Integrar uma fonte de dados atualizada em tempo real.
- Melhorar a organização do código e separar responsabilidades.
- Refinar as análises de reviews.
- Adicionar tratamento de erros para arquivos ausentes ou dados incompletos.
- Evoluir a experiência visual mantendo a identidade cyberpunk.
- Criar conectores seguros para fontes públicas ou oficiais.
- Adicionar mais heurísticas locais para qualidade de reviews.

## Observação

Este projeto ainda está em conclusão e foi criado como experimento pessoal. A versão atual é um protótipo funcional para testes e validação da ideia.
