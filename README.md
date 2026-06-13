# 🏫 Mapa da Sala

Sistema de mapeamento de salas de aula em Streamlit, com visual escuro inspirado
nas Escolas Cívico-Militares do Paraná, troca de alunos por seleção e salvamento
automático.

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura de dados

```
dados/
├── matutino/
│   └── 3A/
│       ├── alunos.json       # {"1": "Nome", "2": "Nome", ...}
│       ├── mapeamento.json   # {"(fila,posição)": "Nome", ...} — gerado automaticamente
│       ├── 1.jpg             # fotos opcionais (nome = nº da chamada)
│       └── 2.png
└── vespertino/
    └── ...
```

- Se `mapeamento.json` não existir, o sistema distribui os alunos automaticamente
  (5 carteiras por fila, em ordem de chamada — a posição 1 é a carteira da frente, junto à mesa do professor) e salva o arquivo.
- Fotos aceitas: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp` (qualquer caixa).
  Sem foto, é exibido o avatar padrão.

## Como trocar alunos de lugar

1. Toque no botão **⇄** no canto do card do primeiro aluno (ele ganha borda dourada).
2. Toque no **⇄** do segundo aluno.
3. A troca acontece e é salva automaticamente em `mapeamento.json`.


## Arquitetura

```
app.py                    # ponto de entrada
components/               # interface
│   ├── sidebar.py
│   ├── cards.py
│   ├── layout_sala.py
│   └── styles.py
services/                 # regras e dados
│   ├── arquivos.py
│   ├── imagens.py
│   ├── mapeamento.py
│   └── persistencia.py
utils/
│   ├── paths.py
│   └── constantes.py
assets/
    └── avatar_padrao.png
```
