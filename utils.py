"""
==========================================================
UTILS.PY
Funções auxiliares do Dashboard de Penalidades
Autor: Paulo Gusmão + ChatGPT
==========================================================
"""

import pandas as pd
from io import BytesIO
import re


# ==========================================================
# FORMATAÇÃO
# ==========================================================

def formatar_moeda(valor):
    """
    Converte número para formato brasileiro.

    Ex:
    12580.5
    ->
    R$ 12.580,50
    """

    try:
        valor = float(valor)
    except:
        valor = 0

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_percentual(valor, casas=2):
    """
    Ex:
    0.1532

    ->

    15,32%
    """

    try:
        valor = float(valor)
    except:
        valor = 0

    return (
        f"{valor:.{casas}%}"
        .replace(".", ",")
    )


# ==========================================================
# NOMES DOS RCAs
# ==========================================================

def nome_curto_rca(nome):
    """
    Transforma:

    3035-LUCAS (3 MARIAS) PASTA LARANJA

    em

    3035 - LUCAS
    """

    if pd.isna(nome):
        return ""

    nome = str(nome).strip()

    if nome == "":
        return ""

    codigo = ""
    restante = nome

    if "-" in nome:
        codigo, restante = nome.split("-", 1)

    codigo = codigo.strip()

    restante = restante.strip()

    # remove tudo após (
    restante = restante.split("(")[0]

    # remove códigos comuns
    restante = (
        restante
        .replace("(OFF)", "")
        .replace("(FER)", "")
        .replace("(AUX)", "")
        .strip()
    )

    restante = re.sub(r"\s+", " ", restante)

    primeiro_nome = restante.split(" ")[0].upper()

    if codigo != "":
        return f"{codigo} - {primeiro_nome}"

    return primeiro_nome


def abreviar_texto(texto, limite=40):

    if pd.isna(texto):
        return ""

    texto = str(texto)

    if len(texto) <= limite:
        return texto

    return texto[:limite] + "..."


# ==========================================================
# INDICADORES
# ==========================================================

def calcular_percentual(parte, total):

    try:
        parte = float(parte)
        total = float(total)

        if total == 0:
            return 0

        return parte / total

    except:
        return 0


def calcular_desvio(realizado, meta):

    try:
        return float(realizado) - float(meta)

    except:
        return 0


# ==========================================================
# EXPORTAÇÃO
# ==========================================================

def dataframe_para_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Dashboard"
        )

    output.seek(0)

    return output.getvalue()


# ==========================================================
# CORES
# ==========================================================

def classificar_penalidade(valor):
    """
    Classificação visual.

    Até 500 = Azul

    500 a 2.000 = Amarelo

    Acima de 2.000 = Vermelho
    """

    valor = abs(valor)

    if valor <= 500:
        return "BAIXA"

    elif valor <= 2000:
        return "MEDIA"

    else:
        return "ALTA"


def cor_penalidade(valor):

    nivel = classificar_penalidade(valor)

    if nivel == "BAIXA":
        return "#00C2FF"

    elif nivel == "MEDIA":
        return "#FDBE2D"

    return "#FF4D6D"


# ==========================================================
# DASHBOARD
# ==========================================================

def total_rcas(df):

    return df["VENDEDOR"].nunique()


def total_supervisores(df):

    return df["SUPERVISOR"].nunique()


def total_penalidades(df):

    return abs(df["DEV. C/ PENALIDADE"].sum())


def total_vendas(df):

    return df["VENDAS"].sum()


def percentual_penalidade(df):

    vendas = total_vendas(df)

    if vendas == 0:
        return 0

    return total_penalidades(df) / vendas


# ==========================================================
# TOP N
# ==========================================================

def top_penalidades(df, quantidade=20):

    return (
        df.sort_values(
            "PENALIDADE_VALOR",
            ascending=False
        )
        .head(quantidade)
    )


def top_percentual_penalidade(df, quantidade=20):

    return (
        df.sort_values(
            "% PENALIDADE SOBRE VENDA",
            ascending=False
        )
        .head(quantidade)
    )


# ==========================================================
# DATAFRAME
# ==========================================================

def copiar_dataframe(df):
    """
    Evita alterar a base principal.
    """
    return df.copy()