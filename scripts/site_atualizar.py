"""Atualiza as partes automáticas do site bemcontadopt.pt (branch claude/site).

Só mexe em ultima/ e em prazos/. O resto do site é editado à mão na pasta site/ do branch por defeito.

Uso:
  python3 site_atualizar.py ultima --site /tmp/site --imagem slide_1.png --data 2026-11-21 \
      --tema "40 anos do IVA em Portugal" --permalink https://www.instagram.com/p/XXXX/ --alt "Descrição da imagem"
  python3 site_atualizar.py prazos --site /tmp/site --dados prazos.json [--permalink https://www.instagram.com/p/XXXX/]
  python3 site_atualizar.py prazos --site /tmp/site --espera 2026-11-23      (página de espera até à primeira lista)

prazos.json:
  {"semana_inicio": "2026-11-23", "semana_fim": "2026-11-29",
   "prazos": [{"data": "2026-11-25", "titulo": "...", "quem": "...", "descricao": "...", "fonte": "https://..."}]}
Cada prazo tem de ter os cinco campos; a fonte é o endereço da página oficial lida. A fonte não aparece no site,
mas é obrigatória: serve para confirmar cada prazo antes de publicar. Sem travessões.
"""
import argparse
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
DIAS_CURTOS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
MESES_CURTOS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
e = html.escape


def falha(msg):
    sys.exit(f"ERRO: {msg}")


def sem_travessoes(texto, onde):
    if "—" in texto or "–" in texto:
        falha(f"travessão em {onde}: {texto[:60]}")


def data_iso(s, onde):
    try:
        return date.fromisoformat(s)
    except Exception:
        falha(f"data inválida em {onde}: {s!r} (usar AAAA-MM-DD)")


def por_extenso(d):
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def intervalo(a, b):
    if a.year == b.year and a.month == b.month:
        return f"{a.day} a {b.day} de {MESES[a.month - 1]} de {a.year}"
    if a.year == b.year:
        return f"{a.day} de {MESES[a.month - 1]} a {b.day} de {MESES[b.month - 1]} de {a.year}"
    return f"{por_extenso(a)} a {por_extenso(b)}"


# ---------------------------------------------------------------- última publicação

def ultima(args):
    site = Path(args.site)
    if not (site / "index.html").exists():
        falha(f"{site} não parece ser o site (falta index.html)")
    if not re.match(r"^https://www\.instagram\.com/", args.permalink):
        falha("o permalink tem de começar por https://www.instagram.com/")
    d = data_iso(args.data, "--data")
    for campo in ("tema", "alt"):
        sem_travessoes(getattr(args, campo), campo)
    origem = Path(args.imagem)
    if not origem.exists():
        falha(f"imagem não encontrada: {origem}")
    ext = origem.suffix.lower()
    if ext not in (".png", ".jpg", ".jpeg", ".webp"):
        falha("a imagem tem de ser png, jpg ou webp")
    pasta = site / "ultima"
    pasta.mkdir(exist_ok=True)
    for antiga in pasta.glob("imagem.*"):
        antiga.unlink()
    destino = pasta / f"imagem{ext}"
    shutil.copyfile(origem, destino)
    dados = {"data": d.isoformat(), "tema": args.tema, "permalink": args.permalink, "alt": args.alt,
             "imagem": f"ultima/{destino.name}", "v": d.strftime("%Y%m%d") + re.sub(r"\W", "", args.permalink)[-8:]}
    (pasta / "dados.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"ok: {pasta / 'dados.json'} e {destino}")


# ---------------------------------------------------------------- página de prazos

CALENDARIO = """<svg class="desenho" viewBox="0 0 400 330" role="img" aria-label="Desenho de um calendário com um dia marcado a âmbar">
      <g class="mao">
        <path class="tr d1" d="M70 66 L330 62 L334 292 L74 296 Z"/>
        <path class="tr d2" d="M70 116 H332"/>
        <path class="tr d2" d="M128 40 V86 M272 40 V86"/>
        <path class="tr d3 fino claro" d="M108 156 H140 M168 156 H200 M228 156 H260 M288 156 H310 M108 206 H140 M168 206 H200 M288 206 H310 M108 256 H140 M168 256 H200 M228 256 H260"/>
        <path class="tr d4 ambar" d="M214 186 Q 246 176 272 192 Q 286 214 262 228 Q 232 238 214 222 Q 202 204 214 186"/>
        <path class="tr d5 ambar" d="M226 206 l10 11 l22 -24"/>
      </g>
    </svg>"""


def pagina(titulo_pagina, descricao, corpo):
    return f"""<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo_pagina)}</title>
<meta name="description" content="{e(descricao)}">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data: https://bemcontadopt.goatcounter.com; base-uri 'none'; form-action 'none'; object-src 'none'">
<meta property="og:title" content="{e(titulo_pagina)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:image" content="https://bemcontadopt.pt/og.png">
<meta property="og:url" content="https://bemcontadopt.pt/prazos/">
<link rel="canonical" href="https://bemcontadopt.pt/prazos/">
<meta name="theme-color" content="#F7F5F0">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="preload" href="../fonts/manrope-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../estilo.css">
<script src="../site.js"></script>
</head>
<body>
<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false">
  <filter id="traco"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>
</svg>
<header class="topo wrap">
  <a class="marca" href="../" aria-label="bem.contado, início">bem<svg class="ponto" viewBox="0 0 10 10" aria-hidden="true"><rect x="1" y="1.6" width="8" height="8"/></svg>contado</a>
  <nav aria-label="Ligações">
    <a href="../prazos/" aria-current="page">Prazos</a>
    <a href="https://www.instagram.com/bem.contadopt/">Instagram</a>
    <a href="https://poupanca.bemcontadopt.pt/instalar/">App Poupança</a>
  </nav>
</header>
<main>
{corpo}
</main>
<footer class="wrap">
  <svg class="linha" viewBox="0 0 1000 20" preserveAspectRatio="none" aria-hidden="true"><path class="pontilhado" d="M0 10 C 250 4, 520 16, 1000 8"/></svg>
  <div class="rodape">
    <p class="marca" aria-label="bem.contado">bem<svg class="ponto" viewBox="0 0 10 10" aria-hidden="true"><rect x="1" y="1.6" width="8" height="8"/></svg>contado</p>
    <p><a href="../">Início</a> · <a href="https://www.instagram.com/bem.contadopt/">Instagram</a> · <a href="https://poupanca.bemcontadopt.pt/instalar/">App Poupança</a> · <a href="mailto:bem.contado@outlook.pt">bem.contado@outlook.pt</a></p>
  </div>
  <p class="nota">Este site conta as visitas de forma anónima e sem cookies. Não recolhe dados pessoais. A informação publicada é geral e não substitui a análise de cada caso.</p>
</footer>
</body>
</html>
"""


def prazos(args):
    site = Path(args.site)
    if not (site / "index.html").exists():
        falha(f"{site} não parece ser o site (falta index.html)")
    pasta = site / "prazos"
    pasta.mkdir(exist_ok=True)

    if args.espera:
        data_iso(args.espera, "--espera")  # validada, mas já não é mostrada na página
        corpo = f"""  <section class="hero wrap">
    <div class="texto">
      <p class="antes">Atualizado à segunda-feira</p>
      <h1>Prazos da semana</h1>
      <p class="sub">Todas as segundas-feiras juntamos aqui os prazos fiscais e da Segurança Social dessa semana que interessam a particulares, trabalhadores independentes e empresas, cada um com a fonte oficial.</p>
      <p class="acoes"><a class="btn" href="https://www.instagram.com/bem.contadopt/" data-contar="instagram-prazos">Seguir no Instagram</a></p>
    </div>
    {CALENDARIO}
  </section>"""
        (pasta / "index.html").write_text(pagina("Prazos da semana · bem.contado",
            "Os prazos fiscais e da Segurança Social de cada semana, com a fonte oficial. Atualizado à segunda-feira.", corpo), encoding="utf-8")
        print(f"ok: página de espera em {pasta / 'index.html'}")
        return

    try:
        dados = json.loads(Path(args.dados).read_text(encoding="utf-8"))
    except Exception as ex:
        falha(f"não consegui ler {args.dados}: {ex}")
    ini = data_iso(dados.get("semana_inicio", ""), "semana_inicio")
    fim = data_iso(dados.get("semana_fim", ""), "semana_fim")
    if fim < ini:
        falha("semana_fim é anterior a semana_inicio")
    lista = dados.get("prazos")
    if not isinstance(lista, list):
        falha("falta a lista 'prazos'")
    itens = []
    for n, p in enumerate(sorted(lista, key=lambda x: x.get("data", "")), 1):
        for campo in ("data", "titulo", "quem", "descricao", "fonte"):
            if not str(p.get(campo, "")).strip():
                falha(f"prazo {n}: falta o campo '{campo}'")
            sem_travessoes(str(p[campo]), f"prazo {n}, {campo}")
        d = data_iso(p["data"], f"prazo {n}")
        if not re.match(r"^https://", p["fonte"]):
            falha(f"prazo {n}: a fonte tem de ser um endereço https://")
        itens.append(f"""      <li class="prazo">
        <p class="dia"><span class="semana">{DIAS_CURTOS[d.weekday()]}</span><span class="numero">{d.day}</span><span class="mes">{MESES_CURTOS[d.month - 1]}</span></p>
        <div>
          <h2>{e(p["titulo"])}</h2>
          <p class="quem">Para quem: {e(p["quem"])}</p>
          <p>{e(p["descricao"])}</p>
        </div>
      </li>""")
    lista_html = ("    <ol class=\"prazos\">\n" + "\n".join(itens) + "\n    </ol>") if itens else \
        "    <p>Não encontrámos prazos relevantes para esta semana nas fontes oficiais.</p>"
    permalink = args.permalink or dados.get("permalink") or ""
    if permalink and not re.match(r"^https://www\.instagram\.com/", permalink):
        falha("o permalink tem de começar por https://www.instagram.com/")
    ligacao_insta = f' <a class="ligacao" href="{e(permalink)}" data-contar="prazos-publicacao">Ver a publicação no Instagram</a>' if permalink else ""
    corpo = f"""  <section class="hero wrap">
    <div class="texto">
      <p class="antes">Semana de {intervalo(ini, fim)}</p>
      <h1>Prazos da semana</h1>
      <p class="sub">Os prazos fiscais e da Segurança Social desta semana que interessam a particulares, trabalhadores independentes e empresas. Atualizado à segunda-feira.</p>
      <p class="ligacoes"><a class="ligacao" href="#lista">Ver a lista</a>{ligacao_insta}</p>
    </div>
    {CALENDARIO}
  </section>
  <section class="wrap" id="lista">
{lista_html}
    <p class="aviso">Informação geral. Os prazos podem ser prorrogados por despacho: antes de entregar ou pagar, confirme sempre na fonte oficial.</p>
  </section>"""
    (pasta / "index.html").write_text(pagina(f"Prazos da semana de {intervalo(ini, fim)} · bem.contado",
        f"Prazos fiscais e da Segurança Social da semana de {intervalo(ini, fim)}, com a fonte oficial.", corpo), encoding="utf-8")
    print(f"ok: {len(itens)} prazos em {pasta / 'index.html'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("ultima")
    for a in ("--site", "--imagem", "--data", "--tema", "--permalink", "--alt"):
        u.add_argument(a, required=True)
    p = sub.add_parser("prazos")
    p.add_argument("--site", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dados")
    g.add_argument("--espera")
    p.add_argument("--permalink")
    args = ap.parse_args()
    {"ultima": ultima, "prazos": prazos}[args.cmd](args)


if __name__ == "__main__":
    main()
