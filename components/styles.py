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
.faixa-titulo {
    display: flex;
    align-items: center;
    gap: 1.1rem;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1.2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(29,78,137,.55) 0%, rgba(11,31,58,.35) 70%);
    border: 1px solid rgba(79,134,198,.35);
    border-bottom: 2px solid rgba(212,160,23,.65);
    box-shadow: 0 14px 34px rgba(0,0,0,.35);
}
.faixa-titulo .brasao {
    width: 62px; height: 62px;
    flex-shrink: 0;
    border-radius: 16px;
    display: grid; place-items: center;
    font-size: 1.9rem;
    background: linear-gradient(150deg, var(--azul-medio), var(--azul-escuro));
    border: 1px solid rgba(212,160,23,.6);
    box-shadow: 0 8px 20px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.1);
}

.titulo-app {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: clamp(1.7rem, 4.2vw, 2.4rem);
    color: var(--texto);
    line-height: 1.1;
    margin: 0;
    letter-spacing: -.01em;
}
.titulo-app .destaque {
    color: var(--dourado);
    text-shadow: 0 0 26px rgba(212,160,23,.35);
}

.linha-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: .6rem;
    margin-top: .45rem;
}
.pill-turno {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    background: rgba(212,160,23,.14);
    border: 1px solid rgba(212,160,23,.6);
    color: var(--dourado);
    border-radius: 999px;
    padding: .26rem .85rem;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
}
.meta-info {
    color: var(--texto-suave);
    font-size: .85rem;
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
    position: relative;
    background: linear-gradient(165deg, var(--superficie-alta) 0%, var(--superficie) 100%);
    border: 1px solid rgba(79,134,198,.28);
    border-radius: var(--raio);
    padding: .45rem .45rem .55rem;
    text-align: center;
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
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
    width: 100%;
    aspect-ratio: 1 / 1;
    border-radius: 10px;
    object-fit: cover;
    border: 1px solid rgba(79,134,198,.45);
    box-shadow: 0 4px 12px rgba(0,0,0,.35);
    display: block;
}
.card-aluno.selecionado .card-foto img { border-color: var(--dourado); }

.card-num-badge {
    position: absolute;
    top: .8rem; left: .8rem;
    z-index: 5;
    background: rgba(11,31,58,.82);
    backdrop-filter: blur(3px);
    color: var(--dourado);
    font-size: .68rem;
    font-weight: 700;
    padding: .1rem .42rem;
    border-radius: 8px;
    border: 1px solid rgba(212,160,23,.55);
    line-height: 1.3;
}

.card-nome {
    color: var(--texto);
    font-weight: 600;
    font-size: .82rem;
    line-height: 1.2;
    margin-top: .45rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

/* Carteira vazia */
.carteira-vazia {
    border: 1.5px dashed rgba(159,179,206,.35);
    border-radius: var(--raio);
    aspect-ratio: 4 / 5;
    display: grid;
    place-items: center;
    color: rgba(159,179,206,.5);
    font-size: .75rem;
    font-weight: 500;
}

/* ---------- Botão de seleção no canto do card ---------- */
div[data-testid="stColumn"] { position: relative; }

div[data-testid="stColumn"] div[data-testid="stElementContainer"]:has(> div.stButton) {
    position: absolute;
    top: .85rem; right: .85rem;
    width: auto !important;
    z-index: 10;
    margin: 0;
}
div[data-testid="stColumn"] div.stButton > button {
    width: 32px; height: 32px;
    min-height: 32px;
    padding: 0;
    border-radius: 50%;
    font-size: .85rem;
    line-height: 1;
    background: rgba(11,31,58,.82);
    backdrop-filter: blur(3px);
    color: var(--cinza-claro);
    border: 1px solid rgba(79,134,198,.55);
    box-shadow: 0 4px 10px rgba(0,0,0,.4);
    transition: all .15s ease;
}
div[data-testid="stColumn"] div.stButton > button:hover {
    background: rgba(212,160,23,.2);
    color: var(--dourado);
    border-color: var(--dourado);
    transform: scale(1.08);
}
div[data-testid="stColumn"] div.stButton > button:focus:not(:active) {
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

/* ---------- Animações ---------- */
@keyframes surgir {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card-aluno, .carteira-vazia, .mesa-professor, .porta-sala, .faixa-titulo {
    animation: surgir .35s ease both;
}
@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}

/* ---------- Responsividade ---------- */
/* Tablet */
@media (max-width: 1024px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
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
    .faixa-titulo { padding: .8rem .9rem; gap: .7rem; }
    .faixa-titulo .brasao { width: 46px; height: 46px; font-size: 1.4rem; border-radius: 12px; }
    .linha-meta { margin-top: .3rem; gap: .4rem; }
    .pill-turno { font-size: .64rem; padding: .2rem .6rem; }
    .meta-info { font-size: .7rem; }

    .card-aluno { padding: .3rem .3rem .4rem; border-radius: 11px; }
    .card-foto img { border-radius: 8px; }
    .card-nome { font-size: .62rem; margin-top: .3rem; }
    .card-num-badge { top: .55rem; left: .55rem; font-size: .56rem; padding: .06rem .3rem; }
    .carteira-vazia { border-radius: 11px; font-size: .6rem; }

    div[data-testid="stColumn"] div[data-testid="stElementContainer"]:has(> div.stButton) {
        top: .55rem; right: .55rem;
    }
    div[data-testid="stColumn"] div.stButton > button {
        width: 24px; height: 24px; min-height: 24px; font-size: .66rem;
    }

    .mesa-professor { font-size: .72rem; padding: .75rem .6rem; letter-spacing: .1em; }
}
</style>
"""


def aplicar_estilos() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
