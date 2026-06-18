"""Regras do mapeamento: leitura, geração automática e troca de posições."""
import json
import re
from utils import paths
from utils.constantes import ALUNOS_POR_FILA

Posicao = tuple[int, int]  # (fila, posicao_na_fila)

_PADRAO_POSICAO = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)")


def chave_para_posicao(chave: str) -> Posicao | None:
    """'(1,2)' -> (1, 2). Tolera espaços: '( 1 , 2 )'."""
    m = _PADRAO_POSICAO.fullmatch(chave.strip())
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def posicao_para_chave(pos: Posicao) -> str:
    """(1, 2) -> '(1,2)'"""
    return f"({pos[0]},{pos[1]})"


def gerar_mapeamento_inicial(alunos: dict[str, str]) -> dict[Posicao, str]:
    """Distribui os alunos em filas, ordenados alfabeticamente pelo nome."""
    nomes = sorted(alunos.keys())
    mapa: dict[Posicao, str] = {}
    for indice, nome in enumerate(nomes):
        fila = indice // ALUNOS_POR_FILA + 1
        posicao = indice % ALUNOS_POR_FILA + 1
        mapa[(fila, posicao)] = nome
    return mapa


def carregar_mapeamento(turno: str, turma: str) -> dict[Posicao, str] | None:
    """Lê mapeamento.json se existir e for válido; senão, None."""
    arquivo = paths.arquivo_mapeamento(turno, turma)
    if not arquivo.is_file():
        return None
    try:
        with arquivo.open(encoding="utf-8") as f:
            bruto = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    mapa: dict[Posicao, str] = {}
    for chave, nome in bruto.items():
        pos = chave_para_posicao(str(chave))
        if pos is not None and str(nome).strip():
            mapa[pos] = str(nome).strip()
    return mapa or None


def carregar_ou_gerar(turno: str, turma: str, alunos: dict[str, str]) -> dict[Posicao, str]:
    """Carrega o mapeamento salvo ou gera (e persiste) o layout inicial."""
    from services.persistencia import salvar_mapeamento
    mapa = carregar_mapeamento(turno, turma)
    if mapa is not None:
        return mapa
    mapa = gerar_mapeamento_inicial(alunos)
    if mapa:
        salvar_mapeamento(turno, turma, mapa)
    return mapa


def trocar_alunos(mapa: dict[Posicao, str], pos_a: Posicao, pos_b: Posicao) -> None:
    """Troca os ocupantes de duas carteiras (in place)."""
    mapa[pos_a], mapa[pos_b] = mapa[pos_b], mapa[pos_a]


def dimensoes(mapa: dict[Posicao, str]) -> tuple[list[int], int]:
    """Retorna (filas ordenadas, maior posição dentro de uma fila)."""
    if not mapa:
        return [], 0
    filas = sorted({pos[0] for pos in mapa})
    max_posicao = max(pos[1] for pos in mapa)
    return filas, max_posicao
