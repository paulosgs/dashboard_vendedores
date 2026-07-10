import streamlit as st
import pandas as pd
import io

# ==========================================================
# IMPORTAÇÕES DO PROJETO
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

from styles import carregar_css

from componentes import *

from graficos import *

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
# AGUARDA O UPLOAD
# ==========================================================

if arquivo is None:

    st.info(
        "Selecione uma planilha (.xlsx) para iniciar o Dashboard."
    )

    st.stop()

# ==========================================================
# CARREGA DADOS
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

    # ------------------------------
    # SUPERVISOR
    # ------------------------------

    lista_supervisores = sorted(

        base_rca["SUPERVISOR"].dropna().unique()

    )

    supervisor = st.multiselect(

        "Supervisor",

        options=lista_supervisores,

        default=lista_supervisores

    )

    # ------------------------------
    # VENDEDOR
    # ------------------------------

    lista_vendedores = sorted(

        base_rca.loc[

            base_rca["SUPERVISOR"].isin(supervisor),

            "VENDEDOR"

        ].dropna().unique()

    )

    vendedor = st.multiselect(

        "Vendedor",

        options=lista_vendedores,

        default=lista_vendedores

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
# RECALCULA TODOS OS DADOS
# (A PARTIR DA BASE FILTRADA)
# ==========================================================

# ------------------------------
# KPIs
# ------------------------------

kpis = indicadores_dashboard(base_rca)

# ------------------------------
# Rankings
# ------------------------------

ranking_pen = ranking_penalidade(base_rca)

ranking_pct = ranking_percentual_penalidade(base_rca)

ranking_super = ranking_supervisor(base_supervisor)

ranking_troca = ranking_trocas(base_rca)

ranking_redes = ranking_grandes_redes(base_rca)

ranking_bonus = ranking_bonificacao(base_rca)

# ------------------------------
# Resumos
# ------------------------------

resumo_faixa = resumo_faixas(base_rca)

# ------------------------------
# Tabelas
# ------------------------------

analitico = tabela_analitica(base_rca)

descontos = tabela_descontos(base_rca)

# ==========================================================
# KPI's
# ==========================================================

linha_kpis(kpis)

espaco()

linha_kpis2(kpis)

espaco(2)

# ==========================================================
# RESUMO EXECUTIVO
# ==========================================================

resumo_executivo(kpis)

espaco()

# ==========================================================
# MOTIVOS DE PENALIDADE
# ==========================================================

quadro_motivos()

espaco(2)

# ==========================================================
# DASHBOARD EXECUTIVO
# ==========================================================

cabecalho_secao(

    "📊 Dashboard Executivo",

    "Acompanhamento das penalidades e indicadores dos vendedores"

)

espaco()

# ==========================================================
# PRIMEIRA LINHA
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(

        grafico_penalidade(

            ranking_pen

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

with col2:

    st.plotly_chart(

        grafico_penalidade_percentual(

            ranking_pct

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

espaco()

# ==========================================================
# SEGUNDA LINHA
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(

        grafico_supervisor(

            ranking_super

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

with col2:

    st.plotly_chart(

        grafico_pareto(

            ranking_pen

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

espaco()

# ==========================================================
# TERCEIRA LINHA
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(

        grafico_faixas(

            resumo_faixa

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

with col2:

    st.plotly_chart(

        grafico_distribuicao(

            base_rca

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

espaco(2)

# ==========================================================
# ANÁLISE DE TROCAS
# ==========================================================

cabecalho_secao(

    "🔁 Análise de Trocas",

    "Acompanhamento da meta de troca, bonificações e grandes redes"

)

espaco()

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# TROCA x META
# ----------------------------------------------------------

with col1:

    st.plotly_chart(

        grafico_troca_meta(

            ranking_troca

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

# ----------------------------------------------------------
# BONIFICAÇÕES
# ----------------------------------------------------------

with col2:

    st.plotly_chart(

        grafico_bonificacao(

            ranking_bonus

        ),

        use_container_width=True,

        config={

            "displaylogo": False,

            "responsive": True

        }

    )

espaco()

# ----------------------------------------------------------
# GRANDES REDES
# ----------------------------------------------------------

st.plotly_chart(

    grafico_grandes_redes(

        ranking_redes

    ),

    use_container_width=True,

    config={

        "displaylogo": False,

        "responsive": True

    }

)

espaco(2)

# ==========================================================
# TABELA ANALÍTICA
# ==========================================================

cabecalho_secao(

    "📋 Tabela Analítica",

    "Detalhamento dos indicadores por vendedor"

)

st.dataframe(

    analitico,

    use_container_width=True,

    height=500

)

espaco(2)

# ==========================================================
# FINANCEIRO
# ==========================================================

cabecalho_secao(

    "💰 Financeiro",

    "Vendedores com desconto por penalidade"

)

st.dataframe(

    descontos,

    use_container_width=True,

    height=500

)

espaco()

# ==========================================================
# EXPORTAÇÃO
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

botao_download_excel(

    "Penalidades.xlsx",

    arquivo_excel.getvalue()

)

espaco(2)

# ==========================================================
# RODAPÉ
# ==========================================================

rodape_dashboard()

