import pandas as pd
import streamlit as st

from cyberdeck.analysis import (
    add_review_signals,
    build_book_summary,
    filter_books,
    filter_reviews,
    radar_cards,
)
from cyberdeck.data_loader import (
    BOOK_COLUMNS,
    BOOKS_DATA,
    REVIEWS_DATA,
    REVIEW_COLUMNS,
    SAMPLE_BOOKS_DATA,
    SAMPLE_REVIEWS_DATA,
    escape_csv_formulas,
    load_csv,
    prepare_books,
    prepare_reviews,
    validate_columns,
)
from cyberdeck.ui import (
    apply_theme,
    bar_reviews_by_rating,
    callout,
    hero,
    metric_cards,
    pie_trust,
    radar_panel,
    scatter_books,
    section,
)


st.set_page_config(
    page_title="Cyberdeck Retro | Revisor de Reviews",
    page_icon="⚡",
    layout="wide",
)

apply_theme()

with st.sidebar:
    st.markdown("## Controle do Cyberdeck")
    st.caption("Use os samples, seus CSVs locais ou envie arquivos pela interface.")

    with st.expander("Como usar", expanded=True):
        st.write(
            "1. Envie CSVs ou use os dados de exemplo.\n\n"
            "2. Ajuste filtros de gênero, preço e nota.\n\n"
            "3. Veja o Radar, compare livros e baixe os resultados."
        )

    uploaded_books = st.file_uploader(
        "Upload de livros (.csv)",
        type=["csv"],
        help="Opcional. Máximo recomendado: 50 MB.",
    )
    uploaded_reviews = st.file_uploader(
        "Upload de reviews (.csv)",
        type=["csv"],
        help="Opcional. Evite dados sensíveis em repositórios públicos.",
    )

    st.markdown("---")
    st.markdown("### Filtros")

if uploaded_books and uploaded_books.size > 50 * 1024 * 1024:
    st.error("O arquivo de livros excede 50 MB. Use uma amostra menor.")
    st.stop()

if uploaded_reviews and uploaded_reviews.size > 50 * 1024 * 1024:
    st.error("O arquivo de reviews excede 50 MB. Use uma amostra menor.")
    st.stop()

df_books_raw, books_source = load_csv(uploaded_books, BOOKS_DATA, SAMPLE_BOOKS_DATA)
df_reviews_raw, reviews_source = load_csv(
    uploaded_reviews, REVIEWS_DATA, SAMPLE_REVIEWS_DATA
)

missing_book_columns = validate_columns(df_books_raw, BOOK_COLUMNS)
missing_review_columns = validate_columns(df_reviews_raw, REVIEW_COLUMNS)

if missing_book_columns:
    st.error(
        "O CSV de livros não possui as colunas esperadas: "
        + ", ".join(missing_book_columns)
    )
    st.stop()

if missing_review_columns:
    st.error(
        "O CSV de reviews não possui as colunas esperadas: "
        + ", ".join(missing_review_columns)
    )
    st.stop()

df_books = prepare_books(df_books_raw)
df_reviews = add_review_signals(prepare_reviews(df_reviews_raw))

with st.sidebar:
    genres = sorted(df_books["genre"].dropna().unique().tolist())
    selected_genre = st.selectbox("Gênero", ["Todos"] + genres)
    title_search = st.text_input("Buscar livro", "")

    min_price = float(df_books["book price"].min())
    max_price = float(df_books["book price"].max())
    max_selected_price = st.slider(
        "Preço máximo ($)",
        min_value=min_price,
        max_value=max_price,
        value=max_price,
    )

    min_rating = float(df_books["rating"].min())
    max_rating = float(df_books["rating"].max())
    selected_min_rating = st.slider(
        "Nota mínima",
        min_value=min_rating,
        max_value=max_rating,
        value=min_rating,
        step=0.1,
    )

    only_verified = st.checkbox("Apenas reviews verificadas", value=False)
    only_fragile = st.checkbox("Somente reviews para revisar", value=False)

    st.markdown("---")
    st.markdown("### Fonte de dados")
    st.write(f"Livros: **{books_source}**")
    st.write(f"Reviews: **{reviews_source}**")

hero()

if books_source == "Amostra pública" or reviews_source == "Amostra pública":
    st.info(
        "Modo demonstração ativo: usando dados públicos anonimizados. "
        "Para analisar sua base completa, use upload de CSV ou coloque os arquivos locais em datasets/."
    )

filtered_books = filter_books(
    df_books,
    selected_genre,
    title_search,
    max_selected_price,
    selected_min_rating,
)
filtered_reviews = filter_reviews(
    df_reviews,
    filtered_books,
    only_verified,
    only_fragile,
)
summary = build_book_summary(filtered_books, filtered_reviews)

total_books = len(filtered_books)
total_reviews = len(filtered_reviews)
avg_book_rating = filtered_books["rating"].mean() if total_books else 0
avg_review_rating = filtered_reviews["reviewer rating"].mean() if total_reviews else 0
verified_pct = filtered_reviews["is_verified"].mean() * 100 if total_reviews else 0
avg_trust = filtered_reviews["trust_score"].mean() if total_reviews else 0
fragile_count = int(filtered_reviews["suspicious_flag"].sum()) if total_reviews else 0

metric_cards(total_books, avg_book_rating, total_reviews, verified_pct)

status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:
    callout("Nota média das reviews", f"{avg_review_rating:.2f}")
with status_col2:
    callout("Confiança média", f"{avg_trust:.0f}/100")
with status_col3:
    callout("Reviews para revisar", str(fragile_count))

if filtered_books.empty:
    st.warning("Nenhum livro encontrado com os filtros atuais.")

if filtered_reviews.empty:
    st.warning("Nenhuma review encontrada com os filtros atuais.")

section("Radar de compra")
radar_panel(radar_cards(summary))

tab_radar, tab_compare, tab_reviews, tab_data, tab_notes = st.tabs(
    ["Radar", "Comparador", "Reviews", "Dados", "Guia"]
)

with tab_radar:
    chart_col1, chart_col2 = st.columns([1.25, 1])
    with chart_col1:
        if not summary.empty:
            st.plotly_chart(scatter_books(summary), width="stretch")
    with chart_col2:
        if not filtered_reviews.empty:
            st.plotly_chart(pie_trust(filtered_reviews), width="stretch")

    st.markdown("#### Ranking do cyberdeck")
    ranking = summary.sort_values("value_score", ascending=False)[
        [
            "book title",
            "author",
            "genre",
            "book price",
            "rating",
            "reviews",
            "verified_pct",
            "trust_score",
            "value_score",
        ]
    ].rename(
        columns={
            "book title": "Livro",
            "author": "Autor",
            "genre": "Gênero",
            "book price": "Preço",
            "rating": "Nota",
            "reviews": "Reviews",
            "verified_pct": "% verificadas",
            "trust_score": "Confiança",
            "value_score": "Score radar",
        }
    )
    st.dataframe(ranking, width="stretch", hide_index=True)

with tab_compare:
    options = summary["book title"].tolist()
    selected_books = st.multiselect(
        "Escolha até 4 livros para comparar",
        options=options,
        default=options[: min(3, len(options))],
        max_selections=4,
    )
    comparison = summary[summary["book title"].isin(selected_books)]
    if comparison.empty:
        st.info("Selecione ao menos um livro para comparar.")
    else:
        cols = st.columns(len(comparison))
        for col, (_, row) in zip(cols, comparison.iterrows()):
            with col:
                st.metric("Nota", f"{row['rating']:.1f}")
                st.metric("Confiança", f"{row['trust_score']:.0f}/100")
                st.metric("Preço", f"${row['book price']:.2f}")
                st.caption(row["book title"])

        compare_table = comparison[
            [
                "book title",
                "author",
                "book price",
                "rating",
                "reviews",
                "verified_pct",
                "trust_score",
                "fragile_reviews",
                "value_score",
            ]
        ].rename(
            columns={
                "book title": "Livro",
                "author": "Autor",
                "book price": "Preço",
                "rating": "Nota",
                "reviews": "Reviews",
                "verified_pct": "% verificadas",
                "trust_score": "Confiança",
                "fragile_reviews": "Para revisar",
                "value_score": "Score radar",
            }
        )
        st.dataframe(compare_table, width="stretch", hide_index=True)

with tab_reviews:
    chart_col1, chart_col2 = st.columns([1, 1])
    with chart_col1:
        if not filtered_reviews.empty:
            st.plotly_chart(bar_reviews_by_rating(filtered_reviews), width="stretch")
    with chart_col2:
        top_reviewed = (
            filtered_reviews["book name"]
            .value_counts()
            .rename_axis("Livro")
            .reset_index(name="Reviews")
            .head(10)
        )
        st.markdown("#### Livros mais comentados")
        st.dataframe(top_reviewed, width="stretch", hide_index=True)

    recent_reviews = filtered_reviews.sort_values(
        by=["date_parsed", "reviewer rating"], ascending=[False, False]
    ).head(25)
    review_table = recent_reviews[
        [
            "book name",
            "review title",
            "reviewer rating",
            "is_verified",
            "trust_score",
            "trust_label",
            "word_count",
            "date",
        ]
    ].rename(
        columns={
            "book name": "Livro",
            "review title": "Título da review",
            "reviewer rating": "Nota",
            "is_verified": "Verificada",
            "trust_score": "Confiança",
            "trust_label": "Faixa",
            "word_count": "Palavras",
            "date": "Data",
        }
    )
    st.dataframe(review_table, width="stretch", hide_index=True)

with tab_data:
    st.markdown("#### Livros filtrados")
    st.dataframe(
        summary.drop(columns=["url"], errors="ignore"),
        width="stretch",
        hide_index=True,
    )

    st.markdown("#### Exportação segura")
    download_col1, download_col2 = st.columns(2)
    with download_col1:
        st.download_button(
            "Baixar livros filtrados",
            data=escape_csv_formulas(summary)
            .to_csv(index=False)
            .encode("utf-8"),
            file_name="livros_filtrados.csv",
            mime="text/csv",
            width="stretch",
        )
    with download_col2:
        export_reviews = filtered_reviews.drop(
            columns=["date_parsed"], errors="ignore"
        )
        st.download_button(
            "Baixar reviews filtradas",
            data=escape_csv_formulas(export_reviews)
            .to_csv(index=False)
            .encode("utf-8"),
            file_name="reviews_filtradas.csv",
            mime="text/csv",
            width="stretch",
        )

with tab_notes:
    st.markdown("#### Como o score funciona")
    st.write(
        "O score de confiança é uma heurística local. Ele reduz pontos quando a review "
        "não é verificada, é muito curta, usa título genérico, combina nota extrema com "
        "ausência de verificação ou contém pontuação repetida. Não é detecção definitiva."
    )
    st.markdown("#### Segurança")
    st.write(
        "O app não chama APIs pagas, não usa LLM, não consome tokens e não faz scraping. "
        "CSVs brutos devem ficar locais. Downloads neutralizam células que poderiam ser "
        "interpretadas como fórmulas em planilhas."
    )

with st.expander("Console do projeto"):
    st.code(
        f"""[CYBERDECK] Fonte de livros: {books_source}
[CYBERDECK] Fonte de reviews: {reviews_source}
[LOCAL] Custo de API: $0
[LOCAL] Tokens consumidos por IA: 0
[DATA] Livros filtrados: {total_books}
[DATA] Reviews filtradas: {total_reviews}
[SIGNAL] Confiança média: {avg_trust:.0f}/100
[SIGNAL] Reviews para revisar: {fragile_count}""",
        language="text",
    )

st.caption(
    "Cyberdeck Retro é experimental e gratuito. Use dados públicos permitidos, CSVs próprios "
    "ou integrações oficiais autorizadas em versões futuras."
)
