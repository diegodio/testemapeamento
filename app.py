"""Mapa de Sala — sistema de mapeamento de salas de aula.

Execução:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st

from components.layout_sala import render_sala
from components.sidebar import render_sidebar
from components.styles import aplicar_estilos
from services.arquivos import carregar_alunos
from services.mapeamento import carregar_ou_gerar, gerar_mapeamento_inicial
from services.persistencia import salvar_mapeamento
from utils.constantes import ROTULOS_TURNOS

st.set_page_config(
    page_title="Mapa da Sala",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilos()

turno, turma = render_sidebar()

if turno is None or turma is None:
    st.markdown(
        """
        <div class="faixa-titulo">
            <div class="brasao">🏫</div>
            <div>
                <p class="titulo-app">Mapa da <span class="destaque">Sala</span></p>
                <p class="subtitulo-app">Crie a estrutura de pastas em
                <code>dados/&lt;turno&gt;/&lt;turma&gt;/alunos.json</code> para começar.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

alunos = carregar_alunos(turno, turma)
if not alunos:
    st.error(f"O arquivo `alunos.json` da turma {turma} está vazio ou inválido.")
    st.stop()

# Índice inverso nome -> número da chamada (para foto e exibição do Nº)
numero_por_nome = {nome: numero for numero, nome in alunos.items()}

# Recarrega o estado quando o usuário muda de turno/turma
contexto = (turno, turma)
if st.session_state.get("contexto") != contexto:
    st.session_state["contexto"] = contexto
    st.session_state["mapa"] = carregar_ou_gerar(turno, turma, alunos)
    st.session_state["selecionado"] = None

# Ação da sidebar: refazer a distribuição automática
if st.session_state.pop("redistribuir", False):
    st.session_state["mapa"] = gerar_mapeamento_inicial(alunos)
    salvar_mapeamento(turno, turma, st.session_state["mapa"])
    st.session_state["selecionado"] = None
    st.toast("Distribuição automática refeita e salva.", icon="↺")

# Feedback da última troca (definida no callback dos botões)
ultima_troca = st.session_state.pop("ultima_troca", None)
if ultima_troca:
    st.toast(f"{ultima_troca[0]} ⇄ {ultima_troca[1]} — troca salva!", icon="✅")

# ---------- Cabeçalho ----------
rotulo_turno = ROTULOS_TURNOS.get(turno, turno.capitalize())
st.markdown(
    f"""
    <div class="faixa-titulo">
        <div class="brasao">🏫</div>
        <div>
            <p class="titulo-app">Turma <span class="destaque">{turma}</span> · {rotulo_turno}</p>
            <p class="subtitulo-app">{len(alunos)} alunos · toque em dois cards para trocar de lugar</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

selecionado = st.session_state.get("selecionado")
if selecionado is not None:
    nome_sel = st.session_state["mapa"].get(selecionado, "")
    st.markdown(
        f'<div class="chip-status">⇄ Trocando: <strong>{nome_sel}</strong>'
        " — escolha a outra carteira</div>",
        unsafe_allow_html=True,
    )

# ---------- Sala ----------
render_sala(turno, turma, numero_por_nome)
