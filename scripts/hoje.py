"""Dados de hoje e do dia da publicação (o dia seguinte) para as tarefas da bem.contado.

Uso:
  python3 hoje.py                       (agora, hora de Lisboa)
  python3 hoje.py 2026-11-22            (simular outra data de execução)
  python3 hoje.py --pub /tmp/pub/publicacoes   (pasta com os estado.json; é a predefinida)

Linhas hoje_*: o dia da execução. Linhas pub_*: o dia da publicação (amanhã).
O fundo alterna por publicação feita: é o contrário do fundo da última publicação
com estado "publicada" (lido dos estado.json). Assim o perfil mantém o padrão
azul/branco mesmo nos dias sem publicação.
"""
import glob
import json
import os
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

INICIO = date(2026, 11, 18)  # 18/11/2026 foi azul (regra antiga, usada só para publicações sem "fundo" gravado)
DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
GRELHA = {
    1: ("prazos", "Publicação + story", "Prazos da semana: imagem única ou carrossel curto (2 a 4 imagens)"),
    2: ("story", "Só story", "Só story (quiz, sondagem ou caixa de perguntas)"),
    3: ("aprender", "Publicação + story", "Aprender: carrossel de 4 a 6 imagens com um conceito e um exemplo com números"),
    4: ("story", "Só story", "Só story (quiz, sondagem ou caixa de perguntas)"),
    5: ("reel", "Publicação + story", "Reel: vídeo em história de 15 a 25 segundos sobre um tema de ensinar"),
    6: ("curiosidade", "Publicação + story", "Curiosidade: carrossel de 6 a 8 imagens contado como história"),
    7: ("story", "Só story", "Só story (quiz, sondagem ou caixa de perguntas)"),
}


def fundo_antigo(d):
    return "azul" if (d - INICIO).days % 2 == 0 else "branco"


def ultima_publicada(pasta, antes_de):
    """Devolve (data, fundo) da última publicação feita antes de `antes_de`, ou (None, None)."""
    melhor = None
    for f in glob.glob(os.path.join(pasta, "*", "estado.json")):
        try:
            e = json.load(open(f, encoding="utf-8"))
            d = date.fromisoformat(e.get("data", ""))
        except Exception:
            continue
        if e.get("estado") == "publicada" and d < antes_de and (melhor is None or d > melhor[0]):
            melhor = (d, e.get("fundo") or fundo_antigo(d))
    return melhor or (None, None)


def main(args):
    pasta = "/tmp/pub/publicacoes"
    if "--pub" in args:
        i = args.index("--pub")
        pasta = args[i + 1]
        args = args[:i] + args[i + 2:]
    hoje = date.fromisoformat(args[0]) if args else datetime.now(ZoneInfo("Europe/Lisbon")).date()
    pub = hoje + timedelta(days=1)
    serie, recomendacao, descricao = GRELHA[pub.isoweekday()]
    ult_data, ult_fundo = ultima_publicada(pasta, pub) if os.path.isdir(pasta) else (None, None)
    if ult_fundo:
        fundo = "branco" if ult_fundo == "azul" else "azul"
        origem = f"contrário da última publicação ({ult_data:%d/%m}, {ult_fundo})"
    else:
        fundo = fundo_antigo(pub)
        origem = "sem publicações registadas: regra antiga por dias desde 18/11"
    segunda = pub - timedelta(days=pub.isoweekday() - 1)
    saida = {
        "hoje_data": hoje.strftime("%d/%m/%Y"),
        "hoje_dia_semana": DIAS[hoje.isoweekday() - 1],
        "hoje_data_iso": hoje.isoformat(),
        "pub_data": pub.strftime("%d/%m/%Y"),
        "pub_data_iso": pub.isoformat(),
        "pub_dia_semana": DIAS[pub.isoweekday() - 1],
        "pub_serie": serie,
        "pub_recomendacao_base": recomendacao,
        "pub_formato": descricao,
        "pub_publicar_as": "18:00" if pub.isoweekday() >= 6 else "13:00",
        "pub_fundo": fundo,
        "pub_fundo_origem": origem,
        "pub_cores": "fundo #17324D, texto creme #F7F5F0, destaque âmbar #E09F3E" if fundo == "azul"
                     else "fundo #FFFFFF, texto azul #17324D, destaque âmbar #E09F3E",
        "pub_semana": f"{segunda:%d/%m} a {segunda + timedelta(days=6):%d/%m}",
    }
    for k, v in saida.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main(sys.argv[1:])
