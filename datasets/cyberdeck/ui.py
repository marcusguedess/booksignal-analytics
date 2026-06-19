import pandas as pd
import plotly.express as px
import streamlit as st


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

.hero, .callout, .metric-card {
    border-radius: 8px;
}

.hero {
    position: relative;
    overflow: hidden;
    min-height: 260px;
    padding: 28px;
    border: 1px solid rgba(34, 211, 238, 0.38);
    background:
        linear-gradient(180deg, rgba(8, 10, 34, 0.96), rgba(5, 3, 18, 0.98) 48%, rgba(7, 3, 12, 1)),
        rgba(3, 7, 18, 0.90);
    box-shadow: 0 0 42px rgba(34, 211, 238, 0.16), inset 0 0 80px rgba(236, 72, 153, 0.08);
}

.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(rgba(34, 211, 238, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34, 211, 238, 0.06) 1px, transparent 1px);
    background-size: 32px 32px;
    mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.75) 48%, rgba(0,0,0,0.95) 100%);
    pointer-events: none;
}

.hero:after {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        180deg,
        rgba(255,255,255,0.035) 0,
        rgba(255,255,255,0.035) 1px,
        transparent 1px,
        transparent 5px
    );
    pointer-events: none;
    mix-blend-mode: screen;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 760px;
}

.hero-title {
    margin: 0;
    max-width: 720px;
    font-size: 2.7rem;
    line-height: 1.08;
    font-weight: 800;
    text-shadow: 0 0 18px rgba(34, 211, 238, 0.46), 0 0 34px rgba(244, 114, 182, 0.22);
}

.hero-subtitle {
    max-width: 920px;
    margin: 12px 0 0;
    color: #C9D7EA;
    font-size: 1rem;
}

.chip-row {
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

.pixel-scene {
    position: absolute;
    right: 24px;
    bottom: 0;
    width: min(42vw, 520px);
    height: 230px;
    z-index: 1;
}

.pixel-sun {
    position: absolute;
    right: 110px;
    top: 12px;
    width: 150px;
    height: 150px;
    background:
        repeating-linear-gradient(
            180deg,
            #FDE047 0 12px,
            #FB7185 12px 22px,
            transparent 22px 30px
        );
    clip-path: polygon(8% 22%, 18% 8%, 50% 0%, 82% 8%, 92% 22%, 100% 50%, 92% 78%, 82% 92%, 50% 100%, 18% 92%, 8% 78%, 0% 50%);
    filter: drop-shadow(0 0 28px rgba(251, 113, 133, 0.72));
    opacity: 0.92;
}

.pixel-moon {
    position: absolute;
    right: 36px;
    top: 28px;
    width: 10px;
    height: 10px;
    background: #A7F3FF;
    box-shadow:
        22px 20px #A7F3FF,
        -26px 34px #E879F9,
        42px 58px #67E8F9,
        -58px 78px #A78BFA;
}

.skyline {
    position: absolute;
    right: 0;
    bottom: 24px;
    display: flex;
    align-items: end;
    gap: 8px;
}

.tower {
    width: 42px;
    background: linear-gradient(180deg, #111827, #020617);
    border: 1px solid rgba(34, 211, 238, 0.34);
    box-shadow: inset 0 0 18px rgba(34, 211, 238, 0.08), 0 0 18px rgba(139, 92, 246, 0.16);
}

.tower:before {
    content: "";
    display: block;
    width: 100%;
    height: 100%;
    background:
        repeating-linear-gradient(180deg, transparent 0 12px, rgba(34, 211, 238, 0.55) 12px 15px),
        repeating-linear-gradient(90deg, transparent 0 12px, rgba(244, 114, 182, 0.45) 12px 15px);
    opacity: 0.72;
}

.t1 { height: 88px; }
.t2 { height: 138px; }
.t3 { height: 112px; }
.t4 { height: 164px; }
.t5 { height: 96px; }
.t6 { height: 126px; }

.pixel-road {
    position: absolute;
    right: -30px;
    bottom: -42px;
    width: 520px;
    height: 118px;
    background:
        linear-gradient(90deg, transparent 0 46%, rgba(34, 211, 238, 0.72) 46% 47%, transparent 47% 53%, rgba(244, 114, 182, 0.72) 53% 54%, transparent 54%),
        repeating-linear-gradient(90deg, rgba(34, 211, 238, 0.0) 0 35px, rgba(34, 211, 238, 0.20) 35px 37px),
        linear-gradient(180deg, rgba(15, 23, 42, 0), rgba(15, 23, 42, 0.95));
    transform: perspective(260px) rotateX(58deg);
    transform-origin: bottom;
}

.metric-grid {
    display: grid;
    gap: 12px;
}

.metric-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    margin: 18px 0 10px;
}

.metric-card {
    border: 1px solid rgba(34, 211, 238, 0.26);
    background: rgba(7, 10, 24, 0.82);
    padding: 16px;
    box-shadow: inset 0 0 24px rgba(139, 92, 246, 0.08);
}

.metric-label {
    font-family: 'JetBrains Mono', monospace;
}

.metric-label {
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

.callout {
    border-left: 3px solid #22D3EE;
    background: rgba(8, 15, 34, 0.88);
    padding: 12px 14px;
    color: #DDEBFF;
}

.creator-signature {
    margin-top: 24px;
    padding: 12px 14px;
    border-top: 1px solid rgba(34, 211, 238, 0.26);
    color: #9FB5D8;
    font-family: "Courier New", monospace;
    font-size: 0.78rem;
    letter-spacing: 0;
    text-align: right;
}

.creator-signature strong {
    color: #FDE68A;
    text-shadow: 0 0 14px rgba(253, 230, 138, 0.42);
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
    .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 620px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }
    .hero-title {
        font-size: 1.75rem;
    }
    .pixel-scene {
        opacity: 0.34;
        right: -90px;
        width: 420px;
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
            <div class="hero-content">
                <p class="hero-title">Review Scanner Arcade</p>
                <p class="hero-subtitle">
                    Livros, reviews e sinais de confiança em um painel neon feito para leitura rápida.
                </p>
                <div class="chip-row">
                    <span class="chip">Radar</span>
                    <span class="chip">Comparador</span>
                    <span class="chip">Score local</span>
                    <span class="chip">Upload CSV</span>
                    <span class="chip">Custo zero</span>
                </div>
            </div>
            <div class="pixel-scene" aria-hidden="true">
                <div class="pixel-sun"></div>
                <div class="pixel-moon"></div>
                <div class="skyline">
                    <div class="tower t1"></div>
                    <div class="tower t2"></div>
                    <div class="tower t3"></div>
                    <div class="tower t4"></div>
                    <div class="tower t5"></div>
                    <div class="tower t6"></div>
                </div>
                <div class="pixel-road"></div>
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
    columns = st.columns(4)
    for column, (label, row) in zip(columns, cards.items()):
        with column:
            with st.container(border=True):
                st.caption(label.upper())
                if row is None:
                    st.markdown("**Sem dados**")
                    st.caption("Ajuste os filtros")
                else:
                    st.markdown(f"**{row['book title']}**")
                    st.metric("Nota", f"{row['rating']:.1f}")
                    st.caption(
                        f"Confiança {row['trust_score']:.0f}/100 | "
                        f"Reviews {int(row['reviews'])}"
                    )


def callout(label: str, value: str):
    st.markdown(
        f"<div class='callout'><strong>{label}</strong><br>{value}</div>",
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
