"""Sidebar: seleção de turno e turma."""

import streamlit as st

from services import arquivos
from utils.constantes import ROTULOS_TURNOS


def render_sidebar() -> tuple[str | None, str | None]:
    """Desenha a sidebar e retorna (turno, turma) selecionados, ou (None, None)."""
    with st.sidebar:
        st.markdown(
            """
            <div style="padding:.2rem 0 1rem;">
                <div style="font-family:'Sora',sans-serif;font-weight:800;
                            font-size:1.05rem;color:#EDF2F9;">
                    🏫 Mapa da Sala
                </div>
                <div style="color:#9FB3CE;font-size:.78rem;margin-top:.15rem;">
                    Escolas Cívico-Militares · PR
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        turnos = arquivos.listar_turnos()
        if not turnos:
            st.warning("Nenhum turno encontrado na pasta `dados/`.")
            return None, None

        turno = st.selectbox(
            "Turno",
            options=turnos,
            format_func=lambda t: ROTULOS_TURNOS.get(t, t.capitalize()),
            key="sel_turno",
        )

        turmas = arquivos.listar_turmas(turno)
        if not turmas:
            st.warning("Nenhuma turma com `alunos.json` neste turno.")
            return turno, None

        turma = st.selectbox("Turma", options=turmas, key="sel_turma")

        st.divider()
        st.caption(
            "Toque no card de um aluno e depois no de outro "
            "para trocá-los de lugar. A troca é salva automaticamente."
        )

    return turno, turma
