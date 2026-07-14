# ==========================================================
# DASHBOARD EXECUTIVO DE PENALIDADES
# Distrinorte Distribuidora
# ==========================================================

import io
import streamlit as st
import pandas as pd

# ==========================================================
# IMPORTAÇÕES DO PROJETO
# ==========================================================

from data import *
from componentes import *
from graficos import *
from styles import carregar_css

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Dashboard Executivo de Penalidades",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CSS
# ==========================================================

carregar_css()

# ==========================================================
# CABEÇALHO
# ==========================================================

cabecalho_dashboard()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## 📂 Base de Dados")

    arquivo = st.file_uploader(
        "Selecione a planilha",
        type=["xlsx"]
    )

    st.markdown("---")

# ==========================================================
# AGUARDA UPLOAD
# ==========================================================

if arquivo is None:

    st.info(
        "Selecione uma planilha (.xlsx) para iniciar o Dashboard."
    )

    st.stop()

# ==========================================================
# CARREGAMENTO DAS BASES
# ==========================================================

with st.spinner("Carregando base de dados..."):

    bases = carregar_bases(arquivo)

# ==========================================================
# BASES
# ==========================================================

base_rca = bases["base_rca"]

base_supervisor = bases["base_supervisor"]

# ==========================================================
# FILTROS
# ==========================================================

with st.sidebar:

    st.markdown("## 🎯 Filtros")

    supervisores = sorted(
        base_rca["SUPERVISOR"]
        .dropna()
        .unique()
        .tolist()
    )

    supervisor = st.multiselect(
        "Supervisor",
        supervisores,
        default=supervisores
    )

    vendedores = sorted(

        base_rca.loc[
            base_rca["SUPERVISOR"].isin(supervisor),
            "VENDEDOR"
        ]

        .dropna()
        .unique()
        .tolist()

    )

    vendedor = st.multiselect(
        "Vendedor",
        vendedores,
        default=vendedores
    )

# ==========================================================
# APLICA FILTROS
# ==========================================================

base_rca = base_rca.loc[
    (
        base_rca["SUPERVISOR"].isin(supervisor)
    )
    &
    (
        base_rca["VENDEDOR"].isin(vendedor)
    )
].copy()

base_supervisor = base_supervisor.loc[
    base_supervisor["SUPERVISOR"].isin(supervisor)
].copy()

# ==========================================================
# SEM DADOS
# ==========================================================

if base_rca.empty:

    st.warning(
        "Nenhum dado encontrado para os filtros selecionados."
    )

    st.stop()
# ==========================================================
# KPI'S
# ==========================================================

kpis = indicadores_dashboard(base_rca)

# ==========================================================
# RANKINGS
# ==========================================================

ranking_pen = ranking_penalidade(base_rca)

ranking_pct = ranking_percentual_penalidade(base_rca)

ranking_super = ranking_supervisor(base_supervisor)

ranking_troca = ranking_trocas(base_rca)

ranking_redes = ranking_grandes_redes(base_rca)

ranking_bonus = ranking_bonificacao(base_rca)

# ==========================================================
# RESUMOS
# ==========================================================

resumo_faixa = resumo_faixas(base_rca)

resumo = resumo_executivo(base_rca)

# ==========================================================
# TABELAS
# ==========================================================

tabela_geral = tabela_analitica(base_rca)

tabela_financeira = tabela_descontos(base_rca)

tabela_meta = tabela_acima_meta(base_rca)

# ==========================================================
# EXCEL
# ==========================================================

arquivo_excel = io.BytesIO()

with pd.ExcelWriter(
    arquivo_excel,
    engine="openpyxl"
) as writer:

    tabela_financeira.to_excel(
        writer,
        sheet_name="Financeiro",
        index=False
    )

    tabela_geral.to_excel(
        writer,
        sheet_name="Analitica",
        index=False
    )

    tabela_meta.to_excel(
        writer,
        sheet_name="Meta",
        index=False
    )

arquivo_excel.seek(0)

# ==========================================================
# CABEÇALHO
# ==========================================================

linha_kpis(kpis)

espaco()

linha_kpis2(kpis)

espaco()

alerta_penalidade(base_rca)

espaco()

resumo_executivo(kpis)

espaco(2)

# ==========================================================
# ABAS
# ==========================================================

(
    aba_visao,
    aba_rankings,
    aba_supervisores,
    aba_tabelas,
    aba_exportacao
) = st.tabs(

    [

        "📊 Visão Geral",

        "🏆 Rankings",

        "👨‍💼 Supervisores",

        "📋 Tabelas",

        "📤 Exportação"

    ]

)
# ==========================================================
# ABA 1 - VISÃO GERAL
# ==========================================================

with aba_visao:

    cabecalho_secao(
        "📊 Visão Geral",
        "Resumo executivo das penalidades da equipe comercial."
    )

    espaco()

    # ======================================================
    # PRIMEIRA LINHA
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_pareto(ranking_pen),
            use_container_width=True,
            key="pareto_visao"
        )

    with col2:

        st.plotly_chart(
            grafico_faixas(resumo_faixa),
            use_container_width=True,
            key="faixas_visao"
        )

    espaco()

    # ======================================================
    # SEGUNDA LINHA
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_distribuicao(base_rca),
            use_container_width=True,
            key="distribuicao_visao"
        )

    with col2:

        st.plotly_chart(
            grafico_heatmap(base_rca),
            use_container_width=True,
            key="heatmap_visao"
        )

    espaco(2)

    # ======================================================
    # RESUMO EXECUTIVO
    # ======================================================

    caixa_informacoes(kpis)

    espaco()

    resumo_executivo(kpis)

    espaco()

    # ======================================================
    # MOTIVOS DAS PENALIDADES
    # ======================================================

    quadro_motivos()

    espaco()

    legenda_penalidades()

# ==========================================================
# ABA 2 - RANKINGS
# ==========================================================

with aba_rankings:

    cabecalho_secao(
        "🏆 Rankings dos RCAs",
        "Comparativo dos vendedores por penalidade, trocas, bonificações e devoluções."
    )

    espaco()

    # ======================================================
    # PRIMEIRA LINHA
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_penalidade(ranking_pen),
            use_container_width=True,
            key="ranking_penalidade"
        )

    with col2:

        st.plotly_chart(
            grafico_penalidade_percentual(ranking_pct),
            use_container_width=True,
            key="ranking_percentual"
        )

    espaco(2)

    # ======================================================
    # SEGUNDA LINHA
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_troca_meta(ranking_troca),
            use_container_width=True,
            key="ranking_troca"
        )

    with col2:

        st.plotly_chart(
            grafico_bonificacao(ranking_bonus),
            use_container_width=True,
            key="ranking_bonificacao"
        )

    espaco(2)

    # ======================================================
    # TERCEIRA LINHA
    # ======================================================

    st.plotly_chart(
        grafico_grandes_redes(ranking_redes),
        use_container_width=True,
        key="ranking_grandes_redes"
    )

    espaco()

    observacao(
        """
        Os rankings apresentam os 20 RCAs com maior impacto financeiro em cada indicador,
        respeitando os filtros aplicados na barra lateral.
        """
    )
# ==========================================================
# ABA 3 - SUPERVISORES
# ==========================================================

with aba_supervisores:

    cabecalho_secao(
        "👨‍💼 Supervisores",
        "Análise consolidada das penalidades por supervisor."
    )

    espaco()

    # ======================================================
    # GRÁFICO PRINCIPAL
    # ======================================================

    st.plotly_chart(
        grafico_supervisor(ranking_super),
        use_container_width=True,
        key="grafico_supervisores"
    )

    espaco(2)

    # ======================================================
    # INDICADORES
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        indicador_simples(
            "Total de Supervisores",
            kpis["supervisores"]
        )

    with col2:

        indicador_simples(
            "RCAs",
            kpis["rcas"]
        )

    with col3:

        indicador_simples(
            "RCAs com Penalidade",
            kpis["rcas_penalidade"]
        )

    espaco(2)

    # ======================================================
    # TABELA DOS SUPERVISORES
    # ======================================================

    titulo_tabela("Resumo por Supervisor")

    tabela_supervisor = ranking_super.copy()

    st.dataframe(
        tabela_supervisor,
        use_container_width=True,
        height=420
    )

    espaco()

    observacao(
        """
        Esta visão consolida os resultados por supervisor,
        permitindo identificar rapidamente quais equipes
        apresentam maior impacto financeiro com penalidades.
        """
    )
# ==========================================================
# ABA 4 - TABELAS
# ==========================================================

with aba_tabelas:

    cabecalho_secao(
        "📋 Tabelas Analíticas",
        "Consulta detalhada das informações utilizadas pelo Dashboard."
    )

    espaco()

    tab1, tab2, tab3 = st.tabs(
        [
            "📊 Analítica",
            "💰 Financeiro",
            "🎯 Acima da Meta"
        ]
    )

    # ------------------------------------------------------
    # ANALÍTICA
    # ------------------------------------------------------

    with tab1:

        titulo_tabela("Tabela Analítica")

        st.dataframe(
            tabela_geral,
            use_container_width=True,
            height=600,
            key="tbl_analitica"
        )

    # ------------------------------------------------------
    # FINANCEIRO
    # ------------------------------------------------------

    with tab2:

        titulo_tabela("Tabela Financeira")

        st.dataframe(
            tabela_financeira,
            use_container_width=True,
            height=600,
            key="tbl_financeiro"
        )

    # ------------------------------------------------------
    # ACIMA DA META
    # ------------------------------------------------------

    with tab3:

        titulo_tabela("RCAs Acima da Meta")

        st.dataframe(
            tabela_meta,
            use_container_width=True,
            height=600,
            key="tbl_meta"
        )

# ==========================================================
# ABA 5 - EXPORTAÇÃO
# ==========================================================

with aba_exportacao:

    cabecalho_secao(
        "📤 Exportação",
        "Exportação dos dados apresentados no Dashboard."
    )

    espaco()

    col1, col2 = st.columns([2, 1])

    with col1:

        observacao(
            """
Os arquivos exportados respeitam todos os filtros aplicados no Dashboard.

Você poderá utilizar estas informações para auditorias, reuniões,
envio para gestores ou análises complementares.
"""
        )

        espaco()

        botao_download_excel(
            "Dashboard_Penalidades.xlsx",
            arquivo_excel.getvalue()
        )

    with col2:

        badge("Dashboard Executivo")

        espaco()

        indicador_simples(
            "RCAs",
            kpis["rcas"]
        )

        indicador_simples(
            "Supervisores",
            kpis["supervisores"]
        )

        indicador_simples(
            "RCAs Penalizados",
            kpis["rcas_penalidade"]
        )

# ==========================================================
# RODAPÉ
# ==========================================================

espaco(2)

linha()

rodape_dashboard()

