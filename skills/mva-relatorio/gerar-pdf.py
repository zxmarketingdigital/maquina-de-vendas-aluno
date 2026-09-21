#!/usr/bin/env python3
"""Gera, no SEU computador, o PDF do seu relatório da Imersão Máquina de Vendas
Automatizada, juntando o que você já respondeu nas etapas 1 a 4 e o seu plano de 7
dias (quando existir).

Este script não fala com nenhum servidor, não envia nada para ninguém e não precisa
de nenhuma chave de API. Ele só lê arquivos que já estão salvos na sua máquina, em
``~/minha-maquina-de-vendas/``, e escreve o PDF do lado.

Uso::

    ./gerar-pdf.py                       # usa ~/minha-maquina-de-vendas
    ./gerar-pdf.py --pasta /outro/lugar  # usa outra pasta
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


# --- Timeout do PDF: constante nomeada + override por env var (nunca chumbado). --- #
def _env_timeout(nome: str, default: float) -> float:
    """Lê timeout de uma env var; valor ausente, inválido, zero ou negativo cai no default."""
    bruto = os.environ.get(nome, "")
    try:
        valor = float(bruto)
    except (TypeError, ValueError):
        return default
    return valor if valor > 0 else default


PDF_TIMEOUT = _env_timeout("MVA_PDF_TIMEOUT", 600.0)

TZ_BR = timezone(timedelta(hours=-3))

NOME_ARQUIVO_PDF = "meu-relatorio.pdf"
NOME_ARQUIVO_PERFIL = "perfil.json"
NOME_ARQUIVO_PLANO = "PLANO-7-DIAS.md"

# Ordem fixa 1→4. O arquivo é o que a etapa concluída grava; o comando é o que o
# aluno roda para completar a etapa quando o arquivo ainda não existe.
ETAPAS = (
    (1, "Diagnóstico — onde você trava pra vender", "01-diagnostico.md", "/mva-diagnostico"),
    (2, "Oferta", "02-oferta.md", "/mva-oferta"),
    (3, "Máquina de leads", "03-maquina.md", "/mva-maquina"),
    (4, "Conversa", "04-conversa.md", "/mva-conversa"),
)


# --------------------------------------------------------------------------- #
# util
# --------------------------------------------------------------------------- #
def slugify(texto: str) -> str:
    base = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base or "aluno"


def agora_br() -> datetime:
    return datetime.now(TZ_BR)


# --------------------------------------------------------------------------- #
# ler o que o aluno já produziu
# --------------------------------------------------------------------------- #
def carregar_perfil(pasta: Path) -> dict:
    """perfil.json ausente ou corrompido não é erro fatal aqui — o nome do aluno
    vira "Aluno" e o resto do relatório segue montado a partir dos .md das etapas."""
    import json

    caminho = pasta / NOME_ARQUIVO_PERFIL
    if not caminho.exists():
        return {}
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        return dados if isinstance(dados, dict) else {}
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return {}


def nome_do_aluno(perfil: dict) -> str:
    aluno = perfil.get("aluno")
    if isinstance(aluno, dict):
        nome = str(aluno.get("nome") or "").strip()
        if nome:
            return nome
    elif isinstance(aluno, str) and aluno.strip():
        return aluno.strip()
    return "Aluno"


def etapas_concluidas(pasta: Path) -> int:
    total = 0
    for _, _, nome_arquivo, _ in ETAPAS:
        caminho = pasta / nome_arquivo
        if caminho.exists() and caminho.read_text(encoding="utf-8", errors="replace").strip():
            total += 1
    return total


def rebaixar_titulos(texto: str, niveis: int = 2) -> str:
    """O arquivo de cada etapa abre com o próprio `# Título`. Como ele entra debaixo
    de um `## Etapa N`, o H1 original inverteria a hierarquia e duplicaria o título
    na página. Rebaixar em `niveis` mantém a estrutura do relatório correta sem
    reescrever o texto do aluno. Linha dentro de bloco de código nunca é cabeçalho.
    """
    saida: list[str] = []
    em_codigo = False
    for linha in texto.split("\n"):
        if linha.lstrip().startswith("```"):
            em_codigo = not em_codigo
            saida.append(linha)
            continue
        if not em_codigo and linha.startswith("#"):
            marcas = len(linha) - len(linha.lstrip("#"))
            resto = linha[marcas:]
            if resto.startswith(" ") or resto == "":
                saida.append("#" * min(marcas + niveis, 6) + resto)
                continue
        saida.append(linha)
    return "\n".join(saida)


# --------------------------------------------------------------------------- #
# markdown do relatório — nunca inventa conteúdo, só junta o que já existe
# --------------------------------------------------------------------------- #
def montar_markdown(pasta: Path) -> str:
    perfil = carregar_perfil(pasta)
    nome = nome_do_aluno(perfil)
    data = agora_br().strftime("%d/%m/%Y")

    linhas: list[str] = []
    add = linhas.append

    add(f"# Máquina de Vendas — {nome}")
    add("")
    add(f"**Imersão Máquina de Vendas Automatizada · relatório gerado em {data}**")
    add("")
    add("Este relatório reúne o que você já registrou em cada etapa, direto dos "
        "arquivos salvos no seu computador.")
    add("")

    for numero, titulo, nome_arquivo, comando in ETAPAS:
        caminho = pasta / nome_arquivo
        add(f"## Etapa {numero} — {titulo}")
        add("")
        conteudo = caminho.read_text(encoding="utf-8", errors="replace").strip() if caminho.exists() else ""
        if conteudo:
            add(rebaixar_titulos(conteudo))
        else:
            add(f"_Você ainda não concluiu esta etapa. Rode `{comando}` no seu Claude Code "
                "para completá-la._")
        add("")

    plano = pasta / NOME_ARQUIVO_PLANO
    if plano.exists():
        conteudo_plano = plano.read_text(encoding="utf-8", errors="replace").strip()
        if conteudo_plano:
            add("## Seu plano de 7 dias")
            add("")
            add(rebaixar_titulos(conteudo_plano))
            add("")

    add("---")
    add("")
    add("Um abraço,")
    add("")
    add("Rafael Castro")
    add("")
    add("Fundador da ZX LAB")
    add("")
    return "\n".join(linhas)


# --------------------------------------------------------------------------- #
# markdown -> html (subconjunto controlado; sem dependência externa)
# --------------------------------------------------------------------------- #
def _inline(texto: str) -> str:
    out = (texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"_(.+?)_", r"<em>\1</em>", out)
    out = re.sub(r"`(.+?)`", r"<code>\1</code>", out)
    out = out.replace("\\|", "|")
    return out


def markdown_para_html(md: str) -> str:
    html: list[str] = []
    linhas = md.split("\n")
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        if linha.lstrip().startswith("```"):
            # Dentro do bloco nada é markdown: o texto vai literal, só escapado.
            i += 1
            codigo = []
            while i < len(linhas) and not linhas[i].lstrip().startswith("```"):
                codigo.append(linhas[i])
                i += 1
            escapado = "\n".join(
                l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                for l in codigo)
            html.append(f"<pre>{escapado}</pre>")
        elif linha.startswith("### "):
            html.append(f"<h3>{_inline(linha[4:])}</h3>")
        elif linha.startswith("## "):
            html.append(f"<h2>{_inline(linha[3:])}</h2>")
        elif linha.startswith("# "):
            html.append(f"<h1>{_inline(linha[2:])}</h1>")
        elif linha.strip() == "---":
            html.append("<hr/>")
        elif linha.startswith("|"):
            tabela = []
            while i < len(linhas) and linhas[i].startswith("|"):
                tabela.append(linhas[i])
                i += 1
            i -= 1
            corpo = [l for l in tabela if not re.match(r"^\|[\s\-:|]+\|$", l)]
            if corpo:
                html.append("<table>")
                cabecalho, *resto = corpo
                cels = [c.strip() for c in cabecalho.strip("|").split("|")]
                html.append("<thead><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cels) + "</tr></thead>")
                html.append("<tbody>")
                for l in resto:
                    cels = [c.strip() for c in l.strip("|").split("|")]
                    html.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cels) + "</tr>")
                html.append("</tbody></table>")
        elif linha.startswith("> "):
            citacao = []
            while i < len(linhas) and linhas[i].startswith("> "):
                citacao.append(linhas[i][2:])
                i += 1
            i -= 1
            html.append("<blockquote>" + " ".join(_inline(x) for x in citacao) + "</blockquote>")
        elif re.match(r"^\d+[.)] ", linha):
            itens = []
            while i < len(linhas) and re.match(r"^\d+[.)] ", linhas[i]):
                itens.append(re.sub(r"^\d+[.)] ", "", linhas[i]))
                i += 1
            i -= 1
            html.append("<ol>" + "".join(f"<li>{_inline(x)}</li>" for x in itens) + "</ol>")
        elif linha.startswith("- "):
            itens = []
            while i < len(linhas) and linhas[i].startswith("- "):
                itens.append(linhas[i][2:])
                i += 1
            i -= 1
            html.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in itens) + "</ul>")
        elif linha.strip():
            html.append(f"<p>{_inline(linha)}</p>")
        i += 1
    return "\n".join(html)


CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm;
        @bottom-center { content: "Imersão Máquina de Vendas Automatizada · ZX LAB · página " counter(page);
                         font-family: Inter, Helvetica, sans-serif; font-size: 8pt; color: #78716c; } }
body { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.55;
       color: #1c1917; }
h1 { font-size: 21pt; color: #0c0a09; margin: 0 0 4pt; letter-spacing: -.4pt; }
h1 + p { color: #78716c; font-size: 9pt; text-transform: uppercase; letter-spacing: .6pt; }
h2 { font-size: 14pt; color: #0c0a09; margin: 20pt 0 6pt; padding-bottom: 4pt;
     border-bottom: 2px solid #D97706; page-break-after: avoid; }
h3 { font-size: 11pt; color: #44403c; margin: 14pt 0 4pt; page-break-after: avoid; }
p { margin: 0 0 7pt; }
strong { color: #0c0a09; }
em { color: #78716c; font-style: italic; }
code { font-family: "JetBrains Mono", Menlo, monospace; font-size: 9pt;
       background: #f5f5f4; padding: 1pt 3pt; border-radius: 3px; color: #92400e; }
ul, ol { margin: 0 0 8pt; padding-left: 16pt; }
li { margin-bottom: 3pt; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0 12pt; font-size: 9pt;
        page-break-inside: avoid; }
th { background: #1c1917; color: #fafaf9; text-align: left; padding: 5pt 7pt;
     font-weight: 600; font-size: 8.5pt; text-transform: uppercase; letter-spacing: .4pt; }
td { padding: 5pt 7pt; border-bottom: 1px solid #e7e5e4; vertical-align: top; }
tr:nth-child(even) td { background: #fafaf9; }
blockquote { margin: 8pt 0 12pt; padding: 8pt 12pt; background: #fffbeb;
             border-left: 3px solid #D97706; font-size: 11pt; color: #451a03;
             page-break-inside: avoid; }
blockquote em { color: #451a03; font-style: normal; font-weight: 600; }
pre { font-family: "JetBrains Mono", Menlo, monospace; font-size: 8.5pt; line-height: 1.45;
      background: #f5f5f4; border-left: 3px solid #d6d3d1; padding: 7pt 9pt;
      margin: 6pt 0 10pt; white-space: pre-wrap; word-break: break-word;
      color: #1c1917; page-break-inside: avoid; }
hr { border: none; border-top: 1px solid #e7e5e4; margin: 18pt 0 10pt; }
"""


# Caminhos fixos de Chrome/Chromium/Edge por sistema. A regra é cobrir os três
# sistemas: o Claude Code roda em macOS, Windows e Linux, e é justamente no
# Windows que o weasyprint costuma faltar — se o navegador também não fosse
# encontrado lá, o aluno de Windows nunca teria PDF, só o HTML de fallback.
CHROME_PATHS_DARWIN = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)
CHROME_PATHS_WINDOWS = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
)
# Nomes procurados no PATH — cobre Linux e também Windows, onde o instalador
# frequentemente deixa o executável acessível por nome.
CHROME_BINARIOS_PATH = ("google-chrome", "google-chrome-stable", "chromium",
                        "chromium-browser", "chrome", "msedge", "microsoft-edge")


def chrome_paths_do_sistema() -> tuple[str, ...]:
    if sys.platform == "darwin":
        return CHROME_PATHS_DARWIN
    if sys.platform.startswith("win"):
        localappdata = os.environ.get("LOCALAPPDATA", "")
        extras = ((os.path.join(localappdata, r"Google\Chrome\Application\chrome.exe"),)
                  if localappdata else ())
        return CHROME_PATHS_WINDOWS + extras
    return ()


def _documento_html(md: str) -> str:
    corpo = markdown_para_html(md)
    return (f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{corpo}</body></html>")


def _preparar_libs_nativas() -> None:
    """weasyprint carrega pango/cairo por dlopen e no macOS o Homebrew não está no
    caminho padrão do dyld. Sem isto o import falha com OSError libgobject e o
    relatório cai silenciosamente pro fallback do navegador (sem numeração de
    página). Setar aqui evita depender de env var na linha de comando."""
    if sys.platform != "darwin":
        return
    candidatos = [p for p in ("/opt/homebrew/lib", "/usr/local/lib") if Path(p).is_dir()]
    if not candidatos:
        return
    atual = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    partes = [x for x in atual.split(":") if x]
    for c in candidatos:
        if c not in partes:
            partes.append(c)
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(partes)


def _pdf_por_weasyprint(md: str, destino: Path) -> bool:
    """Engine preferida: respeita @page e numera as páginas.

    Roda em SUBPROCESSO porque ``write_pdf`` não aceita timeout: um dlopen
    travado ou um documento patológico prenderia o script para sempre, sem
    elapsed no log. No subprocesso o teto é o mesmo PDF_TIMEOUT do navegador.
    """
    import subprocess
    import tempfile

    _preparar_libs_nativas()
    with tempfile.TemporaryDirectory() as tmp:
        origem = Path(tmp) / "doc.html"
        origem.write_text(_documento_html(md), encoding="utf-8")
        codigo = (
            "import sys;from weasyprint import HTML;"
            "HTML(filename=sys.argv[1]).write_pdf(sys.argv[2])"
        )
        t0 = time.monotonic()
        try:
            proc = subprocess.run([sys.executable, "-c", codigo, str(origem), str(destino)],
                                  capture_output=True, timeout=PDF_TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"[gerar-pdf] weasyprint estourou o teto de {PDF_TIMEOUT:.0f}s "
                  f"(ajuste com MVA_PDF_TIMEOUT); tentando navegador.", file=sys.stderr)
            return False
        elapsed = time.monotonic() - t0
        if proc.returncode != 0:
            detalhe = proc.stderr.decode(errors="replace").strip().splitlines()
            print(f"[gerar-pdf] weasyprint indisponível ({detalhe[-1] if detalhe else proc.returncode}); "
                  "tentando navegador.", file=sys.stderr)
            return False
        print(f"[gerar-pdf] PDF levou {elapsed:.0f}s (teto {PDF_TIMEOUT:.0f}s) — weasyprint")
    return destino.exists() and destino.stat().st_size > 0


def _pdf_por_navegador(md: str, destino: Path) -> bool:
    """Fallback: Chrome/Chromium/Edge headless. Sem numeração de página."""
    import shutil
    import subprocess
    import tempfile

    binario = next((c for c in chrome_paths_do_sistema() if Path(c).exists()), None)
    if not binario:
        for nome_bin in CHROME_BINARIOS_PATH:
            achado = shutil.which(nome_bin)
            if achado:
                binario = achado
                break
    if not binario:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        origem = Path(tmp) / "relatorio.html"
        origem.write_text(_documento_html(md), encoding="utf-8")
        cmd = [binario, "--headless=new", "--disable-gpu", "--no-sandbox",
               "--no-pdf-header-footer", f"--user-data-dir={tmp}/perfil",
               f"--print-to-pdf={destino}", origem.as_uri()]
        t0 = time.monotonic()
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=PDF_TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"[gerar-pdf] navegador estourou o teto de {PDF_TIMEOUT:.0f}s "
                  f"(ajuste com MVA_PDF_TIMEOUT)", file=sys.stderr)
            return False
        print(f"[gerar-pdf] PDF levou {time.monotonic() - t0:.0f}s "
              f"(teto {PDF_TIMEOUT:.0f}s) — navegador")
        if proc.returncode != 0 and not destino.exists():
            print(f"[gerar-pdf] navegador saiu {proc.returncode}: "
                  f"{proc.stderr.decode(errors='replace')[:300]}", file=sys.stderr)
            return False
    return destino.exists() and destino.stat().st_size > 0


def render_pdf(md: str, destino: Path) -> tuple[bool, Path]:
    """Tenta weasyprint, depois navegador headless. Só devolve sucesso quando o
    arquivo EXISTE e tem bytes — exit 0 de engine não é prova de PDF escrito.

    Se as duas engines falharem, salva o `.html` ao lado do PDF pretendido e
    devolve (False, caminho_do_html) — você ainda fica com o relatório pronto,
    só não em PDF.
    """
    import shutil
    import tempfile

    destino.parent.mkdir(parents=True, exist_ok=True)
    # Gerar num arquivo provisório e só então substituir: se as duas engines
    # falharem, o PDF que o aluno já tinha continua intacto. Apagar o destino
    # antes de tentar trocaria uma falha de engine por perda de arquivo dele.
    with tempfile.TemporaryDirectory() as tmp:
        provisorio = Path(tmp) / NOME_ARQUIVO_PDF
        for engine in (_pdf_por_weasyprint, _pdf_por_navegador):
            if engine(md, provisorio):
                shutil.move(str(provisorio), str(destino))
                return True, destino
            if provisorio.exists():
                provisorio.unlink()  # sobra de tentativa falha nunca vira "sucesso"
    destino_html = destino.with_suffix(".html")
    destino_html.write_text(_documento_html(md), encoding="utf-8")
    return False, destino_html


# --------------------------------------------------------------------------- #
# orquestração
# --------------------------------------------------------------------------- #
def main() -> int:
    p = argparse.ArgumentParser(
        description="Gera, no seu computador, o PDF do seu relatório da Imersão Máquina de Vendas Automatizada.")
    p.add_argument("--pasta", type=Path, default=Path.home() / "minha-maquina-de-vendas",
                   help="Pasta com seus arquivos da imersão (padrão: ~/minha-maquina-de-vendas).")
    args = p.parse_args()
    pasta = args.pasta.expanduser()

    if not pasta.exists():
        print(f"Não encontrei a pasta {pasta}.")
        print("Rode /maquina-de-vendas no seu Claude Code para começar a imersão.")
        return 1

    if etapas_concluidas(pasta) == 0:
        print("Você ainda não concluiu nenhuma etapa da imersão — por isso não há "
              "nada para colocar no relatório ainda.")
        print("Rode /maquina-de-vendas no seu Claude Code para começar.")
        return 1

    md = montar_markdown(pasta)
    nome = nome_do_aluno(carregar_perfil(pasta))
    destino_pdf = pasta / NOME_ARQUIVO_PDF

    inicio = time.monotonic()
    sucesso, caminho = render_pdf(md, destino_pdf)
    print(f"[gerar-pdf] total: {time.monotonic() - inicio:.0f}s (teto {PDF_TIMEOUT:.0f}s) "
          f"— relatório de {nome} ({slugify(nome)})")

    if sucesso:
        print(f"\nPronto! Seu relatório saiu em PDF: {caminho}")
        return 0

    print(f"\nNão consegui gerar o PDF automaticamente neste computador, mas o seu "
          f"relatório está pronto em HTML: {caminho}")
    print("Abra esse arquivo no seu navegador e use Arquivo > Imprimir > Salvar como PDF "
          "para terminar de gerar o seu PDF.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
