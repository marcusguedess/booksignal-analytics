import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "datasets"
OUTPUT = ROOT / "web" / "src" / "data" / "booksignal.json"

if str(DATASETS) not in sys.path:
    sys.path.insert(0, str(DATASETS))

from booksignal.analysis import (
    add_review_signals,
    build_book_summary,
    data_quality_report,
    radar_cards,
)
from booksignal.data_loader import (  # noqa: E402
    BOOKS_DATA,
    REVIEWS_DATA,
    SAMPLE_BOOKS_DATA,
    SAMPLE_REVIEWS_DATA,
    load_csv,
    prepare_books,
    prepare_reviews,
)


GENRE_BUCKET_RULES = [
    ("children", "Children"),
    ("picture", "Children"),
    ("young adult", "Young Adult"),
    ("new adult", "Young Adult"),
    ("ya", "Young Adult"),
    ("romance", "Romance"),
    ("fantasy", "Fantasy"),
    ("thriller", "Thriller"),
    ("mystery", "Thriller"),
    ("business", "Business"),
    ("finance", "Business"),
    ("economics", "Business"),
    ("self help", "Self Help"),
    ("self-help", "Self Help"),
    ("psychology", "Self Help"),
    ("health", "Health"),
    ("nutrition", "Health"),
    ("fitness", "Health"),
    ("history", "History"),
    ("biography", "Biography"),
    ("memoir", "Biography"),
    ("nonfiction", "Nonfiction"),
    ("cook", "Cooking"),
    ("art", "Arts"),
    ("music", "Arts"),
    ("religion", "Religion"),
    ("politic", "Politics"),
    ("science fiction", "Fiction"),
    ("sciencefiction", "Fiction"),
    ("fiction", "Fiction"),
]


def normalize_genre(value: str) -> str:
    text = str(value).lower()
    for needle, bucket in GENRE_BUCKET_RULES:
        if needle in text:
            return bucket
    return "Other"


def pct(value: float) -> float:
    return round(float(value), 1)


def score_breakdown(row: pd.Series) -> dict[str, float]:
    rating_component = min((float(row["rating"]) / 5) * 100, 100)
    price_component = max(100 - (float(row["book price"]) * 4), 0)
    quality_component = float(row["trust_score"])
    evidence_component = min((int(row["reviews"]) / 10) * 100, 100)
    return {
        "rating": pct(rating_component),
        "price": pct(price_component),
        "reviewQuality": pct(quality_component),
        "evidence": pct(evidence_component),
    }


def validate_payload(payload: dict) -> None:
    required_top_level = {
        "generatedAt",
        "sources",
        "metrics",
        "summary",
        "dataQuality",
        "opportunityCards",
        "books",
        "genres",
        "ratingDistribution",
        "trustDistribution",
        "recentReviews",
    }
    missing = required_top_level - set(payload)
    if missing:
        raise ValueError(f"Campos principais ausentes no dashboard: {sorted(missing)}")

    if not isinstance(payload["books"], list) or not payload["books"]:
        raise ValueError("O payload do dashboard deve incluir pelo menos um livro.")

    required_book_fields = {
        "title",
        "author",
        "genre",
        "rawGenre",
        "price",
        "rating",
        "reviews",
        "verifiedPct",
        "qualityScore",
        "reviewsToAudit",
        "valueScore",
        "ratingStd",
        "scoreBreakdown",
        "genreBenchmark",
    }
    book_missing = required_book_fields - set(payload["books"][0])
    if book_missing:
        raise ValueError(f"Campos ausentes no livro: {sorted(book_missing)}")

    required_score_fields = {"rating", "price", "reviewQuality", "evidence"}
    score_missing = required_score_fields - set(payload["books"][0]["scoreBreakdown"])
    if score_missing:
        raise ValueError(f"Campos ausentes na decomposição do score: {sorted(score_missing)}")


def main() -> None:
    raw_books, books_source = load_csv(None, BOOKS_DATA, SAMPLE_BOOKS_DATA)
    raw_reviews, reviews_source = load_csv(None, REVIEWS_DATA, SAMPLE_REVIEWS_DATA)

    books = prepare_books(raw_books)
    reviews = add_review_signals(prepare_reviews(raw_reviews))
    books["genre_group"] = books["genre"].map(normalize_genre)

    summary = build_book_summary(books, reviews)
    summary["genre_group"] = summary["genre"].map(normalize_genre)
    genre_means = (
        summary.groupby("genre_group", dropna=False)
        .agg(
            avg_genre_rating=("rating", "mean"),
            avg_genre_quality=("trust_score", "mean"),
            avg_genre_value=("value_score", "mean"),
        )
        .reset_index()
    )
    summary = summary.merge(genre_means, on="genre_group", how="left")
    summary = summary.sort_values("value_score", ascending=False)

    dates = reviews["date_parsed"].dropna()
    if dates.empty:
        review_period = "Sem datas"
        data_age = "N/A"
    else:
        newest = dates.max()
        oldest = dates.min()
        today = pd.Timestamp.today().normalize()
        days = max((today - newest.normalize()).days, 0)
        review_period = f"{oldest:%d/%m/%Y} a {newest:%d/%m/%Y}"
        data_age = "Hoje" if days == 0 else f"{days} dias"
    generated_at = newest.isoformat() if not dates.empty else "N/A"

    total_reviews = len(reviews)
    verified_pct = pct(reviews["is_verified"].mean() * 100) if total_reviews else 0
    quality_score = pct(reviews["trust_score"].mean()) if total_reviews else 0
    to_audit = int(reviews["suspicious_flag"].sum()) if total_reviews else 0

    genre_rows = (
        summary.groupby("genre_group", dropna=False)
        .agg(
            books=("book title", "size"),
            avg_rating=("rating", "mean"),
            avg_quality=("trust_score", "mean"),
            avg_value=("value_score", "mean"),
            reviews=("reviews", "sum"),
        )
        .reset_index()
        .sort_values("avg_value", ascending=False)
    )

    rating_rows = (
        reviews["reviewer rating"]
        .value_counts()
        .rename_axis("rating")
        .reset_index(name="count")
        .sort_values("rating")
    )

    trust_rows = (
        reviews["trust_label"]
        .value_counts()
        .rename_axis("label")
        .reset_index(name="count")
    )

    cards = {}
    for label, row in radar_cards(summary).items():
        cards[label] = None if row is None else str(row["book title"])

    quality_report = data_quality_report(raw_books, raw_reviews)
    empty_cells = int(raw_books.isna().sum().sum() + raw_reviews.isna().sum().sum())
    total_cells = int(raw_books.size + raw_reviews.size)
    completeness = 100 if total_cells == 0 else pct((1 - empty_cells / total_cells) * 100)

    books_payload = []
    for _, row in summary.head(60).iterrows():
        books_payload.append(
            {
                "title": str(row["book title"]),
                "author": str(row["author"]),
                "genre": str(row["genre_group"]),
                "rawGenre": str(row["genre"]),
                "price": round(float(row["book price"]), 2),
                "rating": round(float(row["rating"]), 2),
                "reviews": int(row["reviews"]),
                "verifiedPct": pct(row["verified_pct"]),
                "qualityScore": pct(row["trust_score"]),
                "reviewsToAudit": int(row["fragile_reviews"]),
                "valueScore": pct(row["value_score"]),
                "ratingStd": round(float(row["rating_std"]), 2),
                "scoreBreakdown": score_breakdown(row),
                "genreBenchmark": {
                    "rating": pct(row["avg_genre_rating"]),
                    "quality": pct(row["avg_genre_quality"]),
                    "value": pct(row["avg_genre_value"]),
                },
            }
        )

    recent_reviews = []
    for _, row in reviews.sort_values("date_parsed", ascending=False).head(40).iterrows():
        recent_reviews.append(
            {
                "book": str(row["book name"]),
                "title": str(row["review title"]),
                "rating": float(row["reviewer rating"]),
                "verified": bool(row["is_verified"]),
                "qualityScore": int(row["trust_score"]),
                "qualityLabel": str(row["trust_label"]),
                "reasons": str(row["score_reasons"]),
                "words": int(row["word_count"]),
                "date": str(row["date"]),
            }
        )

    payload = {
        "generatedAt": generated_at,
        "sources": {
            "books": books_source,
            "reviews": reviews_source,
            "reviewPeriod": review_period,
            "dataAge": data_age,
        },
        "metrics": {
            "books": int(len(books)),
            "reviews": int(total_reviews),
            "avgRating": round(float(books["rating"].mean()), 2),
            "verifiedPct": verified_pct,
            "qualityScore": quality_score,
            "reviewsToAudit": to_audit,
        },
        "summary": {
            "topGenre": str(genre_rows.iloc[0]["genre_group"]) if not genre_rows.empty else "N/A",
            "topBook": str(summary.iloc[0]["book title"]) if not summary.empty else "N/A",
            "booksWithReviews": int((summary["reviews"] > 0).sum()),
            "auditableBooks": int(summary["fragile_reviews"].sum()) if not summary.empty else 0,
        },
        "dataQuality": {
            "completeness": completeness,
            "emptyCells": empty_cells,
            "duplicates": int(raw_books.duplicated().sum() + raw_reviews.duplicated().sum()),
            "genreBuckets": int(books["genre_group"].nunique()),
            "rawGenreLabels": int(books["genre"].nunique()),
            "tables": quality_report.to_dict(orient="records"),
        },
        "opportunityCards": cards,
        "books": books_payload,
        "genres": genre_rows.round(2).to_dict(orient="records"),
        "ratingDistribution": rating_rows.to_dict(orient="records"),
        "trustDistribution": trust_rows.to_dict(orient="records"),
        "recentReviews": recent_reviews,
    }

    validate_payload(payload)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
