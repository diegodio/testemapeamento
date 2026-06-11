import streamlit as st
import os
import json
import base64

st.set_page_config(
    page_title="Mapeamento",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>

/* Remove espaços excessivos */
.block-container{
    padding-top:0.5rem;
    padding-bottom:0.5rem;
    max-width:100% !important;
}

/* Força 5 colunas */
[data-testid="stHorizontalBlock"]{
    display:flex !important;
    flex-wrap:nowrap !important;
    gap:0.15rem !important;
}

[data-testid="column"]{
    width:20% !important;
    min-width:20% !important;
    max-width:20% !important;
    flex:0 0 20% !important;
}

/* Imagens dos alunos */
.student-photo{
    width:100%;
    aspect-ratio:1/1;
    object-fit:cover;
    border-radius:8px;
    border:1px solid #ddd;
    display:block;
}

/* Desktop */
@media (min-width:769px){

    .student-photo{
        max-height:140px;
    }

    .student-name{
        font-size:11px;
    }

    .student-btn button{
        font-size:11px;
    }
}

/* Celular */
@media (max-width:768px){

    .block-container{
        padding-left:0.2rem !important;
        padding-right:0.2rem !important;
    }

    .student-photo{
        max-height:75px;
    }

    .student-name{
        font-size:8px;
        line-height:1.05;
    }

    .stButton > button{
        font-size:8px !important;
        min-height:22px !important;
        padding:0 !important;
    }
}

/* Botões */
.stButton > button{
    width:100%;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÕES
# =====================================================
def load_data(turno, turma):
    path = os.path.join("turmas", turno, turma)

    json_path = next(
        (
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.endswith(".json")
        ),
        None
    )

    name_map = {}

    if json_path:
        with open(json_path, "r", encoding="utf-8") as f:
            name_map = json.load(f)

    students = []

    for file in os.listdir(path):

        nome, ext = os.path.splitext(file)

        if ext.lower() in [".jpg", ".jpeg", ".png"] and nome.isdigit():

            with open(os.path.join(path, file), "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()

            students.append({
                "numero": nome,
                "nome": name_map.get(nome, "---"),
                "img": img_b64
            })

    return sorted(students, key=lambda x: int(x["numero"]))


# =====================================================
# SESSION STATE
# =====================================================
if "swap" not in st.session_state:
    st.session_state.swap = None

if "data" not in st.session_state:
    st.session_state.data = []

# =====================================================
# SIDEBAR
# =====================================================
turnos = []

if os.path.exists("turmas"):
    turnos = [
        d for d in os.listdir("turmas")
        if os.path.isdir(os.path.join("turmas", d))
    ]

turno = st.sidebar.selectbox("Turno", turnos)

if turno:

    turmas = [
        d for d in os.listdir(os.path.join("turmas", turno))
        if os.path.isdir(os.path.join("turmas", turno, d))
    ]

    turma = st.sidebar.selectbox("Turma", turmas)

    if st.sidebar.button("Carregar Turma"):

        st.session_state.data = load_data(turno, turma)
        st.session_state.swap = None
        st.rerun()

# =====================================================
# TELA PRINCIPAL
# =====================================================
if st.session_state.data:

    st.title(f"📍 {turma}")

    alunos = st.session_state.data

    for inicio in range(0, len(alunos), 5):

        cols = st.columns(5)

        linha = alunos[inicio:inicio+5]

        for idx_col, aluno in enumerate(linha):

            indice_real = inicio + idx_col

            with cols[idx_col]:

                st.markdown(
                    f"""
                    <img
                        src="data:image/png;base64,{aluno['img']}"
                        class="student-photo">
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="student-name"
                         style="
                         text-align:center;
                         margin-top:2px;
                         margin-bottom:4px;">
                        <b>{aluno['numero']}</b><br>
                        {aluno['nome']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                selecionado = (
                    st.session_state.swap == indice_real
                )

                texto = "✓" if selecionado else "↔"

                if st.button(
                    texto,
                    key=f"btn_{indice_real}"
                ):

                    if st.session_state.swap is None:

                        st.session_state.swap = indice_real

                    else:

                        a = st.session_state.swap
                        b = indice_real

                        (
                            st.session_state.data[a],
                            st.session_state.data[b]
                        ) = (
                            st.session_state.data[b],
                            st.session_state.data[a]
                        )

                        st.session_state.swap = None

                    st.rerun()

else:

    st.info(
        "Selecione um turno e uma turma na barra lateral para começar."
    )
