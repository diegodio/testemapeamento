import streamlit as st
import os
import json

st.set_page_config(page_title="Mapeamento Interativo", layout="wide", initial_sidebar_state="collapsed")

# CSS para um Grid de 5 colunas que NUNCA empilha
st.markdown('''
<style>
/* Remove o espaçamento padrão do Streamlit */
.main .block-container { padding-top: 1rem; }

/* Grid fixo de 5 colunas */
.fixed-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    width: 100%;
}

.student-card { 
    background: #ffffff; 
    border: 2px solid #e0e0e0; 
    border-radius: 8px; 
    padding: 5px; 
    text-align: center; 
}
.student-card.selected { border-color: #ff4b4b; background-color: #fff0f0; }

.student-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 4px; }
.student-number { font-weight: 800; color: #ff4b4b; font-size: 0.7rem; }
.student-name { font-size: 0.65rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Botão pequeno para não ocupar espaço */
.stButton button { width: 100%; padding: 0.2rem; font-size: 0.7rem; }
</style>
''', unsafe_allow_html=True)

# --- Funções ---
def get_folders(path):
    if not os.path.exists(path): return []
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def load_class_data(turno, turma):
    path = os.path.join("turmas", turno, turma)
    students = []
    # ... (mesma lógica anterior) ...
    json_path = next((os.path.join(path, f) for f in os.listdir(path) if f.endswith(".json")), None)
    name_map = json.load(open(json_path, 'r', encoding='utf-8')) if json_path else {}
    for file in os.listdir(path):
        name, ext = os.path.splitext(file)
        if ext.lower() in ['.jpg', '.jpeg', '.png'] and name.isdigit():
            students.append({"numero": int(name), "nome": name_map.get(name, "---"), "img_path": os.path.join(path, file)})
    return sorted(students, key=lambda x: x['numero'])

# --- Lógica ---
if 'swap_selection' not in st.session_state: st.session_state.swap_selection = None

st.sidebar.title("🏫 Mapeamento")
turno_sel = st.sidebar.selectbox("Turno", get_folders("turmas"))
if turno_sel:
    turma_sel = st.sidebar.selectbox("Turma", get_folders(os.path.join("turmas", turno_sel)))
    if 'last_loaded' not in st.session_state or st.session_state.last_loaded != f"{turno_sel}_{turma_sel}":
        st.session_state.turma_data = load_class_data(turno_sel, turma_sel)
        st.session_state.last_loaded = f"{turno_sel}_{turma_sel}"

    def process_swap(idx):
        if st.session_state.swap_selection is None: st.session_state.swap_selection = idx
        else:
            data = st.session_state.turma_data
            data[st.session_state.swap_selection], data[idx] = data[idx], data[st.session_state.swap_selection]
            st.session_state.swap_selection = None
            st.rerun()

    st.title(f"📍 {turma_sel}")
    
    # Renderizar o Grid manualmente sem st.columns
    grid_html = '<div class="fixed-grid">'
    st.markdown(grid_html, unsafe_allow_html=True)
    
    for i, student in enumerate(st.session_state.turma_data):
        # Usamos um container para cada aluno para poder ter o botão do Streamlit dentro
        with st.container():
            is_selected = (st.session_state.swap_selection == i)
            st.markdown(f'<div class="student-card {"selected" if is_selected else ""}">', unsafe_allow_html=True)
            st.image(student["img_path"], use_container_width=True)
            st.markdown(f'<div class="student-number">Nº {student["numero"]}</div><div class="student-name">{student["nome"]}</div>', unsafe_allow_html=True)
            st.button("Trocar" if not is_selected else "Ok", key=f"btn_{i}", on_click=process_swap, args=(i,))
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
