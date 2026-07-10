import streamlit as st


def carregar_css():

    st.markdown("""
<style>

/* ===========================================================
   TEMA GERAL
=========================================================== */

.stApp{
    background:#05070D;
    color:white;
}


/* ===========================================================
   CABEÇALHO
=========================================================== */

h1{
    color:white;
    font-weight:700;
    letter-spacing:.5px;
}

h2{
    color:white;
    font-weight:600;
}

h3{
    color:#00C2FF;
}


/* ===========================================================
   SIDEBAR
=========================================================== */

section[data-testid="stSidebar"]{

    background:#0B1220;

    border-right:1px solid #13304A;

}

section[data-testid="stSidebar"] *{

    color:white;

}


/* ===========================================================
   CARDS
=========================================================== */

.card{

    background:#101826;

    border-radius:18px;

    padding:20px;

    border:1px solid #143A56;

    box-shadow:0 0 15px rgba(0,194,255,.08);

    transition:.25s;

    margin-bottom:12px;

}

.card:hover{

    transform:translateY(-2px);

    box-shadow:0 0 18px rgba(0,194,255,.25);

}


/* ===========================================================
   CARD PENALIDADE
=========================================================== */

.card-danger{

    border-left:6px solid #FF4D6D;

}

.card-primary{

    border-left:6px solid #00C2FF;

}

.card-warning{

    border-left:6px solid #FDBE2D;

}

.card-success{

    border-left:6px solid #00D27A;

}


/* ===========================================================
   TITULOS DOS CARDS
=========================================================== */

.card-title{

    color:#A7B7C7;

    font-size:13px;

    font-weight:600;

    text-transform:uppercase;

    margin-bottom:10px;

}


.card-value{

    font-size:40px;

    color:white;

    font-weight:bold;

    margin-bottom:8px;

}


.card-footer{

    color:#8A97A5;

    font-size:13px;

}


/* ===========================================================
   TABS
=========================================================== */

.stTabs [role="tab"]{

    background:#101826;

    color:white;

    border-radius:12px;

    margin-right:8px;

    border:1px solid #183B57;

    padding:10px 18px;

}

.stTabs [aria-selected="true"]{

    background:#006B98 !important;

    color:white !important;

}


/* ===========================================================
   BOTÕES
=========================================================== */

.stButton>button{

    background:#006B98;

    color:white;

    border:none;

    border-radius:10px;

    transition:.2s;

}

.stButton>button:hover{

    background:#00C2FF;

}


/* ===========================================================
   DATAFRAME
=========================================================== */

div[data-testid="stDataFrame"]{

    border:1px solid #16374F;

    border-radius:15px;

}


/* ===========================================================
   METRIC
=========================================================== */

div[data-testid="metric-container"]{

    background:#101826;

    border-radius:15px;

    border:1px solid #143A56;

    padding:12px;

}


/* ===========================================================
   EXPANDER
=========================================================== */

.streamlit-expanderHeader{

    font-weight:600;

    color:#00C2FF;

}


/* ===========================================================
   SCROLLBAR
=========================================================== */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#006B98;

    border-radius:20px;

}


/* ===========================================================
   LINKS
=========================================================== */

a{

    color:#00C2FF;

}


/* ===========================================================
   DIVISORES
=========================================================== */

hr{

    border-color:#183B57;

}


/* ===========================================================
   ALERTAS
=========================================================== */

.alerta{

    background:#1C1218;

    border-left:6px solid #FF4D6D;

    padding:15px;

    border-radius:12px;

}


/* ===========================================================
   QUADRO DE MOTIVOS
=========================================================== */

.motivos{

    background:#0E1625;

    border:1px solid #1D3C58;

    border-radius:16px;

    padding:20px;

}

.motivos h4{

    color:#FDBE2D;

}

.motivos-grid{

    display:grid;

    grid-template-columns:repeat(2,1fr);

    gap:8px;

}

.motivo{

    padding:10px;

    background:#121F30;

    border-radius:10px;

}


/* ===========================================================
   RESPONSIVO
=========================================================== */

@media(max-width:900px){

.motivos-grid{

grid-template-columns:1fr;

}

.card-value{

font-size:28px;

}

}

</style>
""", unsafe_allow_html=True)