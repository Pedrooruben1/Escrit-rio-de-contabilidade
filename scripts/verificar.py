"""Verifica a mensagem do dia e os ficheiros dados*.json antes de publicar.

Uso:
  python3 verificar.py mensagem.txt
  python3 verificar.py mensagem.txt dados.json dados_story.json dados_video.json
  cat mensagem.txt | python3 verificar.py -

Os ficheiros .json são verificados pelo formato (slides, story ou vídeo).
Termina com código 1 se houver ERROS. Os AVISOS não bloqueiam, mas devem ser lidos.
"""
import json
import re
import sys
import unicodedata

# ---------------------------------------------------------------- listas

PALAVRAS_IA = [
    "crucial", "cruciais", "fundamental", "fundamentais", "essencial", "essenciais",
    "robusto", "robusta", "robustos", "robustas", "abrangente", "abrangentes",
    "potenciar", "potencia", "alavancar", "alavanca", "otimizar", "otimiza",
    "mergulhar", "mergulhe", "desbloquear", "desbloqueie", "aprofundar", "intrincado",
    "intrincada", "panorama", "fomentar", "fomenta", "promover", "reforçar", "reforça",
    "sublinhar", "sublinha", "destacar", "destaca", "evidenciar", "evidencia",
    "testemunho", "marco", "decisivo", "decisiva", "determinante", "fascinante",
    "deslumbrante", "majestoso", "majestosa", "diverso", "diversa", "imperdível",
    "incrível", "extraordinário", "extraordinária", "sinergia",
]

EXPRESSOES_IA = [
    "cenário atual", "momento crucial", "desempenha um papel", "no panorama atual",
    "num mundo cada vez mais", "é um marco", "representa algo maior",
    "tem um significado especial", "ponto de viragem", "marca duradoura",
    "profundamente enraizad", "demonstra o compromisso", "relevância contínua",
    "não perca", "parceiro de confiança", "fazemos a diferença",
    "é importante notar", "é importante lembrar", "vale a pena referir",
    "vale a pena notar", "convém lembrar", "importa sublinhar",
    "embora isso possa variar", "até certo ponto", "neste artigo",
    "não se trata apenas", "não só", "mas também", "como também",
    "o que reforça", "contribuindo para", "especialistas dizem",
    "segundo vários analistas", "há quem defenda", "estudos mostram",
    "em suma", "em resumo", "em conclusão", "concluindo", "no fundo",
    "sabia que", "já pensou",
]

CONECTORES = [
    "além disso", "adicionalmente", "por outro lado", "no entanto",
    "deste modo", "assim sendo", "no geral",
]

# palavra brasileira -> forma de Portugal
BRASILEIRISMOS = {
    "você": "3.ª pessoa sem pronome", "vocês": "3.ª pessoa sem pronome",
    "a gente": "nós / 3.ª pessoa", "equipe": "equipa", "registro": "registo",
    "registros": "registos", "celular": "telemóvel", "contato": "contacto",
    "contatos": "contactos", "recepção": "receção", "ônibus": "autocarro",
    "usuário": "utilizador", "usuários": "utilizadores", "mídia": "comunicação social",
    "sutil": "subtil", "time": "equipa", "planilha": "folha de cálculo",
    "cadastro": "registo", "cadastrar": "registar", "economizar": "poupar",
    "geladeira": "frigorífico", "trem": "comboio", "banheiro": "casa de banho",
    "xícara": "chávena", "café da manhã": "pequeno-almoço", "tela": "ecrã",
    "aposentadoria": "reforma", "aposentado": "reformado", "imposto de renda": "IRS",
    "carteira de trabalho": "(não existe em PT)", "conta corrente": "conta à ordem",
    "conta-corrente": "conta à ordem", "boleto": "referência Multibanco",
    "pix": "MB WAY / transferência", "CPF": "NIF", "CNPJ": "NIPC",
}
AVISO_PT = {
    "fato": "em PT é 'facto' (fato = peça de roupa)",
    "arquivo": "confirmar: em PT, para documentos digitais, 'ficheiro'",
}

# Comparação sensível a maiúsculas. "Chega" e "Livre" também são palavras comuns,
# por isso só dão aviso (ver PARTIDOS_AVISO).
PARTIDOS = [
    "PSD", "PS", "IL", "Iniciativa Liberal", "BE",
    "Bloco de Esquerda", "PCP", "CDS", "CDS-PP", "PAN", "JPP", "AD",
    "Aliança Democrática", "CDU", "Partido Socialista", "Partido Social Democrata",
]
PARTIDOS_AVISO = ["Chega", "Livre"]
OPINIAO = ["finalmente", "polémica", "polémico", "vitória", "derrota", "alívio"]
ORCAMENTO = ["orçamento do estado", "oe2026", "oe2027", "oe 2026", "oe 2027", "orçamento de estado"]

SIGLAS_CONHECIDAS = {"IVA", "IRS", "NIF", "AT", "PT", "UE", "MB", "ID", "OCC", "PDF"}

INVISIVEIS = {
    "​": "espaço de largura zero", "‌": "ZWNJ", "‍": "ZWJ",
    "⁠": "word joiner", "﻿": "BOM", "­": "hífen invisível",
    " ": "espaço fino inseparável",
}

# ---------------------------------------------------------------- utilitários

erros, avisos = [], []


def erro(onde, msg):
    erros.append(f"[{onde}] {msg}")


def aviso(onde, msg):
    avisos.append(f"[{onde}] {msg}")


def sem_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def tem_palavra(texto, termo, maiusculas=False):
    flags = 0 if maiusculas else re.IGNORECASE
    return re.search(rf"(?<![\w-]){re.escape(termo)}(?![\w-])", texto, flags) is not None


def e_emoji(c):
    o = ord(c)
    return (0x1F300 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or 0x1F000 <= o <= 0x1F2FF
            or 0xFE0F == o or 0x1F900 <= o <= 0x1F9FF)


def contar_destaques(t):
    return t.count("[")

# ---------------------------------------------------------------- texto


def verificar_texto(texto, onde):
    """Regras que valem para qualquer texto (mensagem, imagens, story, vídeo)."""
    for ch in ("—", "–"):
        if ch in texto:
            n = texto.count(ch)
            erro(onde, f"travessão '{ch}' ({n}x). Usar vírgula, dois pontos, ponto final ou parênteses.")
    for ch, nome in INVISIVEIS.items():
        if ch in texto:
            erro(onde, f"carácter invisível: {nome}")
    emojis = sorted({c for c in texto if e_emoji(c)})
    if emojis:
        erro(onde, f"emojis: {' '.join(emojis)}")
    if "**" in texto or "__" in texto:
        erro(onde, "negrito em markdown (** ou __)")

    baixo = texto.lower()
    # termos técnicos legítimos que contêm palavras da lista
    limpo = re.sub(r"bens (de primeira necessidade|essenciais)|serviços essenciais|serviços mínimos", "", texto, flags=re.I)
    for p in PALAVRAS_IA:
        if tem_palavra(limpo, p):
            erro(onde, f"palavra de IA: '{p}'")
    for e in EXPRESSOES_IA:
        if e in baixo:
            erro(onde, f"expressão de IA: '{e}'")
    if re.search(r"\bnão é [^.,;:]{1,40}, é\b", baixo):
        erro(onde, "paralelismo 'não é X, é Y'")
    if re.search(r"\bdesde [^.]{1,40} até [^.]{1,40}", baixo):
        aviso(onde, "'desde X até Y': confirmar que é uma escala real")

    for bra, pt in BRASILEIRISMOS.items():
        if tem_palavra(texto, bra, maiusculas=bra.isupper()):
            erro(onde, f"brasileirismo '{bra}' -> {pt}")
    for p, nota in AVISO_PT.items():
        if tem_palavra(texto, p):
            aviso(onde, f"'{p}': {nota}")
    for m in re.finditer(r"\b(est(?:á|ão|ou|ava|avam|ar|amos|ive))\s+(\w+ndo)\b", texto, re.I):
        erro(onde, f"gerúndio brasileiro '{m.group(0)}' -> 'está a + infinitivo'")
    nao_gerundio = ("quando", "mundo", "fundo", "segundo", "profundo", "rotundo", "fecundo")
    for m in re.finditer(r"(?:,\s*(\w{4,}ndo)\b|\b(\w{4,}ndo)[.;])", texto):
        g = m.group(1) or m.group(2)
        if g.lower() not in nao_gerundio:
            aviso(onde, f"gerúndio a fechar a frase: '{g}' (usar 'a + infinitivo' ou dividir a frase)")

    for p in PARTIDOS:
        if tem_palavra(texto, p, maiusculas=True):
            erro(onde, f"possível nome de partido: '{p}'")
    for p in PARTIDOS_AVISO:
        if tem_palavra(texto, p, maiusculas=True):
            aviso(onde, f"'{p}' com maiúscula: confirmar que não é o partido")
    for p in OPINIAO:
        if tem_palavra(texto, p):
            aviso(onde, f"palavra com tom de opinião: '{p}'")
    for o in ORCAMENTO:
        if o in baixo:
            erro(onde, "tema do Orçamento do Estado (excluído)")
            break

    for m in re.finditer(r"\b(paga|pagam|pagar) o iva\b|\bo iva todo\b", baixo):
        aviso(onde, f"'{m.group(0)}': confirmar o termo (o consumidor final suporta o IVA; as empresas liquidam e entregam)")
    if re.search(r"\bisent[oa]s?\b", baixo) and "taxa zero" in baixo:
        aviso(onde, "'isento' e 'taxa zero' no mesmo texto: não são a mesma coisa, confirmar com a fonte")

    usados = [c for c in CONECTORES if c in baixo]
    if len(usados) > 1:
        erro(onde, f"conectores a mais ({len(usados)}): {', '.join(usados)}. Máximo um.")


def siglas(texto, onde):
    vistas = []
    for s in re.findall(r"(?<![\w#@])([A-Z][A-Z0-9-]{1,6})(?![\w])", texto):
        if s not in SIGLAS_CONHECIDAS and s not in PARTIDOS and s not in vistas:
            vistas.append(s)
    if vistas:
        aviso(onde, f"siglas a confirmar se estão explicadas na primeira vez: {', '.join(vistas)}")


def blocos(mensagem):
    """Divide a mensagem em blocos pelo cabeçalho 'X:' no início da linha."""
    rotulos = r"(Opção [AB], descritivo para o Instagram|Descritivo para o Instagram|Texto alternativo|Story|Fonte|Texto da imagem|Vídeo|Tema|Porquê hoje|Formato|Fundo|Publicar às|Recomendação)"
    partes = re.split(rf"^{rotulos}:", mensagem, flags=re.M)
    res = []
    for i in range(1, len(partes) - 1, 2):
        res.append((partes[i], partes[i + 1].strip()))
    return res


def verificar_descritivo(texto, onde):
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if not linhas:
        erro(onde, "descritivo vazio")
        return
    hashtags = re.findall(r"(?<!\w)#\w+", texto)
    corpo = " ".join(l for l in linhas if not l.startswith("#"))
    primeira = re.split(r"(?<=[.!?])\s", corpo, maxsplit=1)[0]
    if len(primeira) > 125:
        erro(onde, f"primeira frase com {len(primeira)} caracteres; no feed corta por volta dos 125")
    if not 3 <= len(hashtags) <= 5:
        erro(onde, f"{len(hashtags)} hashtags; devem ser 3 a 5")
    if len(set(h.lower() for h in hashtags)) != len(hashtags):
        erro(onde, "hashtags repetidas")
    frases = [f for f in re.split(r"(?<=[.!?])\s+", corpo) if f]
    if len(frases) > 7:
        aviso(onde, f"{len(frases)} frases; o formato pede 3 a 5 mais a frase de guardar/enviar")
    for f in frases:
        if f.rstrip().endswith("?") and frases.index(f) == 0:
            erro(onde, "descritivo abre com pergunta retórica")
    inicios = [sem_acentos(f.split()[0].lower()) for f in frases if f.split()]
    for w in set(inicios):
        if inicios.count(w) >= 3:
            aviso(onde, f"{inicios.count(w)} frases começam por '{w}'")


def verificar_imagens(texto, onde):
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        t = re.sub(r"^Imagem \d+:\s*", "", linha)
        limpo = t.replace("[", "").replace("]", "")
        if len(limpo) >= 100:
            erro(onde, f"texto de imagem com {len(limpo)} caracteres (máx. 99): {limpo[:50]}...")
        if contar_destaques(t) > 1:
            erro(onde, f"mais de uma parte em âmbar: {t[:50]}")


def verificar_mensagem(mensagem):
    verificar_texto(mensagem, "mensagem")
    if re.search(r"\d[\d,.]*\s?€\s?[+\-=]\s?\d", mensagem) and "conta verificada" not in mensagem.lower():
        aviso("mensagem", "há contas com euros mas falta a linha 'Conta verificada: ...' (calcular com python3)")
    siglas(mensagem, "mensagem")
    bs = blocos(mensagem)
    nomes = [b[0] for b in bs]
    if "Recomendação" not in nomes:
        erro("mensagem", "falta a linha 'Recomendação:'")
    rec = next((c for n, c in bs if n == "Recomendação"), "")
    publica = "publicação" in rec.lower()
    so_story = "só story" in rec.lower()
    descritivos = [(n, c) for n, c in bs if "descritivo" in n.lower()]
    if publica and not descritivos:
        erro("mensagem", "recomendação com publicação mas sem descritivo")
    if (publica or so_story) and "Story" not in nomes:
        erro("mensagem", "recomendação com story mas sem a linha 'Story:'")
    if publica and "Texto alternativo" not in nomes:
        erro("mensagem", "falta o 'Texto alternativo:'")
    if (publica or so_story) and "Fonte" not in nomes:
        erro("mensagem", "falta a 'Fonte:'")
    for n, c in bs:
        if "descritivo" in n.lower():
            verificar_descritivo(c, n)
        elif n == "Texto da imagem":
            verificar_imagens(c, n)
        elif n == "Fonte":
            if "http" not in c:
                erro("Fonte", "sem link")
        elif n == "Story":
            perg = c.split("|")[0]
            perg = perg.split(":", 1)[-1].strip()
            if len(perg.replace("[", "").replace("]", "")) >= 70:
                aviso("Story", f"pergunta com {len(perg)} caracteres (máx. 69 na imagem)")

# ---------------------------------------------------------------- json

CORES_OK = {"FG", "BG", "AM", "#E09F3E", "#e09f3e", "none"}
TAGS_OK = {"path", "circle", "ellipse", "line", "g", "text"}


def verificar_svg(svg, onde, video=False):
    for tag in set(re.findall(r"<\s*([a-zA-Z]+)", svg)):
        if tag not in TAGS_OK:
            erro(onde, f"elemento SVG não permitido: <{tag}>")
    for attr, val in re.findall(r'\b(stroke|fill)="([^"]*)"', svg):
        if val not in CORES_OK:
            erro(onde, f'cor fora da marca: {attr}="{val}"')
    if not video and 'stroke="AM"' in svg:
        erro(onde, 'na imagem e no story o âmbar é "#E09F3E", não "AM"')
    if video and "#E09F3E" in svg.upper():
        aviso(onde, 'no vídeo usar "AM" para o âmbar')
    for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg):
        if len(t.strip()) > 6:
            aviso(onde, f"texto dentro do desenho deve ser só um número ou sigla curta: '{t.strip()}'")
    if "#E09F3E" not in svg.upper() and '"AM"' not in svg:
        aviso(onde, "desenho sem nenhum elemento em âmbar")


def verificar_texto_curto(t, onde, maximo):
    limpo = t.replace("[", "").replace("]", "")
    if len(limpo) >= maximo:
        erro(onde, f"texto com {len(limpo)} caracteres (máx. {maximo - 1})")
    if contar_destaques(t) > 1:
        erro(onde, "mais de uma parte entre parênteses retos")
    if t.count("[") != t.count("]"):
        erro(onde, "parênteses retos desequilibrados")
    verificar_texto(t, onde)


def verificar_json(caminho):
    d = json.load(open(caminho, encoding="utf-8"))
    nome = caminho.rsplit("/", 1)[-1]
    if d.get("fundo") not in ("azul", "branco"):
        erro(nome, f"fundo inválido: {d.get('fundo')!r}")
    etq = d.get("etiqueta", "")
    if not etq:
        erro(nome, "sem etiqueta")
    if "slides" in d:
        n = len(d["slides"])
        if n == 0:
            erro(nome, "sem slides")
        if n > 1 and not etq.startswith(("Curiosidade", "Aprender")):
            aviso(nome, "carrossel com etiqueta que não é 'Curiosidade · ' nem 'Aprender · '")
        for i, s in enumerate(d["slides"], 1):
            verificar_texto_curto(s.get("texto", ""), f"{nome} imagem {i}", 100)
            if s.get("svg"):
                verificar_svg(s["svg"], f"{nome} imagem {i}")
            else:
                aviso(f"{nome} imagem {i}", "sem desenho")
    elif "cenas" in d:
        total = sum(float(c.get("dur", 4)) for c in d["cenas"])
        if not 4 <= len(d["cenas"]) <= 6:
            aviso(nome, f"{len(d['cenas'])} cenas (o normal são 4 a 6)")
        if not 15 <= total <= 25:
            aviso(nome, f"duração total {total:.0f} s (o normal são 15 a 25)")
        for i, c in enumerate(d["cenas"], 1):
            verificar_texto_curto(c.get("texto", ""), f"{nome} cena {i}", 70)
            verificar_svg(c.get("svg", ""), f"{nome} cena {i}", video=True)
    elif "texto" in d:
        if not etq.startswith(("Pergunta", "Quiz")):
            aviso(nome, "etiqueta do story devia ser 'Pergunta · ' ou 'Quiz · '")
        verificar_texto_curto(d["texto"], nome, 70)
        if d.get("svg"):
            verificar_svg(d["svg"], nome)
    else:
        erro(nome, "formato desconhecido (sem slides, cenas ou texto)")

# ---------------------------------------------------------------- main


def main(args):
    if not args:
        print(__doc__)
        return 2
    for a in args:
        if a.endswith(".json"):
            verificar_json(a)
        else:
            texto = sys.stdin.read() if a == "-" else open(a, encoding="utf-8").read()
            verificar_mensagem(texto)
    for e in erros:
        print("ERRO  ", e)
    for a in avisos:
        print("AVISO ", a)
    print(f"\n{len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
