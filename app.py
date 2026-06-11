import streamlit as st
import os
import json
from PIL import Image

# Configuração da página para ocupar toda a largura e ter um título
st.set_page_config(page_title="Mapeamento de Sala", layout="wide", initial_sidebar_state="expanded")

# CSS Customizado para um design moderno
st.markdown("""
    <style>
    .student-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .student-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .student-number {
        font-weight: 800;
        color: #ff4b4b;
        font-size: 1.2rem;
        margin-bottom: 5px;
    }
    .student-name {
        font-size: 1rem;
        color: #31333F;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .room-structure {
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 30px;
        color: white;
    }
    .teacher-desk {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        box-shadow: 0 4px 15px rgba(75, 108, 183, 0.4);
    }
    .door {
        background: linear-gradient(135deg, #8B4513 0%, #5C2E0B 100%);
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Definição do diretório base apontando diretamente para a pasta "turmas"
BASE_DIR = "turmas"

def get_folders(path):
    """Retorna uma lista de pastas dentro de um diretório específico."""
    if not os.path.exists(path):
        return []
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def load_class_data(turno, turma):
    """Carrega as imagens e cruza com o JSON da turma selecionada."""
    path = os.path.join(BASE_DIR, turno, turma)
    students = []
    
    # Encontra o arquivo JSON dinamicamente
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
            
    # Filtra e carrega as imagens
    valid_exts = ['.jpg', '.jpeg', '.png', '.webp']
    if os.path.exists(path):
        for file in os.listdir(path):
            name, ext = os.path.splitext(file)
            if ext.lower() in valid_exts and name.isdigit():
                num_chamada = name
                student_name = name_map.get(num_chamada, "Nome não encontrado")
                students.append({
                    "numero": int(num_chamada),
                    "nome": student_name,
                    "img_path": os.path.join(path, file)
                })
                
    # Ordena os alunos pelo número da chamada
    return sorted(students, key=lambda x: x['numero'])

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
st.sidebar.title("🏫 Mapeamento Escolar")
st.sidebar.markdown("---")

turnos = get_folders(BASE_DIR)

if not turnos:
    st.error(f"⚠️ Diretório '{BASE_DIR}' não encontrado. Certifique-se de que a pasta está no mesmo local que este script.")
    st.stop()

turno_selecionado = st.sidebar.selectbox("1. Selecione o Turno", turnos)
turmas = get_folders(os.path.join(BASE_DIR, turno_selecionado))

if turmas:
    turma_selecionada = st.sidebar.selectbox("2. Selecione a Turma", turmas)
    
    # ==========================================
    # ÁREA PRINCIPAL
    # ==========================================
    st.title(f"📍 Mapeamento: Turma {turma_selecionada} ({turno_selecionado})")
    
    # Layout Físico da Sala (Porta e Mesa do Professor)
    col_vazia1, col_mesa, col_vazia2, col_porta = st.columns([1, 4, 1, 2])
    
    with col_mesa:
        st.markdown('<div class="room-structure teacher-desk">👨‍🏫 Mesa do Professor</div>', unsafe_allow_html=True)
    with col_porta:
        st.markdown('<div class="room-structure door">🚪 Porta</div>', unsafe_allow_html=True)
        
    st.divider()
    
    # Carrega dados da turma
    students = load_class_data(turno_selecionado, turma_selecionada)
    
    if not students:
        st.info("Nenhuma imagem ou dado encontrado para esta turma.")
    else:
        # Configuração do Grid de Carteiras (5 colunas por linha)
        colunas_por_linha = 5
        
        for i in range(0, len(students), colunas_por_linha):
            cols = st.columns(colunas_por_linha)
            
            for j in range(colunas_por_linha):
                if i + j < len(students):
                    student = students[i+j]
                    with cols[j]:
                        try:
                            # Carrega e exibe a foto do aluno
                            img = Image.open(student["img_path"])
                            st.image(img, use_container_width=True)
                        except Exception as e:
                            st.error("Erro na imagem")
                        
                        # Exibe o Card HTML com design moderno
                        st.markdown(f"""
                        <div class="student-card">
                            <div class="student-number">Nº {student['numero']}</div>
                            <div class="student-name" title="{student['nome']}">{student['nome']}</div>
                        </div>
                        """, unsafe_allow_html=True)
else:
    st.sidebar.warning("Nenhuma turma encontrada neste turno.")
