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
    # TESTE
    # ======================================================

    st.success("Base carregada com sucesso!")

    st.write("Quantidade de RCAs:", len(base_rca))

    st.write("Quantidade de Supervisores:", len(base_supervisor))

