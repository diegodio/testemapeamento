import streamlit as st
import os
import json
import base64

st.set_page_config(page_title="Mapeamento", layout="wide", initial_sidebar_state="collapsed")

# CSS para Grid Fixo (Não depende do Streamlit)
st.markdown('''
<style>
    /* Força o grid de 5 colunas em qualquer dispositivo */
    .grid-container {
        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        gap: 5px !important;
        width: 100% !important;
    }
    .card {
        border: 1px solid #ddd;
        border-radius: 5px;
        text-align: center;
        padding: 2px;
        background: white;
    }
    .card.selected { border: 2px solid #ff4b4b; background: #fff0f0; }
    .img-box { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 3px; }
    .txt-n { font-size: 0.6rem; font-weight: bold; color: #ff4b4b; }
    .txt-name { font-size: 0.6rem; white-space: nowrap; overflow: hidden; }
</style>
''', unsafe_allow_html=True)

# Funções
def get_folders(path):
    if not os.path.exists(path): return []
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

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
            students.append({"id": i, "numero": name, "nome": name_map.get(name, "---"), "img": img_b64})
    return sorted(students, key=lambda x: int(x['numero']))

# Estado
if 'swap' not in st.session_state: st.session_state.swap = None
if 'data' not in st.session_state: st.session_state.data = []

# Sidebar
turno = st.sidebar.selectbox("Turno", get_folders("turmas"))
if turno:
    turma = st.sidebar.selectbox("Turma", get_folders(os.path.join("turmas", turno)))
    if st.sidebar.button("Carregar"):
        st.session_state.data = load_data(turno, turma)
        st.rerun()

# Lógica de Troca
def process_swap(idx):
    if st.session_state.swap is None: st.session_state.swap = idx
    else:
        a, b = st.session_state.swap, idx
        st.session_state.data[a], st.session_state.data[b] = st.session_state.data[b], st.session_state.data[a]
        st.session_state.swap = None
        st.rerun()

# Renderização do Grid Manual
if st.session_state.data:
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    for i, s in enumerate(st.session_state.data):
        # Renderizamos os cards dentro da div grid-container
        sel = (st.session_state.swap == i)
        st.markdown(f'''
            <div class="card {'selected' if sel else ''}">
                <img src="data:image/png;base64,{s['img']}" class="img-box">
                <div class="txt-n">Nº {s['numero']}</div>
                <div class="txt-name">{s['nome']}</div>
            </div>
        ''', unsafe_allow_html=True)
        # O botão fica fora da div para garantir o funcionamento do Streamlit
        st.button("T" if not sel else "OK", key=f"btn_{i}", on_click=process_swap, args=(i,))
    st.markdown('</div>', unsafe_allow_html=True)
