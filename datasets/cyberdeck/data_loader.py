from pathlib import Path
from typing import BinaryIO

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
BOOKS_DATA = BASE_DIR / "Top-100 Trending Books.csv"
REVIEWS_DATA = BASE_DIR / "customer reviews.csv"
SAMPLE_BOOKS_DATA = BASE_DIR / "sample_books.csv"
SAMPLE_REVIEWS_DATA = BASE_DIR / "sample_reviews.csv"

BOOK_COLUMNS = [
    "Rank",
    "book title",
    "book price",
    "rating",
    "author",
    "year of publication",
    "genre",
    "url",
]

REVIEW_COLUMNS = [
    "Sno",
    "book name",
    "review title",
    "reviewer",
    "reviewer rating",
    "review description",
    "is_verified",
    "date",
    "timestamp",
    "ASIN",
]


def load_csv(uploaded_file: BinaryIO | None, local_path: Path, sample_path: Path):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file), "Upload"
    if local_path.exists():
        return pd.read_csv(local_path), "CSV local"
    return pd.read_csv(sample_path), "Amostra pública"


def validate_columns(df: pd.DataFrame, expected_columns: list[str]) -> list[str]:
    return [column for column in expected_columns if column not in df.columns]


def prepare_books(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    prepared["book price"] = pd.to_numeric(prepared["book price"], errors="coerce")
    prepared["rating"] = pd.to_numeric(prepared["rating"], errors="coerce")
    prepared["year of publication"] = pd.to_numeric(
        prepared["year of publication"], errors="coerce"
    )
    prepared["genre"] = prepared["genre"].fillna("Sem gênero")
    prepared["author"] = prepared["author"].fillna("Autor não informado")
    prepared["book title"] = prepared["book title"].fillna("")
    return prepared.dropna(subset=["book title", "book price", "rating"])


def prepare_reviews(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    prepared["reviewer rating"] = pd.to_numeric(
        prepared["reviewer rating"], errors="coerce"
    )
    prepared["is_verified"] = (
        prepared["is_verified"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes", "sim", "verified"])
    )
    prepared["book name"] = prepared["book name"].fillna("")
    prepared["review description"] = prepared["review description"].fillna("")
    prepared["review title"] = prepared["review title"].fillna("")
    prepared["reviewer"] = prepared["reviewer"].fillna("Anônimo")
    prepared["review_length"] = prepared["review description"].str.len()
    prepared["word_count"] = prepared["review description"].str.split().str.len()
    prepared["date_parsed"] = pd.to_datetime(
        prepared["date"], errors="coerce", dayfirst=True
    )
    return prepared.dropna(subset=["book name", "reviewer rating"])


def escape_csv_formulas(df: pd.DataFrame) -> pd.DataFrame:
    """Neutralize spreadsheet formula injection in exported CSV files."""
    escaped = df.copy()
    formula_prefixes = ("=", "+", "-", "@")
    for column in escaped.select_dtypes(include="object").columns:
        escaped[column] = escaped[column].map(
            lambda value: f"'{value}"
            if isinstance(value, str) and value.startswith(formula_prefixes)
            else value
        )
    return escaped
