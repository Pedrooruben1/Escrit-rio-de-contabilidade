"""Dados do dia para a tarefa: dia da semana, fundo, cores e hora de publicação.

Uso:
  python3 hoje.py              (hoje, hora de Lisboa)
  python3 hoje.py 2026-11-22   (outra data, para testar)

O fundo alterna todos os dias a partir de 18/11/2026 (dia 0 = azul).
"""
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

INICIO = date(2026, 11, 18)
DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]


def dados(d):
    n = (d - INICIO).days
    azul = n % 2 == 0
    fim_de_semana = d.isoweekday() >= 6
    segunda = d - timedelta(days=d.isoweekday() - 1)
    return {
        "data": d.strftime("%d/%m/%Y"),
        "dia_semana": DIAS[d.isoweekday() - 1],
        "sabado": d.isoweekday() == 6,
        "fundo": "azul" if azul else "branco",
        "cores": "fundo #17324D, texto creme #F7F5F0, destaque âmbar #E09F3E" if azul
                 else "fundo #FFFFFF, texto azul #17324D, destaque âmbar #E09F3E",
        "publicar_as": "18h00" if fim_de_semana else "13h00",
        "semana": f"{segunda:%d/%m} a {segunda + timedelta(days=6):%d/%m}",
    }


if __name__ == "__main__":
    d = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.now(ZoneInfo("Europe/Lisbon")).date()
    for k, v in dados(d).items():
        print(f"{k}: {v}")
