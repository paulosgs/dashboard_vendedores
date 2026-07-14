import streamlit as st
import pandas as pd
import io

# ==========================================================
# IMPORTAÇÕES
# ==========================================================

from data import (
    carregar_bases,
    indicadores_dashboard,
    ranking_penalidade,
    ranking_percentual_penalidade,
    ranking_supervisor,
    ranking_trocas,
    ranking_grandes_redes,
    ranking_bonificacao,
    resumo_faixas,
    tabela_descontos,
    tabela_analitica
)

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

    try:
        st.image(
            "assets/logo.png",
            use_container_width=True
        )
    except:
        pass

    st.markdown("---")

    st.subheader("📂 Base de Dados")

    arquivo = st.file_uploader(
        "Selecione a planilha",
        type=["xlsx"]
    )

# ==========================================================
# AGUARDA UPLOAD
# ==========================================================

if arquivo is None:

    st.info(
        "Selecione uma planilha (.xlsx) para iniciar o Dashboard."
    )

    st.stop()

# ==========================================================
# CARREGA BASES
# ==========================================================

bases = carregar_bases(arquivo)

base_rca = bases["base_rca"]

base_supervisor = bases["base_supervisor"]

# ==========================================================
# FILTROS
# ==========================================================

with st.sidebar:

    st.markdown("---")

    st.subheader("🎯 Filtros")

    supervisores = sorted(
        base_rca["SUPERVISOR"]
        .dropna()
        .unique()
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
    (base_rca["SUPERVISOR"].isin(supervisor))
    &
    (base_rca["VENDEDOR"].isin(vendedor))
].copy()

base_supervisor = base_supervisor.loc[
    base_supervisor["SUPERVISOR"].isin(supervisor)
].copy()

# ==========================================================
# CASO NÃO EXISTA DADOS
# ==========================================================

if base_rca.empty:

    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )

    st.stop()

# ==========================================================
# KPI's
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

# ==========================================================
# TABELAS
# ==========================================================

analitico = tabela_analitica(base_rca)

descontos = tabela_descontos(base_rca)

# ==========================================================
# EXCEL PARA DOWNLOAD
# ==========================================================

arquivo_excel = io.BytesIO()

with pd.ExcelWriter(
    arquivo_excel,
    engine="openpyxl"
) as writer:

    descontos.to_excel(
        writer,
        sheet_name="Descontos",
        index=False
    )

arquivo_excel.seek(0)

# ==========================================================
# KPI's DO TOPO
# ==========================================================

linha_kpis(kpis)

espaco()

linha_kpis2(kpis)

espaco(2)

# ==========================================================
# ALERTA EXECUTIVO
# ==========================================================

alerta_penalidade(base_rca)

# ==========================================================
# RESUMO EXECUTIVO
# ==========================================================

resumo_executivo(kpis)

espaco(2)

# ==========================================================
# ABAS PRINCIPAIS
# ==========================================================

(
    aba_visao,
    aba_rankings,
    aba_performance,
    aba_tabelas,
    aba_exportacao,
) = st.tabs(
    [
        "📊 Visão Geral",
        "🏆 Rankings",
        "📈 Performance",
        "📋 Tabelas",
        "📤 Exportação",
    ]
)

# ==========================================================
# ABA 1 - VISÃO GERAL
# ==========================================================

with aba_visao:

    cabecalho_secao(
        "📊 Visão Geral",
        "Resumo executivo das penalidades, distribuição e indicadores."
    )

    espaco()

# ------------------------------------------------------
# PRIMEIRA LINHA
# ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_pareto(ranking_pen),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    with col2:

        st.plotly_chart(
            grafico_supervisor(ranking_super),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    espaco()

# ------------------------------------------------------
# SEGUNDA LINHA
# ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_faixas(resumo_faixa),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    with col2:

        st.plotly_chart(
            grafico_distribuicao(base_rca),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    espaco(2)

    # ------------------------------------------------------
    # RESUMO DA BASE
    # ------------------------------------------------------

    caixa_informacoes(kpis)

    espaco()

    # ------------------------------------------------------
    # MOTIVOS DAS PENALIDADES
    # ------------------------------------------------------

    quadro_motivos()

    espaco()

    # ------------------------------------------------------
    # LEGENDA
    # ------------------------------------------------------

    legenda_penalidades()
    # ==========================================================
# ABA 2 - RANKINGS
# ==========================================================

with aba_rankings:

    cabecalho_secao(
        "🏆 Rankings",
        "Rankings dos vendedores por indicador."
    )

    espaco()

    # ------------------------------------------------------
    # PRIMEIRA LINHA
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_penalidade(ranking_pen),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    with col2:

        st.plotly_chart(
            grafico_penalidade_percentual(ranking_pct),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    espaco()

    # ------------------------------------------------------
    # SEGUNDA LINHA
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_troca_meta(ranking_troca),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    with col2:

        st.plotly_chart(
            grafico_bonificacao(ranking_bonus),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    espaco()

    # ------------------------------------------------------
    # TERCEIRA LINHA
    # ------------------------------------------------------

    st.plotly_chart(
        grafico_grandes_redes(ranking_redes),
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True
        }
    )

# ==========================================================
# ABA 3 - PERFORMANCE
# ==========================================================

with aba_performance:

    cabecalho_secao(
        "📈 Performance Comercial",
        "Análises consolidadas de desempenho."
    )

    espaco()

    # ------------------------------------------------------
    # PRIMEIRA LINHA
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_supervisor(ranking_super),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    with col2:

        st.plotly_chart(
            grafico_pareto(ranking_pen),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    espaco()

    # ------------------------------------------------------
    # SEGUNDA LINHA
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            grafico_faixas(resumo_faixa),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    with col2:

        st.plotly_chart(
            grafico_distribuicao(base_rca),
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True
            }
        )

    espaco()

    # ------------------------------------------------------
    # HEATMAP
    # ------------------------------------------------------

    st.plotly_chart(
        grafico_heatmap(base_rca),
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True
        }
    )

# ==========================================================
# ABA 4 - TABELAS
# ==========================================================

with aba_tabelas:

    cabecalho_secao(
        "📋 Tabelas Analíticas",
        "Consultas detalhadas para análise dos indicadores."
    )

    espaco()

    tab1, tab2 = st.tabs([
        "📊 Analítica",
        "💰 Financeiro"
    ])

    # ------------------------------------------------------
    # TABELA ANALÍTICA
    # ------------------------------------------------------

    with tab1:

        st.dataframe(
            analitico,
            use_container_width=True,
            height=650
        )

    # ------------------------------------------------------
    # TABELA FINANCEIRO
    # ------------------------------------------------------

    with tab2:

        st.dataframe(
            descontos,
            use_container_width=True,
            height=650
        )

# ==========================================================
# ABA 5 - EXPORTAÇÃO
# ==========================================================

with aba_exportacao:

    cabecalho_secao(
        "📤 Exportação",
        "Exportação das informações do Dashboard."
    )

    espaco()

    col1, col2 = st.columns([2,1])

    with col1:

        observacao("""
Utilize este botão para exportar a relação dos vendedores
com penalidades financeiras para Excel.

O arquivo respeita todos os filtros aplicados no Dashboard.
""")

        espaco()

        botao_download_excel(
            "Penalidades.xlsx",
            arquivo_excel.getvalue()
        )

    with col2:

        st.metric(
            "RCAs",
            kpis["rcas"]
        )

        st.metric(
            "Supervisores",
            kpis["supervisores"]
        )

        st.metric(
            "RCAs Penalizados",
            kpis["rcas_penalidade"]
        )

# ==========================================================
# RODAPÉ
# ==========================================================

espaco(2)

linha()

rodape_dashboard()