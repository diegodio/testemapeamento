import streamlit as st
import os
import json
import base64
from pathlib import Path

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mapeamento de Turmas",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}
BASE_DIR = Path(__file__).parent / "turmas"

# ─── THEME / CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ── */
.stApp {
    background: #f0f2f6;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2158 0%, #071540 100%);
    border-right: 3px solid #C9A84C;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #C9A84C !important;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 0.75rem;
}
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(201,168,76,0.5) !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #ffffff !important;
    background: transparent !important;
}

/* ── Main header ── */
.header-container {
    background: linear-gradient(135deg, #0A2158 0%, #1a3a6b 60%, #0A2158 100%);
    border-bottom: 4px solid #C9A84C;
    padding: 1.5rem 2rem;
    margin: -1rem -1rem 1.5rem -1rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
}
.header-emblem {
    font-size: 2.8rem;
    line-height: 1;
}
.header-title {
    font-family: 'Oswald', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.04em;
    margin: 0;
    line-height: 1.1;
}
.header-subtitle {
    font-size: 0.8rem;
    color: #C9A84C;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0;
}

/* ── Turma badge ── */
.turma-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: linear-gradient(135deg, #0A2158, #1a3a6b);
    border: 2px solid #C9A84C;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    margin-bottom: 1.2rem;
}
.turma-badge-text {
    font-family: 'Oswald', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.08em;
}
.turma-badge-turno {
    font-size: 0.75rem;
    color: #C9A84C;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    background: rgba(201,168,76,0.15);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
}

/* ── Classroom map container ── */
.classroom-container {
    background: #ffffff;
    border-radius: 12px;
    border: 2px solid #d0d8e8;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(10,33,88,0.08);
    position: relative;
}

/* ── Room elements ── */
.room-label {
    font-family: 'Oswald', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.room-wall {
    background: #0A2158;
    border-radius: 6px;
    padding: 0.5rem;
    text-align: center;
    color: #C9A84C;
}
.room-door {
    background: linear-gradient(135deg, #1B4332, #2d6a4f);
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    text-align: center;
    color: #C9A84C;
    border: 2px dashed rgba(201,168,76,0.6);
}
.teacher-desk {
    background: linear-gradient(135deg, #0A2158, #1a3a6b);
    border: 2px solid #C9A84C;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    text-align: center;
    color: #ffffff;
}
.teacher-desk-title {
    font-family: 'Oswald', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #C9A84C;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Student card ── */
.student-card {
    background: #ffffff;
    border: 1.5px solid #d8e0f0;
    border-radius: 10px;
    padding: 0.6rem 0.4rem;
    text-align: center;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(10,33,88,0.06);
    position: relative;
    overflow: hidden;
}
.student-card:hover {
    border-color: #C9A84C;
    box-shadow: 0 4px 16px rgba(10,33,88,0.14);
    transform: translateY(-2px);
}
.student-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #0A2158, #C9A84C);
}
.student-photo {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #0A2158;
    margin: 0.3rem auto 0.4rem;
    display: block;
}
.student-number {
    font-family: 'Oswald', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #C9A84C;
    background: #0A2158;
    border-radius: 4px;
    padding: 0 0.35rem;
    display: inline-block;
    margin-bottom: 0.3rem;
    letter-spacing: 0.04em;
}
.student-name {
    font-size: 0.62rem;
    font-weight: 500;
    color: #1a2a4a;
    line-height: 1.3;
    word-break: break-word;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.empty-seat {
    background: #f7f8fc;
    border: 1.5px dashed #c5cde0;
    border-radius: 10px;
    height: 100%;
    min-height: 105px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.empty-seat-inner {
    color: #c5cde0;
    font-size: 1.5rem;
}

/* ── Stats bar ── */
.stats-bar {
    background: linear-gradient(135deg, #0A2158, #1a3a6b);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    display: flex;
    gap: 2rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(201,168,76,0.3);
}
.stat-item {
    text-align: center;
}
.stat-value {
    font-family: 'Oswald', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1;
}
.stat-label {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.7);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 500;
}

/* ── Row label ── */
.row-label {
    font-family: 'Oswald', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    color: #0A2158;
    background: rgba(201,168,76,0.2);
    border: 1px solid rgba(201,168,76,0.5);
    border-radius: 4px;
    text-align: center;
    padding: 0.3rem 0.1rem;
    letter-spacing: 0.06em;
    writing-mode: horizontal-tb;
}
.blackboard {
    background: linear-gradient(180deg, #1B4332 0%, #145228 100%);
    border: 3px solid #0d3b22;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    text-align: center;
    color: rgba(255,255,255,0.85);
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
    font-family: 'Oswald', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.section-divider {
    border: none;
    border-top: 2px solid #d0d8e8;
    margin: 1rem 0;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #4a5568;
}
.legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def get_image_base64(img_path: Path) -> str | None:
    """Read an image file and return as base64 data URI."""
    if not img_path.exists():
        return None
    try:
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        suffix = img_path.suffix.lower().lstrip(".")
        mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
        return f"data:image/{mime};base64,{data}"
    except Exception:
        return None


def load_turmas(base: Path) -> dict:
    """
    Walk base/turno/turma and return a nested dict:
        { turno: { turma: Path } }
    """
    result = {}
    if not base.exists():
        return result
    for turno_dir in sorted(base.iterdir()):
        if not turno_dir.is_dir():
            continue
        result[turno_dir.name] = {}
        for turma_dir in sorted(turno_dir.iterdir()):
            if not turma_dir.is_dir():
                continue
            result[turno_dir.name][turma_dir.name] = turma_dir
    return result


def load_turma_data(turma_path: Path) -> dict:
    """
    Load the JSON and map each number to { nome, foto_b64 }.
    Returns a dict keyed by int (chamada number).
    """
    json_file = turma_path / "alunos.json"
    if not json_file.exists():
        st.error(f"Arquivo alunos.json não encontrado em {turma_path}")
        return {}

    with open(json_file, encoding="utf-8") as f:
        raw = json.load(f)

    alunos = {}
    for num_str, nome in raw.items():
        num = int(num_str)
        # Try all common extensions
        foto = None
        for ext in IMAGE_EXTENSIONS:
            candidate = turma_path / f"{num_str}{ext}"
            if candidate.exists():
                foto = get_image_base64(candidate)
                break
            # also try zero-padded
            candidate2 = turma_path / f"{num_str.zfill(2)}{ext}"
            if candidate2.exists():
                foto = get_image_base64(candidate2)
                break
        alunos[num] = {"nome": nome, "foto": foto}

    return alunos


def generate_placeholder_svg(number: int, name: str) -> str:
    """Generate an inline SVG avatar when no photo is found."""
    parts = name.split()
    initials = (parts[0][0] + parts[1][0]).upper() if len(parts) >= 2 else name[:2].upper()
    palette = [
        ("#0A2158", "#C9A84C"),
        ("#1B4332", "#f0d060"),
        ("#1a3a6b", "#e8c84a"),
        ("#2c3e50", "#f39c12"),
        ("#0d3b5e", "#ffd700"),
    ]
    bg, fg = palette[number % len(palette)]
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='56' height='56' viewBox='0 0 56 56'>
      <circle cx='28' cy='28' r='27' fill='{bg}' stroke='{fg}' stroke-width='2'/>
      <text x='28' y='32' text-anchor='middle' fill='{fg}'
            font-family='Oswald,Arial,sans-serif' font-size='18' font-weight='700'>{initials}</text>
    </svg>"""
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"


def student_card_html(num: int, aluno: dict) -> str:
    foto = aluno.get("foto") or generate_placeholder_svg(num, aluno["nome"])
    nome = aluno["nome"]
    # First name + last name only for display
    parts = nome.split()
    display_name = f"{parts[0]}<br>{' '.join(parts[1:])}" if len(parts) > 1 else nome
    return f"""
    <div class="student-card">
        <img class="student-photo" src="{foto}" alt="Aluno {num}"/>
        <div class="student-number">Nº {num}</div>
        <div class="student-name">{display_name}</div>
    </div>"""


def empty_seat_html() -> str:
    return """<div class="empty-seat"><div class="empty-seat-inner">—</div></div>"""


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
        <div style="font-size:3rem">🎖️</div>
        <div style="font-family:'Oswald',sans-serif; font-size:1.1rem; font-weight:700;
                    color:#C9A84C; letter-spacing:0.08em; line-height:1.2;">
            ESCOLA CÍVICO-MILITAR
        </div>
        <div style="font-size:0.7rem; color:rgba(255,255,255,0.5);
                    letter-spacing:0.12em; text-transform:uppercase; margin-top:0.2rem;">
            Sistema de Mapeamento
        </div>
    </div>
    <hr style="border-color:rgba(201,168,76,0.3); margin-bottom:1.2rem"/>
    """, unsafe_allow_html=True)

    turmas_dict = load_turmas(BASE_DIR)

    if not turmas_dict:
        st.error("Nenhuma turma encontrada.")
        st.stop()

    # Turno selector
    turnos = list(turmas_dict.keys())
    selected_turno = st.selectbox("🕐 Turno", turnos)

    # Turma selector
    turmas_do_turno = list(turmas_dict[selected_turno].keys())
    selected_turma = st.selectbox("🏫 Turma", turmas_do_turno)

    turma_path = turmas_dict[selected_turno][selected_turma]

    st.markdown("<hr style='border-color:rgba(201,168,76,0.3); margin: 1.2rem 0'/>",
                unsafe_allow_html=True)

    # Layout settings
    st.markdown(
        "<p style='color:#C9A84C !important; font-weight:600; font-size:0.75rem;"
        "letter-spacing:0.08em; text-transform:uppercase;'>⚙️ Layout da Sala</p>",
        unsafe_allow_html=True,
    )
    cols_per_row = st.slider("Colunas por fileira", 4, 8, 6)
    door_position = st.radio("Posição da Porta", ["Frente-Esquerda", "Frente-Direita",
                                                   "Fundo-Esquerda", "Fundo-Direita"],
                             index=0)
    teacher_side = st.radio("Mesa do professor", ["Frente-Esquerda", "Frente-Direita"],
                            index=1)

    st.markdown("<hr style='border-color:rgba(201,168,76,0.3); margin: 1.2rem 0'/>",
                unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.65rem; color:rgba(255,255,255,0.4); line-height:1.6;">
        🗂️ Estrutura de pastas:<br>
        <code style="color:rgba(201,168,76,0.7)">turmas/turno/turma/</code><br>
        • <code style="color:rgba(201,168,76,0.7)">alunos.json</code><br>
        • <code style="color:rgba(201,168,76,0.7)">&lt;nº&gt;.jpg/.png/…</code>
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────

# Header
st.markdown(f"""
<div class="header-container">
    <div class="header-emblem">🏫</div>
    <div>
        <p class="header-title">Mapeamento de Turmas</p>
        <p class="header-subtitle">Escola Cívico-Militar · Sistema de Gestão de Sala</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
alunos = load_turma_data(turma_path)
if not alunos:
    st.warning("Nenhum aluno encontrado nesta turma.")
    st.stop()

total = len(alunos)
numeros = sorted(alunos.keys())
rows_count = -(-total // cols_per_row)  # ceiling division

# Turma badge + stats
col_badge, col_stats = st.columns([1, 2])

with col_badge:
    st.markdown(f"""
    <div class="turma-badge">
        <span style="font-size:1.8rem">🎓</span>
        <div>
            <div class="turma-badge-text">{selected_turma}</div>
            <div class="turma-badge-turno">{selected_turno}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_stats:
    with_photo = sum(1 for a in alunos.values() if a.get("foto"))
    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Alunos</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{rows_count}</div>
            <div class="stat-label">Fileiras</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{cols_per_row}</div>
            <div class="stat-label">Colunas</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{with_photo}</div>
            <div class="stat-label">Com Foto</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── CLASSROOM LAYOUT ─────────────────────────────────────────────────────────
st.markdown("### 🗺️ Mapa da Sala")

with st.container():

    # ── TOP WALL (quadro + optional door/teacher at front) ──
    door_front = "Frente" in door_position
    door_left = "Esquerda" in door_position
    teacher_left = "Esquerda" in teacher_side

    # Blackboard row
    st.markdown('<div class="blackboard">📋 &nbsp; Quadro-Negro / Frente da Sala</div>',
                unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    # Front row: door + teacher desk
    front_cols = st.columns([1, 2, 2, 1])
    with front_cols[0]:
        if door_front and door_left:
            st.markdown('<div class="room-door"><div class="room-label">🚪 PORTA</div></div>',
                        unsafe_allow_html=True)
    with front_cols[1]:
        if teacher_left:
            st.markdown("""
            <div class="teacher-desk">
                <div class="teacher-desk-title">🖥️ Mesa do Professor</div>
                <div style="font-size:0.65rem; color:rgba(255,255,255,0.6);">Frente da sala</div>
            </div>""", unsafe_allow_html=True)
    with front_cols[2]:
        if not teacher_left:
            st.markdown("""
            <div class="teacher-desk">
                <div class="teacher-desk-title">🖥️ Mesa do Professor</div>
                <div style="font-size:0.65rem; color:rgba(255,255,255,0.6);">Frente da sala</div>
            </div>""", unsafe_allow_html=True)
    with front_cols[3]:
        if door_front and not door_left:
            st.markdown('<div class="room-door"><div class="room-label">🚪 PORTA</div></div>',
                        unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    # ── STUDENT GRID ──
    idx = 0
    for row_i in range(rows_count):
        row_label_col, *desk_cols, spacer_col = st.columns(
            [0.4] + [1] * cols_per_row + [0.4]
        )
        with row_label_col:
            st.markdown(
                f'<div class="row-label" style="margin-top:0.3rem">F{row_i+1}</div>',
                unsafe_allow_html=True,
            )
        for col_i, col in enumerate(desk_cols):
            with col:
                if idx < total:
                    num = numeros[idx]
                    st.markdown(student_card_html(num, alunos[num]),
                                unsafe_allow_html=True)
                    idx += 1
                else:
                    st.markdown(empty_seat_html(), unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:0.4rem'></div>", unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

    # ── BACK WALL ──
    back_cols = st.columns([1, 4, 1])
    with back_cols[0]:
        if not door_front and door_left:
            st.markdown('<div class="room-door"><div class="room-label">🚪 PORTA</div></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="room-wall"><div class="room-label" style="color:#C9A84C">◀ Parede</div></div>',
                unsafe_allow_html=True,
            )
    with back_cols[1]:
        st.markdown(
            '<div class="room-wall"><div class="room-label" style="color:#C9A84C; font-size:0.7rem">'
            '▬ &nbsp; Fundo da Sala &nbsp; ▬</div></div>',
            unsafe_allow_html=True,
        )
    with back_cols[2]:
        if not door_front and not door_left:
            st.markdown('<div class="room-door"><div class="room-label">🚪 PORTA</div></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="room-wall"><div class="room-label" style="color:#C9A84C">Parede ▶</div></div>',
                unsafe_allow_html=True,
            )


# ── LEGEND ───────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
leg_cols = st.columns(5)
legends = [
    ("#0A2158", "Carteiras de alunos"),
    ("#1B4332", "Porta de entrada"),
    ("#C9A84C", "Mesa do professor"),
    ("#d0d8e8", "Carteira vazia"),
    ("#1a3a6b", "Parede / fundo"),
]
for col, (color, label) in zip(leg_cols, legends):
    with col:
        st.markdown(
            f'<div class="legend-item">'
            f'<span class="legend-dot" style="background:{color};'
            f'{"border:1.5px dashed #c5cde0" if color == "#d0d8e8" else ""}"></span>'
            f'<span>{label}</span></div>',
            unsafe_allow_html=True,
        )

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:2.5rem; padding: 1rem;
            border-top: 2px solid #d0d8e8; color:#8a9abf; font-size:0.7rem;
            letter-spacing:0.08em; text-transform:uppercase;">
    🎖️ &nbsp; Sistema de Mapeamento de Turmas · Escola Cívico-Militar do Paraná &nbsp; 🎖️
</div>
""", unsafe_allow_html=True)
