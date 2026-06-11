import streamlit as st
import os
import json
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Mapeamento Interativo", layout="wide", initial_sidebar_state="collapsed")

# CSS para o Grid Responsivo e feedback visual
st.markdown('''
<style>
.classroom-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 30px; }
.student-card { background: #ffffff; border: 2px solid #e0e0e0; border-radius: 10px; padding: 10px; text-align: center; }
.student-card.selected { border-color: #ff4b4b; background-color: #fff0f0; }
.student-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 5px; }
.student-number { font-weight: 800; color: #ff4b4b; margin-top: 5px; }
.student-name { font-size: 0.8rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.room-footer { display: flex; justify-content: space-between; gap: 20px; margin-top: 20px; }
</style>
''', unsafe_allow_html=True)

# --- Funções de Carregamento ---
def get_folders(path):
    if not os.path.exists(path): return []
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def load_class_data(turno, turma):
    path = os.path.join("turmas", turno, turma)
    students = []
    json_path = None
    
    # Procura arquivo JSON
    for file in os.listdir(path):
        if file.endswith(".json"):
            json_path = os.path.join(path, file)
            break
            
    name_map = {}
    if json_path and os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            name_map = json.load(f)
            
    # Carrega imagens
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

# --- Inicialização ---
if 'swap_selection' not in st.session_state:
    st.session_state.swap_selection = None

# --- Sidebar ---
st.sidebar.title("🏫 Mapeamento")
turnos = get_folders("turmas")
turno_sel = st.sidebar.selectbox("Turno", turnos)

if turno_sel:
    turmas = get_folders(os.path.join("turmas", turno_sel))
    turma_sel = st.sidebar.selectbox("Turma", turmas)
    
    # Carregar dados se a turma mudou ou não existe
    current_key = f"{turno_sel}_{turma_sel}"
    if 'last_loaded' not in st.session_state or st.session_state.last_loaded != current_key:
        st.session_state.turma_data = load_class_data(turno_sel, turma_sel)
        st.session_state.last_loaded = current_key
        st.session_state.swap_selection = None

    # --- Lógica de Troca ---
    def process_swap(idx):
        if st.session_state.swap_selection is None:
            st.session_state.swap_selection = idx
        else:
            idx_a = st.session_state.swap_selection
            idx_b = idx
            data = st.session_state.turma_data
            data[idx_a], data[idx_b] = data[idx_b], data[idx_a]
            st.session_state.swap_selection = None
            st.rerun()

    # --- Renderização ---
    st.title(f"📍 Turma: {turma_sel}")
    
    grid_col = st.columns(5)
    for i, student in enumerate(st.session_state.turma_data):
        with grid_col[i % 5]:
            is_selected = (st.session_state.swap_selection == i)
            
            st.markdown(f'<div class="student-card {"selected" if is_selected else ""}">', unsafe_allow_html=True)
            st.image(student["img_path"], use_container_width=True)
            st.markdown(f'''
                <div class="student-number">Nº {student["numero"]}</div>
                <div class="student-name">{student["nome"]}</div>
            ''', unsafe_allow_html=True)
            
            btn_label = "Selecionado" if is_selected else "Trocar"
            st.button(btn_label, key=f"btn_{i}", on_click=process_swap, args=(i,))
            st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('''<div class="room-footer">
        <div style="background:#8B4513; color:white; padding:10px; border-radius:5px; flex:1; text-align:center">🚪 PORTA</div>
        <div style="background:#182848; color:white; padding:10px; border-radius:5px; flex:1; text-align:center">👨‍🏫 MESA PROFESSOR</div>
    </div>''', unsafe_allow_html=True)
