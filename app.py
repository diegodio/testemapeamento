import streamlit as st
import os
import json
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Mapeamento Interativo", layout="wide", initial_sidebar_state="collapsed")

# CSS FORÇANDO O GRID DE 5 COLUNAS
st.markdown('''
<style>
/* Força o container do Streamlit a aceitar nosso grid */
[data-testid="column"] {
    width: 20% !important;
    flex: 1 1 20% !important;
    max-width: 20% !important;
}
.classroom-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 30px; }
.student-card { background: #ffffff; border: 2px solid #e0e0e0; border-radius: 10px; padding: 5px; text-align: center; }
.student-card.selected { border-color: #ff4b4b; background-color: #fff0f0; }
.student-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 5px; }
.student-number { font-weight: 800; color: #ff4b4b; margin-top: 2px; font-size: 0.7rem; }
.student-name { font-size: 0.7rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.room-footer { display: flex; justify-content: space-between; gap: 20px; margin-top: 20px; }
</style>
''', unsafe_allow_html=True)

# --- Funções ---
def get_folders(path):
    if not os.path.exists(path): return []
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def load_class_data(turno, turma):
    path = os.path.join("turmas", turno, turma)
    students = []
    json_path = None
    for file in os.listdir(path):
        if file.endswith(".json"):
            json_path = os.path.join(path, file)
            break
    name_map = {}
    if json_path and os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            name_map = json.load(f)
    valid_exts = ['.jpg', '.jpeg', '.png', '.webp']
    for file in os.listdir(path):
        name, ext = os.path.splitext(file)
        if ext.lower() in valid_exts and name.isdigit():
            students.append({
                "numero": int(name),
                "nome": name_map.get(name, "Desconhecido"),
                "img_path": os.path.join(path, file)
            })
    return sorted(students, key=lambda x: x['numero'])

# --- Lógica de Estado ---
if 'swap_selection' not in st.session_state: st.session_state.swap_selection = None

# --- Sidebar ---
st.sidebar.title("🏫 Mapeamento")
turno_sel = st.sidebar.selectbox("Turno", get_folders("turmas"))

if turno_sel:
    turma_sel = st.sidebar.selectbox("Turma", get_folders(os.path.join("turmas", turno_sel)))
    
    current_key = f"{turno_sel}_{turma_sel}"
    if 'last_loaded' not in st.session_state or st.session_state.last_loaded != current_key:
        st.session_state.turma_data = load_class_data(turno_sel, turma_sel)
        st.session_state.last_loaded = current_key
        st.session_state.swap_selection = None

    def process_swap(idx):
        if st.session_state.swap_selection is None:
            st.session_state.swap_selection = idx
        else:
            idx_a, idx_b = st.session_state.swap_selection, idx
            data = st.session_state.turma_data
            data[idx_a], data[idx_b] = data[idx_b], data[idx_a]
            st.session_state.swap_selection = None
            st.rerun()

    st.title(f"📍 Turma: {turma_sel}")
    
    # Criando colunas forçadas via CSS injetado acima
    cols = st.columns(5)
    for i, student in enumerate(st.session_state.turma_data):
        with cols[i % 5]:
            is_selected = (st.session_state.swap_selection == i)
            st.markdown(f'<div class="student-card {"selected" if is_selected else ""}">', unsafe_allow_html=True)
            st.image(student["img_path"], use_container_width=True)
            st.markdown(f'<div class="student-number">Nº {student["numero"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="student-name">{student["nome"]}</div>', unsafe_allow_html=True)
            st.button("Trocar" if not is_selected else "Ok", key=f"btn_{i}", on_click=process_swap, args=(i,))
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('''<div class="room-footer">
        <div style="background:#8B4513; color:white; padding:10px; border-radius:5px; flex:1; text-align:center">🚪 PORTA</div>
        <div style="background:#182848; color:white; padding:10px; border-radius:5px; flex:1; text-align:center">👨‍🏫 MESA PROFESSOR</div>
    </div>''', unsafe_allow_html=True)
