import streamlit as st
import os
import json
import base64

st.set_page_config(
    page_title="Mapeamento",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* Remove margens */
.block-container{
    padding-top:0.3rem;
    padding-left:0.2rem;
    padding-right:0.2rem;
    max-width:100%;
}

/* força 5 colunas */
[data-testid="stHorizontalBlock"]{
    gap:2px !important;
}

[data-testid="column"]{
    padding:0 !important;
}

/* card */
.student-card{
    text-align:center;
    padding:0;
    margin:0;
}

.photo-container{
    position:relative;
}

.student-photo{
    width:100%;
    aspect-ratio:1/1;
    object-fit:cover;
    border-radius:4px;
    border:1px solid #ddd;
    display:block;
}

.student-number{
    position:absolute;
    top:1px;
    left:1px;

    background:rgba(0,0,0,0.75);
    color:white;

    font-size:7px;
    padding:0px 3px;
    border-radius:2px;
}

.student-name{
    font-size:7px;
    line-height:1;
    margin-top:1px;

    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

/* botão */
.stButton > button{
    width:100%;
    height:18px !important;
    min-height:18px !important;

    padding:0 !important;
    margin-top:1px !important;

    font-size:8px !important;
}

/* celular */
@media (max-width:768px){

    .student-photo{
        max-height:58px;
    }

    .student-name{
        font-size:6px;
    }

    .student-number{
        font-size:6px;
    }

    .stButton > button{
        height:16px !important;
        min-height:16px !important;
        font-size:7px !important;
    }
}

/* desktop */
@media (min-width:769px){

    .student-photo{
        max-height:120px;
    }

    .student-name{
        font-size:10px;
    }

    .student-number{
        font-size:9px;
    }
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
# SESSION
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
# GRID
# =====================================================

if st.session_state.data:

    st.title(f"📍 {turma}")

    alunos = st.session_state.data

    for inicio in range(0, len(alunos), 5):

        linha = alunos[inicio:inicio+5]

        cols = st.columns(5)

        for idx_col, aluno in enumerate(linha):

            indice_real = inicio + idx_col

            with cols[idx_col]:

                st.markdown(
                    f"""
                    <div class="student-card">

                        <div class="photo-container">

                            <img
                                src="data:image/png;base64,{aluno['img']}"
                                class="student-photo">

                            <div class="student-number">
                                {aluno['numero']}
                            </div>

                        </div>

                        <div class="student-name">
                            {aluno['nome']}
                        </div>

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

                        st.session_state.data[a], st.session_state.data[b] = (
                            st.session_state.data[b],
                            st.session_state.data[a]
                        )

                        st.session_state.swap = None

                    st.rerun()

else:

    st.info(
        "Selecione um turno e uma turma na barra lateral."
    )
