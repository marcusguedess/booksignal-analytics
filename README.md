# BookSignal Analytics

BookSignal Analytics é um projeto de portfólio para decisão editorial. Ele combina metadados de livros, preço, rating e sinais de confiança para indicar quais títulos devem ser promovidos, auditados ou mantidos em observação.

O projeto não tenta coletar dados automaticamente de Amazon, Mercado Livre ou lojas editoriais. Essas fontes dependem de APIs oficiais, permissão de uso, exportações autorizadas ou contratos de dados. A proposta aqui é mostrar a etapa de análise depois da ingestão: o usuário pode testar a demo com dados de amostra ou importar um CSV local no navegador.

O projeto tem duas camadas:

- um pipeline Python que limpa CSVs e exporta um contrato JSON;
- uma interface em Next.js que apresenta recomendações acionáveis, ranking explicável, benchmarks por categoria e importação local de CSV.

## Interface

A interface foi reformulada como uma mesa de decisão:

- `Promover`: títulos com boa combinação de preço, rating e confiança.
- `Auditar`: títulos que exigem leitura manual de reviews ou validação da base.
- `Observar`: títulos úteis, mas ainda sem prioridade clara.
- `Importar CSV`: leitura local no navegador, sem envio para servidor.

Colunas aceitas no CSV:

```csv
title,author,genre,price,rating,reviews,verifiedPct,qualityScore
Livro Exemplo,Autora Exemplo,Fiction,19.90,4.6,128,82,78
```

Também são aceitos alguns nomes em português, como `titulo`, `autor`, `genero`, `preco`, `nota` e `avaliacoes`.

## Glossário Rápido

- `Scraping`: copiar dados automaticamente de páginas de um site. Pode quebrar com mudanças de layout, ser bloqueado por captcha/rate limit ou violar termos de uso.
- `Crawler`: programa que navega por páginas para encontrar ou coletar informações.
- `API`: acesso oficial que um serviço oferece para outros sistemas usarem seus dados.
- `CSV`: planilha simples em texto, compatível com Excel, Google Sheets e sistemas internos.
- `Score`: pontuação calculada para comparar itens. No BookSignal Analytics, combina nota, preço, reviews e confiança.
- `Rating`: nota média dada por leitores, normalmente de 1 a 5 estrelas.
- `Review`: avaliação escrita por leitor.
- `Benchmark`: comparação com uma média de referência, como a média do gênero.

As imagens abaixo foram capturadas a partir do build estático de produção.

![Dashboard desktop do BookSignal](assets/screenshots/dashboard-desktop.png)

Versão mobile:

![Dashboard mobile do BookSignal](assets/screenshots/dashboard-mobile.png)

## Perguntas Que O Projeto Responde

- Quais livros são bons candidatos para promoção ou curadoria?
- Quais livros precisam de auditoria antes de entrar em campanha?
- Quais gêneros mostram melhor relação entre preço, rating e qualidade das reviews?
- O que a ferramenta consegue concluir quando só existe uma base exportada pelo usuário?

## Estrutura

```text
.
├── analytics/
│   └── export_booksignal.py        # Gera o JSON do dashboard
├── datasets/
│   ├── booksignal/                 # Funções Python de análise
│   ├── sample_books.csv
│   └── sample_reviews.csv
├── docs/
│   ├── ARQUITETURA.md
│   ├── METODOLOGIA.md
│   └── CHECKLIST_PUBLICACAO.md
├── scripts/
│   └── validate.ps1
├── tests/
│   ├── test_analysis.py
│   └── test_export_booksignal.py
└── web/
    ├── src/app/
    ├── src/components/dashboard.tsx
    └── src/data/booksignal.json
```

## Stack

- Python e Pandas para preparação dos dados.
- Next.js, React e TypeScript para a interface.
- Export estático para GitHub Pages.
- GitHub Actions para testes, lint, typecheck e publicação.

## Como Rodar

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

Gere os dados do dashboard:

```bash
python analytics/export_booksignal.py
```

Rode a interface:

```bash
cd web
npm install
npm run dev
```

Abra `http://localhost:3000`.

## Validação

Testes Python:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Checks do frontend:

```bash
cd web
npm run lint
npm run typecheck
npm run build
```

Validação completa no Windows:

```powershell
.\scripts\validate.ps1
```

## GitHub Pages

O app Next.js está configurado para export estático. Para simular um build local com o caminho do repositório:

```powershell
.\scripts\validate.ps1 -BasePath "/NOME_DO_REPOSITORIO" -SiteUrl "https://USUARIO.github.io/NOME_DO_REPOSITORIO"
```

O artefato final é gerado em `web/out`.

O workflow `.github/workflows/pages.yml` executa exportação dos dados, testes Python, lint, typecheck e build estático antes de publicar no GitHub Pages.

## Observações Sobre Dados

O repositório inclui CSVs de amostra para demonstração. Bases brutas de terceiros não devem ser commitadas sem licença, permissão de uso e revisão de privacidade.

Marketplaces e livrarias online costumam ter termos de uso, bloqueios técnicos e restrições de redistribuição. Por isso, o projeto evita scraping automático e trabalha com dados autorizados, dados públicos permitidos ou arquivos exportados pelo usuário.

O score de qualidade das reviews é uma heurística local. Ele destaca evidências fracas, como texto curto, review não verificada e rating extremo, mas não deve ser interpretado como detecção de fraude.

## Documentação

- [Arquitetura](docs/ARQUITETURA.md)
- [Metodologia](docs/METODOLOGIA.md)
- [Checklist de publicação](docs/CHECKLIST_PUBLICACAO.md)
