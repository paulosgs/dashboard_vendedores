# ==========================================================
# DASHBOARD EXECUTIVO DE PENALIDADES
# Distrinorte Distribuidora
# ==========================================================

import streamlit as st

from layout_dashboard import executar_dashboard

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
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    executar_dashboard()
