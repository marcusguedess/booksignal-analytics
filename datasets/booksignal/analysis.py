import pandas as pd


GENERIC_TITLES = {
    "great",
    "good",
    "ok",
    "nice",
    "amazing",
    "wow",
    "love it",
    "loved it",
    "recommended",
}


def add_review_signals(reviews: pd.DataFrame) -> pd.DataFrame:
    scored = reviews.copy()
    title = scored["review title"].str.strip().str.lower()
    description = scored["review description"].str.strip()

    scored["review_length"] = description.str.len()
    scored["word_count"] = description.str.split().str.len()
    scored["short_review"] = scored["word_count"] < 18
    scored["generic_title"] = title.isin(GENERIC_TITLES) | (title.str.len() <= 4)
    scored["extreme_rating"] = scored["reviewer rating"].isin([1, 5])
    scored["unverified_extreme"] = (~scored["is_verified"]) & scored["extreme_rating"]
    scored["repeated_punctuation"] = description.str.contains(
        r"[!?]{3,}", regex=True, na=False
    )

    score = pd.Series(100, index=scored.index, dtype="int64")
    score -= (~scored["is_verified"]).astype(int) * 22
    score -= scored["short_review"].astype(int) * 18
    score -= scored["generic_title"].astype(int) * 12
    score -= scored["unverified_extreme"].astype(int) * 16
    score -= scored["repeated_punctuation"].astype(int) * 6

    scored["trust_score"] = score.clip(lower=0, upper=100)
    scored["suspicious_flag"] = scored["trust_score"] < 58
    scored["trust_label"] = pd.cut(
        scored["trust_score"],
        bins=[-1, 57, 78, 100],
        labels=["Revisar", "Boa", "Forte"],
    ).astype(str)
    scored["score_reasons"] = scored.apply(review_reason_summary, axis=1)
    return scored


def review_reason_summary(row: pd.Series) -> str:
    reasons = []
    if not bool(row["is_verified"]):
        reasons.append("não verificada")
    if bool(row["short_review"]):
        reasons.append("texto curto")
    if bool(row["generic_title"]):
        reasons.append("título genérico")
    if bool(row["unverified_extreme"]):
        reasons.append("nota extrema sem verificação")
    if bool(row["repeated_punctuation"]):
        reasons.append("pontuação repetida")
    return ", ".join(reasons) if reasons else "sem alertas relevantes"


def build_book_summary(books: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    review_summary = (
        reviews.groupby("book name", dropna=False)
        .agg(
            reviews=("book name", "size"),
            review_rating=("reviewer rating", "mean"),
            verified_pct=("is_verified", "mean"),
            trust_score=("trust_score", "mean"),
            fragile_reviews=("suspicious_flag", "sum"),
            rating_std=("reviewer rating", "std"),
        )
        .reset_index()
        .rename(columns={"book name": "book title"})
    )
    summary = books.merge(review_summary, on="book title", how="left")
    summary["reviews"] = summary["reviews"].fillna(0).astype(int)
    summary["review_rating"] = summary["review_rating"].fillna(0)
    summary["verified_pct"] = (summary["verified_pct"].fillna(0) * 100).round(1)
    summary["trust_score"] = summary["trust_score"].fillna(0).round(1)
    summary["fragile_reviews"] = summary["fragile_reviews"].fillna(0).astype(int)
    summary["rating_std"] = summary["rating_std"].fillna(0).round(2)
    summary["value_score"] = (
        (summary["rating"] * 18)
        + (summary["trust_score"] * 0.55)
        + (summary["verified_pct"] * 0.2)
        - (summary["book price"] * 1.4)
    ).round(1)
    return summary


def radar_cards(summary: pd.DataFrame) -> dict[str, pd.Series | None]:
    if summary.empty:
        return {
            "Melhor custo-benefício": None,
            "Mais confiável": None,
            "Mais comentado": None,
            "Mais controverso": None,
        }

    with_reviews = summary[summary["reviews"] > 0]
    base = with_reviews if not with_reviews.empty else summary
    return {
        "Melhor custo-benefício": summary.sort_values(
            ["value_score", "rating"], ascending=False
        ).iloc[0],
        "Mais confiável": base.sort_values(
            ["trust_score", "verified_pct", "reviews"], ascending=False
        ).iloc[0],
        "Mais comentado": base.sort_values("reviews", ascending=False).iloc[0],
        "Mais controverso": base.sort_values(
            ["rating_std", "fragile_reviews"], ascending=False
        ).iloc[0],
    }


def filter_books(
    books: pd.DataFrame,
    genre: str,
    title_search: str,
    max_price: float,
    min_rating: float,
) -> pd.DataFrame:
    filtered = books.copy()
    if genre != "Todos":
        filtered = filtered[filtered["genre"] == genre]
    if title_search:
        filtered = filtered[
            filtered["book title"].str.contains(
                title_search, case=False, na=False, regex=False
            )
        ]
    return filtered[
        (filtered["book price"] <= max_price) & (filtered["rating"] >= min_rating)
    ]


def filter_reviews(
    reviews: pd.DataFrame,
    visible_books: pd.DataFrame,
    only_verified: bool,
    only_fragile: bool,
    review_search: str = "",
) -> pd.DataFrame:
    filtered = reviews[reviews["book name"].isin(visible_books["book title"])].copy()
    if only_verified:
        filtered = filtered[filtered["is_verified"]]
    if only_fragile:
        filtered = filtered[filtered["suspicious_flag"]]
    if review_search:
        needle = review_search.strip()
        if needle:
            title_match = filtered["review title"].str.contains(
                needle, case=False, na=False, regex=False
            )
            body_match = filtered["review description"].str.contains(
                needle, case=False, na=False, regex=False
            )
            book_match = filtered["book name"].str.contains(
                needle, case=False, na=False, regex=False
            )
            filtered = filtered[title_match | body_match | book_match]
    return filtered


def data_quality_report(books: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "Área": "Livros",
            "Linhas": len(books),
            "Colunas": len(books.columns),
            "Células vazias": int(books.isna().sum().sum()),
            "Duplicatas": int(books.duplicated().sum()),
        },
        {
            "Área": "Reviews",
            "Linhas": len(reviews),
            "Colunas": len(reviews.columns),
            "Células vazias": int(reviews.isna().sum().sum()),
            "Duplicatas": int(reviews.duplicated().sum()),
        },
    ]
    return pd.DataFrame(rows)
