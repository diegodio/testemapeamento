import streamlit as st
import os
import json
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Mapeamento de Sala", layout="wide", initial_sidebar_state="collapsed")

# CSS Avançado para Grid Responsivo e Detecção de Dispositivo
st.markdown('''
    <style>
    /* Container do Grid de Alunos */
    .classroom-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr); /* Força 5 colunas sempre */
        gap: 10px;
        width: 100%;
        margin-bottom: 40px;
    }

    /* Card do Aluno */
    .student-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 5px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .student-number {
        font-weight: 800;
        color: #ff4b4b;
        font-size: 0.9rem;
    }

    .student-name {
        font-size: 0.8rem;
        color: #31333F;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 500;
    }

    /* Imagem Adaptável */
    .student-img {
        width: 100%;
        aspect-ratio: 1/1;
        object-fit: cover;
        border-radius: 4px;
        margin-bottom: 5px;
    }

    /* Estruturas da Sala (Mesa e Porta) */
    .room-footer {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-top: 20px;
        width: 100%;
    }

    .footer-item {
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        color: white;
        flex-grow: 1;
    }

    .teacher-desk {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
    }

    .door {
        background: linear-gradient(135deg, #8B4513 0%, #5C2E0B 100%);
        max-width: 200px;
    }

    /* Ajustes específicos para CELULAR (Telas menores que 768px) */
    @media (max-width: 768px) {
        .classroom-grid {
            gap: 5px; /* Menos espaço entre as carteiras no celular */
        }
        .student-name {
            font-size: 0.6rem; /* Nome menor para caber no celular */
        }
        .student-number {
            font-size: 0.7rem;
        }
        .student-card {
            padding: 2px;
        }
    }
    </style>
''', unsafe_allow_html=True)

BASE_DIR = "turmas"

def get_folders(path):
    if not os.path.exists(path):
        return []
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def get_image_as_base64(path):
    import base64
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def load_class_data(turno, turma):
    path = os.path.join(BASE_DIR, turno, turma)
    students = []
    json_path = None
    if os.path.exists(path):
        for file in os.listdir(path):
            if file.endswith(".json"):
                json_path = os.path.join(path, file)
                break
                
    name_map = {}
    if json_path and os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            name_map = json.load(f)
            
    valid_exts = ['.jpg', '.jpeg', '.png', '.webp']
    if os.path.exists(path):
        for file in os.listdir(path):
            name, ext = os.path.splitext(file)
            if ext.lower() in valid_exts and name.isdigit():
                num_chamada = name
                student_name = name_map.get(num_chamada, "---")
                students.append({
                    "numero": int(num_chamada),
                    "nome": student_name,
                    "img_path": os.path.join(path, file)
                })
    return sorted(students, key=lambda x: x['numero'])

# --- SIDEBAR ---
st.sidebar.title("🏫 Mapeamento")
turnos = get_folders(BASE_DIR)

if not turnos:
    st.error("Pasta 'turmas' não encontrada.")
    st.stop()

turno_sel = st.sidebar.selectbox("Turno", turnos)
turmas = get_folders(os.path.join(BASE_DIR, turno_sel))

if turmas:
    turma_sel = st.sidebar.selectbox("Turma", turmas)
    
    # --- CONTEÚDO PRINCIPAL ---
    st.title(f"📍 Sala: {turma_sel}")
    
    students = load_class_data(turno_sel, turma_sel)
    
    if not students:
        st.info("Sem dados para esta turma.")
    else:
        # Iniciando o Grid de Alunos (Sempre 5 colunas via CSS)
        grid_html = '<div class="classroom-grid">'
        
        for s in students:
            # Convertendo imagem para base64 para o HTML não quebrar no deploy
            img_b64 = get_image_as_base64(s["img_path"])
            
            grid_html += f'''
                <div class="student-card">
                    <img src="data:image/png;base64,{img_b64}" class="student-img">
                    <div class="student-number">Nº {s['numero']}</div>
                    <div class="student-name" title="{s['nome']}">{s['nome']}</div>
                </div>
            '''
        
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

        # --- MESA E PORTA NO FINAL ---
        st.markdown(f'''
            <div class="room-footer">
                <div class="footer-item door">🚪 PORTA</div>
                <div class="footer-item teacher-desk">👨‍🏫 MESA DO PROFESSOR</div>
            </div>
        ''', unsafe_allow_html=True)

else:
    st.sidebar.warning("Nenhuma turma encontrada.")
