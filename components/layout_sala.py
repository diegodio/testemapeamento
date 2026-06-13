"""Renderização da sala: grade de carteiras, mesa do professor e porta."""

import streamlit as st

from components.cards import (
    html_card_aluno,
    html_carteira_vazia,
    html_mesa_professor,
    html_porta,
)
from services.imagens import foto_data_uri
from services.mapeamento import Posicao, dimensoes, trocar_alunos
from services.persistencia import salvar_mapeamento
from utils import paths


def _ao_clicar(pos: Posicao, turno: str, turma: str) -> None:
    """Callback dos botões: seleciona, desseleciona ou troca + salva."""
    selecionado: Posicao | None = st.session_state.get("selecionado")
    mapa = st.session_state["mapa"]

    if selecionado is None:
        st.session_state["selecionado"] = pos
    elif selecionado == pos:
        st.session_state["selecionado"] = None
    else:
        trocar_alunos(mapa, selecionado, pos)
        salvar_mapeamento(turno, turma, mapa)
        st.session_state["selecionado"] = None
        st.session_state["ultima_troca"] = (mapa[selecionado], mapa[pos])


def render_sala(turno: str, turma: str, numero_por_nome: dict[str, str]) -> None:
    """Desenha a grade de carteiras com interação de troca."""
    mapa = st.session_state["mapa"]
    selecionado: Posicao | None = st.session_state.get("selecionado")
    pasta = paths.pasta_turma(turno, turma)

    filas, max_posicao = dimensoes(mapa)
    if not filas:
        st.info("Nenhum aluno mapeado nesta turma.")
        return

    for fila in filas:
        st.markdown(
            f'<div class="rotulo-fila">Fila {fila}</div>',
            unsafe_allow_html=True,
        )
        colunas = st.columns(max_posicao, gap="small")
        for indice in range(1, max_posicao + 1):
            pos = (fila, indice)
            with colunas[indice - 1]:
                if pos not in mapa:
                    st.markdown(html_carteira_vazia(), unsafe_allow_html=True)
                    continue

                nome = mapa[pos]
                numero = numero_por_nome.get(nome)
                foto = foto_data_uri(pasta, numero)
                esta_selecionado = selecionado == pos

                st.markdown(
                    html_card_aluno(nome, numero, foto, esta_selecionado),
                    unsafe_allow_html=True,
                )
                rotulo = "✕ Cancelar" if esta_selecionado else (
                    "⇄ Trocar" if selecionado is not None else "Selecionar"
                )
                st.button(
                    rotulo,
                    key=f"sel_{fila}_{indice}",
                    on_click=_ao_clicar,
                    args=(pos, turno, turma),
                    use_container_width=True,
                )

    st.markdown(html_mesa_professor(), unsafe_allow_html=True)
    st.markdown(html_porta(), unsafe_allow_html=True)
