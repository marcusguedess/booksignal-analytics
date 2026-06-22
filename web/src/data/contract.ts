export type Book = {
  title: string;
  author: string;
  genre: string;
  rawGenre: string;
  price: number;
  rating: number;
  reviews: number;
  verifiedPct: number;
  qualityScore: number;
  reviewsToAudit: number;
  valueScore: number;
  ratingStd: number;
  scoreBreakdown: {
    rating: number;
    price: number;
    reviewQuality: number;
    evidence: number;
  };
  genreBenchmark: {
    rating: number;
    quality: number;
    value: number;
  };
};

export type Review = {
  book: string;
  title: string;
  rating: number;
  verified: boolean;
  qualityScore: number;
  qualityLabel: string;
  reasons: string;
  words: number;
  date: string;
};

export type GenreRow = {
  genre_group: string;
  books: number;
  avg_rating: number;
  avg_quality: number;
  avg_value: number;
  reviews: number;
};

export type DistributionRow = {
  rating?: number;
  label?: string;
  count: number;
};

export type DashboardData = {
  generatedAt: string;
  sources: {
    books: string;
    reviews: string;
    reviewPeriod: string;
    dataAge: string;
  };
  metrics: {
    books: number;
    reviews: number;
    avgRating: number;
    verifiedPct: number;
    qualityScore: number;
    reviewsToAudit: number;
  };
  summary: {
    topGenre: string;
    topBook: string;
    booksWithReviews: number;
    auditableBooks: number;
  };
  dataQuality: {
    completeness: number;
    emptyCells: number;
    duplicates: number;
    genreBuckets: number;
    rawGenreLabels: number;
    tables: Array<Record<string, string | number>>;
  };
  opportunityCards: Record<string, string | null>;
  books: Book[];
  genres: GenreRow[];
  ratingDistribution: DistributionRow[];
  trustDistribution: DistributionRow[];
  recentReviews: Review[];
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function hasNumber(record: Record<string, unknown>, key: string) {
  return typeof record[key] === "number" && Number.isFinite(record[key]);
}

function hasString(record: Record<string, unknown>, key: string) {
  return typeof record[key] === "string";
}

function assertBook(value: unknown): asserts value is Book {
  if (!isRecord(value)) throw new Error("Registro de livro inválido.");
  const strings = ["title", "author", "genre", "rawGenre"];
  const numbers = [
    "price",
    "rating",
    "reviews",
    "verifiedPct",
    "qualityScore",
    "reviewsToAudit",
    "valueScore",
    "ratingStd",
  ];
  for (const key of strings) {
    if (!hasString(value, key)) throw new Error(`Campo textual inválido no livro: ${key}`);
  }
  for (const key of numbers) {
    if (!hasNumber(value, key)) throw new Error(`Campo numérico inválido no livro: ${key}`);
  }
  if (!isRecord(value.scoreBreakdown)) throw new Error("Decomposição de score inválida.");
  for (const key of ["rating", "price", "reviewQuality", "evidence"]) {
    if (!hasNumber(value.scoreBreakdown, key)) {
      throw new Error(`Campo inválido na decomposição do score: ${key}`);
    }
  }
  if (!isRecord(value.genreBenchmark)) throw new Error("Benchmark de gênero inválido.");
  for (const key of ["rating", "quality", "value"]) {
    if (!hasNumber(value.genreBenchmark, key)) {
      throw new Error(`Campo inválido no benchmark de gênero: ${key}`);
    }
  }
}

export function parseDashboardData(value: unknown): DashboardData {
  if (!isRecord(value)) throw new Error("Os dados do dashboard devem ser um objeto.");
  for (const key of ["generatedAt"]) {
    if (!hasString(value, key)) throw new Error(`Campo textual inválido no dashboard: ${key}`);
  }
  for (const key of [
    "sources",
    "metrics",
    "summary",
    "dataQuality",
    "opportunityCards",
  ]) {
    if (!isRecord(value[key])) throw new Error(`Campo objeto inválido no dashboard: ${key}`);
  }
  for (const key of [
    "books",
    "genres",
    "ratingDistribution",
    "trustDistribution",
    "recentReviews",
  ]) {
    if (!Array.isArray(value[key])) throw new Error(`Campo lista inválido no dashboard: ${key}`);
  }
  const books = value.books;
  if (!Array.isArray(books) || books.length === 0) {
    throw new Error("Os dados do dashboard devem incluir livros.");
  }
  books.forEach(assertBook);
  return value as DashboardData;
}
