"""Persistência do mapeamento em disco (gravação atômica)."""

import json
import os
import tempfile

from services.mapeamento import Posicao, posicao_para_chave
from utils import paths


def salvar_mapeamento(turno: str, turma: str, mapa: dict[Posicao, str]) -> None:
    """Salva o mapeamento como JSON legível, com gravação atômica
    (escreve em arquivo temporário e substitui), evitando corrupção."""
    arquivo = paths.arquivo_mapeamento(turno, turma)
    arquivo.parent.mkdir(parents=True, exist_ok=True)

    ordenado = dict(sorted(mapa.items()))
    serializavel = {posicao_para_chave(pos): nome for pos, nome in ordenado.items()}

    fd, caminho_tmp = tempfile.mkstemp(
        dir=arquivo.parent, prefix=".mapeamento_", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(serializavel, f, ensure_ascii=False, indent=4)
        os.replace(caminho_tmp, arquivo)
    except OSError:
        if os.path.exists(caminho_tmp):
            os.remove(caminho_tmp)
        raise
