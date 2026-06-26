"use client";

import { useMemo, useState } from "react";
import type { ChangeEvent, ReactNode } from "react";
import type { Book, DashboardData, DistributionRow, GenreRow } from "@/data/contract";

type DecisionMode = "promote" | "audit" | "value";
type SortKey = "decision" | "valueScore" | "qualityScore" | "reviews" | "rating";

const modeLabels: Record<DecisionMode, string> = {
  promote: "Promover",
  audit: "Auditar",
  value: "Barganhas",
};

const modeDescriptions: Record<DecisionMode, string> = {
  promote: "Destaque títulos com sinal consistente.",
  audit: "Encontre sinais que pedem revisão humana.",
  value: "Compare preço, nota e evidências.",
};

const decisionModes: DecisionMode[] = ["promote", "audit", "value"];

const sortLabels: Record<SortKey, string> = {
  decision: "Recomendação",
  valueScore: "Score",
  qualityScore: "Confiança",
  reviews: "Reviews",
  rating: "Rating",
};

function formatNumber(value: number, digits = 0) {
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  }).format(value);
}

function modeScore(book: Book, mode: DecisionMode) {
  if (mode === "audit") {
    return book.reviewsToAudit * 35 + book.ratingStd * 25 + (100 - book.qualityScore);
  }
  if (mode === "value") {
    return book.scoreBreakdown.price * 0.42 + book.rating * 12 + book.qualityScore * 0.34;
  }
  return book.valueScore;
}

function recommendation(book: Book) {
  if (book.qualityScore >= 75 && book.valueScore >= 115 && book.reviewsToAudit === 0) {
    return {
      label: "Promover",
      tone: "strong",
      reason: "Bom equilibrio entre rating, preco e confianca das evidencias.",
    };
  }
  if (book.reviewsToAudit > 0 || book.qualityScore < 62 || book.ratingStd >= 1) {
    return {
      label: "Auditar",
      tone: "warn",
      reason: "Antes de destacar, leia as reviews com baixa confianca ou alta dispersao.",
    };
  }
  return {
    label: "Observar",
    tone: "neutral",
    reason: "Tem sinais uteis, mas ainda nao e uma prioridade clara.",
  };
}

function decisionCopy(book: Book, mode: DecisionMode) {
  const rec = recommendation(book);
  if (mode === "audit") {
    return rec.label === "Auditar"
      ? "Prioridade de auditoria: a amostra pede leitura manual antes de qualquer acao comercial."
      : "Baixo risco aparente na amostra atual, mas a decisao ainda depende da origem dos dados.";
  }
  if (mode === "value") {
    return "Leitura de barganha: prioriza preco competitivo sem ignorar rating e confianca.";
  }
  return rec.reason;
}

function maxValue(rows: DistributionRow[], key: keyof DistributionRow = "count") {
  return Math.max(...rows.map((row) => Number(row[key]) || 0), 1);
}

function parseCsv(text: string) {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (char === '"' && quoted && next === '"') {
      cell += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(cell.trim());
      cell = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") index += 1;
      row.push(cell.trim());
      if (row.some(Boolean)) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }

  row.push(cell.trim());
  if (row.some(Boolean)) rows.push(row);
  return rows;
}

function numberFrom(value: string | undefined, fallback = 0) {
  if (!value) return fallback;
  const parsed = Number(value.replace(",", ".").replace(/[^\d.-]/g, ""));
  return Number.isFinite(parsed) ? parsed : fallback;
}

function normalizeHeader(value: string) {
  return value.trim().toLowerCase().replace(/\s+/g, "_");
}

function percentilePrice(price: number, maxPrice: number) {
  if (maxPrice <= 0) return 50;
  return Math.max(0, Math.min(100, 100 - (price / maxPrice) * 80));
}

function buildImportedData(source: DashboardData, text: string): DashboardData {
  const rows = parseCsv(text);
  if (rows.length < 2) throw new Error("O CSV precisa ter cabecalho e pelo menos um livro.");

  const headers = rows[0].map(normalizeHeader);
  const records = rows.slice(1).map((row) =>
    Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ""])),
  );
  const maxPrice = Math.max(...records.map((row) => numberFrom(row.price || row.preco, 0)), 1);

  const books: Book[] = records.map((row, index) => {
    const title = row.title || row.titulo || row.book || row.livro || `Livro ${index + 1}`;
    const author = row.author || row.autor || "Autor nao informado";
    const genre = row.genre || row.genero || row.category || row.categoria || "Sem categoria";
    const rawGenre = row.rawgenre || row.genero_original || genre;
    const price = numberFrom(row.price || row.preco, 0);
    const rating = Math.max(0, Math.min(5, numberFrom(row.rating || row.nota, 0)));
    const reviews = Math.max(0, Math.round(numberFrom(row.reviews || row.avaliacoes, 0)));
    const qualityScore = Math.max(
      25,
      Math.min(92, numberFrom(row.qualityscore || row.confianca, 55 + Math.min(reviews, 20) * 1.4)),
    );
    const verifiedPct = Math.max(0, Math.min(100, numberFrom(row.verifiedpct || row.verificadas, 0)));
    const reviewsToAudit = qualityScore < 62 || verifiedPct < 40 ? 1 : 0;
    const ratingStd = reviewsToAudit ? 1 : 0;
    const scoreBreakdown = {
      rating: rating * 20,
      price: percentilePrice(price, maxPrice),
      reviewQuality: qualityScore,
      evidence: Math.min(100, reviews * 10),
    };
    const valueScore =
      scoreBreakdown.rating * 0.42 +
      scoreBreakdown.price * 0.28 +
      scoreBreakdown.reviewQuality * 0.22 +
      scoreBreakdown.evidence * 0.08;

    return {
      title,
      author,
      genre,
      rawGenre,
      price,
      rating,
      reviews,
      verifiedPct,
      qualityScore,
      reviewsToAudit,
      valueScore,
      ratingStd,
      scoreBreakdown,
      genreBenchmark: { rating, quality: qualityScore, value: valueScore },
    };
  });

  const genres = Array.from(new Set(books.map((book) => book.genre))).map((genre): GenreRow => {
    const group = books.filter((book) => book.genre === genre);
    return {
      genre_group: genre,
      books: group.length,
      avg_rating: group.reduce((sum, book) => sum + book.rating, 0) / group.length,
      avg_quality: group.reduce((sum, book) => sum + book.qualityScore, 0) / group.length,
      avg_value: group.reduce((sum, book) => sum + book.valueScore, 0) / group.length,
      reviews: group.reduce((sum, book) => sum + book.reviews, 0),
    };
  });

  const ratingDistribution = [1, 2, 3, 4, 5].map((rating) => ({
    rating,
    count: books.filter((book) => Math.round(book.rating) === rating).length,
  }));
  const auditable = books.filter((book) => recommendation(book).label === "Auditar").length;

  return {
    ...source,
    generatedAt: new Date().toISOString(),
    sources: {
      books: "CSV importado no navegador",
      reviews: "Nao importadas",
      reviewPeriod: "Sessao local",
      dataAge: "agora",
    },
    metrics: {
      books: books.length,
      reviews: books.reduce((sum, book) => sum + book.reviews, 0),
      avgRating: books.reduce((sum, book) => sum + book.rating, 0) / books.length,
      verifiedPct: 0,
      qualityScore: books.reduce((sum, book) => sum + book.qualityScore, 0) / books.length,
      reviewsToAudit: auditable,
    },
    summary: {
      topGenre: genres.sort((a, b) => b.avg_value - a.avg_value)[0]?.genre_group ?? "Sem categoria",
      topBook: [...books].sort((a, b) => b.valueScore - a.valueScore)[0]?.title ?? "",
      booksWithReviews: books.filter((book) => book.reviews > 0).length,
      auditableBooks: auditable,
    },
    dataQuality: {
      completeness: 100,
      emptyCells: 0,
      duplicates: 0,
      genreBuckets: genres.length,
      rawGenreLabels: genres.length,
      tables: [
        {
          "Area": "CSV importado",
          "Linhas": books.length,
          "Colunas": headers.length,
          "Celulas vazias": records.reduce(
            (sum, row) => sum + Object.values(row).filter((value) => !value).length,
            0,
          ),
          "Duplicatas": books.length - new Set(books.map((book) => book.title)).size,
        },
      ],
    },
    opportunityCards: {
      "Promover primeiro": [...books].sort((a, b) => b.valueScore - a.valueScore)[0]?.title ?? null,
      "Auditar antes": [...books].sort((a, b) => modeScore(b, "audit") - modeScore(a, "audit"))[0]?.title ?? null,
      "Melhor barganha": [...books].sort((a, b) => modeScore(b, "value") - modeScore(a, "value"))[0]?.title ?? null,
    },
    books,
    genres,
    ratingDistribution,
    trustDistribution: [
      { label: "Promover", count: books.filter((book) => recommendation(book).label === "Promover").length },
      { label: "Auditar", count: auditable },
      { label: "Observar", count: books.filter((book) => recommendation(book).label === "Observar").length },
    ],
    recentReviews: [],
  };
}

export function Dashboard({ data: initialData }: { data: DashboardData }) {
  const [data, setData] = useState(initialData);
  const [genre, setGenre] = useState("Todos");
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("decision");
  const [decisionMode, setDecisionMode] = useState<DecisionMode>("promote");
  const [selectedTitle, setSelectedTitle] = useState(initialData.books[0]?.title ?? "");
  const [importStatus, setImportStatus] = useState("Demo carregada com dados de amostra.");

  const genres = useMemo(
    () => ["Todos", ...Array.from(new Set(data.books.map((book) => book.genre))).sort()],
    [data.books],
  );

  const filteredBooks = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return data.books
      .filter((book) => genre === "Todos" || book.genre === genre)
      .filter((book) => {
        if (!needle) return true;
        return `${book.title} ${book.author} ${book.genre} ${book.rawGenre}`.toLowerCase().includes(needle);
      })
      .sort((a, b) => {
        if (sortKey === "decision") return modeScore(b, decisionMode) - modeScore(a, decisionMode);
        return b[sortKey] - a[sortKey];
      });
  }, [data.books, decisionMode, genre, query, sortKey]);

  const selectedBook =
    filteredBooks.find((book) => book.title === selectedTitle) ?? filteredBooks[0] ?? data.books[0];
  const selectedReviews = data.recentReviews.filter((review) => review.book === selectedBook?.title).slice(0, 3);
  const topGenres = [...data.genres].sort((a, b) => b.avg_value - a.avg_value).slice(0, 6);
  const genreMax = Math.max(...topGenres.map((row) => row.avg_value), 1);
  const ratingMax = maxValue(data.ratingDistribution);
  const promoteCount = data.books.filter((book) => recommendation(book).label === "Promover").length;
  const auditCount = data.books.filter((book) => recommendation(book).label === "Auditar").length;
  const observeCount = data.books.length - promoteCount - auditCount;
  const decisionDistribution = [
    { label: "Promover", count: promoteCount },
    { label: "Auditar", count: auditCount },
    { label: "Observar", count: observeCount },
  ];
  const decisionMax = maxValue(decisionDistribution);
  const selectedGenre = data.genres.find((row) => row.genre_group === selectedBook?.genre);
  const hasActiveFilters = query.length > 0 || genre !== "Todos" || sortKey !== "decision";

  function resetFilters() {
    setGenre("Todos");
    setQuery("");
    setSortKey("decision");
  }

  function importText(text: string) {
    const imported = buildImportedData(initialData, text);
    setData(imported);
    setGenre("Todos");
    setQuery("");
    setSelectedTitle(imported.books[0]?.title ?? "");
    setImportStatus(`${imported.books.length} livros importados. Nada foi enviado para servidor.`);
  }

  function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    file
      .text()
      .then(importText)
      .catch(() => setImportStatus("Nao consegui ler o arquivo. Confira se ele esta em CSV UTF-8."));
  }

  const template =
    "title,author,genre,price,rating,reviews,verifiedPct,qualityScore\n" +
    "Livro Exemplo,Autora Exemplo,Fiction,19.90,4.6,128,82,78\n";

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand__mark" aria-hidden="true">BS</span>
          <div>
            <strong>BookSignal Analytics</strong>
            <span>Decisão editorial com CSV local</span>
          </div>
        </div>
        <span className="topbar__status">Amostra ativa</span>
      </header>

      <section className="hero">
        <div className="hero__content">
          <p className="eyebrow">Produto de dados para catálogo editorial</p>
          <h1>Da planilha para uma decisão editorial clara.</h1>
          <p className="hero__copy">
            Compare sinais de preço, avaliação e qualidade para decidir onde promover, onde revisar
            e o que manter em observação.
          </p>
          <div className="hero__actions">
            <label className="file-button">
              Importar CSV
              <input accept=".csv,text/csv" type="file" onChange={handleFile} />
            </label>
            <a
              className="ghost-button"
              download="booksignal-template.csv"
              href={`data:text/csv;charset=utf-8,${encodeURIComponent(template)}`}
            >
              Baixar template
            </a>
          </div>
          <p className="import-status" aria-live="polite">{importStatus}</p>
        </div>
        <div className="decision-board" aria-label="Resumo de decisoes">
          <DecisionTile label="Promover" value={promoteCount} tone="strong" />
          <DecisionTile label="Auditar" value={auditCount} tone="warn" />
          <DecisionTile label="Livros" value={data.metrics.books} tone="neutral" />
          <DecisionTile label="Reviews" value={data.metrics.reviews} tone="neutral" />
        </div>
      </section>

      <section className="context-bar" aria-label="Contexto dos dados">
        <div className="context-item">
          <span>Fonte</span>
          <strong>{data.sources.books}</strong>
        </div>
        <div className="context-item">
          <span>Período</span>
          <strong>{data.sources.reviewPeriod}</strong>
        </div>
        <div className="context-item">
          <span>Atualização</span>
          <strong>{data.sources.dataAge}</strong>
        </div>
        <details className="scope-details">
          <summary>Dados e limites</summary>
          <p>
            A análise começa após a ingestão. A demo processa CSVs localmente e não coleta dados de
            marketplaces ou lojas sem API, permissão ou exportação autorizada.
          </p>
        </details>
      </section>

      <section className="workspace" aria-labelledby="workspace-title">
        <div className="workspace__header">
          <div>
            <p className="section-kicker">Mesa de decisão</p>
            <h2 id="workspace-title">Escolha uma intenção e explore a base.</h2>
          </div>
          <span className="workspace__count">{data.metrics.books} títulos na base</span>
        </div>

        <div className="decision-tabs" role="group" aria-label="Intenção de decisão">
          {decisionModes.map((mode) => (
            <button
              aria-pressed={decisionMode === mode}
              className={`decision-tab ${decisionMode === mode ? "is-active" : ""}`}
              key={mode}
              onClick={() => setDecisionMode(mode)}
              type="button"
            >
              <strong>{modeLabels[mode]}</strong>
              <span>{modeDescriptions[mode]}</span>
            </button>
          ))}
        </div>

        <div className="filters">
          <input
            aria-label="Buscar livro, autor ou genero"
            placeholder="Buscar título, autor ou categoria"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <select aria-label="Filtrar genero" value={genre} onChange={(event) => setGenre(event.target.value)}>
            {genres.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
          <select aria-label="Ordenar ranking" value={sortKey} onChange={(event) => setSortKey(event.target.value as SortKey)}>
            {Object.entries(sortLabels).map(([key, label]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </select>
          {hasActiveFilters ? (
            <button className="clear-button" onClick={resetFilters} type="button">
              Limpar filtros
            </button>
          ) : (
            <span className="filters__hint">Ordenado por recomendação</span>
          )}
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="panel panel--large">
          <div className="panel__header">
            <div>
              <p className="section-kicker">Ranking acionável</p>
              <h2>{filteredBooks.length} livros encontrados</h2>
            </div>
            <span>{modeDescriptions[decisionMode]}</span>
          </div>
          {filteredBooks.length ? (
            <div className="book-list">
              {filteredBooks.map((book, index) => {
                const rec = recommendation(book);
                return (
                  <button
                    aria-pressed={book.title === selectedBook?.title}
                    className={`book-row ${book.title === selectedBook?.title ? "is-active" : ""}`}
                    key={book.title}
                    type="button"
                    onClick={() => setSelectedTitle(book.title)}
                  >
                    <span className="rank">{String(index + 1).padStart(2, "0")}</span>
                    <span className="book-main">
                      <strong>{book.title}</strong>
                      <small>{book.author.trim()} · {book.genre}</small>
                    </span>
                    <span className={`status status--${rec.tone}`}>{rec.label}</span>
                    <span className="book-score">
                      {formatNumber(modeScore(book, decisionMode), 1)}
                      <small>prioridade</small>
                    </span>
                  </button>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">
              <strong>Nenhum livro encontrado</strong>
              <p>Altere a busca ou limpe os filtros para voltar à base completa.</p>
              <button className="clear-button" onClick={resetFilters} type="button">Limpar filtros</button>
            </div>
          )}
        </div>

        <aside className="panel insight">
          <p className="section-kicker">Leitura recomendada</p>
          <h2>{selectedBook?.title}</h2>
          <p>
            {selectedBook?.author.trim()} · {selectedBook?.rawGenre}
          </p>
          {selectedBook ? <span className={`status status--${recommendation(selectedBook).tone}`}>{recommendation(selectedBook).label}</span> : null}
          <div className="insight__stats">
            <Stat label="Preco" value={`$${selectedBook?.price.toFixed(2)}`} />
            <Stat label="Rating medio" value={selectedBook?.rating.toFixed(1) ?? "0"} />
            <Stat label="Reviews" value={selectedBook?.reviews.toString() ?? "0"} />
            <Stat label="Confianca" value={`${selectedBook?.qualityScore.toFixed(0) ?? "0"}/100`} />
          </div>
          <div className="decision">
            <strong>Por que essa decisao?</strong>
            <p>{selectedBook ? decisionCopy(selectedBook, decisionMode) : "Selecione um livro para detalhar."}</p>
          </div>
          {selectedGenre ? (
            <div className="decision decision--secondary">
              <strong>Referência da categoria</strong>
              <p>
                Média de {selectedBook?.genre}: rating {selectedGenre.avg_rating.toFixed(2)}, confiança {selectedGenre.avg_quality.toFixed(1)}
                e score {selectedGenre.avg_value.toFixed(1)}.
              </p>
            </div>
          ) : null}
          {selectedBook ? (
            <div className="score-breakdown" aria-label="Decomposicao do score">
              <ScorePart label="Rating" value={selectedBook.scoreBreakdown.rating} />
              <ScorePart label="Preco" value={selectedBook.scoreBreakdown.price} />
              <ScorePart label="Reviews" value={selectedBook.scoreBreakdown.reviewQuality} />
              <ScorePart label="Evidencia" value={selectedBook.scoreBreakdown.evidence} />
            </div>
          ) : null}
        </aside>
      </section>

      <section className="analytics-grid">
        <ChartPanel title="Categorias com melhor sinal">
          {topGenres.map((row) => (
            <Bar key={row.genre_group} label={row.genre_group} value={row.avg_value} max={genreMax} suffix="score" />
          ))}
        </ChartPanel>
        <ChartPanel title="Distribuicao de ratings">
          {data.ratingDistribution.map((row) => (
            <Bar key={row.rating} label={`${row.rating} estrelas`} value={row.count} max={ratingMax} suffix="registros" />
          ))}
        </ChartPanel>
        <ChartPanel title="Saída da decisão">
          {decisionDistribution.map((row) => (
            <Bar key={row.label} label={row.label} value={row.count} max={decisionMax} suffix="livros" />
          ))}
        </ChartPanel>
      </section>

      <section className="details-grid">
        <details className="details-panel">
          <summary>Como a recomendação é calculada</summary>
          <p>O score combina rating, preço, volume de reviews e sinais de qualidade. Ele organiza a leitura da base, sem substituir uma decisão humana.</p>
        </details>
        <details className="details-panel">
          <summary>Campos aceitos no CSV</summary>
          <p>title, author, genre, price, rating, reviews, verifiedPct e qualityScore. Também são aceitos os nomes equivalentes em português.</p>
        </details>
      </section>

      {selectedReviews.length ? (
        <section className="panel">
          <div className="panel__header">
            <div>
              <p className="section-kicker">Evidencias</p>
              <h2>Reviews recentes do livro selecionado</h2>
            </div>
            <span>{selectedReviews.length} registros</span>
          </div>
          <div className="review-grid">
            {selectedReviews.map((review) => (
              <article className="review-card" key={`${review.book}-${review.title}-${review.date}`}>
                <div>
                  <strong>{review.title}</strong>
                  <span>{review.book}</span>
                </div>
                <p>{review.reasons}</p>
                <footer>
                  <span>{review.rating} estrelas</span>
                  <span>{review.qualityScore}/100</span>
                  <span>{review.verified ? "verificada" : "nao verificada"}</span>
                </footer>
              </article>
            ))}
          </div>
        </section>
      ) : null}
    </main>
  );
}

function DecisionTile({ label, value, tone }: { label: string; value: number; tone: string }) {
  return (
    <article className={`decision-tile decision-tile--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="stat">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ScorePart({ label, value }: { label: string; value: number }) {
  return (
    <div className="score-part">
      <div>
        <span>{label}</span>
        <strong>{value.toFixed(0)}</strong>
      </div>
      <div className="bar-track">
        <span style={{ width: `${Math.max(4, Math.min(100, value))}%` }} />
      </div>
    </div>
  );
}

function ChartPanel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="panel chart-panel">
      <h2>{title}</h2>
      <div className="bars">{children}</div>
    </div>
  );
}

function Bar({ label, value, max, suffix }: { label: string; value: number; max: number; suffix: string }) {
  const width = `${Math.max(6, (value / max) * 100)}%`;
  return (
    <div className="bar-row">
      <div className="bar-row__top">
        <span>{label}</span>
        <strong>
          {formatNumber(value, value % 1 === 0 ? 0 : 1)} {suffix}
        </strong>
      </div>
      <div className="bar-track">
        <span style={{ width }} />
      </div>
    </div>
  );
}
