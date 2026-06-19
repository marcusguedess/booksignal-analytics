import pandas as pd
import plotly.express as px
import streamlit as st
from html import escape


CYBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

.stApp {
    background:
        linear-gradient(135deg, rgba(139, 92, 246, 0.20), transparent 34%),
        radial-gradient(circle at 82% 6%, rgba(34, 211, 238, 0.18), transparent 28%),
        radial-gradient(circle at 18% 82%, rgba(244, 114, 182, 0.14), transparent 26%),
        linear-gradient(180deg, #05030A 0%, #070816 100%);
    color: #EEF5FF;
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
    padding-top: 1.6rem;
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

.hero, .callout, .radar-card, .metric-card {
    border-radius: 8px;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 28px;
    border: 1px solid rgba(34, 211, 238, 0.38);
    background:
        linear-gradient(135deg, rgba(34, 211, 238, 0.14), rgba(139, 92, 246, 0.16)),
        rgba(3, 7, 18, 0.90);
    box-shadow: 0 0 38px rgba(34, 211, 238, 0.14);
}

.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(34, 211, 238, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34, 211, 238, 0.06) 1px, transparent 1px);
    background-size: 30px 30px;
    mask-image: linear-gradient(90deg, rgba(0,0,0,0.74), transparent);
    pointer-events: none;
}

.hero-title {
    position: relative;
    margin: 0;
    font-size: 2.45rem;
    line-height: 1.08;
    font-weight: 800;
}

.hero-subtitle {
    position: relative;
    max-width: 920px;
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
    font-size: 0.80rem;
    font-family: 'JetBrains Mono', monospace;
}

.metric-grid, .radar-grid {
    display: grid;
    gap: 12px;
}

.metric-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    margin: 18px 0 10px;
}

.radar-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    margin: 12px 0 18px;
}

.metric-card, .radar-card {
    border: 1px solid rgba(34, 211, 238, 0.26);
    background: rgba(7, 10, 24, 0.82);
    padding: 16px;
    box-shadow: inset 0 0 24px rgba(139, 92, 246, 0.08);
}

.metric-label, .radar-label, .section-title {
    font-family: 'JetBrains Mono', monospace;
}

.metric-label, .radar-label {
    color: #98A6BA;
    font-size: 0.76rem;
    text-transform: uppercase;
}

.metric-value {
    margin-top: 8px;
    font-size: 1.85rem;
    color: #FFFFFF;
    font-weight: 800;
}

.radar-title {
    margin-top: 9px;
    color: #FFFFFF;
    font-weight: 800;
    line-height: 1.15;
}

.radar-meta {
    color: #B7C5D9;
    font-size: 0.86rem;
    margin-top: 8px;
}

.callout {
    border-left: 3px solid #22D3EE;
    background: rgba(8, 15, 34, 0.88);
    padding: 12px 14px;
    color: #DDEBFF;
}

.section-title {
    margin-top: 20px;
    color: #67E8F9;
    font-weight: 700;
}

div[data-testid="stDataFrame"], div[data-testid="stTable"] {
    border: 1px solid rgba(34, 211, 238, 0.16);
    border-radius: 8px;
}

.stAlert {
    border-radius: 8px;
}

.stDownloadButton button, .stButton button {
    border-radius: 6px;
    border: 1px solid rgba(34, 211, 238, 0.65);
    background: linear-gradient(135deg, #0EA5E9, #8B5CF6 55%, #EC4899);
    color: #FFFFFF;
    font-weight: 800;
    box-shadow: 0 0 22px rgba(34, 211, 238, 0.22);
}

.stDownloadButton button:hover, .stButton button:hover {
    border-color: #F472B6;
    box-shadow: 0 0 28px rgba(244, 114, 182, 0.34);
}

footer, #MainMenu {
    visibility: hidden;
}

@media (max-width: 1100px) {
    .radar-grid, .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 620px) {
    .radar-grid, .metric-grid {
        grid-template-columns: 1fr;
    }
    .hero-title {
        font-size: 1.75rem;
    }
}
</style>
"""


def apply_theme():
    st.markdown(CYBER_CSS, unsafe_allow_html=True)


def hero():
    st.markdown(
        """
        <div class="hero">
            <p class="hero-title">Cyberdeck Retro</p>
            <p class="hero-subtitle">
                Um painel gratuito para revisar livros, comparar sinais de confiança
                e navegar por reviews com estética arcade cyberpunk. Sem API paga,
                sem tokens, sem scraping.
            </p>
            <div class="chip-row">
                <span class="chip">Review Scanner</span>
                <span class="chip">Radar de Compra</span>
                <span class="chip">Comparador</span>
                <span class="chip">Custo zero</span>
                <span class="chip">Night City UI</span>
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


def radar_panel(cards: dict):
    html = ["<div class='radar-grid'>"]
    for label, row in cards.items():
        if row is None:
            title = "Sem dados"
            meta = "Ajuste os filtros"
        else:
            title = escape(str(row["book title"]))
            meta = escape(
                f"Nota {row['rating']:.1f} | Confiança {row['trust_score']:.0f} | "
                f"Reviews {int(row['reviews'])}"
            )
        html.append(
            f"""
            <div class="radar-card">
                <div class="radar-label">{label}</div>
                <div class="radar-title">{title}</div>
                <div class="radar-meta">{meta}</div>
            </div>
            """
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def callout(label: str, value: str):
    st.markdown(
        f"<div class='callout'><strong>{label}</strong><br>{value}</div>",
        unsafe_allow_html=True,
    )


def section(title: str):
    st.markdown(f"<p class='section-title'>{title}</p>", unsafe_allow_html=True)


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


def scatter_books(summary: pd.DataFrame):
    fig = px.scatter(
        summary,
        x="book price",
        y="rating",
        hover_name="book title",
        color="genre",
        size="trust_score",
        title="Preço x avaliação x confiança",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    return style_chart(fig)


def bar_reviews_by_rating(reviews: pd.DataFrame):
    rating_counts = (
        reviews["reviewer rating"]
        .value_counts()
        .rename_axis("Nota")
        .reset_index(name="Quantidade")
        .sort_values("Nota")
    )
    fig = px.bar(
        rating_counts,
        x="Nota",
        y="Quantidade",
        title="Distribuição das notas",
        color="Nota",
        color_continuous_scale="Turbo",
    )
    fig.update_layout(coloraxis_showscale=False)
    return style_chart(fig)


def pie_trust(reviews: pd.DataFrame):
    trust = (
        reviews["trust_label"]
        .value_counts()
        .rename_axis("Faixa")
        .reset_index(name="Quantidade")
    )
    fig = px.pie(
        trust,
        names="Faixa",
        values="Quantidade",
        title="Faixas de confiança das reviews",
        color="Faixa",
        color_discrete_map={
            "Forte": "#22D3EE",
            "Boa": "#8B5CF6",
            "Revisar": "#F472B6",
        },
        hole=0.48,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return style_chart(fig)
