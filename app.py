import streamlit as st
import os
import json
import base64

st.set_page_config(page_title="Mapeamento", layout="wide", initial_sidebar_state="collapsed")

# CSS simplificado apenas para garantir o layout sem interferir na renderização principal
st.markdown('''
<style>
    /* Força as colunas do Streamlit a manterem a largura */
    [data-testid="column"] {
        width: 20% !important;
        flex: 1 1 20% !important;
        max-width: 20% !important;
    }
    .stButton>button {
        width: 100%;
        padding: 2px;
        font-size: 0.6rem;
    }
</style>
''', unsafe_allow_html=True)

# Funções
def load_data(turno, turma):
    path = os.path.join("turmas", turno, turma)
    json_path = next((os.path.join(path, f) for f in os.listdir(path) if f.endswith(".json")), None)
    name_map = json.load(open(json_path, 'r', encoding='utf-8')) if json_path else {}
    students = []
    for file in os.listdir(path):
        name, ext = os.path.splitext(file)
        if ext.lower() in ['.jpg', '.jpeg', '.png'] and name.isdigit():
            with open(os.path.join(path, file), "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            students.append({"numero": name, "nome": name_map.get(name, "---"), "img": img_b64})
    return sorted(students, key=lambda x: int(x['numero']))

# Estado
if 'swap' not in st.session_state: st.session_state.swap = None
if 'data' not in st.session_state: st.session_state.data = []

# Sidebar
turnos = [d for d in os.listdir("turmas") if os.path.isdir(os.path.join("turmas", d))] if os.path.exists("turmas") else []
turno = st.sidebar.selectbox("Turno", turnos)
if turno:
    turmas = [d for d in os.listdir(os.path.join("turmas", turno)) if os.path.isdir(os.path.join("turmas", turno, d))]
    turma = st.sidebar.selectbox("Turma", turmas)
    if st.sidebar.button("Carregar Turma"):
        st.session_state.data = load_data(turno, turma)
        st.session_state.swap = None
        st.rerun()

# Lógica de Troca
if st.session_state.data:
    st.title(f"📍 {turma}")
    
    # Criar grid de 5 colunas nativo do Streamlit
    cols = st.columns(5)
    
    for i, s in enumerate(st.session_state.data):
        with cols[i % 5]:
            is_sel = (st.session_state.swap == i)
            
            # Exibir imagem usando st.image (mais estável que HTML puro)
            st.image(f"data:image/png;base64,{s['img']}", use_container_width=True)
            st.caption(f"Nº {s['numero']} - {s['nome']}")
            
            # Botão de troca
            label = "Selecionado" if is_sel else "Trocar"
            if st.button(label, key=f"btn_{i}"):
                if st.session_state.swap is None:
                    st.session_state.swap = i
                    st.rerun()
                else:
                    a, b = st.session_state.swap, i
                    st.session_state.data[a], st.session_state.data[b] = st.session_state.data[b], st.session_state.data[a]
                    st.session_state.swap = None
                    st.rerun()
else:
    st.info("Selecione um turno e turma na barra lateral para começar.")
