"""Atualiza as partes automáticas do site bemcontadopt.pt (branch claude/site).

Só mexe em ultima/ e em prazos/ (incluindo prazos/calendario.json e prazos/ics/). O resto do site é editado à mão na pasta site/ do branch por defeito.

Uso:
  python3 site_atualizar.py ultima --site /tmp/site --imagem slide_1.png --data 2026-11-21 \
      --tema "40 anos do IVA em Portugal" --permalink https://www.instagram.com/p/XXXX/ --alt "Descrição da imagem"
  python3 site_atualizar.py prazos --site /tmp/site --dados prazos.json [--permalink https://www.instagram.com/p/XXXX/]
  python3 site_atualizar.py prazos --site /tmp/site --espera 2026-11-23      (página sem a lista da semana)
  python3 site_atualizar.py calendario --site /tmp/site --dados calendario.json

calendario.json (a ferramenta "Os teus prazos", com filtro por perfil e ficheiros .ics):
  {"atualizado": "2026-11-22", "ate": "2026-12-31", "falta": "frase opcional sobre o que ainda não está na lista",
   "prazos": [{"data": "2026-12-21", "titulo": "...", "descricao": "...", "nota": "opcional",
               "quem": ["iva_mensal"], "fonte": "https://..."}]}
  "quem" usa estas etiquetas (o prazo aparece a quem tiver pelo menos uma):
    carro          quem tem carro (IUC)
    casa           quem tem casa ou outro imóvel (IMI)
    atividade      independentes e empresas
    independente   trabalhadores independentes (os dois regimes)
    empresa        sociedades (IRC)
    retencao       quem faz retenções na fonte: empresas, independentes com contabilidade organizada, quem tem trabalhadores
    empregador     quem tem trabalhadores
    iva_isento     isentos de IVA (artigo 53.º)
    iva_trimestral IVA trimestral
    iva_mensal     IVA mensal

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
import hashlib
from datetime import date, datetime, timedelta, timezone
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


def pagina(titulo_pagina, descricao, corpo, extra_head='<script src="prazos.js" defer></script>'):
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
{extra_head}
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


FERRAMENTA = """  <section class="wrap ferramenta" id="teus" aria-labelledby="t-teus">
    <h2 id="t-teus">Os teus prazos</h2>
    <p class="sub">Escolhe o teu caso e vê só os prazos das Finanças e da Segurança Social que te dizem respeito. Depois, se quiseres, junta-os ao calendário do telemóvel.</p>
    <form class="perfil" id="perfil" aria-label="O teu caso">
      <fieldset>
        <legend>A tua situação</legend>
        <label><input type="radio" name="s" value="p" checked> Particular (só salário ou pensão)</label>
        <label><input type="radio" name="s" value="s"> Trabalhador independente, regime simplificado</label>
        <label><input type="radio" name="s" value="o"> Trabalhador independente, contabilidade organizada</label>
        <label><input type="radio" name="s" value="e"> Empresa (sociedade)</label>
      </fieldset>
      <fieldset class="so-atividade">
        <legend>IVA</legend>
        <label><input type="radio" name="i" value="x" checked> Isento (artigo 53.º)</label>
        <label><input type="radio" name="i" value="t"> Trimestral</label>
        <label><input type="radio" name="i" value="m"> Mensal</label>
      </fieldset>
      <fieldset>
        <legend>Também tens</legend>
        <label class="so-atividade"><input type="checkbox" name="t"> Trabalhadores</label>
        <label><input type="checkbox" name="c" checked> Carro</label>
        <label><input type="checkbox" name="h" checked> Casa ou outro imóvel</label>
      </fieldset>
    </form>
    <noscript><p>Para filtrar os prazos é preciso ter o JavaScript ligado.</p></noscript>
    <div id="lista-teus" aria-live="polite"></div>
    <div class="calendario-acoes" id="cal" hidden>
      <h3>Juntar ao calendário</h3>
      <p>Só com os prazos do caso que escolheste, com aviso três dias antes e na véspera.</p>
      <p class="ligacoes">
        <a class="ligacao" id="cal-google" href="#" target="_blank" rel="noopener" data-contar="calendario-google">Google Calendar (Android)</a>
        <a class="ligacao" id="cal-sub" href="#" data-contar="calendario-apple">iPhone ou Mac</a>
        <a class="ligacao" id="cal-outlook" href="#" target="_blank" rel="noopener" data-contar="calendario-outlook">Outlook</a>
      </p>
      <p class="pequeno">Assim o calendário fica subscrito: quando acrescentarmos prazos, aparecem sozinhos, sem teres de voltar aqui. No Google Calendar pede para entrares na conta Google e confirmares; depois aparece também na app do telemóvel (se não aparecer, na app vai a Definições e liga o calendário "Prazos (bem.contado)").</p>
      <p class="pequeno">Outra aplicação? <a id="cal-ics" href="#" download data-contar="calendario-descarregar">Descarrega o ficheiro .ics</a> (fica como está, não atualiza) ou <button class="texto" type="button" id="cal-copiar" data-contar="calendario-copiar">copia o endereço</button> para subscrever.</p>
    </div>
    <p class="aviso">Informação geral, a partir da agenda fiscal da Autoridade Tributária e da Segurança Social. Mostramos os prazos mais comuns: há obrigações para casos específicos (operações com outros países da União Europeia, imposto do selo, setores especiais) que não estão aqui. Os prazos podem ser prorrogados por despacho, por isso confirma sempre antes de entregar ou pagar.</p>
  </section>"""


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
      <p class="antes">Finanças e Segurança Social</p>
      <h1>Prazos</h1>
      <p class="sub">Os prazos fiscais e da Segurança Social que estão a chegar, filtrados para o teu caso. Às segundas-feiras publicamos também os da semana no Instagram.</p>
      <p class="ligacoes"><a class="ligacao" href="#teus">Ver os teus prazos</a> <a class="ligacao" href="https://www.instagram.com/bem.contadopt/" data-contar="instagram-prazos">Seguir no Instagram</a></p>
    </div>
    {CALENDARIO}
  </section>
{FERRAMENTA}"""
        (pasta / "index.html").write_text(pagina("Prazos fiscais e da Segurança Social · bem.contado",
            "Os prazos das Finanças e da Segurança Social filtrados para o teu caso: particular, trabalhador independente ou empresa, IVA mensal ou trimestral. Com ficheiro para o calendário.", corpo), encoding="utf-8")
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
          <h3>{e(p["titulo"])}</h3>
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
      <p class="antes">Finanças e Segurança Social</p>
      <h1>Prazos</h1>
      <p class="sub">Os prazos fiscais e da Segurança Social que estão a chegar, filtrados para o teu caso. Mais abaixo, os desta semana, que também publicámos no Instagram.</p>
      <p class="ligacoes"><a class="ligacao" href="#teus">Ver os teus prazos</a> <a class="ligacao" href="#lista">Esta semana</a>{ligacao_insta}</p>
    </div>
    {CALENDARIO}
  </section>
{FERRAMENTA}
  <section class="wrap semana" id="lista" aria-labelledby="t-semana">
    <h2 id="t-semana">Esta semana: {intervalo(ini, fim)}</h2>
{lista_html}
    <p class="aviso">Informação geral. Os prazos podem ser prorrogados por despacho: antes de entregar ou pagar, confirme sempre na fonte oficial.</p>
  </section>"""
    (pasta / "index.html").write_text(pagina("Prazos fiscais e da Segurança Social · bem.contado",
        f"Os prazos das Finanças e da Segurança Social filtrados para o teu caso, com ficheiro para o calendário. Esta semana: {intervalo(ini, fim)}.", corpo), encoding="utf-8")
    print(f"ok: {len(itens)} prazos em {pasta / 'index.html'}")


ETIQUETAS = {"carro", "casa", "atividade", "independente", "empresa", "retencao", "empregador",
             "iva_isento", "iva_trimestral", "iva_mensal"}
IVA = {"x": "iva_isento", "t": "iva_trimestral", "m": "iva_mensal"}


def etiquetas_do_perfil(s, i, t, c, h):
    """O mesmo cálculo que prazos.js faz no browser."""
    et = set()
    if c:
        et.add("carro")
    if h:
        et.add("casa")
    if s != "p":
        et |= {"atividade", IVA[i]}
        if s in "so":
            et.add("independente")
        if s in "oe":
            et.add("retencao")
        if s == "e":
            et.add("empresa")
        if t:
            et |= {"empregador", "retencao"}
    return et


def perfis():
    for c in (0, 1):
        for h in (0, 1):
            yield ("p", "x", 0, c, h)
            for s in "soe":
                for i in "xtm":
                    for t in (0, 1):
                        yield (s, i, t, c, h)


def ics_texto(v):
    return v.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def ics_dobrar(linha):
    b = linha.encode("utf-8")
    if len(b) <= 75:
        return linha
    partes, atual = [], b""
    for ch in linha:
        cb = ch.encode("utf-8")
        if len(atual) + len(cb) > (75 if not partes else 74):
            partes.append(atual.decode("utf-8"))
            atual = b""
        atual += cb
    partes.append(atual.decode("utf-8"))
    return "\r\n ".join(partes)


def ics(lista, agora):
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//bem.contado//Prazos//PT", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
         "X-WR-CALNAME:Prazos (bem.contado)", "X-WR-TIMEZONE:Europe/Lisbon",
         "REFRESH-INTERVAL;VALUE=DURATION:P1D", "X-PUBLISHED-TTL:P1D"]
    for p in lista:
        d = date.fromisoformat(p["data"])
        uid = hashlib.sha1((p["data"] + p["titulo"]).encode("utf-8")).hexdigest()[:20]
        desc = p["descricao"] + (" " + p["nota"] if p.get("nota") else "") + \
            " Informação geral: confirma sempre antes de entregar ou pagar. https://bemcontadopt.pt/prazos/"
        L += ["BEGIN:VEVENT", f"UID:{uid}@bemcontadopt.pt", f"DTSTAMP:{agora}",
              f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}",
              f"SUMMARY:{ics_texto(p['titulo'])}", f"DESCRIPTION:{ics_texto(desc)}",
              "URL:https://bemcontadopt.pt/prazos/", "TRANSP:TRANSPARENT"]
        for gatilho, quando in (("-P2DT15H", "Daqui a 3 dias"), ("-PT15H", "Amanhã")):
            L += ["BEGIN:VALARM", "ACTION:DISPLAY", f"TRIGGER:{gatilho}",
                  f"DESCRIPTION:{ics_texto(quando + ': ' + p['titulo'])}", "END:VALARM"]
        L.append("END:VEVENT")
    L.append("END:VCALENDAR")
    return "\r\n".join(ics_dobrar(x) for x in L) + "\r\n"


def calendario(args):
    site = Path(args.site)
    if not (site / "index.html").exists():
        falha(f"{site} não parece ser o site (falta index.html)")
    try:
        dados = json.loads(Path(args.dados).read_text(encoding="utf-8"))
    except Exception as ex:
        falha(f"não consegui ler {args.dados}: {ex}")
    data_iso(dados.get("atualizado", ""), "atualizado")
    ate = data_iso(dados.get("ate", ""), "ate")
    if dados.get("falta"):
        sem_travessoes(dados["falta"], "falta")
    lista = dados.get("prazos")
    if not isinstance(lista, list) or not lista:
        falha("falta a lista 'prazos'")
    vistos = set()
    for n, p in enumerate(lista, 1):
        for campo in ("data", "titulo", "descricao", "fonte"):
            if not str(p.get(campo, "")).strip():
                falha(f"prazo {n}: falta o campo '{campo}'")
        for campo in ("titulo", "descricao", "nota"):
            if p.get(campo):
                sem_travessoes(str(p[campo]), f"prazo {n}, {campo}")
        d = data_iso(p["data"], f"prazo {n}")
        if d > ate:
            falha(f"prazo {n}: {p['data']} é depois de 'ate' ({dados['ate']})")
        if not re.match(r"^https://", p["fonte"]):
            falha(f"prazo {n}: a fonte tem de ser um endereço https://")
        q = p.get("quem")
        if not isinstance(q, list) or not q or not set(q) <= ETIQUETAS:
            falha(f"prazo {n}: 'quem' tem de ser uma lista com etiquetas de {sorted(ETIQUETAS)}")
        chave = (p["data"], p["titulo"])
        if chave in vistos:
            falha(f"prazo {n}: repetido ({p['data']}, {p['titulo']})")
        vistos.add(chave)
    lista.sort(key=lambda x: (x["data"], x["titulo"]))
    pasta = site / "prazos"
    (pasta / "ics").mkdir(parents=True, exist_ok=True)
    (pasta / "calendario.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    agora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    n_fich = 0
    for pf in perfis():
        et = etiquetas_do_perfil(*pf)
        meus = [p for p in lista if et & set(p["quem"])]
        nome = "".join(str(x) for x in pf) + ".ics"
        (pasta / "ics" / nome).write_text(ics(meus, agora), encoding="utf-8", newline="")
        n_fich += 1
    print(f"ok: {len(lista)} prazos até {dados['ate']}, {n_fich} ficheiros .ics em {pasta / 'ics'}")


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
    c = sub.add_parser("calendario")
    c.add_argument("--site", required=True)
    c.add_argument("--dados", required=True)
    args = ap.parse_args()
    {"ultima": ultima, "prazos": prazos, "calendario": calendario}[args.cmd](args)


if __name__ == "__main__":
    main()
