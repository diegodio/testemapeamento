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
# CSS - FORÇA 5 COLUNAS MESMO NO CELULAR
# =====================================================
st.markdown("""
<style>

/* Container principal */
.block-container{
    padding-top:0.5rem;
    padding-bottom:0.5rem;
}

/* Força as linhas de colunas */
[data-testid="stHorizontalBlock"]{
    display:flex !important;
    flex-wrap:nowrap !important;
    gap:0.2rem !important;
}

/* Força cada coluna a ocupar exatamente 20% */
[data-testid="column"]{
    min-width:20% !important;
    width:20% !important;
    flex:0 0 20% !important;
    max-width:20% !important;
}

/* Imagens */
[data-testid="stImage"] img{
    width:100% !important;
    height:auto !important;
}

/* Botões */
.stButton > button{
    width:100%;
    padding:2px;
    font-size:0.55rem;
    min-height:28px;
}

/* Mobile */
@media (max-width:768px){

    .block-container{
        padding-left:0.2rem !important;
        padding-right:0.2rem !important;
        max-width:100% !important;
    }

    [data-testid="column"]{
        min-width:20% !important;
        width:20% !important;
        flex:0 0 20% !important;
        max-width:20% !important;
    }

    .stButton > button{
        font-size:0.45rem !important;
        padding:1px !important;
        min-height:24px !important;
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

    name_map = (
        json.load(open(json_path, "r", encoding="utf-8"))
        if json_path
        else {}
    )

    students = []

    for file in os.listdir(path):
        name, ext = os.path.splitext(file)

        if ext.lower() in [".jpg", ".jpeg", ".png"] and name.isdigit():

            with open(os.path.join(path, file), "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()

            students.append(
                {
                    "numero": name,
                    "nome": name_map.get(name, "---"),
                    "img": img_b64
                }
            )

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
# INTERFACE
# =====================================================
if st.session_state.data:

    st.title(f"📍 {turma}")

    alunos = st.session_state.data

    for inicio in range(0, len(alunos), 5):

        linha = alunos[inicio:inicio + 5]

        cols = st.columns(5)

        for idx_col, aluno in enumerate(linha):

            indice_real = inicio + idx_col

            with cols[idx_col]:

                st.image(
                    f"data:image/png;base64,{aluno['img']}",
                    use_container_width=True
                )

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        font-size:10px;
                        line-height:1.1;
                        margin-top:2px;
                        margin-bottom:4px;
                    ">
                        <b>{aluno['numero']}</b><br>
                        {aluno['nome']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                selecionado = (
                    st.session_state.swap == indice_real
                )

                texto_botao = "✓" if selecionado else "↔"

                if st.button(
                    texto_botao,
                    key=f"btn_{indice_real}"
                ):

                    if st.session_state.swap is None:

                        st.session_state.swap = indice_real
                        st.rerun()

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
        "Selecione um turno e uma turma na barra lateral para começar."
    )
