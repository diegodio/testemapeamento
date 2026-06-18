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
    """Lista as turmas (subpastas com info.json) de um turno, em ordem alfabética."""
    pasta = paths.pasta_turno(turno)
    if not pasta.is_dir():
        return []
    turmas = [
        p.name
        for p in pasta.iterdir()
        if p.is_dir() and (p / "info.json").is_file()
    ]
    return sorted(turmas)


def carregar_alunos(turno: str, turma: str) -> dict[str, str]:
    """Carrega info.json -> {nome: nome}."""
    arquivo = paths.pasta_turno(turno) / turma / "info.json"
    if not arquivo.is_file():
        return {}
    with arquivo.open(encoding="utf-8") as f:
        dados = json.load(f)
    return {str(k).strip(): str(k).strip() for k in dados if str(k).strip()}

def carregar_info(turno: str, turma: str) -> dict[str, dict]:
    """Carrega info.json -> {nome: {numero, posicao}}."""
    arquivo = paths.pasta_turno(turno) / turma / "info.json"
    if not arquivo.is_file():
        return {}
    with arquivo.open(encoding="utf-8") as f:
        return json.load(f)
