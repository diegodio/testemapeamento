"""Geração do HTML dos cards de aluno e da carteira vazia."""

import html


def html_card_aluno(nome: str, numero: str | None, foto_uri: str, selecionado: bool) -> str:
    classe = "card-aluno selecionado" if selecionado else "card-aluno"
    nome_seguro = html.escape(nome)
    badge = (
        f'<span class="card-num-badge">{html.escape(str(numero))}</span>'
        if numero is not None
        else ""
    )
    return f"""
    <div class="{classe}">
        {badge}
        <div class="card-foto">
            <img src="{foto_uri}" alt="Foto de {nome_seguro}">
        </div>
        <div class="card-nome" title="{nome_seguro}">{nome_seguro}</div>
    </div>
    """


def html_carteira_vazia() -> str:
    return '<div class="carteira-vazia">vazia</div>'


def html_mesa_professor() -> str:
    return """
    <div class="mesa-professor">
        <span class="selo">★</span>MESA DO PROFESSOR
    </div>
    """


def html_porta() -> str:
    return '<div class="porta-sala">🚪 PORTA</div>'
