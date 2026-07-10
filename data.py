"""
=========================================================
DATA.PY
Leitura e tratamento da planilha
Dashboard Executivo de Penalidades
=========================================================
"""

import pandas as pd
import numpy as np
import streamlit as st


# =========================================================
# MAPEAMENTO DAS COLUNAS
# =========================================================

COLUNAS = {

    "SUPERVISOR": "SUPERVISOR",

    "VENDEDOR": "VENDEDOR",

    "META": "META MENSAL",

    "META_TROCA": "META TROCA",

    "VENDAS": "VENDAS",

    "TV11": "TROCAS TV11",

    "TV5": "BONIFICAÇÕES TV5",

    "PENALIDADE": "DEV. C/ PENALIDADE",

    "GRANDES_REDES": "DEV. GRANDES REDES",

    "ACIMA_TABELA": "ACIMA DA TABELA",

    "CC_REAL": "CONTA_CORRENTE_REAL"

}


# =========================================================
# LEITURA DA PLANILHA
# =========================================================

@st.cache_data(show_spinner=False)

def carregar_dados(arquivo):

    df = pd.read_excel(arquivo)

    df = padronizar_colunas(df)

    validar_colunas(df)

    tratar_nulos(df)

    converter_numericos(df)

    criar_indicadores(df)

    return df


# =========================================================
# PADRONIZAÇÃO DOS NOMES
# =========================================================

def padronizar_colunas(df):

    renomear = {

        "CODSUPERVISOR":"COD SUPERVISOR",

        "SUPERVISOR":"SUPERVISOR",

        "RCA":"VENDEDOR",

        "VENDEDOR":"VENDEDOR",

        "META":"META MENSAL",

        "META MENSAL":"META MENSAL",

        "META_CC":"META TROCA",

        "META TROCA":"META TROCA",

        "VLVENDA":"VENDAS",

        "VENDAS":"VENDAS",

        "TV11":"TROCAS TV11",

        "TROCAS TV11":"TROCAS TV11",

        "TV5":"BONIFICAÇÕES TV5",

        "BONIFICAÇÕES TV5":"BONIFICAÇÕES TV5",

        "DEV_C_PENALIDADE":"DEV. C/ PENALIDADE",

        "DEV. C/ PENALIDADE":"DEV. C/ PENALIDADE",

        "DEV_GRANDES_REDES":"DEV. GRANDES REDES",

        "DEV. GRANDES REDES":"DEV. GRANDES REDES",

        "ACIMA_TABELA":"ACIMA DA TABELA",

        "CC_MAIS_TABELA":"CONTA_CORRENTE_REAL",

        "CONTA_CORRENTE_REAL":"CONTA_CORRENTE_REAL"

    }

    df = df.rename(columns=renomear)

    return df


# =========================================================
# VALIDAÇÃO
# =========================================================

def validar_colunas(df):

    obrigatorias = list(COLUNAS.values())

    faltando = []

    for coluna in obrigatorias:

        if coluna not in df.columns:

            faltando.append(coluna)

    if len(faltando):

        st.error("As seguintes colunas não foram encontradas:")

        st.write(faltando)

        st.stop()


# =========================================================
# TRATAMENTO DE NULOS
# =========================================================

def tratar_nulos(df):

    numericas = [

        COLUNAS["META"],

        COLUNAS["META_TROCA"],

        COLUNAS["VENDAS"],

        COLUNAS["TV11"],

        COLUNAS["TV5"],

        COLUNAS["PENALIDADE"],

        COLUNAS["GRANDES_REDES"],

        COLUNAS["ACIMA_TABELA"],

        COLUNAS["CC_REAL"]

    ]

    for coluna in numericas:

        df[coluna] = df[coluna].fillna(0)

    df["SUPERVISOR"] = df["SUPERVISOR"].fillna("SEM SUPERVISOR")

    df["VENDEDOR"] = df["VENDEDOR"].fillna("SEM RCA")


# =========================================================
# CONVERSÃO
# =========================================================

def converter_numericos(df):

    numericas = [

        COLUNAS["META"],

        COLUNAS["META_TROCA"],

        COLUNAS["VENDAS"],

        COLUNAS["TV11"],

        COLUNAS["TV5"],

        COLUNAS["PENALIDADE"],

        COLUNAS["GRANDES_REDES"],

        COLUNAS["ACIMA_TABELA"],

        COLUNAS["CC_REAL"]

    ]

    for coluna in numericas:

        df[coluna] = pd.to_numeric(

            df[coluna],

            errors="coerce"

        ).fillna(0)


# =========================================================
# INDICADORES
# =========================================================

def criar_indicadores(df):

    # Penalidade positiva
    df["PENALIDADE_VALOR"] = df["DEV. C/ PENALIDADE"].abs()

    # % Penalidade sobre Venda
    df["% PENALIDADE SOBRE VENDA"] = np.where(

        df["VENDAS"] > 0,

        df["PENALIDADE_VALOR"] / df["VENDAS"],

        0

    )

    # % Troca
    df["% TROCA"] = np.where(

        df["VENDAS"] > 0,

        df["TROCAS TV11"] / df["VENDAS"],

        0

    )

    # % Bonificação
    df["% BONIFICAÇÃO"] = np.where(

        df["VENDAS"] > 0,

        df["BONIFICAÇÕES TV5"] / df["VENDAS"],

        0

    )

    # % Grandes Redes
    df["% GRANDES REDES"] = np.where(

        df["VENDAS"] > 0,

        df["DEV. GRANDES REDES"].abs() / df["VENDAS"],

        0

    )

    # % Meta Troca
    df["% META TROCA"] = np.where(

        df["META TROCA"] > 0,

        df["TROCAS TV11"] / df["META TROCA"],

        0

    )

    # Desvio da Meta
    df["DESVIO META TROCA"] = (

        df["TROCAS TV11"]

        -

        df["META TROCA"]

    )

    # Situação da Meta
    df["STATUS TROCA"] = np.where(

        df["DESVIO META TROCA"] > 0,

        "ACIMA DA META",

        "DENTRO DA META"

    )

    # Faixa de Penalidade
    df["FAIXA PENALIDADE"] = pd.cut(

        df["PENALIDADE_VALOR"],

        bins=[-1,500,2000,5000,100000000],

        labels=[

            "BAIXA",

            "MÉDIA",

            "ALTA",

            "CRÍTICA"

        ]

    )
    # =========================================================
# RESUMO POR RCA
# =========================================================

def resumo_rca(df):

    base = (
        df.groupby(
            ["SUPERVISOR", "VENDEDOR"],
            as_index=False
        )
        .agg({

            "META MENSAL":"sum",

            "META TROCA":"sum",

            "VENDAS":"sum",

            "TROCAS TV11":"sum",

            "BONIFICAÇÕES TV5":"sum",

            "DEV. C/ PENALIDADE":"sum",

            "DEV. GRANDES REDES":"sum",

            "ACIMA DA TABELA":"sum",

            "CONTA_CORRENTE_REAL":"sum"

        })
    )

    # =====================================================
    # Indicadores
    # =====================================================

    base["PENALIDADE_VALOR"] = base["DEV. C/ PENALIDADE"].abs()

    base["% PENALIDADE SOBRE VENDA"] = np.where(

        base["VENDAS"] > 0,

        base["PENALIDADE_VALOR"] / base["VENDAS"],

        0

    )

    base["% TROCA"] = np.where(

        base["VENDAS"] > 0,

        base["TROCAS TV11"] / base["VENDAS"],

        0

    )

    base["% META TROCA"] = np.where(

        base["META TROCA"] > 0,

        base["TROCAS TV11"] / base["META TROCA"],

        0

    )

    base["DESVIO META TROCA"] = (

        base["TROCAS TV11"]

        -

        base["META TROCA"]

    )

    base["STATUS TROCA"] = np.where(

        base["DESVIO META TROCA"] > 0,

        "ACIMA DA META",

        "DENTRO DA META"

    )

    base["TEM PENALIDADE"] = np.where(

        base["PENALIDADE_VALOR"] > 0,

        "SIM",

        "NÃO"

    )

    base["FAIXA PENALIDADE"] = pd.cut(

    base["PENALIDADE_VALOR"],

    bins=[-1,500,2000,5000,999999999],

    labels=[

        "BAIXA",

        "MÉDIA",

        "ALTA",

        "CRÍTICA"

    ]

)

    return base


# =========================================================
# RESUMO POR SUPERVISOR
# =========================================================

def resumo_supervisor(df):

    base = (

        df.groupby(

            "SUPERVISOR",

            as_index=False

        )

        .agg({

            "META MENSAL":"sum",

            "META TROCA":"sum",

            "VENDAS":"sum",

            "TROCAS TV11":"sum",

            "BONIFICAÇÕES TV5":"sum",

            "DEV. C/ PENALIDADE":"sum",

            "DEV. GRANDES REDES":"sum",

            "ACIMA DA TABELA":"sum",

            "CONTA_CORRENTE_REAL":"sum"

        })

    )

    base["PENALIDADE_VALOR"] = base["DEV. C/ PENALIDADE"].abs()

    base["% PENALIDADE SOBRE VENDA"] = np.where(

        base["VENDAS"] > 0,

        base["PENALIDADE_VALOR"] / base["VENDAS"],

        0

    )

    base["% TROCA"] = np.where(

        base["VENDAS"] > 0,

        base["TROCAS TV11"] / base["VENDAS"],

        0

    )

    base["% META TROCA"] = np.where(

        base["META TROCA"] > 0,

        base["TROCAS TV11"] / base["META TROCA"],

        0

    )

    base["RCAS"] = (

        df.groupby("SUPERVISOR")["VENDEDOR"]

        .nunique()

        .values

    )

    base["RCAS COM PENALIDADE"] = (

        resumo_rca(df)

        .groupby("SUPERVISOR")["TEM PENALIDADE"]

        .apply(lambda x:(x=="SIM").sum())

        .values

    )

    return base


# =========================================================
# INDICADORES EXECUTIVOS
# =========================================================

def indicadores_dashboard(base_rca):

    indicadores = {

        "total_vendas":

            base_rca["VENDAS"].sum(),

        "total_penalidade":

            base_rca["PENALIDADE_VALOR"].sum(),

        "total_troca":

            base_rca["TROCAS TV11"].sum(),

        "total_meta":

            base_rca["META TROCA"].sum(),

        "total_bonificacao":

            base_rca["BONIFICAÇÕES TV5"].sum(),

        "total_grandes_redes":

            base_rca["DEV. GRANDES REDES"].sum(),

        "rcas":

            base_rca["VENDEDOR"].nunique(),

        "supervisores":

            base_rca["SUPERVISOR"].nunique(),

        "rcas_penalidade":

            (

                base_rca["PENALIDADE_VALOR"] > 0

            ).sum()

    }

    if indicadores["total_vendas"] > 0:

        indicadores["perc_penalidade"] = (

            indicadores["total_penalidade"]

            /

            indicadores["total_vendas"]

        )

    else:

        indicadores["perc_penalidade"] = 0

    if indicadores["total_meta"] > 0:

        indicadores["perc_meta"] = (

            indicadores["total_troca"]

            /

            indicadores["total_meta"]

        )

    else:

        indicadores["perc_meta"] = 0

    return indicadores
# =========================================================
# RANKING - PENALIDADE FINANCEIRA
# =========================================================

def ranking_penalidade(base_rca, top=20):

    ranking = (
        base_rca
        .copy()
        .sort_values(
            "PENALIDADE_VALOR",
            ascending=False
        )
        .head(top)
    )

    return ranking


# =========================================================
# RANKING - % PENALIDADE SOBRE VENDA
# =========================================================

def ranking_percentual_penalidade(base_rca, top=20):

    ranking = (
        base_rca
        .copy()
        .query("VENDAS > 0")
        .sort_values(
            "% PENALIDADE SOBRE VENDA",
            ascending=False
        )
        .head(top)
    )

    return ranking


# =========================================================
# RANKING - TROCAS TV11
# =========================================================

def ranking_trocas(base_rca, top=20):

    ranking = (
        base_rca
        .copy()
        .sort_values(
            "TROCAS TV11",
            ascending=False
        )
        .head(top)
    )

    return ranking


# =========================================================
# RANKING - % META TROCA
# =========================================================

def ranking_meta_troca(base_rca, top=20):

    ranking = (
        base_rca
        .copy()
        .query("`META TROCA` > 0")
        .sort_values(
            "% META TROCA",
            ascending=False
        )
        .head(top)
    )

    return ranking


# =========================================================
# RANKING - GRANDES REDES
# =========================================================

def ranking_grandes_redes(base_rca, top=20):

    ranking = (
        base_rca
        .copy()
        .sort_values(
            "DEV. GRANDES REDES",
            ascending=False
        )
        .head(top)
    )

    return ranking


# =========================================================
# RANKING - BONIFICAÇÕES
# =========================================================

def ranking_bonificacao(base_rca, top=20):

    ranking = (
        base_rca
        .copy()
        .sort_values(
            "BONIFICAÇÕES TV5",
            ascending=False
        )
        .head(top)
    )

    return ranking


# =========================================================
# RANKING - ACIMA DA TABELA
# =========================================================

def ranking_acima_tabela(base_rca, top=20):

    ranking = (
        base_rca
        .copy()
        .sort_values(
            "ACIMA DA TABELA",
            ascending=False
        )
        .head(top)
    )

    return ranking


# =========================================================
# RANKING - SUPERVISORES
# =========================================================

def ranking_supervisor(base_supervisor):

    ranking = (
        base_supervisor
        .copy()
        .sort_values(
            "PENALIDADE_VALOR",
            ascending=False
        )
    )

    return ranking


# =========================================================
# RCAS COM PENALIDADE
# =========================================================

def tabela_penalidades(base_rca):

    tabela = (
        base_rca
        .copy()
        .query("PENALIDADE_VALOR > 0")
        .sort_values(
            "PENALIDADE_VALOR",
            ascending=False
        )
    )

    return tabela


# =========================================================
# RCAS ACIMA DA META
# =========================================================

def tabela_acima_meta(base_rca):

    tabela = (
        base_rca
        .copy()
        .query("STATUS TROCA == 'ACIMA DA META'")
        .sort_values(
            "DESVIO META TROCA",
            ascending=False
        )
    )

    return tabela


# =========================================================
# TOP 5
# =========================================================

def top5_penalidade(base_rca):

    return ranking_penalidade(base_rca, top=5)


def top5_percentual(base_rca):

    return ranking_percentual_penalidade(base_rca, top=5)


def top5_troca(base_rca):

    return ranking_trocas(base_rca, top=5)


# =========================================================
# TOP 10
# =========================================================

def top10_penalidade(base_rca):

    return ranking_penalidade(base_rca, top=10)


def top10_percentual(base_rca):

    return ranking_percentual_penalidade(base_rca, top=10)


# =========================================================
# TOP 20 (PADRÃO DO DASHBOARD)
# =========================================================

def top20_penalidade(base_rca):

    return ranking_penalidade(base_rca, top=20)


def top20_percentual(base_rca):

    return ranking_percentual_penalidade(base_rca, top=20)


def top20_troca(base_rca):

    return ranking_trocas(base_rca, top=20)


# =========================================================
# RESUMO EXECUTIVO
# =========================================================

def resumo_executivo(base_rca):

    resumo = {}

    resumo["maior_penalidade"] = (
        base_rca["PENALIDADE_VALOR"].max()
    )

    resumo["menor_penalidade"] = (
        base_rca["PENALIDADE_VALOR"].min()
    )

    resumo["media_penalidade"] = (
        base_rca["PENALIDADE_VALOR"].mean()
    )

    resumo["media_percentual"] = (
        base_rca["% PENALIDADE SOBRE VENDA"].mean()
    )

    resumo["media_troca"] = (
        base_rca["% TROCA"].mean()
    )

    resumo["rcas_com_penalidade"] = (
        base_rca["PENALIDADE_VALOR"] > 0
    ).sum()

    resumo["rcas_sem_penalidade"] = (
        base_rca["PENALIDADE_VALOR"] == 0
    ).sum()

    return resumo
# =========================================================
# TABELA ANALÍTICA
# =========================================================

def tabela_analitica(base_rca):

    tabela = base_rca.copy()

    tabela = tabela.sort_values(
        "PENALIDADE_VALOR",
        ascending=False
    )

    return tabela


# =========================================================
# TABELA FINANCEIRO
# (Somente RCAs com desconto)
# =========================================================

def tabela_descontos(base_rca):

    tabela = (

        base_rca
        .copy()
        .query("PENALIDADE_VALOR > 0")
        .sort_values(
            "PENALIDADE_VALOR",
            ascending=False
        )

    )

    return tabela


# =========================================================
# RESUMO POR FAIXA DE PENALIDADE
# =========================================================

def resumo_faixas(base_rca):

    resumo = (

        base_rca

        .groupby(

            "FAIXA PENALIDADE",

            as_index=False

        )

        .agg({

            "VENDEDOR":"count",

            "PENALIDADE_VALOR":"sum"

        })

    )

    resumo = resumo.rename(columns={

        "VENDEDOR":"QUANTIDADE RCAs",

        "PENALIDADE_VALOR":"TOTAL PENALIDADE"

    })

    return resumo


# =========================================================
# RESUMO POR STATUS DA META
# =========================================================

def resumo_meta(base_rca):

    resumo = (

        base_rca

        .groupby(

            "STATUS TROCA",

            as_index=False

        )

        .agg({

            "VENDEDOR":"count"

        })

    )

    resumo = resumo.rename(columns={

        "VENDEDOR":"TOTAL"

    })

    return resumo


# =========================================================
# PREPARAÇÃO DAS BASES
# =========================================================

def preparar_bases(df):

    base_rca = resumo_rca(df)

    base_supervisor = resumo_supervisor(df)

    bases = {

        # Bases principais
        "base_rca": base_rca,

        "base_supervisor": base_supervisor,

        # KPIs
        "kpis": indicadores_dashboard(base_rca),

        "resumo": resumo_executivo(base_rca),

        # Rankings
        "ranking_penalidade": ranking_penalidade(base_rca),

        "ranking_penalidade_pct": ranking_percentual_penalidade(base_rca),

        "ranking_trocas": ranking_trocas(base_rca),

        "ranking_meta": ranking_meta_troca(base_rca),

        "ranking_grandes_redes": ranking_grandes_redes(base_rca),

        "ranking_bonificacao": ranking_bonificacao(base_rca),

        "ranking_acima_tabela": ranking_acima_tabela(base_rca),

        "ranking_supervisor": ranking_supervisor(base_supervisor),

        # Tabelas
        "tabela_analitica": tabela_analitica(base_rca),

        "tabela_descontos": tabela_descontos(base_rca),

        "tabela_penalidades": tabela_penalidades(base_rca),

        "tabela_meta": tabela_acima_meta(base_rca),

        # Resumos
        "resumo_faixas": resumo_faixas(base_rca),

        "resumo_meta": resumo_meta(base_rca)

    }

    return bases


# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================

def carregar_bases(arquivo):

    df = carregar_dados(arquivo)

    return preparar_bases(df)