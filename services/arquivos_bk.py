"""Leitura de diretórios e arquivos de dados (turnos, turmas, alunos)."""

import json

from utils import paths
from utils.constantes import TURNOS


def listar_turnos() -> list[str]:
    """Retorna os turnos que de fato existem em disco, na ordem definida."""
    existentes = []
    for turno in TURNOS:
        if paths.pasta_turno(turno).is_dir():
            existentes.append(turno)
    return existentes


def listar_turmas(turno: str) -> list[str]:
    """Lista as turmas (subpastas com alunos.json) de um turno, em ordem alfabética."""
    pasta = paths.pasta_turno(turno)
    if not pasta.is_dir():
        return []
    turmas = [
        p.name
        for p in pasta.iterdir()
        if p.is_dir() and (p / "alunos.json").is_file()
    ]
    return sorted(turmas)


def carregar_alunos(turno: str, turma: str) -> dict[str, str]:
    """Carrega alunos.json -> {numero_chamada: nome}."""
    arquivo = paths.arquivo_alunos(turno, turma)
    if not arquivo.is_file():
        return {}
    with arquivo.open(encoding="utf-8") as f:
        dados = json.load(f)
    # Garante chaves como string e remove entradas vazias
    return {str(k): str(v).strip() for k, v in dados.items() if str(v).strip()}
