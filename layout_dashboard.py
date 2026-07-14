# ==========================================================
# LAYOUT DASHBOARD
# Dashboard Executivo de Penalidades
# Distrinorte Distribuidora
# ==========================================================

import streamlit as st
import pandas as pd
import io

# ==========================================================
# MÓDULOS DO PROJETO
# ==========================================================

import data
import componentes
import graficos
import styles
import utils

# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def executar_dashboard():

    # ======================================================
    # CSS
    # ======================================================

    styles.carregar_css()

    # ======================================================
    # CABEÇALHO
    # ======================================================

    componentes.cabecalho_dashboard()

    # ======================================================
    # SIDEBAR
    # ======================================================

    with st.sidebar:

        st.header("📂 Base de Dados")

        arquivo = st.file_uploader(
            label="Selecione a planilha",
            type=["xlsx"],
            accept_multiple_files=False
        )

        st.divider()

        st.header("ℹ️ Informações")

        st.info(
            """
            Dashboard Executivo de Penalidades

            Desenvolvido para acompanhamento de:

            • Penalidades

            • Trocas (TV11)

            • Bonificações (TV5)

            • Grandes Redes

            • Supervisores
            """
        )

    # ======================================================
    # AGUARDANDO PLANILHA
    # ======================================================

    if arquivo is None:

        st.info(
            "Selecione uma planilha para iniciar a análise."
        )

        return

    # ======================================================
    # CARREGAMENTO
    # ======================================================

    with st.spinner("Carregando base de dados..."):

        try:

            bases = data.carregar_bases(arquivo)

        except Exception as erro:

            st.error("Erro ao carregar a planilha.")

            st.exception(erro)

            return

    # ======================================================
    # BASES PRINCIPAIS
    # ======================================================

    base_rca = bases["base_rca"]

    base_supervisor = bases["base_supervisor"]

    # ======================================================
    # FILTROS
    # ======================================================

    with st.sidebar:

        st.divider()

        st.header("🎯 Filtros")

    # -----------------------------------------
    # SUPERVISOR
    # -----------------------------------------

    lista_supervisores = sorted(
            base_rca["SUPERVISOR"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    supervisor = st.multiselect(
            "Supervisor",
            options=lista_supervisores,
            default=lista_supervisores
        )

    # -----------------------------------------
    # RCA
    # -----------------------------------------

    base_aux = base_rca.copy()

    if len(supervisor):

            base_aux = base_aux[
                base_aux["SUPERVISOR"].isin(supervisor)
            ]

    lista_rcas = sorted(
            base_aux["VENDEDOR"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    vendedor = st.multiselect(
            "Vendedor",
            options=lista_rcas,
            default=lista_rcas
        )

    # ======================================================
    # APLICA FILTROS
    # ======================================================

    if len(supervisor):

        base_rca = base_rca[
            base_rca["SUPERVISOR"].isin(supervisor)
        ]

        base_supervisor = base_supervisor[
            base_supervisor["SUPERVISOR"].isin(supervisor)
        ]

    if len(vendedor):

        base_rca = base_rca[
            base_rca["VENDEDOR"].isin(vendedor)
        ]

    # ======================================================
    # SEM DADOS
    # ======================================================

    if base_rca.empty:

        st.warning(
            "Nenhum registro encontrado para os filtros selecionados."
        )

        return

    # ======================================================
    # RESUMO DA BASE
    # ======================================================

    st.success("Base carregada com sucesso!")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "RCAs",
            base_rca["VENDEDOR"].nunique()
        )

    with col2:

        st.metric(
            "Supervisores",
            base_supervisor["SUPERVISOR"].nunique()
        )

    with col3:

        st.metric(
            "Registros",
            f"{len(base_rca):,}".replace(",", ".")
        )

    # ======================================================
    # PREPARAÇÃO DOS DADOS
    # ======================================================

    with st.spinner("Preparando indicadores..."):

        # KPIs
        kpis = data.indicadores_dashboard(base_rca)

        # Rankings
        ranking_pen = data.ranking_penalidade(base_rca)

        ranking_percentual = data.ranking_percentual_penalidade(base_rca)

        ranking_supervisor = data.ranking_supervisor(base_supervisor)

        ranking_troca = data.ranking_trocas(base_rca)

        ranking_bonificacao = data.ranking_bonificacao(base_rca)

        ranking_grandes_redes = data.ranking_grandes_redes(base_rca)

        # Tabelas
        tabela_analitica = data.tabela_analitica(base_rca)

        tabela_financeira = data.tabela_descontos(base_rca)

        tabela_meta = data.tabela_acima_meta(base_rca)

    # ======================================================
    # EXPORTAÇÃO
    # ======================================================

    arquivo_excel = io.BytesIO()

    with pd.ExcelWriter(
        arquivo_excel,
        engine="openpyxl"
    ) as writer:

        tabela_analitica.to_excel(
            writer,
            sheet_name="Analítica",
            index=False
        )

        tabela_financeira.to_excel(
            writer,
            sheet_name="Financeiro",
            index=False
        )

        tabela_meta.to_excel(
            writer,
            sheet_name="Acima da Meta",
            index=False
        )

    arquivo_excel.seek(0)
    # ======================================================
    # KPIs EXECUTIVOS
    # ======================================================

    st.markdown("---")

    componentes.linha_kpis(kpis)

    st.markdown("")

    componentes.linha_kpis2(kpis)

    st.markdown("")

    componentes.alerta_penalidade(base_rca)

    st.markdown("")

    componentes.resumo_executivo(kpis)

    st.markdown("---")

    # ======================================================
    # ABAS DO DASHBOARD
    # ======================================================

    (
        aba_visao,
        aba_rankings,
        aba_supervisores,
        aba_tabelas,
        aba_exportacao,
    ) = st.tabs(
        [
            "📊 Visão Geral",
            "🏆 Rankings",
            "👨‍💼 Supervisores",
            "📋 Tabelas",
            "📤 Exportação",
        ]
    )
    # ======================================================
    # ABA 1 - VISÃO GERAL
    # ======================================================

    with aba_visao:

        componentes.cabecalho_secao(
            "📊 Visão Geral",
            "Resumo executivo das penalidades da equipe comercial."
        )

        st.markdown("")

        # ==================================================
        # PRIMEIRA LINHA
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(
                graficos.grafico_pareto(ranking_pen),
                use_container_width=True,
                key="grafico_pareto"
            )

        with col2:

            st.plotly_chart(
                graficos.grafico_faixas(base_rca),
                use_container_width=True,
                key="grafico_faixas"
            )

        st.markdown("")

        # ==================================================
        # SEGUNDA LINHA
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(
                graficos.grafico_distribuicao(base_rca),
                use_container_width=True,
                key="grafico_distribuicao"
            )

        with col2:

            st.plotly_chart(
                graficos.grafico_heatmap(base_rca),
                use_container_width=True,
                key="grafico_heatmap"
            )

        st.markdown("")

        componentes.quadro_motivos()

        st.markdown("")

        componentes.legenda_penalidades()


