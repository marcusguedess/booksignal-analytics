import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuração da aba do navegador
st.set_page_config(page_title="Cyberdeck Retro", layout="wide")

# --- ESTILO CYBERPUNK / NIGHT CITY ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    .stApp {
        background: radial-gradient(circle at top left, #1B0035 0%, #05030A 35%, #050407 100%);
        color: #E6EFFB;
        font-family: 'VT323', monospace;
        font-size: 18px;
    }
    .css-18ni7ap.e8zbici2,
    .stContainer {
        background: rgba(12, 5, 20, 0.95) !important;
        border: 1px solid rgba(128, 0, 255, 0.55) !important;
        box-shadow: 0 0 30px rgba(128, 0, 255, 0.3);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(20, 0, 40, 0.96) 0%, rgba(4, 2, 12, 0.95) 100%);
        border-right: 2px solid #7C3AED;
    }
    h1, h2, h3, h4 {
        color: #72FFEE !important;
        font-family: 'Press Start 2P', cursive;
        text-shadow: 0 0 12px rgba(114, 255, 238, 0.6);
    }
    .stButton>button {
        background: linear-gradient(135deg, #5B21B6, #0EA5E9) !important;
        color: #FFFFFF !important;
        border: 1px solid #8B5CF6 !important;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.35);
    }
    .stTextInput>div>label, .stSlider>div>label, .stSelectbox>div>label {
        color: #A78BFA !important;
    }
    .stCodeBlock, .stMarkdown code, pre {
        background: #030617 !important;
        color: #22D3EE !important;
        border: 1px solid rgba(34, 211, 238, 0.4) !important;
        box-shadow: inset 0 0 25px rgba(34, 211, 238, 0.12);
    }
    .streamlit-expanderHeader {
        color: #FBCFE8 !important;
    }
    .hack-banner {
        padding: 16px;
        background: rgba(8, 15, 34, 0.95);
        border: 1px solid #38BDF8;
        border-radius: 12px;
        color: #22D3EE;
        margin-bottom: 18px;
    }
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Cyberdeck Retro - Análise de Dados")
st.markdown("**Iniciando conexão com o servidor de dados...** :zap:")
st.markdown("**Status:** `ONLINE`  |  **Host:** Night City Grid 13")
st.write("---")

# Carregando os dados
BASE_DIR = Path(__file__).resolve().parent
df_books = pd.read_csv(BASE_DIR / "Top-100 Trending Books.csv")
df_reviews = pd.read_csv(BASE_DIR / "customer reviews.csv")

# Menu lateral
st.sidebar.markdown("### PAINEL DE CONTROLE CYBERDECK")
generos = df_books['genre'].dropna().unique().tolist()
genero_selecionado = st.sidebar.selectbox("Filtro de gênero:", ["Todas"] + generos)

titulo_busca = st.sidebar.text_input("Buscar título de livro:", "")

preco_maximo = st.sidebar.slider(
    "Orçamento máximo ($):",
    min_value=float(df_books['book price'].min()),
    max_value=float(df_books['book price'].max()),
    value=float(df_books['book price'].max())
)

nota_minima = st.sidebar.slider(
    "Avaliação mínima:",
    min_value=float(df_books['rating'].min()),
    max_value=float(df_books['rating'].max()),
    value=float(df_books['rating'].min()),
    step=0.1
)

mostrar_somente_verificados = st.sidebar.checkbox("Mostrar apenas reviews verificadas", value=False)
hacker_mode = st.sidebar.checkbox("Modo Hacker", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### Visão Geral")
if genero_selecionado != "Todas":
    st.sidebar.write(f"Gênero: **{genero_selecionado}**")
if titulo_busca:
    st.sidebar.write(f"Buscando: **{titulo_busca}**")
st.sidebar.write(f"Preço máximo: **${preco_maximo:.2f}**")
st.sidebar.write(f"Avaliação mínima: **{nota_minima:.1f}**")
if hacker_mode:
    st.sidebar.markdown("<span style='color:#34D399;'>MODO HACKER ATIVADO</span>", unsafe_allow_html=True)

# Aplicando filtros
df_filtrado = df_books.copy()

if genero_selecionado != "Todas":
    df_filtrado = df_filtrado[df_filtrado['genre'] == genero_selecionado]

if titulo_busca:
    df_filtrado = df_filtrado[df_filtrado['book title'].str.contains(titulo_busca, case=False, na=False, regex=False)]

if df_filtrado.empty:
    st.warning("Nenhum livro encontrado com esses filtros. Ajuste a busca ou os parâmetros.")

df_filtrado = df_filtrado[(df_filtrado['book price'] <= preco_maximo) &
                          (df_filtrado['rating'] >= nota_minima)]

if mostrar_somente_verificados:
    df_reviews = df_reviews[df_reviews['is_verified'] == True]

# Métricas principais
total_livros = len(df_filtrado)
media_rating = df_filtrado['rating'].mean() if total_livros else 0
media_preco = df_filtrado['book price'].mean() if total_livros else 0

total_reviews = len(df_reviews)
media_avaliacoes = df_reviews['reviewer rating'].mean() if total_reviews else 0
verificado_pct = (df_reviews['is_verified'].mean() * 100) if total_reviews else 0

st.markdown("## Painel de Controle")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("Livros ativos", total_livros)
metric_col2.metric("Nota média de livros", f"{media_rating:.2f}")
metric_col3.metric("Reviews carregadas", total_reviews)
metric_col4.metric("Reviews verificadas", f"{verificado_pct:.1f}%")

if hacker_mode:
    with st.expander("💾 Hacker Console - Fluxo de Dados"):
        st.markdown(
            "<div class='hack-banner'><strong>HACKER CONSOLE:</strong> sistema em modo stealth, exibindo pacotes do grid e análise em tempo real.</div>",
            unsafe_allow_html=True
        )
        st.code(
            """[NIGHT-CORE] Iniciando interface...
[NETRUN] Validando porta 31337...
[OK] Firewall bypassed.
[DATASTREAM] Conectado à base de livros e reviews.
[PROC] Filtrando payloads por gênero, título e avaliação.
[ALERT] Modo hacker ativo. Visualização ampliada.
[STREAM] Próxima atualização em 0.7s...""",
            language='bash'
        )
        st.markdown(
            "<div class='hack-banner' style='border-color:#F472B6;'>"
            "<strong>TERM SHELL:</strong> hardware estabilizado. Gráficos ajustados ao modo cyberpunk."
            "</div>",
            unsafe_allow_html=True
        )

st.write("---")

# Gráficos principais
chart_col1, chart_col2 = st.columns([2, 1])
with chart_col1:
    st.markdown("### Matriz de Preço x Avaliação")
    fig_scatter = px.scatter(
        df_filtrado,
        x="book price",
        y="rating",
        hover_name="book title",
        color="genre",
        title="Preco vs Rating por Livro",
        color_discrete_sequence=px.colors.sequential.Emrld
    )
    fig_scatter.update_layout(
        paper_bgcolor='#05030A',
        plot_bgcolor='#05030A',
        font_color='#E6E6FF',
        title_font_family="'Press Start 2P', cursive",
        legend_title_text='Gênero'
    )
    st.plotly_chart(fig_scatter, width='stretch')

with chart_col2:
    st.markdown("### Distribuição de Reviews")
    rating_counts = df_reviews['reviewer rating'].value_counts().sort_index().reset_index()
    rating_counts.columns = ['Avaliação', 'Contagem']
    fig_rating = px.bar(
        rating_counts,
        x='Avaliação',
        y='Contagem',
        title='Distribuição de Notas dos Reviews',
        color='Avaliação',
        color_continuous_scale='Turbo'
    )
    fig_rating.update_layout(
        paper_bgcolor='#05030A',
        plot_bgcolor='#05030A',
        font_color='#E6E6FF',
        title_font_family="'Press Start 2P', cursive",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_rating, width='stretch')

st.markdown("---")

# Painel de reviews e livros mais comentados
review_col1, review_col2 = st.columns(2)
with review_col1:
    st.markdown("### Livros por Ano de Publicação")
    livros_por_ano = df_filtrado['year of publication'].value_counts().reset_index()
    livros_por_ano.columns = ['Ano', 'Quantidade']
    fig_bar = px.bar(
        livros_por_ano,
        x='Ano',
        y='Quantidade',
        title='Livros Disponíveis por Ano',
        color='Quantidade',
        color_continuous_scale=['#8B5CF6', '#EC4899']
    )
    fig_bar.update_layout(
        paper_bgcolor='#05030A',
        plot_bgcolor='#05030A',
        font_color='#E6E6FF',
        title_font_family="'Press Start 2P', cursive",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, width='stretch')

with review_col2:
    st.markdown("### Verificação de Reviews")
    verified = df_reviews['is_verified'].sum()
    unverified = total_reviews - verified
    df_verify = pd.DataFrame({
        'Status': ['Verificado', 'Não Verificado'],
        'Contagem': [verified, unverified]
    })
    fig_pie = px.pie(
        df_verify,
        names='Status',
        values='Contagem',
        title='Proporção de Reviews Verificadas',
        color='Status',
        color_discrete_map={'Verificado': '#22D3EE', 'Não Verificado': '#F472B6'}
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        paper_bgcolor='#05030A',
        plot_bgcolor='#05030A',
        font_color='#E6E6FF',
        title_font_family="'Press Start 2P', cursive"
    )
    st.plotly_chart(fig_pie, width='stretch')

st.markdown("---")

with st.expander("📡 Top Livros mais comentados e últimas reviews"):
    top_reviews = (
        df_reviews['book name']
            .value_counts()
            .rename_axis('book name')
            .reset_index(name='review_count')
            .head(10)
    )
    st.markdown("#### Top 10 livros com mais reviews")
    st.table(top_reviews)

    st.markdown("#### Últimas reviews carregadas")
    latest_reviews = df_reviews.sort_values(by='timestamp', ascending=False).head(8)
    st.dataframe(
        latest_reviews[['book name', 'reviewer', 'reviewer rating', 'is_verified', 'date', 'review title']].rename(columns={
            'book name': 'Livro',
            'reviewer': 'Revisor',
            'reviewer rating': 'Nota',
            'is_verified': 'Verificado',
            'date': 'Data',
            'review title': 'Título do Review'
        }),
        width='stretch'
    )

st.markdown("---")

st.markdown(
    "*Sistema inspirado em consoles de dados de Night City — visual cyberpunk com foco em análises reais.*"
)
