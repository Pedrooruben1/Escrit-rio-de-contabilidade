"""Marca os CSS e JS das páginas do site com ?v=<impressão do conteúdo>.

O GitHub Pages deixa os browsers guardar cada ficheiro 10 minutos. Sem isto, depois de uma atualização
um visitante pode receber o HTML novo com o JS antigo (ou o contrário) e a página falha.
Uso: python3 versoes_site.py PASTA_DO_SITE   (trata todos os .html da pasta e subpastas)
"""
import hashlib
import re
import sys
from pathlib import Path

REF = re.compile(r'((?:href|src)=")([^"?#:]+\.(?:css|js))(?:\?v=[^"]*)?(")')


def impressao(caminho):
    return hashlib.sha1(caminho.read_bytes()).hexdigest()[:8]


def tratar(raiz, html):
    texto = html.read_text(encoding="utf-8")

    def troca(m):
        rel = m.group(2)
        alvo = (raiz / rel.lstrip("/")) if rel.startswith("/") else (html.parent / rel)
        if not alvo.exists():
            return m.group(0)
        return f"{m.group(1)}{rel}?v={impressao(alvo)}{m.group(3)}"

    novo = REF.sub(troca, texto)
    if novo != texto:
        html.write_text(novo, encoding="utf-8")
        return True
    return False


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raiz = Path(sys.argv[1]).resolve()
    mudadas = [str(h.relative_to(raiz)) for h in sorted(raiz.rglob("*.html")) if tratar(raiz, h)]
    print("ok:", ", ".join(mudadas) if mudadas else "nada a mudar")


if __name__ == "__main__":
    main()
