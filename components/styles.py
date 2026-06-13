"""CSS customizado — identidade visual escura com destaques dourados."""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --azul-escuro: #0B1F3A;
    --azul-medio: #1D4E89;
    --azul-claro: #4F86C6;
    --dourado: #D4A017;
    --cinza-escuro: #1E1E1E;
    --cinza-medio: #444444;
    --cinza-claro: #D9D9D9;
    --superficie: #122A4E;
    --superficie-alta: #16335C;
    --texto: #EDF2F9;
    --texto-suave: #9FB3CE;
    --raio: 14px;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

/* ---------- Fundo geral ---------- */
.stApp {
    background:
        radial-gradient(1100px 500px at 85% -10%, rgba(79,134,198,.16), transparent 60%),
        radial-gradient(900px 420px at -10% 110%, rgba(29,78,137,.25), transparent 55%),
        var(--azul-escuro);
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer { visibility: hidden; }

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2.5rem;
    max-width: 1180px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D2444 0%, #0B1F3A 100%);
    border-right: 1px solid rgba(79,134,198,.18);
}
section[data-testid="stSidebar"] * { color: var(--texto); }
section[data-testid="stSidebar"] label {
    color: var(--texto-suave) !important;
    font-size: .78rem !important;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
}

div[data-baseweb="select"] > div {
    background: var(--superficie) !important;
    border: 1px solid rgba(79,134,198,.35) !important;
    border-radius: 10px !important;
    color: var(--texto) !important;
}
div[data-baseweb="popover"] li { background: var(--superficie); }

/* ---------- Cabeçalho da página ---------- */
.titulo-app {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: clamp(1.4rem, 3.2vw, 2rem);
    color: var(--texto);
    line-height: 1.15;
    margin: 0;
}
.titulo-app .destaque { color: var(--dourado); }

.subtitulo-app {
    color: var(--texto-suave);
    font-size: .9rem;
    margin: .25rem 0 0;
}

.faixa-titulo {
    display: flex;
    align-items: center;
    gap: .9rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(79,134,198,.18);
    margin-bottom: 1.1rem;
}
.faixa-titulo .brasao {
    width: 46px; height: 46px;
    border-radius: 12px;
    display: grid; place-items: center;
    font-size: 1.4rem;
    background: linear-gradient(150deg, var(--azul-medio), var(--azul-escuro));
    border: 1px solid rgba(212,160,23,.55);
    box-shadow: 0 6px 18px rgba(0,0,0,.35);
}

.chip-status {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: rgba(212,160,23,.12);
    border: 1px solid rgba(212,160,23,.5);
    color: var(--dourado);
    border-radius: 999px;
    padding: .3rem .8rem;
    font-size: .78rem;
    font-weight: 600;
    margin-bottom: .9rem;
}

/* ---------- Cards de aluno ---------- */
.card-aluno {
    background: linear-gradient(165deg, var(--superficie-alta) 0%, var(--superficie) 100%);
    border: 1px solid rgba(79,134,198,.28);
    border-radius: var(--raio);
    padding: .8rem .45rem .55rem;
    text-align: center;
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    min-height: 148px;
}
.card-aluno:hover {
    transform: translateY(-3px);
    border-color: var(--azul-claro);
    box-shadow: 0 12px 26px rgba(0,0,0,.38);
}
.card-aluno.selecionado {
    border: 2px solid var(--dourado);
    box-shadow: 0 0 0 4px rgba(212,160,23,.22), 0 14px 30px rgba(0,0,0,.5);
    transform: translateY(-3px);
}

.card-foto img {
    width: 68px; height: 68px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--azul-claro);
    box-shadow: 0 4px 12px rgba(0,0,0,.35);
}
.card-aluno.selecionado .card-foto img { border-color: var(--dourado); }

.card-nome {
    color: var(--texto);
    font-weight: 600;
    font-size: .84rem;
    line-height: 1.2;
    margin-top: .5rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
.card-num {
    color: var(--dourado);
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .08em;
    margin-top: .15rem;
}

/* Carteira vazia */
.carteira-vazia {
    border: 1.5px dashed rgba(159,179,206,.35);
    border-radius: var(--raio);
    min-height: 148px;
    display: grid;
    place-items: center;
    color: rgba(159,179,206,.5);
    font-size: .75rem;
    font-weight: 500;
}

/* ---------- Botões dos cards ---------- */
div[data-testid="stButton"] > button {
    width: 100%;
    background: rgba(79,134,198,.14);
    color: var(--texto-suave);
    border: 1px solid rgba(79,134,198,.35);
    border-radius: 10px;
    font-size: .76rem;
    font-weight: 600;
    padding: .3rem .4rem;
    margin-top: .35rem;
    transition: all .15s ease;
}
div[data-testid="stButton"] > button:hover {
    background: rgba(212,160,23,.16);
    color: var(--dourado);
    border-color: var(--dourado);
}
div[data-testid="stButton"] > button:focus:not(:active) {
    border-color: var(--dourado);
    color: var(--dourado);
    box-shadow: 0 0 0 3px rgba(212,160,23,.25);
}

/* ---------- Mesa do professor e porta ---------- */
.mesa-professor {
    margin: 1.6rem auto .9rem;
    max-width: 460px;
    background: linear-gradient(150deg, var(--azul-medio), #173E6E);
    border: 1px solid rgba(212,160,23,.6);
    border-radius: var(--raio);
    color: var(--texto);
    text-align: center;
    padding: .95rem 1rem;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    letter-spacing: .14em;
    font-size: .86rem;
    box-shadow: 0 10px 26px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.08);
}
.mesa-professor .selo { color: var(--dourado); margin-right: .45rem; }

.porta-sala {
    margin: 0 auto;
    width: max-content;
    color: var(--texto-suave);
    border: 1px solid rgba(159,179,206,.3);
    border-radius: 999px;
    padding: .42rem 1.2rem;
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .12em;
    background: rgba(18,42,78,.6);
}

/* Rótulo de fila */
.rotulo-fila {
    color: rgba(159,179,206,.55);
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin: .2rem 0 .35rem;
}

/* ---------- Animações ---------- */
@keyframes surgir {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card-aluno, .carteira-vazia, .mesa-professor, .porta-sala {
    animation: surgir .35s ease both;
}
@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}

/* ---------- Responsividade ---------- */
/* Tablet */
@media (max-width: 1024px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .card-foto img { width: 58px; height: 58px; }
    .card-aluno { min-height: 136px; }
    .carteira-vazia { min-height: 136px; }
}

/* Celular: mantém a grade da sala, com cards compactos e sem rolagem horizontal */
@media (max-width: 640px) {
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: .35rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }
    .card-aluno { padding: .5rem .25rem .4rem; min-height: 116px; border-radius: 11px; }
    .carteira-vazia { min-height: 116px; border-radius: 11px; }
    .card-foto img { width: 42px; height: 42px; }
    .card-nome { font-size: .66rem; }
    .card-num { font-size: .58rem; }
    div[data-testid="stButton"] > button { font-size: .62rem; padding: .22rem .2rem; }
    .mesa-professor { font-size: .72rem; padding: .75rem .6rem; letter-spacing: .1em; }
}
</style>
"""


def aplicar_estilos() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
