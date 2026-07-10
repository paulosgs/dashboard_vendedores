import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Dashboard de Penalidades e Trocas",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# PALETA
# ==========================================================
FUNDO = "#05070D"
CARD = "#0B1120"
CARD_2 = "#0F172A"
AZUL_NEON = "#00C2FF"
AZUL_NEON_2 = "#007BFF"
VERDE = "#00D084"
VERMELHO = "#FF4D6D"
AMARELO = "#FDBE2D"
BRANCO = "#F8FAFC"
CINZA = "#94A3B8"

# ==========================================================
# CSS
# ==========================================================
st.markdown(f"""
<style>
    .stApp {{
        background-color: {FUNDO};
    }}

    .main {{
        background-color: {FUNDO};
    }}

    .block-container {{
        padding-top: 5rem;
        padding-bottom: 1rem;
        padding-left: 1.8rem;
        padding-right: 1.8rem;
        max-width: 98%;
    }}

    footer {{visibility: hidden;}}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #070B14 0%, #0C1220 100%);
        border-right: 1px solid rgba(0,194,255,0.15);
    }}

    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}

    .titulo-dashboard {{
        font-size: 38px;
        font-weight: 900;
        color: {BRANCO};
        margin-bottom: 0px;
        letter-spacing: -0.5px;
    }}

    .subtitulo-dashboard {{
        font-size: 16px;
        color: #C7D2FE;
        margin-top: 2px;
        margin-bottom: 18px;
    }}

    .secao-titulo {{
        font-size: 25px;
        font-weight: 850;
        color: {BRANCO};
        margin-top: 10px;
        margin-bottom: 10px;
    }}

    .subsecao-titulo {{
        font-size: 18px;
        font-weight: 800;
        color: {BRANCO};
        margin-top: 8px;
        margin-bottom: 10px;
    }}

    .kpi-card {{
        background: linear-gradient(180deg, {CARD} 0%, {CARD_2} 100%);
        border: 1px solid rgba(0,194,255,0.20);
        border-left: 4px solid {AZUL_NEON};
        border-radius: 16px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 0 24px rgba(0,194,255,0.07);
        min-height: 128px;
    }}

    .kpi-card-alerta {{
        background: linear-gradient(180deg, #1B0E14 0%, #25101A 100%);
        border: 1px solid rgba(255,77,109,0.25);
        border-left: 4px solid {VERMELHO};
        box-shadow: 0 0 22px rgba(255,77,109,0.08);
    }}

    .kpi-card-ok {{
        background: linear-gradient(180deg, #0B1A16 0%, #10221C 100%);
        border: 1px solid rgba(0,208,132,0.22);
        border-left: 4px solid {VERDE};
        box-shadow: 0 0 22px rgba(0,208,132,0.07);
    }}

    .kpi-card-neutro {{
        border-left: 4px solid {AZUL_NEON};
    }}

    .kpi-titulo {{
        font-size: 13px;
        color: #B6C2D1;
        margin-bottom: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .kpi-valor {{
        font-size: 31px;
        font-weight: 900;
        color: white;
        line-height: 1.05;
    }}

    .kpi-rodape {{
        font-size: 12px;
        color: #9FB3C8;
        margin-top: 8px;
    }}

    .motivos-box {{
        background: linear-gradient(180deg, #0B1120 0%, #0F172A 100%);
        border: 1px solid rgba(0,194,255,0.18);
        border-left: 4px solid {AMARELO};
        border-radius: 16px;
        padding: 16px 18px;
        margin-top: 10px;
        margin-bottom: 20px;
        box-shadow: 0 0 18px rgba(0,194,255,0.06);
    }}

    .motivos-titulo {{
        font-size: 18px;
        font-weight: 800;
        color: {BRANCO};
        margin-bottom: 12px;
    }}

    .motivos-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(260px, 1fr));
        gap: 8px 20px;
    }}

    .motivo-item {{
        font-size: 14px;
        color: #D9E3F0;
        line-height: 1.5;
    }}

    .motivo-codigo {{
        color: {AZUL_NEON};
        font-weight: 800;
    }}

    .motivo-alerta {{
        font-size: 12px;
        color: {CINZA};
        margin-top: 12px;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 48px;
        border-radius: 12px;
        padding-left: 18px;
        padding-right: 18px;
        font-weight: 800;
        background-color: #0B1220;
        color: white;
        border: 1px solid rgba(0,194,255,0.12);
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, #07283A 0%, #0A3954 100%) !important;
        color: white !important;
        border: 1px solid rgba(0,194,255,0.35) !important;
        box-shadow: 0 0 16px rgba(0,194,255,0.10);
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid rgba(0,194,255,0.12);
        border-radius: 12px;
        overflow: hidden;
    }}

    hr {{
        border-color: rgba(255,255,255,0.06);
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# FUNÇÕES
# ==========================================================
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor):
    return f"{valor:.2%}".replace(".", ",")

def abreviar_nome(nome, limite=42):
    nome = str(nome)
    return nome if len(nome) <= limite else nome[:limite] + "..."

def criar_card(titulo, valor, rodape="", tipo="neutro"):
    classe = "kpi-card"
    if tipo == "alerta":
        classe += " kpi-card-alerta"
    elif tipo == "ok":
        classe += " kpi-card-ok"
    else:
        classe += " kpi-card-neutro"

    st.markdown(
        f"""
        <div class="{classe}">
            <div class="kpi-titulo">{titulo}</div>
            <div class="kpi-valor">{valor}</div>
            <div class="kpi-rodape">{rodape}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def estilo_plotly(fig):
    fig.update_layout(
        paper_bgcolor=FUNDO,
        plot_bgcolor=FUNDO,
        font=dict(color=BRANCO, size=12),
        title_font=dict(size=18, color=BRANCO),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=BRANCO)
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        tickfont=dict(color=BRANCO)
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        tickfont=dict(color=BRANCO)
    )
    return fig

def to_excel_bytes(df_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_export.to_excel(writer, index=False, sheet_name="Dashboard")
    output.seek(0)
    return output.getvalue()

# ==========================================================
# LEITURA E TRATAMENTO DA BASE
# ==========================================================
@st.cache_data
def carregar_dados(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel("analise_vendedores.xlsx")

    df.columns = df.columns.str.strip().str.upper()

    colunas_necessarias = [
        "CODSUPERVISOR",
        "SUPERVISOR",
        "RCA",
        "META_CC",
        "VLVENDA",
        "TV11",
        "TV5",
        "DEV_C_PENALIDADE",
        "DEV_GRANDES_REDES"
    ]

    faltando = [c for c in colunas_necessarias if c not in df.columns]
    if faltando:
        st.error(f"As seguintes colunas não foram encontradas na planilha: {faltando}")
        st.stop()

    if "ACIMA_TABELA" not in df.columns:
        df["ACIMA_TABELA"] = 0

    colunas_numericas = [
        "META_CC",
        "VLVENDA",
        "TV11",
        "TV5",
        "DEV_C_PENALIDADE",
        "DEV_GRANDES_REDES",
        "ACIMA_TABELA"
    ]

    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["SUPERVISOR"] = df["SUPERVISOR"].astype(str).str.strip()
    df["RCA"] = df["RCA"].astype(str).str.strip()

    # Penalidade
    df["DEV. C/ PENALIDADE ORIGINAL"] = df["DEV_C_PENALIDADE"]
    df["PENALIDADE_VALOR"] = df["DEV_C_PENALIDADE"].abs()

    # Indicadores
    df["% META TROCA"] = np.where(df["META_CC"] > 0, df["TV11"] / df["META_CC"], 0)
    df["DESVIO META TROCA"] = df["TV11"] - df["META_CC"]
    df["% TROCA SOBRE VENDA"] = np.where(df["VLVENDA"] > 0, df["TV11"] / df["VLVENDA"], 0)

    df["% PENALIDADE SOBRE VENDA"] = np.where(
        df["VLVENDA"] > 0,
        df["PENALIDADE_VALOR"] / df["VLVENDA"],
        0
    )

    df["% DEV. GRANDES REDES SOBRE VENDA"] = np.where(
        df["VLVENDA"] > 0,
        df["DEV_GRANDES_REDES"].abs() / df["VLVENDA"],
        0
    )

    df["% BONIFICAÇÃO SOBRE VENDA"] = np.where(
        df["VLVENDA"] > 0,
        df["TV5"].abs() / df["VLVENDA"],
        0
    )

    df["STATUS META TROCA"] = np.where(
        df["TV11"] > df["META_CC"],
        "ACIMA DA META",
        "DENTRO DA META"
    )

    df["TEM PENALIDADE"] = np.where(df["PENALIDADE_VALOR"] > 0, "SIM", "NÃO")

    # Renomear colunas
    df = df.rename(columns={
        "CODSUPERVISOR": "COD. SUPERVISOR",
        "SUPERVISOR": "SUPERVISOR",
        "RCA": "VENDEDOR",
        "META_CC": "META TROCA",
        "VLVENDA": "VENDAS",
        "TV11": "TROCAS TV11",
        "TV5": "BONIFICAÇÕES TV5",
        "DEV_C_PENALIDADE": "DEV. C/ PENALIDADE",
        "DEV_GRANDES_REDES": "DEV. GRANDES REDES",
        "ACIMA_TABELA": "ACIMA DA TABELA"
    })

    return df

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.markdown("## 📂 Base do Dashboard")

uploaded_file = st.sidebar.file_uploader(
    "Carregar nova planilha (.xlsx)",
    type=["xlsx"]
)

col_sb1, col_sb2 = st.sidebar.columns(2)

with col_sb1:
    if st.button("🔄 Atualizar dashboard", key="atualizar_dashboard"):
        st.rerun()

with col_sb2:
    if st.button("🧹 Limpar filtros", key="limpar_filtros"):
        st.rerun()

if st.sidebar.button("🔄 Limpar cache da base"):
    st.cache_data.clear()
    st.rerun()

df = carregar_dados(uploaded_file)

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎯 Filtros")

lista_supervisores = sorted(df["SUPERVISOR"].dropna().unique())
supervisores_sel = st.sidebar.multiselect(
    "Supervisor",
    options=lista_supervisores,
    default=[]
)

if supervisores_sel:
    df_filtrado = df[df["SUPERVISOR"].isin(supervisores_sel)].copy()
else:
    df_filtrado = df.copy()

lista_vendedores = sorted(df_filtrado["VENDEDOR"].dropna().unique())
vendedores_sel = st.sidebar.multiselect(
    "Vendedor",
    options=lista_vendedores,
    default=[]
)

if vendedores_sel:
    df_filtrado = df_filtrado[df_filtrado["VENDEDOR"].isin(vendedores_sel)].copy()

status_meta_sel = st.sidebar.multiselect(
    "Status da Meta de Troca",
    options=["ACIMA DA META", "DENTRO DA META"],
    default=[]
)

if status_meta_sel:
    df_filtrado = df_filtrado[df_filtrado["STATUS META TROCA"].isin(status_meta_sel)].copy()

penalidade_sel = st.sidebar.multiselect(
    "Situação de Penalidade",
    options=["SIM", "NÃO"],
    default=[]
)

if penalidade_sel:
    df_filtrado = df_filtrado[df_filtrado["TEM PENALIDADE"].isin(penalidade_sel)].copy()

st.sidebar.markdown("---")
st.sidebar.write(f"**Registros filtrados:** {len(df_filtrado)}")

if uploaded_file is not None:
    st.sidebar.success(f"Planilha carregada: {uploaded_file.name}")
else:
    st.sidebar.info("Usando arquivo padrão: analise_vendedores.xlsx")

# ==========================================================
# BASE AGRUPADA POR VENDEDOR
# ==========================================================
base_vendedor = df_filtrado.groupby(["SUPERVISOR", "VENDEDOR"], as_index=False).agg({
    "META TROCA": "sum",
    "TROCAS TV11": "sum",
    "VENDAS": "sum",
    "BONIFICAÇÕES TV5": "sum",
    "DEV. C/ PENALIDADE ORIGINAL": "sum",
    "PENALIDADE_VALOR": "sum",
    "DEV. GRANDES REDES": "sum",
    "ACIMA DA TABELA": "sum"
})

base_vendedor["% META TROCA"] = np.where(
    base_vendedor["META TROCA"] > 0,
    base_vendedor["TROCAS TV11"] / base_vendedor["META TROCA"],
    0
)

base_vendedor["DESVIO META TROCA"] = base_vendedor["TROCAS TV11"] - base_vendedor["META TROCA"]

base_vendedor["% TROCA SOBRE VENDA"] = np.where(
    base_vendedor["VENDAS"] > 0,
    base_vendedor["TROCAS TV11"] / base_vendedor["VENDAS"],
    0
)

base_vendedor["% PENALIDADE SOBRE VENDA"] = np.where(
    base_vendedor["VENDAS"] > 0,
    base_vendedor["PENALIDADE_VALOR"] / base_vendedor["VENDAS"],
    0
)

base_vendedor["% DEV. GRANDES REDES SOBRE VENDA"] = np.where(
    base_vendedor["VENDAS"] > 0,
    base_vendedor["DEV. GRANDES REDES"].abs() / base_vendedor["VENDAS"],
    0
)

base_vendedor["STATUS META TROCA"] = np.where(
    base_vendedor["TROCAS TV11"] > base_vendedor["META TROCA"],
    "ACIMA DA META",
    "DENTRO DA META"
)

base_vendedor["TEM PENALIDADE"] = np.where(
    base_vendedor["PENALIDADE_VALOR"] > 0,
    "SIM",
    "NÃO"
)

base_vendedor["VENDEDOR_CURTO"] = base_vendedor["VENDEDOR"].apply(lambda x: abreviar_nome(x, 42))

# ==========================================================
# BASE AGRUPADA POR SUPERVISOR
# ==========================================================
base_supervisor = df_filtrado.groupby("SUPERVISOR", as_index=False).agg({
    "META TROCA": "sum",
    "TROCAS TV11": "sum",
    "VENDAS": "sum",
    "BONIFICAÇÕES TV5": "sum",
    "DEV. C/ PENALIDADE ORIGINAL": "sum",
    "PENALIDADE_VALOR": "sum",
    "DEV. GRANDES REDES": "sum"
})

base_supervisor["% META TROCA"] = np.where(
    base_supervisor["META TROCA"] > 0,
    base_supervisor["TROCAS TV11"] / base_supervisor["META TROCA"],
    0
)

base_supervisor["DESVIO META TROCA"] = base_supervisor["TROCAS TV11"] - base_supervisor["META TROCA"]

base_supervisor["% TROCA SOBRE VENDA"] = np.where(
    base_supervisor["VENDAS"] > 0,
    base_supervisor["TROCAS TV11"] / base_supervisor["VENDAS"],
    0
)

base_supervisor["% PENALIDADE SOBRE VENDA"] = np.where(
    base_supervisor["VENDAS"] > 0,
    base_supervisor["PENALIDADE_VALOR"] / base_supervisor["VENDAS"],
    0
)

base_supervisor["RCAS ACIMA META"] = (
    base_vendedor.groupby("SUPERVISOR")["STATUS META TROCA"]
    .apply(lambda x: (x == "ACIMA DA META").sum())
    .reindex(base_supervisor["SUPERVISOR"])
    .fillna(0)
    .values
)

base_supervisor["RCAS COM PENALIDADE"] = (
    base_vendedor.groupby("SUPERVISOR")["TEM PENALIDADE"]
    .apply(lambda x: (x == "SIM").sum())
    .reindex(base_supervisor["SUPERVISOR"])
    .fillna(0)
    .values
)

base_supervisor["TOTAL RCAS"] = (
    base_vendedor.groupby("SUPERVISOR")["VENDEDOR"]
    .count()
    .reindex(base_supervisor["SUPERVISOR"])
    .fillna(0)
    .values
)

# ==========================================================
# KPIs
# ==========================================================
total_penalidade = base_vendedor["PENALIDADE_VALOR"].sum()
total_vendas = base_vendedor["VENDAS"].sum()
perc_penalidade_venda = total_penalidade / total_vendas if total_vendas > 0 else 0
rcas_com_penalidade = int((base_vendedor["PENALIDADE_VALOR"] > 0).sum())

if len(base_vendedor[base_vendedor["PENALIDADE_VALOR"] > 0]) > 0:
    maior_penalidade_row = base_vendedor.sort_values("PENALIDADE_VALOR", ascending=False).iloc[0]
    maior_penalidade_valor = maior_penalidade_row["PENALIDADE_VALOR"]
    maior_penalidade_nome = abreviar_nome(maior_penalidade_row["VENDEDOR"], 34)
else:
    maior_penalidade_valor = 0
    maior_penalidade_nome = "-"

meta_troca_total = base_vendedor["META TROCA"].sum()
troca_realizada_total = base_vendedor["TROCAS TV11"].sum()
perc_meta_troca = troca_realizada_total / meta_troca_total if meta_troca_total > 0 else 0
qtd_acima_meta = int((base_vendedor["STATUS META TROCA"] == "ACIMA DA META").sum())

# ==========================================================
# TÍTULO
# ==========================================================
st.markdown('<div class="titulo-dashboard">💸 Dashboard de Penalidades e Trocas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitulo-dashboard">Foco principal em penalidade de devolução, com trocas e devoluções como apoio à gestão dos vendedores e supervisores</div>',
    unsafe_allow_html=True
)

# ==========================================================
# QUADRO DE MOTIVOS DE PENALIDADE
# ==========================================================
st.markdown("""
<div class="motivos-box">
    <div class="motivos-titulo">📌 Motivos de devolução que geram penalidade ao vendedor</div>

    <div class="motivos-grid">
        <div class="motivo-item"><span class="motivo-codigo">6</span> — Pedido Duplicado</div>
        <div class="motivo-item"><span class="motivo-codigo">7</span> — Cliente não Pediu Mercadoria</div>

        <div class="motivo-item"><span class="motivo-codigo">11</span> — Desacordo (Preço/F. de pagamento)</div>
        <div class="motivo-item"><span class="motivo-codigo">28</span> — Desacordo com o Pedido</div>

        <div class="motivo-item"><span class="motivo-codigo">88</span> — Desacordo (Falta troca)</div>
        <div class="motivo-item"><span class="motivo-codigo">104</span> — Desacordo (Brinde/Bonificação)</div>

        <div class="motivo-item"><span class="motivo-codigo">105</span> — Cliente sem pedido</div>
        <div class="motivo-item"><span class="motivo-codigo">106</span> — Desacordo (Acordo Comercial)</div>

        <div class="motivo-item"><span class="motivo-codigo">127</span> — Produto Incorreto</div>
        <div class="motivo-item"><span class="motivo-codigo">129</span> — Erro no código do cliente</div>

        <div class="motivo-item"><span class="motivo-codigo">180</span> — Desacordo</div>
        <div class="motivo-item"><span class="motivo-codigo">194</span> — Refatura - Vendas</div>
    </div>

    <div class="motivo-alerta">
        Quadro de referência dos motivos que geram desconto/penalidade ao vendedor. Esta informação é fixa no cabeçalho e não depende da planilha.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CARDS
# ==========================================================
st.markdown('<div class="secao-titulo">Resumo Executivo</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)

with c1:
    criar_card(
        "Total DEV. C/ Penalidade",
        formatar_moeda(total_penalidade),
        "Valor total a descontar dos vendedores",
        tipo="alerta"
    )

with c2:
    criar_card(
        "% Penalidade sobre Venda",
        formatar_percentual(perc_penalidade_venda),
        "Penalidade absoluta / vendas",
        tipo="alerta" if total_penalidade > 0 else "ok"
    )

with c3:
    criar_card(
        "RCAs com Penalidade",
        str(rcas_com_penalidade),
        "Quantidade de vendedores com penalidade",
        tipo="alerta" if rcas_com_penalidade > 0 else "ok"
    )

with c4:
    criar_card(
        "Maior Penalidade Individual",
        formatar_moeda(maior_penalidade_valor),
        maior_penalidade_nome,
        tipo="alerta"
    )

with c5:
    criar_card(
        "Meta Total de Troca (TV11)",
        formatar_moeda(meta_troca_total),
        "Soma das metas de troca dos RCAs",
        tipo="neutro"
    )

with c6:
    criar_card(
        "Troca Realizada (TV11)",
        formatar_moeda(troca_realizada_total),
        "Total de TV11 no filtro aplicado",
        tipo="neutro"
    )

with c7:
    criar_card(
        "% Meta de Troca",
        formatar_percentual(perc_meta_troca),
        "Troca realizada / meta de troca",
        tipo="alerta" if perc_meta_troca > 1 else "ok"
    )

with c8:
    criar_card(
        "RCAs Acima da Meta",
        str(qtd_acima_meta),
        "Quantidade de vendedores acima da meta de troca",
        tipo="alerta" if qtd_acima_meta > 0 else "ok"
    )

st.markdown("")

# ==========================================================
# ABAS
# ==========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "💸 Penalidades",
    "🔁 Trocas",
    "📊 Supervisores",
    "📋 Tabela Analítica"
])

# ==========================================================
# ABA 1 - PENALIDADES
# ==========================================================
with tab1:
    st.markdown('<div class="subsecao-titulo">Rankings de Penalidade</div>', unsafe_allow_html=True)

    penalizados = base_vendedor[base_vendedor["PENALIDADE_VALOR"] > 0].copy()

    col1, col2 = st.columns(2)

    with col1:
        top_penalidade = penalizados.sort_values("PENALIDADE_VALOR", ascending=False).head(15).copy()

        fig_penalidade = px.bar(
            top_penalidade.sort_values("PENALIDADE_VALOR", ascending=True),
            x="PENALIDADE_VALOR",
            y="VENDEDOR_CURTO",
            orientation="h",
            title="Top 15 RCAs por Penalidade",
            text_auto=".2s",
            color="PENALIDADE_VALOR",
            color_continuous_scale=["#1B0E14", "#FF4D6D"]
        )
        fig_penalidade = estilo_plotly(fig_penalidade)
        fig_penalidade.update_layout(
            height=620,
            xaxis_title="Penalidade",
            yaxis_title="Vendedor",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_penalidade, use_container_width=True)

    with col2:
        top_penalidade_pct = penalizados[penalizados["VENDAS"] > 0].copy()
        top_penalidade_pct = top_penalidade_pct.sort_values("% PENALIDADE SOBRE VENDA", ascending=False).head(15)

        fig_penalidade_pct = px.bar(
            top_penalidade_pct.sort_values("% PENALIDADE SOBRE VENDA", ascending=True),
            x="% PENALIDADE SOBRE VENDA",
            y="VENDEDOR_CURTO",
            orientation="h",
            title="Top 15 RCAs por % Penalidade sobre Venda",
            text=top_penalidade_pct.sort_values("% PENALIDADE SOBRE VENDA", ascending=True)["% PENALIDADE SOBRE VENDA"].apply(lambda x: f"{x:.1%}"),
            color="% PENALIDADE SOBRE VENDA",
            color_continuous_scale=["#1B0E14", "#FF4D6D"]
        )
        fig_penalidade_pct = estilo_plotly(fig_penalidade_pct)
        fig_penalidade_pct.update_layout(
            height=620,
            xaxis_title="% Penalidade sobre Venda",
            yaxis_title="Vendedor",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_penalidade_pct, use_container_width=True)

    st.markdown("")
    st.markdown('<div class="subsecao-titulo">Penalidade por Supervisor</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1.2, 1.8])

    with col3:
        penalidade_sup = base_supervisor.sort_values("PENALIDADE_VALOR", ascending=False).copy()
        penalidade_sup["SUPERVISOR_CURTO"] = penalidade_sup["SUPERVISOR"].apply(lambda x: abreviar_nome(x, 30))

        fig_sup_pen = px.bar(
            penalidade_sup,
            x="SUPERVISOR_CURTO",
            y="PENALIDADE_VALOR",
            title="Penalidade por Supervisor",
            text_auto=".2s",
            color="PENALIDADE_VALOR",
            color_continuous_scale=["#0B1325", "#00C2FF"]
        )
        fig_sup_pen = estilo_plotly(fig_sup_pen)
        fig_sup_pen.update_layout(
            height=500,
            xaxis_title="Supervisor",
            yaxis_title="Penalidade",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_sup_pen, use_container_width=True)

    with col4:
        quadro_pen_sup = base_supervisor.copy().sort_values("PENALIDADE_VALOR", ascending=False)

        quadro_pen_sup_exibir = quadro_pen_sup[[
            "SUPERVISOR",
            "PENALIDADE_VALOR",
            "% PENALIDADE SOBRE VENDA",
            "VENDAS",
            "RCAS COM PENALIDADE",
            "TOTAL RCAS",
            "META TROCA",
            "TROCAS TV11"
        ]].copy()

        quadro_pen_sup_exibir = quadro_pen_sup_exibir.rename(columns={
            "PENALIDADE_VALOR": "PENALIDADE"
        })

        quadro_pen_sup_exibir["PENALIDADE"] = quadro_pen_sup_exibir["PENALIDADE"].apply(formatar_moeda)
        quadro_pen_sup_exibir["% PENALIDADE SOBRE VENDA"] = quadro_pen_sup_exibir["% PENALIDADE SOBRE VENDA"].apply(formatar_percentual)
        quadro_pen_sup_exibir["VENDAS"] = quadro_pen_sup_exibir["VENDAS"].apply(formatar_moeda)
        quadro_pen_sup_exibir["META TROCA"] = quadro_pen_sup_exibir["META TROCA"].apply(formatar_moeda)
        quadro_pen_sup_exibir["TROCAS TV11"] = quadro_pen_sup_exibir["TROCAS TV11"].apply(formatar_moeda)

        st.markdown("##### Quadro Executivo de Penalidade por Supervisor")
        st.dataframe(
            quadro_pen_sup_exibir,
            use_container_width=True,
            hide_index=True,
            height=500
        )

# ==========================================================
# ABA 2 - TROCAS
# ==========================================================
with tab2:
    st.markdown('<div class="subsecao-titulo">Rankings de Troca</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        top_troca = base_vendedor.sort_values("TROCAS TV11", ascending=False).head(15)

        fig_troca = px.bar(
            top_troca.sort_values("TROCAS TV11", ascending=True),
            x="TROCAS TV11",
            y="VENDEDOR_CURTO",
            orientation="h",
            title="Top 15 RCAs por Valor de Troca",
            text_auto=".2s",
            color="TROCAS TV11",
            color_continuous_scale=["#061425", "#00C2FF"]
        )
        fig_troca = estilo_plotly(fig_troca)
        fig_troca.update_layout(
            height=620,
            xaxis_title="Troca TV11",
            yaxis_title="Vendedor",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_troca, use_container_width=True)

    with col2:
        top_meta_troca = base_vendedor.sort_values("% META TROCA", ascending=False).head(15)

        fig_meta_troca = px.bar(
            top_meta_troca.sort_values("% META TROCA", ascending=True),
            x="% META TROCA",
            y="VENDEDOR_CURTO",
            orientation="h",
            title="Top 15 RCAs por % da Meta de Troca",
            text=top_meta_troca.sort_values("% META TROCA", ascending=True)["% META TROCA"].apply(lambda x: f"{x:.1%}"),
            color="% META TROCA",
            color_continuous_scale=["#1A1205", "#FDBE2D"]
        )
        fig_meta_troca = estilo_plotly(fig_meta_troca)
        fig_meta_troca.update_layout(
            height=620,
            xaxis_title="% Meta de Troca",
            yaxis_title="Vendedor",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_meta_troca, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        top_troca_venda = base_vendedor[base_vendedor["VENDAS"] > 0].copy()
        top_troca_venda = top_troca_venda.sort_values("% TROCA SOBRE VENDA", ascending=False).head(15)

        fig_troca_venda = px.bar(
            top_troca_venda.sort_values("% TROCA SOBRE VENDA", ascending=True),
            x="% TROCA SOBRE VENDA",
            y="VENDEDOR_CURTO",
            orientation="h",
            title="Top 15 RCAs por % Troca sobre Venda",
            text=top_troca_venda.sort_values("% TROCA SOBRE VENDA", ascending=True)["% TROCA SOBRE VENDA"].apply(lambda x: f"{x:.1%}"),
            color="% TROCA SOBRE VENDA",
            color_continuous_scale=["#061425", "#00C2FF"]
        )
        fig_troca_venda = estilo_plotly(fig_troca_venda)
        fig_troca_venda.update_layout(
            height=620,
            xaxis_title="% Troca sobre Venda",
            yaxis_title="Vendedor",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_troca_venda, use_container_width=True)

    with col4:
        top_criticos = base_vendedor.sort_values("% META TROCA", ascending=False).head(12).copy()
        top_criticos["VENDEDOR_CURTO"] = top_criticos["VENDEDOR"].apply(lambda x: abreviar_nome(x, 28))

        base_criticos = top_criticos.melt(
            id_vars="VENDEDOR_CURTO",
            value_vars=["META TROCA", "TROCAS TV11"],
            var_name="INDICADOR",
            value_name="VALOR"
        )

        fig_meta_x_troca = px.bar(
            base_criticos,
            x="VENDEDOR_CURTO",
            y="VALOR",
            color="INDICADOR",
            barmode="group",
            title="Meta x Troca dos RCAs Mais Críticos",
            text_auto=".2s",
            color_discrete_map={
                "META TROCA": AZUL_NEON,
                "TROCAS TV11": AMARELO
            }
        )
        fig_meta_x_troca = estilo_plotly(fig_meta_x_troca)
        fig_meta_x_troca.update_layout(
            height=620,
            xaxis_title="Vendedor",
            yaxis_title="Valor"
        )
        st.plotly_chart(fig_meta_x_troca, use_container_width=True)

# ==========================================================
# ABA 3 - SUPERVISORES
# ==========================================================
with tab3:
    st.markdown('<div class="subsecao-titulo">Visão Consolidada por Supervisor</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        sup_pen = base_supervisor.sort_values("PENALIDADE_VALOR", ascending=False).copy()
        sup_pen["SUPERVISOR_CURTO"] = sup_pen["SUPERVISOR"].apply(lambda x: abreviar_nome(x, 28))

        fig_sup_pen = px.bar(
            sup_pen,
            x="SUPERVISOR_CURTO",
            y="PENALIDADE_VALOR",
            title="Penalidade por Supervisor",
            text_auto=".2s",
            color="PENALIDADE_VALOR",
            color_continuous_scale=["#061425", "#00C2FF"]
        )
        fig_sup_pen = estilo_plotly(fig_sup_pen)
        fig_sup_pen.update_layout(
            height=500,
            xaxis_title="Supervisor",
            yaxis_title="Penalidade",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_sup_pen, use_container_width=True)

    with col2:
        sup_troca = base_supervisor.sort_values("% META TROCA", ascending=False).copy()
        sup_troca["SUPERVISOR_CURTO"] = sup_troca["SUPERVISOR"].apply(lambda x: abreviar_nome(x, 28))

        fig_sup_troca = px.bar(
            sup_troca,
            x="SUPERVISOR_CURTO",
            y="% META TROCA",
            title="% Meta de Troca por Supervisor",
            text=sup_troca["% META TROCA"].apply(lambda x: f"{x:.1%}"),
            color="% META TROCA",
            color_continuous_scale=["#1A1205", "#FDBE2D"]
        )
        fig_sup_troca = estilo_plotly(fig_sup_troca)
        fig_sup_troca.update_layout(
            height=500,
            xaxis_title="Supervisor",
            yaxis_title="% Meta de Troca",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_sup_troca, use_container_width=True)

    st.markdown("")
    st.markdown('<div class="subsecao-titulo">Quadro Executivo por Supervisor</div>', unsafe_allow_html=True)

    quadro_sup = base_supervisor.copy().sort_values("PENALIDADE_VALOR", ascending=False)

    quadro_sup_exibir = quadro_sup[[
        "SUPERVISOR",
        "PENALIDADE_VALOR",
        "% PENALIDADE SOBRE VENDA",
        "RCAS COM PENALIDADE",
        "TOTAL RCAS",
        "META TROCA",
        "TROCAS TV11",
        "% META TROCA",
        "DESVIO META TROCA",
        "% TROCA SOBRE VENDA",
        "VENDAS"
    ]].copy()

    quadro_sup_exibir = quadro_sup_exibir.rename(columns={
        "PENALIDADE_VALOR": "PENALIDADE"
    })

    quadro_sup_exibir["PENALIDADE"] = quadro_sup_exibir["PENALIDADE"].apply(formatar_moeda)
    quadro_sup_exibir["% PENALIDADE SOBRE VENDA"] = quadro_sup_exibir["% PENALIDADE SOBRE VENDA"].apply(formatar_percentual)
    quadro_sup_exibir["META TROCA"] = quadro_sup_exibir["META TROCA"].apply(formatar_moeda)
    quadro_sup_exibir["TROCAS TV11"] = quadro_sup_exibir["TROCAS TV11"].apply(formatar_moeda)
    quadro_sup_exibir["% META TROCA"] = quadro_sup_exibir["% META TROCA"].apply(formatar_percentual)
    quadro_sup_exibir["DESVIO META TROCA"] = quadro_sup_exibir["DESVIO META TROCA"].apply(formatar_moeda)
    quadro_sup_exibir["% TROCA SOBRE VENDA"] = quadro_sup_exibir["% TROCA SOBRE VENDA"].apply(formatar_percentual)
    quadro_sup_exibir["VENDAS"] = quadro_sup_exibir["VENDAS"].apply(formatar_moeda)

    st.dataframe(
        quadro_sup_exibir,
        use_container_width=True,
        hide_index=True,
        height=520
    )

# ==========================================================
# ABA 4 - TABELA ANALÍTICA
# ==========================================================
with tab4:
    st.markdown('<div class="subsecao-titulo">Tabela Analítica</div>', unsafe_allow_html=True)

    tabela = base_vendedor.copy()
    tabela = tabela[[
        "SUPERVISOR",
        "VENDEDOR",
        "PENALIDADE_VALOR",
        "DEV. C/ PENALIDADE ORIGINAL",
        "% PENALIDADE SOBRE VENDA",
        "VENDAS",
        "META TROCA",
        "TROCAS TV11",
        "DESVIO META TROCA",
        "% META TROCA",
        "% TROCA SOBRE VENDA",
        "BONIFICAÇÕES TV5",
        "DEV. GRANDES REDES",
        "% DEV. GRANDES REDES SOBRE VENDA",
        "STATUS META TROCA",
        "TEM PENALIDADE"
    ]].copy()

    tabela = tabela.rename(columns={
        "PENALIDADE_VALOR": "PENALIDADE",
        "DEV. C/ PENALIDADE ORIGINAL": "PENALIDADE ORIGINAL"
    })

    tabela = tabela.sort_values("PENALIDADE", ascending=False)
    tabela_export = tabela.copy()

    cols_moeda = [
        "PENALIDADE",
        "PENALIDADE ORIGINAL",
        "VENDAS",
        "META TROCA",
        "TROCAS TV11",
        "DESVIO META TROCA",
        "BONIFICAÇÕES TV5",
        "DEV. GRANDES REDES"
    ]

    cols_pct = [
        "% PENALIDADE SOBRE VENDA",
        "% META TROCA",
        "% TROCA SOBRE VENDA",
        "% DEV. GRANDES REDES SOBRE VENDA"
    ]

    for col in cols_moeda:
        tabela[col] = tabela[col].apply(formatar_moeda)

    for col in cols_pct:
        tabela[col] = tabela[col].apply(formatar_percentual)

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
        height=700
    )

    st.markdown("")
    excel_bytes = to_excel_bytes(tabela_export)

    st.download_button(
        label="📥 Baixar tabela analítica em Excel",
        data=excel_bytes,
        file_name="dashboard_penalidades_tabela_analitica.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )