"""Renderização da sala: grade de carteiras, mesa do professor e porta.
Orientação: cada fila é uma coluna de carteiras. A posição 1 é a carteira
da frente (mais próxima da mesa do professor, exibida abaixo do mapeamento);
portanto a primeira linha da tela corresponde às últimas carteiras de cada fila.
"""
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
    """Callback do botão de seleção: seleciona, desseleciona ou troca + salva."""
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

    # Da última carteira (fundo da sala, topo da tela) até a primeira (frente)
    for posicao_na_fila in range(max_posicao, 0, -1):
        colunas = st.columns(len(filas), gap="small")
        for indice, fila in enumerate(filas):
            pos = (fila, posicao_na_fila)
            with colunas[indice]:
                if pos not in mapa:
                    st.markdown(html_carteira_vazia(), unsafe_allow_html=True)
                    continue

                nome = mapa[pos]
                numero = numero_por_nome.get(nome)
                foto = foto_data_uri(pasta, nome)  # busca por nome, não por número
                esta_selecionado = selecionado == pos

                st.markdown(
                    html_card_aluno(nome, numero, foto, esta_selecionado),
                    unsafe_allow_html=True,
                )
                st.button(
                    "⇄",
                    key=f"sel_{fila}_{posicao_na_fila}",
                    on_click=_ao_clicar,
                    args=(pos, turno, turma),
                )

    st.markdown(html_mesa_professor(), unsafe_allow_html=True)
    st.markdown(html_porta(), unsafe_allow_html=True)
