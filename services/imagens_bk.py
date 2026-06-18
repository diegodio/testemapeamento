"""Localização e preparo das fotos dos alunos."""

import base64
from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

from utils import paths
from utils.constantes import EXTENSOES_IMAGEM

_TAMANHO_FOTO = (192, 192)


def localizar_imagem(pasta_turma: Path, numero_chamada: str) -> Path | None:
    """Procura {numero}.{ext} na pasta da turma, em qualquer formato popular,
    de forma case-insensitive (1.jpg, 1.JPG, 1.WebP...)."""
    if not pasta_turma.is_dir():
        return None
    alvo = str(numero_chamada)
    for arquivo in pasta_turma.iterdir():
        if not arquivo.is_file():
            continue
        if arquivo.stem == alvo and arquivo.suffix.lower() in EXTENSOES_IMAGEM:
            return arquivo
    return None


@st.cache_data(show_spinner=False)
def _carregar_data_uri(caminho: str, mtime: float) -> str:
    """Abre a imagem, recorta em quadrado, redimensiona e devolve um data URI.
    `mtime` participa da chave de cache para invalidar quando a foto mudar."""
    with Image.open(caminho) as img:
        img = ImageOps.exif_transpose(img)
        img = ImageOps.fit(img.convert("RGB"), _TAMANHO_FOTO, Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=82)
    dados = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{dados}"


def foto_data_uri(pasta_turma: Path, numero_chamada: str | None) -> str:
    """Retorna o data URI da foto do aluno, ou do avatar padrão."""
    caminho = None
    if numero_chamada is not None:
        caminho = localizar_imagem(pasta_turma, numero_chamada)
    if caminho is None:
        caminho = paths.AVATAR_PADRAO
    if not caminho.is_file():
        # Último recurso: pixel transparente (nunca quebra a interface)
        return ("data:image/png;base64,"
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
                "AAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
    return _carregar_data_uri(str(caminho), caminho.stat().st_mtime)
