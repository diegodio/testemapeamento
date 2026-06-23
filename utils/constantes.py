"""Constantes globais do sistema."""

# Quantidade de carteiras por fila (profundidade de cada fila) na geração automática
ALUNOS_POR_FILA = 8

# Extensões de imagem aceitas (a busca é case-insensitive)
EXTENSOES_IMAGEM = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

# Ordem de exibição dos turnos na sidebar
TURNOS = ("matutino", "vespertino")

# Rótulos amigáveis para os turnos
ROTULOS_TURNOS = {
    "matutino": "Matutino",
    "vespertino": "Vespertino",
}

# Nomes dos arquivos de dados
ARQUIVO_ALUNOS = "alunos.json"
ARQUIVO_MAPEAMENTO = "mapeamento.json"

# Paleta — Escolas Cívico-Militares do Paraná
COR_AZUL_ESCURO = "#0B1F3A"
COR_AZUL_MEDIO = "#1D4E89"
COR_AZUL_CLARO = "#4F86C6"
COR_DOURADO = "#D4A017"
COR_CINZA_ESCURO = "#1E1E1E"
COR_CINZA_MEDIO = "#444444"
COR_CINZA_CLARO = "#D9D9D9"
