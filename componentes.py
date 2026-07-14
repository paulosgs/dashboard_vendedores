"""
=========================================================
COMPONENTES.PY
Componentes visuais do Dashboard Executivo
=========================================================
"""
import streamlit as st
from textwrap import dedent
from utils import (
    formatar_moeda,
    formatar_percentual
)

# ==========================================================
# TÍTULOS
# ==========================================================

def titulo_principal():
    st.markdown(
        dedent("""
        <div style="margin-bottom:8px;">
            <h1 style="
                color:white;
                margin-bottom:0px;
                font-size:40px;
                font-weight:700;
            ">
                💸 Dashboard Executivo de Penalidades
            </h1>
            <span style="
                color:#A7B7C7;
                font-size:17px;
            ">
                Gestão Comercial • Penalidades • Trocas • Devoluções
            </span>
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# TÍTULO DAS SEÇÕES
# ==========================================================

def titulo_secao(texto):
    st.markdown(
        dedent(f"""
        <div style="
            margin-top:25px;
            margin-bottom:15px;
        ">
            <h2 style="
                color:#00C2FF;
                font-weight:600;
                margin-bottom:0px;
            ">
                {texto}
            </h2>
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# SUBTÍTULO
# ==========================================================

def subtitulo(texto):
    st.markdown(
        dedent(f"""
        <span style="
            color:#9BA8B8;
            font-size:15px;
        ">
            {texto}
        </span>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# CARD KPI
# ==========================================================

def card_kpi(
    titulo,
    valor,
    subtitulo="",
    cor="#00C2FF",
    icone="📊"
):
    st.markdown(
        dedent(f"""
        <div class="card">
            <div class="card-title">
                {icone} {titulo}
            </div>
            <div
            class="card-value"
            style="
            color:{cor};
            ">
                {valor}
            </div>
            <div class="card-footer">
                {subtitulo}
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# LINHA DE 4 KPIs
# ==========================================================

def linha_kpis(kpis):
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        card_kpi(
            "TOTAL PENALIDADE",
            formatar_moeda(
                kpis["total_penalidade"]
            ),
            "Valor total a descontar",
            "#FF4D6D",
            "💰"
        )
    with col2:
        card_kpi(
            "% PENALIDADE",
            formatar_percentual(
                kpis["perc_penalidade"]
            ),
            "Sobre as vendas",
            "#FDBE2D",
            "📉"
        )
    with col3:
        card_kpi(
            "RCAs COM PENALIDADE",
            kpis["rcas_penalidade"],
            "Com desconto",
            "#00C2FF",
            "👤"
        )
    with col4:
        card_kpi(
            "TOTAL VENDAS",
            formatar_moeda(
                kpis["total_vendas"]
            ),
            "Valor vendido",
            "#00D084",
            "📈"
        )

# ==========================================================
# SEGUNDA LINHA KPIs
# ==========================================================

def linha_kpis2(kpis):
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        card_kpi(
            "TOTAL TROCAS",
            formatar_moeda(
                kpis["total_troca"]
            ),
            "TV11",
            "#00C2FF",
            "🔁"
        )
    with col2:
        card_kpi(
            "% META TROCA",
            formatar_percentual(
                kpis["perc_meta"]
            ),
            "Meta atingida",
            "#FDBE2D",
            "🎯"
        )
    with col3:
        card_kpi(
            "BONIFICAÇÕES",
            formatar_moeda(
                kpis["total_bonificacao"]
            ),
            "TV5",
            "#00D084",
            "🎁"
        )
    with col4:
        card_kpi(
            "GRANDES REDES",
            formatar_moeda(
                kpis["total_grandes_redes"]
            ),
            "Devoluções",
            "#FF4D6D",
            "🏪"
        )

# ==========================================================
# DIVISOR
# ==========================================================

def divisor():
    st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# ESPAÇO
# ==========================================================

def espaco(linhas=1):
    for _ in range(linhas):
        st.write("")

# ==========================================================
# MENSAGEM SEM DADOS
# ==========================================================

def sem_dados():
    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )

# ==========================================================
# CABEÇALHO EXECUTIVO
# ==========================================================

def cabecalho_dashboard():
    titulo_principal()
    subtitulo(
        "Dashboard desenvolvido para acompanhamento das penalidades financeiras, trocas e devoluções dos vendedores."
    )
    espaco()

# ==========================================================
# QUADRO DE MOTIVOS DE PENALIDADE
# ==========================================================

def quadro_motivos():
    st.markdown(
        dedent("""
        <div class="motivos">
            <h4>⚠️ Motivos que Geram Penalidade ao Vendedor</h4>
            <div class="motivos-grid">
                <div class="motivo"><b>6</b> • Pedido Duplicado</div>
                <div class="motivo"><b>7</b> • Cliente não Pediu Mercadoria</div>
                <div class="motivo"><b>11</b> • Desacordo (Preço / Forma Pagamento)</div>
                <div class="motivo"><b>28</b> • Desacordo com o Pedido</div>
                <div class="motivo"><b>88</b> • Desacordo (Falta Troca)</div>
                <div class="motivo"><b>104</b> • Desacordo (Brinde / Bonificação)</div>
                <div class="motivo"><b>105</b> • Cliente sem Pedido</div>
                <div class="motivo"><b>106</b> • Desacordo (Acordo Comercial)</div>
                <div class="motivo"><b>127</b> • Produto Incorreto</div>
                <div class="motivo"><b>129</b> • Erro Código Cliente</div>
                <div class="motivo"><b>180</b> • Desacordo</div>
                <div class="motivo"><b>194</b> • Refatura - Vendas</div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# CAIXA DE INFORMAÇÕES DA BASE
# ==========================================================

def caixa_informacoes(kpis):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(
            f"""
👤 **RCAs**
{kpis['rcas']}
"""
        )
    with c2:
        st.info(
            f"""
👨‍💼 **Supervisores**
{kpis['supervisores']}
"""
        )
    with c3:
        st.info(
            """
🏆 **Ranking**
Top 20 RCAs
"""
        )

# ==========================================================
# LEGENDA DAS CORES
# ==========================================================

def legenda_penalidades():
    st.markdown(
        dedent("""
        <div class="card">
        <b style="color:white;font-size:17px;">
        🎨 Legenda das Penalidades
        </b>
        <br><br>
        🔵 Até R$ 500,00
        <br>
        🟡 Entre R$ 500,01 e R$ 2.000,00
        <br>
        🔴 Acima de R$ 2.000,00
        <br>
        🟣 Acima de R$ 5.000,00 (Crítica)
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# ALERTA EXECUTIVO
# ==========================================================

def alerta_penalidade(base_rca):
    criticos = (
        base_rca["PENALIDADE_VALOR"] > 5000
    ).sum()
    if criticos > 0:
        st.markdown(
            dedent(f"""
            <div class="alerta">
                <b style="color:white;">
                ⚠ Atenção
                </b>
                <br><br>
                Existem
                <b>{criticos}</b>
                vendedores com penalidade superior a
                <b>R$ 5.000,00</b>.
            </div>
            """),
            unsafe_allow_html=True
        )

# ==========================================================
# RESUMO EXECUTIVO
# ==========================================================

def resumo_executivo(kpis):
    percentual = formatar_percentual(
        kpis["perc_penalidade"]
    )
    st.markdown(
        dedent(f"""
        <div class="card">
        <h3 style="margin-top:0;">
        📊 Resumo Executivo
        </h3>
        <hr>
        <p>
        • Total de Penalidades:
        <b>{formatar_moeda(kpis["total_penalidade"])}</b>
        </p>
        <p>
        • Total de Vendas:
        <b>{formatar_moeda(kpis["total_vendas"])}</b>
        </p>
        <p>
        • Impacto das Penalidades:
        <b>{percentual}</b>
        </p>
        <p>
        • RCAs com Penalidade:
        <b>{kpis["rcas_penalidade"]}</b>
        </p>
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# CABEÇALHO DE SEÇÃO
# ==========================================================

def cabecalho_secao(titulo, descricao=""):
    st.markdown(
        dedent(f"""
        <div style="margin-top:15px;margin-bottom:10px;">
            <h2 style="color:#00C2FF;margin-bottom:3px;">
            {titulo}
            </h2>
            <span style="color:#8FA4B7;">
            {descricao}
            </span>
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# LINHA DIVISÓRIA
# ==========================================================

def linha():
    st.markdown(
        "<hr style='margin-top:20px;margin-bottom:20px;'>",
        unsafe_allow_html=True
    )

# ==========================================================
# RODAPÉ
# ==========================================================

def rodape_dashboard():
    st.markdown(
        dedent("""
        <br><br>
        <hr>
        <div style="text-align:center;
                    color:#7E8A97;
                    font-size:13px;
                    padding-bottom:15px;">
            Dashboard Executivo de Penalidades • Distrinorte Distribuidora
            <br>
            Desenvolvido em Python • Streamlit • Plotly
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# DOWNLOAD EXCEL
# ==========================================================

def botao_download_excel(nome_arquivo, dados):
    st.download_button(
        label="📥 Exportar Excel",
        data=dados,
        file_name=nome_arquivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ==========================================================
# MENSAGEM DE SUCESSO
# ==========================================================

def sucesso(texto):
    st.success(texto)

# ==========================================================
# MENSAGEM DE ERRO
# ==========================================================

def erro(texto):
    st.error(texto)

# ==========================================================
# MENSAGEM DE AVISO
# ==========================================================

def aviso(texto):
    st.warning(texto)

# ==========================================================
# MENSAGEM INFO
# ==========================================================

def informacao(texto):
    st.info(texto)

# ==========================================================
# CABEÇALHO TABELAS
# ==========================================================

def titulo_tabela(texto):
    st.markdown(
        dedent(f"""
        <div style="
            margin-top:15px;
            margin-bottom:8px;
            font-size:20px;
            font-weight:600;
            color:#00C2FF;
        ">
            📋 {texto}
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# BLOCO OBSERVAÇÃO
# ==========================================================

def observacao(texto):
    st.markdown(
        dedent(f"""
        <div style="
            background:#111C2B;
            border-left:5px solid #FDBE2D;
            padding:15px;
            border-radius:10px;
            margin-top:10px;
            margin-bottom:10px;
            color:white;
        ">
            💡 {texto}
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# BADGE
# ==========================================================

def badge(texto, cor="#006B98"):
    st.markdown(
        dedent(f"""
        <span style="
            background:{cor};
            color:white;
            padding:6px 12px;
            border-radius:20px;
            font-size:13px;
            font-weight:600;
        ">
            {texto}
        </span>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# CARD DE INDICADOR SIMPLES
# ==========================================================

def indicador_simples(titulo, valor):
    st.markdown(
        dedent(f"""
        <div class="card">
            <div class="card-title">
                {titulo}
            </div>
            <div class="card-value">
                {valor}
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

# ==========================================================
# PLACEHOLDER PARA FUTURAS MELHORIAS
# ==========================================================

def em_desenvolvimento():
    st.markdown(
        dedent("""
        <div class="card">
            <h3 style="color:#FDBE2D;">
                🚧 Em desenvolvimento
            </h3>
            Este recurso estará disponível nas próximas versões.
        </div>
        """),
        unsafe_allow_html=True
    )