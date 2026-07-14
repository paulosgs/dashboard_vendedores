# ==========================================================
# LAYOUT DASHBOARD
# Dashboard Executivo de Penalidades
# Distrinorte Distribuidora
# ==========================================================

import io

from openpyxl import utils
import pandas as pd
import streamlit as st

# ==========================================================
# MÓDULOS DO PROJETO
# ==========================================================

import componentes
import data
import graficos
import styles

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
            "Selecione a planilha",
            type=["xlsx"],
            accept_multiple_files=False
        )

        st.divider()

        st.header("ℹ️ Informações")

        st.info(
            """
Dashboard Executivo de Penalidades

Este painel apresenta:

• Penalidades Financeiras

• Trocas (TV11)

• Bonificações (TV5)

• Grandes Redes

• Supervisores

• Rankings

• Indicadores Executivos
"""
        )

    # ======================================================
    # AGUARDANDO PLANILHA
    # ======================================================

    if arquivo is None:

        st.info(
            "Selecione uma planilha para iniciar o Dashboard."
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
    # BASES
    # ======================================================

    base_rca = bases["base_rca"]

    base_supervisor = bases["base_supervisor"]

    # ======================================================
    # KPIs
    # ======================================================

    kpis = bases["kpis"]

    # ======================================================
    # RANKINGS
    # ======================================================

    ranking_penalidade = bases["ranking_penalidade"]

    ranking_percentual = bases["ranking_penalidade_pct"]

    ranking_trocas = bases["ranking_trocas"]

    ranking_meta = bases["ranking_meta"]

    ranking_grandes_redes = bases["ranking_grandes_redes"]

    ranking_bonificacao = bases["ranking_bonificacao"]

    ranking_supervisor = bases["ranking_supervisor"]

    # ======================================================
    # TABELAS
    # ======================================================

    tabela_analitica = bases["tabela_analitica"]

    tabela_descontos = bases["tabela_descontos"]

    tabela_penalidades = bases["tabela_penalidades"]

    tabela_meta = bases["tabela_meta"]

    # ======================================================
    # RESUMOS
    # ======================================================

    resumo_faixas = bases["resumo_faixas"]

    resumo_meta = bases["resumo_meta"]

    # ======================================================
    # FILTROS
    # ======================================================

    with st.sidebar:

        st.divider()

        st.header("🎯 Filtros")

        lista_supervisores = sorted(
            base_rca["SUPERVISOR"]
            .dropna()
            .unique()
            .tolist()
        )

        supervisor = st.multiselect(
            "Supervisor",
            options=lista_supervisores,
            default=lista_supervisores
        )

        if supervisor:

            base_aux = base_rca[
                base_rca["SUPERVISOR"].isin(supervisor)
            ]

        else:

            base_aux = base_rca.copy()

        lista_vendedores = sorted(
            base_aux["VENDEDOR"]
            .dropna()
            .unique()
            .tolist()
        )

        vendedor = st.multiselect(
            "Vendedor",
            options=lista_vendedores,
            default=lista_vendedores
        )

    # ======================================================
    # APLICAÇÃO DOS FILTROS
    # ======================================================

    if supervisor:

        base_rca = base_rca[
            base_rca["SUPERVISOR"].isin(supervisor)
        ]

        base_supervisor = base_supervisor[
            base_supervisor["SUPERVISOR"].isin(supervisor)
        ]

    if vendedor:

        base_rca = base_rca[
            base_rca["VENDEDOR"].isin(vendedor)
        ]

    # ======================================================
    # VALIDAÇÃO
    # ======================================================

    if base_rca.empty:

        componentes.sem_dados()

        return

    # ======================================================
    # REPROCESSA SOMENTE O NECESSÁRIO APÓS OS FILTROS
    # ======================================================

    kpis = data.indicadores_dashboard(base_rca)

    ranking_penalidade = data.ranking_penalidade(base_rca)

    ranking_percentual = data.ranking_percentual_penalidade(base_rca)

    ranking_trocas = data.ranking_trocas(base_rca)

    ranking_meta = data.ranking_meta_troca(base_rca)

    ranking_grandes_redes = data.ranking_grandes_redes(base_rca)

    ranking_bonificacao = data.ranking_bonificacao(base_rca)

    ranking_supervisor = data.ranking_supervisor(base_supervisor)

    tabela_analitica = data.tabela_analitica(base_rca)

    tabela_descontos = data.tabela_descontos(base_rca)

    tabela_penalidades = data.tabela_penalidades(base_rca)

    tabela_meta = data.tabela_acima_meta(base_rca)

    resumo_faixas = data.resumo_faixas(base_rca)

    resumo_meta = data.resumo_meta(base_rca)

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

        tabela_descontos.to_excel(
            writer,
            sheet_name="Descontos",
            index=False
        )

        tabela_meta.to_excel(
            writer,
            sheet_name="Meta",
            index=False
        )

    arquivo_excel.seek(0)

    # ======================================================
    # CABEÇALHO EXECUTIVO
    # ======================================================

    componentes.divisor()

    componentes.linha_kpis(kpis)

    componentes.espaco()

    componentes.linha_kpis2(kpis)

    componentes.espaco()

    componentes.alerta_penalidade(base_rca)

    componentes.espaco()

    componentes.resumo_executivo(kpis)

    componentes.espaco(2)

    # ======================================================
    # INFORMAÇÕES DA BASE
    # ======================================================

    componentes.caixa_informacoes(kpis)

    componentes.espaco()

    # ======================================================
    # ABAS
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

        componentes.espaco()

        # ==================================================
        # PRIMEIRA LINHA
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(

                graficos.grafico_pareto(
                    ranking_penalidade
                ),

                use_container_width=True,

                key="pareto"

            )

        with col2:

            st.plotly_chart(

                graficos.grafico_faixas(
                    resumo_faixas
                ),

                use_container_width=True,

                key="faixas"

            )

        componentes.espaco()

        # ==================================================
        # SEGUNDA LINHA
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(

                graficos.grafico_distribuicao(
                    base_rca
                ),

                use_container_width=True,

                key="distribuicao"

            )

        with col2:

            st.plotly_chart(

                graficos.grafico_heatmap(
                    base_rca
                ),

                use_container_width=True,

                key="heatmap"

            )

        componentes.espaco(2)

        # ==================================================
        # MOTIVOS DAS PENALIDADES
        # ==================================================

        componentes.quadro_motivos()

        componentes.espaco()

        componentes.legenda_penalidades()

    # ======================================================
    # ABA 2 - RANKINGS
    # ======================================================

    with aba_rankings:

        componentes.cabecalho_secao(
            "🏆 Rankings dos RCAs",
            "Comparativo dos vendedores por penalidades, trocas, bonificações e devoluções."
        )

        componentes.espaco()

        # ==================================================
        # PENALIDADE x %
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(

                graficos.grafico_penalidade(
                    ranking_penalidade
                ),

                use_container_width=True,

                key="ranking_penalidade"

            )

        with col2:

            st.plotly_chart(

                graficos.grafico_penalidade_percentual(
                    ranking_percentual
                ),

                use_container_width=True,

                key="ranking_percentual"

            )

        componentes.espaco(2)

        # ==================================================
        # TROCAS x BONIFICAÇÕES
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(

                graficos.grafico_troca_meta(
                    ranking_trocas
                ),

                use_container_width=True,

                key="ranking_trocas"

            )

        with col2:

            st.plotly_chart(

                graficos.grafico_bonificacao(
                    ranking_bonificacao
                ),

                use_container_width=True,

                key="ranking_bonificacao"

            )

        componentes.espaco(2)

        # ==================================================
        # GRANDES REDES
        # ==================================================

        st.plotly_chart(

            graficos.grafico_grandes_redes(
                ranking_grandes_redes
            ),

            use_container_width=True,

            key="ranking_grandes_redes"

        )

        componentes.espaco()

        componentes.observacao(
            """
Os rankings apresentados consideram somente os filtros aplicados
na barra lateral e exibem os vendedores com maior impacto financeiro.
"""
        )

    # ======================================================
    # ABA 3 - SUPERVISORES
    # ======================================================

    with aba_supervisores:

        componentes.cabecalho_secao(
            "👨‍💼 Supervisores",
            "Resumo dos resultados consolidados por supervisor."
        )

        componentes.espaco()

        # ==================================================
        # GRÁFICO
        # ==================================================

        st.plotly_chart(

            graficos.grafico_supervisor(
                ranking_supervisor
            ),

            use_container_width=True,

            key="grafico_supervisor"

        )

        componentes.espaco(2)

        # ==================================================
        # TABELA
        # ==================================================

        componentes.titulo_tabela(
            "Resumo por Supervisor"
        )

        st.dataframe(

            base_supervisor,

            use_container_width=True,

            hide_index=True

        )

        componentes.espaco()

        componentes.observacao(
            """
Os valores apresentados representam o consolidado dos vendedores
pertencentes a cada supervisor considerando os filtros aplicados.
"""
        )

    # ======================================================
    # ABA 4 - TABELAS
    # ======================================================

    with aba_tabelas:

        componentes.cabecalho_secao(
            "📋 Tabelas Analíticas",
            "Consulta detalhada das informações processadas pelo dashboard."
        )

        componentes.espaco()

        # ==================================================
        # ANALÍTICA
        # ==================================================

        with st.expander(
            "📊 Tabela Analítica",
            expanded=True
        ):

            componentes.titulo_tabela(
                "Tabela Analítica"
            )

            st.dataframe(
                tabela_analitica,
                use_container_width=True,
                hide_index=True
            )

        # ==================================================
        # PENALIDADES
        # ==================================================

        with st.expander(
            "💰 Penalidades",
            expanded=False
        ):

            componentes.titulo_tabela(
                "Tabela de Penalidades"
            )

            st.dataframe(
                tabela_penalidades,
                use_container_width=True,
                hide_index=True
            )

        # ==================================================
        # DESCONTOS
        # ==================================================

        with st.expander(
            "💵 Descontos",
            expanded=False
        ):

            componentes.titulo_tabela(
                "Tabela de Descontos"
            )

            st.dataframe(
                tabela_descontos,
                use_container_width=True,
                hide_index=True
            )

        # ==================================================
        # META
        # ==================================================

        with st.expander(
            "🎯 Acima da Meta",
            expanded=False
        ):

            componentes.titulo_tabela(
                "Tabela Acima da Meta"
            )

            st.dataframe(
                tabela_meta,
                use_container_width=True,
                hide_index=True
            )

        componentes.espaco(2)

        componentes.observacao(
            """
Todas as tabelas respeitam os filtros selecionados na barra lateral e
podem ser ordenadas diretamente pelo Streamlit clicando no cabeçalho
das colunas.
"""
        )

    # ======================================================
    # ABA 5 - EXPORTAÇÃO
    # ======================================================

    with aba_exportacao:

        componentes.cabecalho_secao(
            "📤 Exportação",
            "Exportação das informações do Dashboard."
        )

        componentes.espaco()

        col1, col2 = st.columns([2,1])

        # ==================================================
        # DOWNLOAD
        # ==================================================

        with col1:

            componentes.observacao(
                """
O arquivo Excel será exportado contendo todas as informações
já filtradas no Dashboard.

São exportadas:

• Tabela Analítica

• Tabela de Descontos

• Tabela Acima da Meta
                """
            )

            componentes.espaco()

            componentes.botao_download_excel(
                "Dashboard_Penalidades.xlsx",
                arquivo_excel.getvalue()
            )

        # ==================================================
        # INDICADORES
        # ==================================================

        with col2:

            componentes.badge("Dashboard Executivo")

            componentes.espaco()

            componentes.indicador_simples(
                "RCAs",
                kpis["rcas"]
            )

            componentes.indicador_simples(
                "Supervisores",
                kpis["supervisores"]
            )

            componentes.indicador_simples(
                "RCAs Penalizados",
                kpis["rcas_penalidade"]
            )

            componentes.indicador_simples(
                "Total Penalidade",
                utils.formatar_moeda(
                    kpis["total_penalidade"]
                )
            )

    # ======================================================
    # RODAPÉ
    # ======================================================

    componentes.espaco(3)

    componentes.linha()

    componentes.rodape_dashboard()
    