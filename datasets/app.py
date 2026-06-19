from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Cyberdeck Retro | Revisor de Reviews",
    page_icon="⚡",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
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


CYBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    --bg: #05030A;
    --panel: rgba(10, 13, 30, 0.82);
    --panel-strong: rgba(16, 10, 36, 0.92);
    --cyan: #22D3EE;
    --pink: #F472B6;
    --violet: #8B5CF6;
    --green: #34D399;
    --text: #EEF5FF;
    --muted: #9CA3AF;
}

.stApp {
    background:
        linear-gradient(135deg, rgba(139, 92, 246, 0.18), transparent 34%),
        radial-gradient(circle at 82% 6%, rgba(34, 211, 238, 0.16), transparent 28%),
        radial-gradient(circle at 18% 82%, rgba(244, 114, 182, 0.12), transparent 26%),
        #05030A;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(8, 5, 24, 0.98), rgba(3, 6, 23, 0.96));
    border-right: 1px solid rgba(34, 211, 238, 0.34);
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #DDEBFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    letter-spacing: 0;
}

h1 {
    color: #F8FBFF;
    font-weight: 800;
}

h2, h3 {
    color: #A7F3FF;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 26px 28px;
    border: 1px solid rgba(34, 211, 238, 0.38);
    background:
        linear-gradient(135deg, rgba(34, 211, 238, 0.13), rgba(139, 92, 246, 0.14)),
        rgba(3, 7, 18, 0.88);
    box-shadow: 0 0 34px rgba(34, 211, 238, 0.13);
    border-radius: 8px;
}

.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(34, 211, 238, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34, 211, 238, 0.06) 1px, transparent 1px);
    background-size: 30px 30px;
    mask-image: linear-gradient(90deg, rgba(0,0,0,0.72), transparent);
    pointer-events: none;
}

.hero-title {
    position: relative;
    margin: 0;
    font-size: 2.25rem;
    line-height: 1.08;
    font-weight: 800;
}

.hero-subtitle {
    position: relative;
    max-width: 900px;
    margin: 12px 0 0;
    color: #C9D7EA;
    font-size: 1rem;
}

.chip-row {
    position: relative;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 18px;
}

.chip {
    border: 1px solid rgba(167, 139, 250, 0.52);
    color: #EDE9FE;
    background: rgba(17, 24, 39, 0.68);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin: 18px 0 10px;
}

.metric-card {
    border: 1px solid rgba(34, 211, 238, 0.26);
    background: rgba(7, 10, 24, 0.82);
    border-radius: 8px;
    padding: 16px;
    box-shadow: inset 0 0 24px rgba(139, 92, 246, 0.08);
}

.metric-label {
    color: #98A6BA;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0;
    font-family: 'JetBrains Mono', monospace;
}

.metric-value {
    margin-top: 8px;
    font-size: 1.85rem;
    color: #FFFFFF;
    font-weight: 800;
}

.status-card {
    border-left: 3px solid #22D3EE;
    background: rgba(8, 15, 34, 0.88);
    border-radius: 6px;
    padding: 12px 14px;
    color: #DDEBFF;
}

.section-title {
    margin-top: 20px;
    font-family: 'JetBrains Mono', monospace;
    color: #67E8F9;
    font-weight: 700;
}

div[data-testid="stMetric"] {
    background: rgba(7, 10, 24, 0.72);
    border: 1px solid rgba(34, 211, 238, 0.18);
    border-radius: 8px;
    padding: 14px;
}

div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    border: 1px solid rgba(34, 211, 238, 0.16);
    border-radius: 8px;
}

.stAlert {
    border-radius: 8px;
}

.stDownloadButton button,
.stButton button {
    border-radius: 6px;
    border: 1px solid rgba(34, 211, 238, 0.65);
    background: linear-gradient(135deg, #0EA5E9, #8B5CF6 55%, #EC4899);
    color: #FFFFFF;
    font-weight: 800;
    box-shadow: 0 0 22px rgba(34, 211, 238, 0.22);
}

.stDownloadButton button:hover,
.stButton button:hover {
    border-color: #F472B6;
    box-shadow: 0 0 28px rgba(244, 114, 182, 0.34);
}

footer, #MainMenu {
    visibility: hidden;
}

@media (max-width: 900px) {
    .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .hero-title {
        font-size: 1.7rem;
    }
}

@media (max-width: 560px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""


def load_csv(uploaded_file, local_path: Path, sample_path: Path):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file), "Upload"
    if local_path.exists():
        return pd.read_csv(local_path), "CSV local"
    return pd.read_csv(sample_path), "Amostra pública"


def validate_columns(df: pd.DataFrame, expected_columns: list[str], label: str):
    missing = [column for column in expected_columns if column not in df.columns]
    if missing:
        st.error(
            f"O arquivo de {label} não possui as colunas esperadas: "
            f"{', '.join(missing)}."
        )
        st.stop()


def prepare_books(df: pd.DataFrame):
    prepared = df.copy()
    prepared["book price"] = pd.to_numeric(prepared["book price"], errors="coerce")
    prepared["rating"] = pd.to_numeric(prepared["rating"], errors="coerce")
    prepared["year of publication"] = pd.to_numeric(
        prepared["year of publication"], errors="coerce"
    )
    return prepared.dropna(subset=["book title", "book price", "rating"])


def prepare_reviews(df: pd.DataFrame):
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
    prepared["review description"] = prepared["review description"].fillna("")
    prepared["review title"] = prepared["review title"].fillna("")
    prepared["review_length"] = prepared["review description"].str.len()
    prepared["short_review"] = prepared["review_length"] < 80
    prepared["suspicious_flag"] = (
        (prepared["reviewer rating"] >= 5)
        & (~prepared["is_verified"])
        & prepared["short_review"]
    )
    prepared["date_parsed"] = pd.to_datetime(
        prepared["date"], errors="coerce", dayfirst=True
    )
    return prepared.dropna(subset=["book name", "reviewer rating"])


def apply_cyber_layout():
    st.markdown(CYBER_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero">
            <p class="hero-title">Cyberdeck Retro</p>
            <p class="hero-subtitle">
                Painel gratuito para revisar livros e reviews, com filtros, sinais de confiança
                e visual cyberpunk. Sem APIs pagas, sem tokens e sem scraping da Amazon.
            </p>
            <div class="chip-row">
                <span class="chip">Streamlit</span>
                <span class="chip">Pandas</span>
                <span class="chip">Plotly</span>
                <span class="chip">Custo zero</span>
                <span class="chip">Dados locais ou upload</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_cards(total_books, avg_book_rating, total_reviews, verified_pct):
    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Livros analisados</div>
                <div class="metric-value">{total_books:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Nota média dos livros</div>
                <div class="metric-value">{avg_book_rating:.2f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Reviews carregadas</div>
                <div class="metric-value">{total_reviews:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Reviews verificadas</div>
                <div class="metric-value">{verified_pct:.1f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,3,10,0.96)",
        font_color="#E6EFFB",
        title_font_color="#A7F3FF",
        legend_title_font_color="#D8B4FE",
        margin=dict(l=12, r=12, t=58, b=12),
    )
    fig.update_xaxes(gridcolor="rgba(148, 163, 184, 0.14)")
    fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.14)")
    return fig


st.markdown(CYBER_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Controle do Cyberdeck")
    st.caption("Use CSV local, amostra pública ou envie seus próprios arquivos.")

    uploaded_books = st.file_uploader(
        "Upload de livros (.csv)",
        type=["csv"],
        help="Opcional. Se não enviar, o app usa CSV local ou sample público.",
    )
    uploaded_reviews = st.file_uploader(
        "Upload de reviews (.csv)",
        type=["csv"],
        help="Opcional. Mantenha dados sensíveis fora do GitHub.",
    )

    st.markdown("---")
    st.markdown("### Filtros")

df_books_raw, books_source = load_csv(uploaded_books, BOOKS_DATA, SAMPLE_BOOKS_DATA)
df_reviews_raw, reviews_source = load_csv(
    uploaded_reviews, REVIEWS_DATA, SAMPLE_REVIEWS_DATA
)

validate_columns(df_books_raw, BOOK_COLUMNS, "livros")
validate_columns(df_reviews_raw, REVIEW_COLUMNS, "reviews")

df_books = prepare_books(df_books_raw)
df_reviews = prepare_reviews(df_reviews_raw)

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
    only_suspicious = st.checkbox("Destacar possíveis reviews frágeis", value=False)

    st.markdown("---")
    st.markdown("### Fonte de dados")
    st.write(f"Livros: **{books_source}**")
    st.write(f"Reviews: **{reviews_source}**")

apply_cyber_layout()

if books_source == "Amostra pública" or reviews_source == "Amostra pública":
    st.info(
        "Modo demonstração ativo: o app está usando dados públicos anonimizados. "
        "Para analisar sua base completa, use upload de CSV ou coloque os arquivos locais em datasets/."
    )

filtered_books = df_books.copy()
filtered_reviews = df_reviews.copy()

if selected_genre != "Todos":
    filtered_books = filtered_books[filtered_books["genre"] == selected_genre]

if title_search:
    filtered_books = filtered_books[
        filtered_books["book title"].str.contains(
            title_search, case=False, na=False, regex=False
        )
    ]

filtered_books = filtered_books[
    (filtered_books["book price"] <= max_selected_price)
    & (filtered_books["rating"] >= selected_min_rating)
]

if only_verified:
    filtered_reviews = filtered_reviews[filtered_reviews["is_verified"]]

if only_suspicious:
    filtered_reviews = filtered_reviews[filtered_reviews["suspicious_flag"]]

total_books = len(filtered_books)
avg_book_rating = filtered_books["rating"].mean() if total_books else 0
avg_price = filtered_books["book price"].mean() if total_books else 0
total_reviews = len(filtered_reviews)
avg_review_rating = filtered_reviews["reviewer rating"].mean() if total_reviews else 0
verified_pct = (
    filtered_reviews["is_verified"].mean() * 100 if total_reviews else 0
)
suspicious_count = int(filtered_reviews["suspicious_flag"].sum()) if total_reviews else 0

metric_cards(total_books, avg_book_rating, total_reviews, verified_pct)

status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:
    st.markdown(
        f"<div class='status-card'><strong>Preço médio:</strong><br>${avg_price:.2f}</div>",
        unsafe_allow_html=True,
    )
with status_col2:
    st.markdown(
        f"<div class='status-card'><strong>Nota média das reviews:</strong><br>{avg_review_rating:.2f}</div>",
        unsafe_allow_html=True,
    )
with status_col3:
    st.markdown(
        f"<div class='status-card'><strong>Reviews frágeis sinalizadas:</strong><br>{suspicious_count}</div>",
        unsafe_allow_html=True,
    )

if filtered_books.empty:
    st.warning("Nenhum livro encontrado com os filtros atuais.")

if filtered_reviews.empty:
    st.warning("Nenhuma review encontrada com os filtros atuais.")

st.markdown("<p class='section-title'>Visualização de livros</p>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns([1.35, 1])

with chart_col1:
    fig_scatter = px.scatter(
        filtered_books,
        x="book price",
        y="rating",
        hover_name="book title",
        color="genre",
        size="rating",
        title="Preço x avaliação por livro",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    st.plotly_chart(style_chart(fig_scatter), width="stretch")

with chart_col2:
    books_by_year = (
        filtered_books["year of publication"]
        .dropna()
        .astype(int)
        .value_counts()
        .rename_axis("Ano")
        .reset_index(name="Quantidade")
        .sort_values("Ano")
    )
    fig_year = px.bar(
        books_by_year,
        x="Ano",
        y="Quantidade",
        title="Livros por ano de publicação",
        color="Quantidade",
        color_continuous_scale=["#22D3EE", "#8B5CF6", "#F472B6"],
    )
    fig_year.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig_year), width="stretch")

st.markdown("<p class='section-title'>Leitura das reviews</p>", unsafe_allow_html=True)
review_col1, review_col2 = st.columns([1, 1])

with review_col1:
    rating_counts = (
        filtered_reviews["reviewer rating"]
        .value_counts()
        .rename_axis("Nota")
        .reset_index(name="Quantidade")
        .sort_values("Nota")
    )
    fig_ratings = px.bar(
        rating_counts,
        x="Nota",
        y="Quantidade",
        title="Distribuição das notas",
        color="Nota",
        color_continuous_scale="Turbo",
    )
    fig_ratings.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig_ratings), width="stretch")

with review_col2:
    verification = pd.DataFrame(
        {
            "Status": ["Verificada", "Não verificada"],
            "Quantidade": [
                int(filtered_reviews["is_verified"].sum()),
                int((~filtered_reviews["is_verified"]).sum()),
            ],
        }
    )
    fig_verified = px.pie(
        verification,
        names="Status",
        values="Quantidade",
        title="Confiança das reviews",
        color="Status",
        color_discrete_map={
            "Verificada": "#22D3EE",
            "Não verificada": "#F472B6",
        },
        hole=0.48,
    )
    fig_verified.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(style_chart(fig_verified), width="stretch")

tab_overview, tab_reviews, tab_quality = st.tabs(
    ["Livros em destaque", "Reviews recentes", "Sinais locais"]
)

with tab_overview:
    display_books = filtered_books[
        [
            "book title",
            "author",
            "genre",
            "book price",
            "rating",
            "year of publication",
        ]
    ].rename(
        columns={
            "book title": "Livro",
            "author": "Autor",
            "genre": "Gênero",
            "book price": "Preço",
            "rating": "Nota",
            "year of publication": "Ano",
        }
    )
    st.dataframe(display_books.head(20), width="stretch", hide_index=True)

with tab_reviews:
    recent_reviews = filtered_reviews.sort_values(
        by=["date_parsed", "reviewer rating"], ascending=[False, False]
    ).head(20)
    display_reviews = recent_reviews[
        [
            "book name",
            "review title",
            "reviewer rating",
            "is_verified",
            "date",
            "review_length",
        ]
    ].rename(
        columns={
            "book name": "Livro",
            "review title": "Título da review",
            "reviewer rating": "Nota",
            "is_verified": "Verificada",
            "date": "Data",
            "review_length": "Tamanho do texto",
        }
    )
    st.dataframe(display_reviews, width="stretch", hide_index=True)

with tab_quality:
    top_reviewed = (
        filtered_reviews["book name"]
        .value_counts()
        .rename_axis("Livro")
        .reset_index(name="Reviews")
        .head(10)
    )
    signal_col1, signal_col2 = st.columns([1, 1])
    with signal_col1:
        st.markdown("#### Livros mais comentados")
        st.dataframe(top_reviewed, width="stretch", hide_index=True)
    with signal_col2:
        st.markdown("#### Critério simples de alerta")
        st.write(
            "Uma review é sinalizada como frágil quando combina nota máxima, "
            "texto muito curto e ausência de verificação. É uma heurística local, "
            "não uma classificação definitiva."
        )
        fragile_reviews = filtered_reviews[filtered_reviews["suspicious_flag"]][
            [
                "book name",
                "review title",
                "reviewer rating",
                "is_verified",
                "review_length",
            ]
        ].rename(
            columns={
                "book name": "Livro",
                "review title": "Título",
                "reviewer rating": "Nota",
                "is_verified": "Verificada",
                "review_length": "Tamanho",
            }
        )
        st.dataframe(fragile_reviews.head(10), width="stretch", hide_index=True)

st.markdown("<p class='section-title'>Exportação</p>", unsafe_allow_html=True)
download_col1, download_col2 = st.columns(2)
with download_col1:
    st.download_button(
        "Baixar livros filtrados",
        data=filtered_books.to_csv(index=False).encode("utf-8"),
        file_name="livros_filtrados.csv",
        mime="text/csv",
        width="stretch",
    )
with download_col2:
    st.download_button(
        "Baixar reviews filtradas",
        data=filtered_reviews.drop(columns=["date_parsed"], errors="ignore")
        .to_csv(index=False)
        .encode("utf-8"),
        file_name="reviews_filtradas.csv",
        mime="text/csv",
        width="stretch",
    )

with st.expander("Console do projeto"):
    st.code(
        f"""[CYBERDECK] Fonte de livros: {books_source}
[CYBERDECK] Fonte de reviews: {reviews_source}
[LOCAL] Custo de API: $0
[LOCAL] Tokens consumidos por IA: 0
[DATA] Livros filtrados: {total_books}
[DATA] Reviews filtradas: {total_reviews}
[SIGNAL] Reviews frágeis sinalizadas: {suspicious_count}""",
        language="text",
    )

st.caption(
    "Projeto experimental em evolução. Para dados atuais sem custo, use upload de CSVs "
    "ou datasets públicos permitidos. Integrações oficiais podem ser adicionadas no futuro."
)

