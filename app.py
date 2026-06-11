import streamlit as st
import os
import json
import base64

# Configuração da página
st.set_page_config(page_title="Mapeamento de Sala", layout="wide", initial_sidebar_state="collapsed")

# CSS para forçar 5 colunas e responsividade
st.markdown('''
<style>
    /* Força as colunas do Streamlit a terem 20% de largura sempre */
    [data-testid="column"] {
        width: 20% !important;
        flex: 1 1 20% !important;
        max-width: 20% !important;
    }
    .student-card { 
        background: #ffffff; 
        border: 2px solid #e0e0e0; 
        border-radius: 8px; 
        padding: 5px; 
        text-align: center; 
        margin-bottom: 10px;
    }
    .student-card.selected { border-color: #ff4b4b; background-color: #fff0f0; }
    .student-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 4px; }
    .student-number { font-weight: 800; color: #ff4b4b; font-size: 0.7rem; margin-top: 5px; }
    .student-name { font-size: 0.7rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>
''', unsafe_allow_html=True)

# Funções
def get_folders(path):
    if not os.path.exists(path): return []
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def load_class_data(turno, turma):
    path = os.path.join("turmas", turno, turma)
    json_path = next((os.path.join(path, f) for f in os.listdir(path) if f.endswith(".json")), None)
    name_map = json.load(open(json_path, 'r', encoding='utf-8')) if json_path else {}
    students = []
    for file in os.listdir(path):
        name, ext = os.path.splitext(file)
        if ext.lower() in ['.jpg', '.jpeg', '.png'] and name.isdigit():
            with open(os.path.join(path, file), "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            students.append({"numero": int(name), "nome": name_map.get(name, "---"), "img": img_b64})
    return sorted(students, key=lambda x: x['numero'])

# Estado
if 'swap_selection' not in st.session_state: st.session_state.swap_selection = None

# Sidebar
turno_sel = st.sidebar.selectbox("Turno", get_folders("turmas"))
if turno_sel:
    turma_sel = st.sidebar.selectbox("Turma", get_folders(os.path.join("turmas", turno_sel)))
    if 'last_loaded' not in st.session_state or st.session_state.last_loaded != f"{turno_sel}_{turma_sel}":
        st.session_state.turma_data = load_class_data(turno_sel, turma_sel)
        st.session_state.last_loaded = f"{turno_sel}_{turma_sel}"
        st.session_state.swap_selection = None

    # Função de Troca
    def process_swap(idx):
        if st.session_state.swap_selection is None:
            st.session_state.swap_selection = idx
        else:
            idx_a = st.session_state.swap_selection
            data = st.session_state.turma_data
            data[idx_a], data[idx] = data[idx], data[idx_a]
            st.session_state.swap_selection = None
            st.rerun()

    st.title(f"📍 {turma_sel}")
    
    # Grid de 5 colunas
    cols = st.columns(5)
    for i, s in enumerate(st.session_state.turma_data):
        with cols[i % 5]:
            is_sel = (st.session_state.swap_selection == i)
            st.markdown(f'<div class="student-card {"selected" if is_sel else ""}">', unsafe_allow_html=True)
            st.image(f"data:image/png;base64,{s['img']}", use_container_width=True)
            st.markdown(f'<div class="student-number">Nº {s["numero"]}</div><div class="student-name">{s["nome"]}</div>', unsafe_allow_html=True)
            st.button("Trocar" if not is_sel else "OK", key=f"btn_{i}", on_click=process_swap, args=(i,))
            st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.divider()
    f1, f2 = st.columns(2)
    f1.markdown("🚪 **PORTA**")
    f2.markdown("👨‍🏫 **MESA DO PROFESSOR**")
