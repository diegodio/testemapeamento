"""Resolução centralizada de caminhos do projeto."""

from pathlib import Path

from utils.constantes import ARQUIVO_ALUNOS, ARQUIVO_MAPEAMENTO

# Raiz do projeto (pasta que contém app.py)
RAIZ = Path(__file__).resolve().parent.parent

DADOS = RAIZ / "dados"
ASSETS = RAIZ / "assets"
AVATAR_PADRAO = ASSETS / "avatar_padrao.png"


def pasta_turno(turno: str) -> Path:
    """Pasta de um turno. Ex.: dados/matutino"""
    return DADOS / turno


def pasta_turma(turno: str, turma: str) -> Path:
    """Pasta de uma turma. Ex.: dados/matutino/3A"""
    return DADOS / turno / turma


def arquivo_alunos(turno: str, turma: str) -> Path:
    return pasta_turma(turno, turma) / ARQUIVO_ALUNOS


def arquivo_mapeamento(turno: str, turma: str) -> Path:
    return pasta_turma(turno, turma) / ARQUIVO_MAPEAMENTO
