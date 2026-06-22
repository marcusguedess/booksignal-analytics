"use client";

// mão do Marcus Guedes
import { useMemo, useState } from "react";
import type { Book, DashboardData, DistributionRow } from "@/data/contract";

type SortKey = "valueScore" | "qualityScore" | "reviews" | "rating";
type DecisionMode = "promote" | "audit" | "value" | "category";
type ViewKey = "overview" | "ranking" | "reviews" | "data" | "methodology";

const sortLabels: Record<SortKey, string> = {
  valueScore: "Oportunidade",
  qualityScore: "Confiança",
  reviews: "Volume",
  rating: "Rating",
};

const modeLabels: Record<DecisionMode, string> = {
  promote: "Promover agora",
  audit: "Auditar risco",
  value: "Achar barganhas",
  category: "Explorar categoria",
};

const viewLabels: Record<ViewKey, string> = {
  overview: "Visão geral",
  ranking: "Ranking",
  reviews: "Reviews",
  data: "Dados",
  methodology: "Metodologia",
};

function modeScore(book: Book, mode: DecisionMode) {
  if (mode === "audit") {
    return book.reviewsToAudit * 35 + book.ratingStd * 25 + (100 - book.qualityScore);
  }
  if (mode === "value") {
    return book.scoreBreakdown.price * 0.42 + book.rating * 12 + book.qualityScore * 0.34;
  }
  if (mode === "category") {
    return book.reviews * 4 + book.qualityScore * 0.45 + book.rating * 12;
  }
  return book.valueScore;
}

function decisionCopy(book: Book, mode: DecisionMode) {
  if (mode === "audit") {
    if (book.reviewsToAudit > 0 || book.ratingStd >= 1) {
      return "Prioridade de auditoria: há dispersão ou sinais de baixa qualidade que precisam ser lidos antes de promoção.";
    }
    return "Baixo risco de auditoria na amostra atual, com boa consistência entre qualidade e avaliações.";
  }
  if (mode === "value") {
    return "Leitura de barganha: combina preço, rating e qualidade para encontrar livros eficientes para curadoria.";
  }
  if (mode === "category") {
    return "Leitura de categoria: prioriza força social, volume e confiança para orientar exploração editorial.";
  }
  if (book.qualityScore >= 85 && book.valueScore >= 120) {
    return "Candidato forte para destaque: combina preço competitivo, bom rating e base de reviews confiável.";
  }
  return "Candidato exige revisão adicional antes de priorização comercial.";
}

function formatNumber(value: number, digits = 0) {
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  }).format(value);
}

function maxValue(rows: DistributionRow[], key: keyof DistributionRow = "count") {
  return Math.max(...rows.map((row) => Number(row[key]) || 0), 1);
}

export function Dashboard({ data }: { data: DashboardData }) {
  const genres = useMemo(
    () => ["Todos", ...Array.from(new Set(data.books.map((book) => book.genre))).sort()],
    [data.books],
  );
  const [genre, setGenre] = useState("Todos");
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("valueScore");
  const [decisionMode, setDecisionMode] = useState<DecisionMode>("promote");
  const [activeView, setActiveView] = useState<ViewKey>("overview");
  const [selectedTitle, setSelectedTitle] = useState(data.books[0]?.title ?? "");

  const filteredBooks = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return data.books
      .filter((book) => genre === "Todos" || book.genre === genre)
      .filter((book) => {
        if (!needle) return true;
        return `${book.title} ${book.author} ${book.genre} ${book.rawGenre}`
          .toLowerCase()
          .includes(needle);
      })
      .sort((a, b) => {
        if (decisionMode === "promote") return b[sortKey] - a[sortKey];
        return modeScore(b, decisionMode) - modeScore(a, decisionMode);
      });
  }, [data.books, decisionMode, genre, query, sortKey]);

  const selectedBook =
    filteredBooks.find((book) => book.title === selectedTitle) ?? filteredBooks[0] ?? data.books[0];

  const selectedReviews = data.recentReviews
    .filter((review) => review.book === selectedBook?.title)
    .slice(0, 4);

  const ratingMax = maxValue(data.ratingDistribution);
  const trustMax = maxValue(data.trustDistribution);
  const topGenres = [...data.genres].sort((a, b) => b.avg_value - a.avg_value).slice(0, 6);
  const genreMax = Math.max(...topGenres.map((row) => row.avg_value), 1);
  const selectedGenre = data.genres.find((row) => row.genre_group === selectedBook?.genre);
  const qualityRows = data.dataQuality.tables.slice();
  const visibleBooks = filteredBooks.slice(0, activeView === "ranking" ? 18 : 10);

  return (
    <main className="shell">
      <section className="hero">
        <div className="hero__content">
          <p className="eyebrow">BookSignal Analytics</p>
          <h1>Inteligência visual para catálogo editorial e qualidade de reviews.</h1>
          <p className="hero__copy">
            Um painel de decisão para identificar livros promissores, auditar sinais fracos
            nas avaliações e transformar uma base bruta em leitura de mercado.
          </p>
          <div className="hero__meta" aria-label="Fontes de dados">
            <span>Livros: {data.sources.books}</span>
            <span>Reviews: {data.sources.reviews}</span>
            <span>{data.sources.reviewPeriod}</span>
            <span>Atualização: {data.sources.dataAge}</span>
            <span>Gênero líder: {data.summary.topGenre}</span>
            <span>Livro líder: {data.summary.topBook}</span>
          </div>
        </div>
        <div className="radar" aria-hidden="true">
          <div className="radar__orb" />
          <div className="radar__grid">
            {data.books.slice(0, 24).map((book, index) => (
              <span
                key={book.title}
                style={{
                  left: `${8 + ((index * 19) % 82)}%`,
                  top: `${12 + ((index * 31) % 74)}%`,
                  opacity: 0.28 + book.qualityScore / 160,
                  transform: `scale(${0.65 + book.valueScore / 260})`,
                }}
              />
            ))}
          </div>
        </div>
      </section>

      <section className="metrics" aria-label="Métricas principais">
        <Metric label="Livros" value={data.metrics.books.toString()} hint="catálogo normalizado" />
        <Metric label="Reviews" value={data.metrics.reviews.toString()} hint="amostra auditável" />
        <Metric label="Rating médio" value={data.metrics.avgRating.toFixed(2)} hint="base filtrada" />
        <Metric label="Score de qualidade" value={`${data.metrics.qualityScore.toFixed(1)}`} hint="média das reviews" />
      </section>

      <section className="command">
        <div>
          <p className="section-kicker">Controle de análise</p>
          <h2>Explore o catálogo por intenção de decisão.</h2>
        </div>
        <div className="filters">
          <input
            aria-label="Buscar livro, autor ou gênero"
            placeholder="Buscar livro, autor ou gênero"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <select aria-label="Filtrar gênero" value={genre} onChange={(event) => setGenre(event.target.value)}>
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
          <select
            aria-label="Modo de decisão"
            value={decisionMode}
            onChange={(event) => setDecisionMode(event.target.value as DecisionMode)}
          >
            {Object.entries(modeLabels).map(([key, label]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </select>
        </div>
      </section>

      <nav className="view-tabs" aria-label="Seções do dashboard">
        {Object.entries(viewLabels).map(([key, label]) => (
          <button
            className={activeView === key ? "is-active" : ""}
            key={key}
            type="button"
            onClick={() => setActiveView(key as ViewKey)}
          >
            {label}
          </button>
        ))}
      </nav>

      {activeView === "overview" ? (
      <section className="opportunities">
        {Object.entries(data.opportunityCards).map(([label, title]) => {
          const book = data.books.find((item) => item.title === title);
          return (
            <button
              className="opportunity"
              key={label}
              type="button"
              onClick={() => title && setSelectedTitle(title)}
            >
              <span>{label}</span>
              <strong>{title ?? "Sem dados"}</strong>
              {book ? <small>{book.genre} · {book.qualityScore.toFixed(0)}/100 confiança</small> : null}
            </button>
          );
        })}
      </section>
      ) : null}

      {activeView === "overview" || activeView === "ranking" ? (
      <section className="dashboard-grid">
        <div className="panel panel--large">
          <div className="panel__header">
            <div>
              <p className="section-kicker">Ranking</p>
              <h2>Prioridade comercial</h2>
            </div>
            <span>{filteredBooks.length} livros</span>
          </div>
          <div className="book-list">
            {visibleBooks.map((book, index) => (
              <button
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
                <span className="book-score">
                  {formatNumber(modeScore(book, decisionMode), 1)}
                  <small>score</small>
                </span>
              </button>
            ))}
          </div>
        </div>

        <aside className="panel insight">
          <p className="section-kicker">Livro selecionado</p>
          <h2>{selectedBook?.title}</h2>
          <p>{selectedBook?.author.trim()} · {selectedBook?.rawGenre}</p>
          <div className="insight__stats">
            <Stat label="Preço" value={`$${selectedBook?.price.toFixed(2)}`} />
            <Stat label="Rating" value={selectedBook?.rating.toFixed(1) ?? "0"} />
            <Stat label="Reviews" value={selectedBook?.reviews.toString() ?? "0"} />
            <Stat label="Confiança" value={`${selectedBook?.qualityScore.toFixed(0) ?? "0"}/100`} />
          </div>
          {selectedGenre ? (
            <div className="decision decision--secondary">
              <strong>Benchmark da categoria</strong>
              <p>
                Média do gênero: rating {selectedGenre.avg_rating.toFixed(2)}, confiança{" "}
                {selectedGenre.avg_quality.toFixed(1)} e score {selectedGenre.avg_value.toFixed(1)}.
              </p>
            </div>
          ) : null}
          <div className="decision">
            <strong>Leitura de decisão</strong>
            <p>{selectedBook ? decisionCopy(selectedBook, decisionMode) : "Selecione um livro para detalhar."}</p>
          </div>
          {selectedBook ? (
            <div className="score-breakdown" aria-label="Decomposição do score">
              <ScorePart label="Rating" value={selectedBook.scoreBreakdown.rating} />
              <ScorePart label="Preço" value={selectedBook.scoreBreakdown.price} />
              <ScorePart label="Reviews" value={selectedBook.scoreBreakdown.reviewQuality} />
              <ScorePart label="Evidência" value={selectedBook.scoreBreakdown.evidence} />
            </div>
          ) : null}
        </aside>
      </section>
      ) : null}

      {activeView === "overview" || activeView === "data" ? (
      <section className="analytics-grid">
        <ChartPanel title="Gêneros com melhor oportunidade">
          {topGenres.map((row) => (
            <Bar
              key={row.genre_group}
              label={row.genre_group}
              value={row.avg_value}
              max={genreMax}
              suffix="score"
            />
          ))}
        </ChartPanel>

        <ChartPanel title="Distribuição de ratings">
          {data.ratingDistribution.map((row) => (
            <Bar
              key={row.rating}
              label={`${row.rating} estrelas`}
              value={row.count}
              max={ratingMax}
              suffix="reviews"
            />
          ))}
        </ChartPanel>

        <ChartPanel title="Qualidade das reviews">
          {data.trustDistribution.map((row) => (
            <Bar
              key={row.label}
              label={row.label ?? ""}
              value={row.count}
              max={trustMax}
              suffix="reviews"
            />
          ))}
        </ChartPanel>
      </section>
      ) : null}

      {activeView === "data" || activeView === "methodology" ? (
      <section className="quality-grid">
        <div className="panel">
          <p className="section-kicker">Qualidade da base</p>
          <h2>O que sustenta a leitura</h2>
          <div className="quality-stats">
            <Stat label="Completude" value={`${data.dataQuality.completeness.toFixed(1)}%`} />
            <Stat label="Células vazias" value={data.dataQuality.emptyCells.toString()} />
            <Stat label="Duplicatas" value={data.dataQuality.duplicates.toString()} />
            <Stat label="Gêneros normalizados" value={`${data.dataQuality.genreBuckets}/${data.dataQuality.rawGenreLabels}`} />
          </div>
        </div>
        <div className="panel methodology">
          <p className="section-kicker">Metodologia</p>
          <h2>Score com pesos visíveis</h2>
          <p>
            O ranking combina rating, preço, qualidade das reviews e força da evidência.
            Os modos de decisão mudam os pesos para promoção, auditoria, barganha ou categoria.
          </p>
          <div className="quality-table">
            <div className="quality-table__head" aria-hidden="true">
              <span>Área</span>
              <span>Linhas</span>
              <span>Colunas</span>
              <span>Vazias</span>
              <span>Duplicatas</span>
            </div>
            {qualityRows.map((row) => (
              <div className="quality-table__row" key={String(row["Área"])}>
                <strong>{String(row["Área"])}</strong>
                <span className="quality-pill">
                  <strong>{String(row["Linhas"])}</strong>
                  <small>linhas</small>
                </span>
                <span className="quality-pill">
                  <strong>{String(row["Colunas"])}</strong>
                  <small>colunas</small>
                </span>
                <span className="quality-pill">
                  <strong>{String(row["Células vazias"])}</strong>
                  <small>vazias</small>
                </span>
                <span className="quality-pill">
                  <strong>{String(row["Duplicatas"])}</strong>
                  <small>duplicatas</small>
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>
      ) : null}

      {activeView === "reviews" ? (
      <section className="panel">
        <div className="panel__header">
          <div>
            <p className="section-kicker">Amostra auditável</p>
            <h2>Reviews recentes do livro selecionado</h2>
          </div>
          <span>{selectedReviews.length || "sem"} registros</span>
        </div>
        <div className="review-grid">
          {(selectedReviews.length ? selectedReviews : data.recentReviews.slice(0, 4)).map((review) => (
            <article className="review-card" key={`${review.book}-${review.title}-${review.date}`}>
              <div>
                <strong>{review.title}</strong>
                <span>{review.book}</span>
              </div>
              <p>{review.reasons}</p>
              <footer>
                <span>{review.rating} estrelas</span>
                <span>{review.qualityScore}/100</span>
                <span>{review.verified ? "verificada" : "não verificada"}</span>
              </footer>
            </article>
          ))}
        </div>
      </section>
      ) : null}

      {activeView === "methodology" ? (
        <section className="method-grid">
          <article className="panel method-card">
            <p className="section-kicker">Leitura do score</p>
            <h2>O ranking é comparativo</h2>
            <p>
              O score organiza prioridades dentro da amostra carregada. Ele não substitui
              leitura editorial, contrato de dados ou análise comercial externa.
            </p>
          </article>
          <article className="panel method-card">
            <p className="section-kicker">Sinais de review</p>
            <h2>Confiança é evidência textual</h2>
            <p>
              Reviews curtas, não verificadas ou extremas reduzem confiança. O painel aponta
              registros para leitura manual, sem classificar fraude.
            </p>
          </article>
          <article className="panel method-card">
            <p className="section-kicker">Uso operacional</p>
            <h2>Fonte e data importam</h2>
            <p>
              Em bases reais, preço, rating e reviews precisam carregar origem, permissão de
              uso e data de coleta. O build público usa amostras estáticas.
            </p>
          </article>
        </section>
      ) : null}
    </main>
  );
}

function Metric({ label, value, hint }: { label: string; value: string; hint: string }) {
  return (
    <article className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{hint}</small>
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
        <span style={{ width: `${Math.max(4, value)}%` }} />
      </div>
    </div>
  );
}

function ChartPanel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="panel chart-panel">
      <h2>{title}</h2>
      <div className="bars">{children}</div>
    </div>
  );
}

function Bar({
  label,
  value,
  max,
  suffix,
}: {
  label: string;
  value: number;
  max: number;
  suffix: string;
}) {
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
