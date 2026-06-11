import streamlit as st
import os
import json
import base64

st.set_page_config(page_title="Mapeamento Interativo", layout="wide", initial_sidebar_state="collapsed")

# CSS FORÇADO: O container principal do Streamlit não vai interferir no nosso grid
st.markdown('''
<style>
.fixed-grid { 
    display: grid !important; 
    grid-template-columns: repeat(5, 1fr) !important; 
    gap: 5px !important; 
    width: 100% !important; 
}
.student-card { 
    background: #ffffff; border: 2px solid #e0e0e0; border-radius: 6px; 
    padding: 4px; text-align: center; display: flex; flex-direction: column; 
}
.student-card.selected { border-color: #ff4b4b; background-color: #fff0f0; }
.student-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 4px; }
.student-number { font-weight: 800; color: #ff4b4b; font-size: 0.6rem; }
.student-name { font-size: 0.6rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.swap-btn { 
    margin-top: 5px; background: #eee; border: none; border-radius: 4px; 
    font-size: 0.6rem; cursor: pointer; width: 100%; 
}
</style>
''', unsafe_allow_html=True)

# --- Funções ---
def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def load_data(turno, turma):
    path = os.path.join("turmas", turno, turma)
    json_path = next((os.path.join(path, f) for f in os.listdir(path) if f.endswith(".json")), None)
    name_map = json.load(open(json_path, 'r', encoding='utf-8')) if json_path else {}
    students = []
    for file in os.listdir(path):
        name, ext = os.path.splitext(file)
        if ext.lower() in ['.jpg', '.jpeg', '.png'] and name.isdigit():
            students.append({"numero": int(name), "nome": name_map.get(name, "---"), "img": get_image_base64(os.path.join(path, file))})
    return sorted(students, key=lambda x: x['numero'])

# --- Lógica de Troca via Query Params (URL) ---
query = st.query_params
if 'swap_a' in query and 'swap_b' in query:
    idx_a, idx_b = int(query['swap_a']), int(query['swap_b'])
    data = st.session_state.turma_data
    data[idx_a], data[idx_b] = data[idx_b], data[idx_a]
    st.session_state.swap_selection = None
    st.query_params.clear()
    st.rerun()

# --- SIDEBAR E ESTADO ---
turno = st.sidebar.selectbox("Turno", [d for d in os.listdir("turmas") if os.path.isdir(os.path.join("turmas", d))])
turma = st.sidebar.selectbox("Turma", [d for d in os.listdir(os.path.join("turmas", turno)) if os.path.isdir(os.path.join("turmas", turno, d))])
key = f"{turno}_{turma}"

if 'last' not in st.session_state or st.session_state.last != key:
    st.session_state.turma_data = load_data(turno, turma)
    st.session_state.last = key
    st.session_state.swap_selection = None

# --- GRID (Totalmente em HTML) ---
st.title(f"📍 {turma}")
grid_html = '<div class="fixed-grid">'

for i, s in enumerate(st.session_state.turma_data):
    sel = st.session_state.swap_selection
    is_sel = (sel == i)
    
    # Lógica de seleção via clique de botão
    if st.button("Trocar" if not is_sel else "Selecionado", key=f"btn_{i}"):
        if sel is None: st.session_state.swap_selection = i; st.rerun()
        elif sel == i: st.session_state.swap_selection = None; st.rerun()
        else: st.query_params.update(swap_a=sel, swap_b=i)

    grid_html += f'''
    <div class="student-card {'selected' if is_sel else ''}">
        <img src="data:image/png;base64,{s['img']}" class="student-img">
        <div class="student-number">Nº {s['numero']}</div>
        <div class="student-name">{s['nome']}</div>
    </div>
    '''

grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)
