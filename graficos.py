"""
=========================================================
GRAFICOS.PY
Dashboard Executivo de Penalidades
=========================================================
"""

import plotly.express as px
import plotly.graph_objects as go

from utils import (
    formatar_moeda,
    nome_curto_rca
)

# ==========================================================
# CORES
# ==========================================================

AZUL = "#006B98"

AZUL_NEON = "#00C2FF"

AMARELO = "#FDBE2D"

VERMELHO = "#FF4D6D"

VERDE = "#00D084"

FUNDO = "#05070D"

CARD = "#101826"

GRADE = "#183B57"

FONTE = "white"

# ==========================================================
# TEMA PADRÃO
# ==========================================================

def aplicar_tema(fig):

    fig.update_layout(

        paper_bgcolor=FUNDO,

        plot_bgcolor=FUNDO,

        font=dict(

            color=FONTE,

            family="Arial"

        ),

        title_font=dict(

            size=22,

            color="white"

        ),

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        hoverlabel=dict(

            bgcolor="#101826",

            font_size=13,

            font_family="Arial"

        ),

        legend=dict(

            bgcolor="rgba(0,0,0,0)"

        )

    )

    fig.update_xaxes(

        gridcolor=GRADE,

        zeroline=False

    )

    fig.update_yaxes(

        gridcolor=GRADE,

        zeroline=False

    )

    return fig


# ==========================================================
# PREPARAÇÃO DOS NOMES
# ==========================================================

def preparar_nomes(df):

    base = df.copy()

    base["VENDEDOR_CURTO"] = (

        base["VENDEDOR"]

        .apply(nome_curto_rca)

    )

    return base


# ==========================================================
# RANKING PENALIDADE
# ==========================================================

def grafico_penalidade(base):

    base = preparar_nomes(base)

    fig = px.bar(

        base.sort_values(

            "PENALIDADE_VALOR",

            ascending=True

        ),

        x="PENALIDADE_VALOR",

        y="VENDEDOR_CURTO",

        orientation="h",

        text="PENALIDADE_VALOR",

        color="PENALIDADE_VALOR",

        color_continuous_scale=[

            AZUL,

            AZUL_NEON,

            VERMELHO

        ],

        title="💸 Top 20 RCAs por Penalidade Financeira"

    )

    fig.update_traces(

        texttemplate="R$ %{x:,.2f}",

        textposition="auto",

        hovertemplate="""

<b>%{y}</b>

<br>Penalidade: R$ %{x:,.2f}

<extra></extra>

"""

    )

    fig.update_layout(

        height=600,

        coloraxis_showscale=False,

        xaxis_title="Penalidade (R$)",

        yaxis_title=""

    )

    return aplicar_tema(fig)


# ==========================================================
# RANKING %
# ==========================================================

def grafico_penalidade_percentual(base):

    base = preparar_nomes(base)

    fig = px.bar(

        base.sort_values(

            "% PENALIDADE SOBRE VENDA",

            ascending=True

        ),

        x="% PENALIDADE SOBRE VENDA",

        y="VENDEDOR_CURTO",

        orientation="h",

        text="% PENALIDADE SOBRE VENDA",

        color="% PENALIDADE SOBRE VENDA",

        color_continuous_scale=[

            AZUL,

            AMARELO,

            VERMELHO

        ],

        title="📈 Top 20 RCAs por % Penalidade sobre Venda"

    )

    fig.update_traces(

        texttemplate="%{x:.2%}",

        textposition="auto",

        hovertemplate="""

<b>%{y}</b>

<br>% Penalidade: %{x:.2%}

<extra></extra>

"""

    )

    fig.update_layout(

        height=600,

        coloraxis_showscale=False,

        xaxis_tickformat=".1%",

        xaxis_title="% Penalidade sobre Venda",

        yaxis_title=""

    )

    return aplicar_tema(fig)
# ==========================================================
# PENALIDADE POR SUPERVISOR
# ==========================================================

def grafico_supervisor(base):

    base = base.sort_values(
        "PENALIDADE_VALOR",
        ascending=True
    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=base["PENALIDADE_VALOR"],

            y=base["SUPERVISOR"],

            orientation="h",

            marker=dict(

                color=AZUL_NEON,

                line=dict(

                    color=AZUL,

                    width=1

                )

            ),

            text=[
                formatar_moeda(x)
                for x in base["PENALIDADE_VALOR"]
            ],

            textposition="auto",

            hovertemplate=
            "<b>%{y}</b><br>"
            "Penalidade: %{text}"
            "<extra></extra>"

        )

    )

    fig.update_layout(

        title="👨‍💼 Penalidade por Supervisor",

        height=550,

        showlegend=False,

        xaxis_title="Penalidade (R$)",

        yaxis_title=""

    )
    
    fig.update_traces(

    cliponaxis=False

)
    return aplicar_tema(fig)


# ==========================================================
# TROCA x META
# ==========================================================

def grafico_troca_meta(base):

    base = preparar_nomes(base)

    base = (
        base
        .sort_values(
            "DESVIO META TROCA",
            ascending=False
        )
        .head(20)
    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            name="Meta",

            x=base["VENDEDOR_CURTO"],

            y=base["META TROCA"],

            marker_color=AZUL

        )

    )

    fig.add_trace(

        go.Bar(

            name="Troca",

            x=base["VENDEDOR_CURTO"],

            y=base["TROCAS TV11"],

            marker_color=AMARELO

        )

    )

    fig.update_layout(

        barmode="group",

        title="🎯 Meta de Troca x Troca Real",

        height=650,

        xaxis_title="",

        yaxis_title="Valor"

    )

    fig.update_xaxes(

        tickangle=-35

    )

    return aplicar_tema(fig)


# ==========================================================
# GRANDES REDES
# ==========================================================

def grafico_grandes_redes(base):

    base = preparar_nomes(base)

    base = (
        base
        .sort_values(
            "DEV. GRANDES REDES",
            ascending=False
        )
        .head(20)
        .sort_values(
            "DEV. GRANDES REDES"
        )
    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=base["DEV. GRANDES REDES"],

            y=base["VENDEDOR_CURTO"],

            orientation="h",

            marker_color=VERMELHO,

            text=[
                formatar_moeda(x)
                for x in base["DEV. GRANDES REDES"]
            ],

            textposition="auto"

        )

    )

    fig.update_layout(

        title="🏪 Top 20 Devoluções Grandes Redes",

        height=650,

        showlegend=False,

        xaxis_title="Valor",

        yaxis_title=""

    )

    return aplicar_tema(fig)


# ==========================================================
# BONIFICAÇÕES
# ==========================================================

def grafico_bonificacao(base):

    base = preparar_nomes(base)

    base = (
        base
        .sort_values(
            "BONIFICAÇÕES TV5",
            ascending=False
        )
        .head(20)
        .sort_values(
            "BONIFICAÇÕES TV5"
        )
    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=base["BONIFICAÇÕES TV5"],

            y=base["VENDEDOR_CURTO"],

            orientation="h",

            marker_color=VERDE,

            text=[
                formatar_moeda(x)
                for x in base["BONIFICAÇÕES TV5"]
            ],

            textposition="auto"

        )

    )

    fig.update_layout(

        title="🎁 Top 20 Bonificações (TV5)",

        height=650,

        showlegend=False,

        xaxis_title="Valor",

        yaxis_title=""

    )

    return aplicar_tema(fig)
# ==========================================================
# PARETO DAS PENALIDADES
# ==========================================================

def grafico_pareto(base):

    base = (
        base
        .sort_values(
            "PENALIDADE_VALOR",
            ascending=False
        )
        .copy()
    )

    base["ACUMULADO"] = (
        base["PENALIDADE_VALOR"]
        .cumsum()
        /
        base["PENALIDADE_VALOR"].sum()
    )

    base = preparar_nomes(base)

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=base["VENDEDOR_CURTO"],

            y=base["PENALIDADE_VALOR"],

            name="Penalidade",

            marker_color=AZUL_NEON

        )

    )

    fig.add_trace(

        go.Scatter(

            x=base["VENDEDOR_CURTO"],

            y=base["ACUMULADO"],

            yaxis="y2",

            mode="lines+markers+text",

            line=dict(

                color=VERMELHO,

                width=3

            ),

            name="% Acumulado"

        )

    )

    fig.update_layout(

        title="📈 Pareto das Penalidades",

        height=650,

        yaxis=dict(

            title="Penalidade"

        ),

        yaxis2=dict(

            title="% Acumulado",

            overlaying="y",

            side="right",

            tickformat=".0%"

        ),

        xaxis_tickangle=-45

    )

    return aplicar_tema(fig)


# ==========================================================
# DONUT DAS FAIXAS
# ==========================================================

def grafico_faixas(resumo_faixas):

    fig = px.pie(

        resumo_faixas,

        names="FAIXA PENALIDADE",

        values="QUANTIDADE RCAs",

        hole=.65,

        color="FAIXA PENALIDADE",

        color_discrete_map={

            "BAIXA":AZUL,

            "MÉDIA":AMARELO,

            "ALTA":VERMELHO,

            "CRÍTICA":"#8B0000"

        },

        title="🍩 Distribuição das Penalidades"

    )

    fig.update_traces(

        textinfo="percent+label"

    )

    return aplicar_tema(fig)


# ==========================================================
# HISTOGRAMA
# ==========================================================

def grafico_distribuicao(base):

    fig = px.histogram(

        base,

        x="PENALIDADE_VALOR",

        nbins=20,

        color_discrete_sequence=[AZUL_NEON],

        title="📊 Distribuição das Penalidades"

    )

    fig.update_layout(

        height=450

    )

    return aplicar_tema(fig)


# ==========================================================
# HEATMAP
# ==========================================================

def grafico_heatmap(base):

    tabela = (

        base

        .pivot_table(

            index="SUPERVISOR",

            columns="FAIXA PENALIDADE",

            values="PENALIDADE_VALOR",

            aggfunc="count",

            fill_value=0

        )

    )

    fig = px.imshow(

        tabela,

        text_auto=True,

        aspect="auto",

        color_continuous_scale=[

            "#101826",

            AZUL,

            AZUL_NEON,

            AMARELO,

            VERMELHO

        ],

        title="🔥 Heatmap Supervisor x Penalidade"

    )

    fig.update_layout(

        height=450

    )

    return aplicar_tema(fig)


# ==========================================================
# TABELA ANALÍTICA
# ==========================================================

def tabela_analitica(base):

    mostrar = [

        "SUPERVISOR",

        "VENDEDOR",

        "VENDAS",

        "META TROCA",

        "TROCAS TV11",

        "PENALIDADE_VALOR",

        "% PENALIDADE SOBRE VENDA",

        "STATUS TROCA"

    ]

    tabela = (

        base

        [mostrar]

        .sort_values(

            "PENALIDADE_VALOR",

            ascending=False

        )

    )

    return tabela
