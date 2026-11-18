"""Cálculo de feriados nacionais brasileiros e dias úteis."""
from __future__ import annotations

import calendar
from datetime import date, timedelta

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


def pascoa(ano: int) -> date:
    """Domingo de Páscoa (algoritmo de Meeus/Jones/Butcher, calendário gregoriano)."""
    a = ano % 19
    b, c = divmod(ano, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes, dia = divmod(h + l - 7 * m + 114, 31)
    return date(ano, mes, dia + 1)


def feriados(ano: int, carnaval: bool = False, corpus_christi: bool = False) -> dict[date, str]:
    """Feriados nacionais do ano.

    Carnaval e Corpus Christi são pontos facultativos nacionais, por isso são opcionais.
    """
    p = pascoa(ano)
    f: dict[date, str] = {
        date(ano, 1, 1): "Confraternização Universal",
        p - timedelta(days=2): "Sexta-feira Santa",
        date(ano, 4, 21): "Tiradentes",
        date(ano, 5, 1): "Dia do Trabalho",
        date(ano, 9, 7): "Independência do Brasil",
        date(ano, 10, 12): "Nossa Senhora Aparecida",
        date(ano, 11, 2): "Finados",
        date(ano, 11, 15): "Proclamação da República",
        date(ano, 12, 25): "Natal",
    }
    if ano >= 2024:  # Lei 14.759/2023
        f[date(ano, 11, 20)] = "Dia Nacional de Zumbi e da Consciência Negra"
    if carnaval:
        f[p - timedelta(days=48)] = "Carnaval (segunda-feira)"
        f[p - timedelta(days=47)] = "Carnaval (terça-feira)"
    if corpus_christi:
        f[p + timedelta(days=60)] = "Corpus Christi"
    return dict(sorted(f.items()))


def calendario(ano: int, carnaval: bool = False, corpus_christi: bool = False) -> dict:
    """Calendário anual com dias úteis e marcação do 5º e 10º dia útil de cada mês."""
    fer = feriados(ano, carnaval, corpus_christi)
    meses = []
    for mes in range(1, 13):
        dias = []
        uteis = 0
        quinto = decimo = None
        for dia in range(1, calendar.monthrange(ano, mes)[1] + 1):
            d = date(ano, mes, dia)
            fim_semana = d.weekday() >= 5
            feriado = fer.get(d)
            util = not fim_semana and feriado is None
            ordem = None
            if util:
                uteis += 1
                ordem = uteis
                if uteis == 5:
                    quinto = dia
                elif uteis == 10:
                    decimo = dia
            dias.append({
                "dia": dia,
                "dia_semana": d.weekday(),  # 0 = segunda
                "util": util,
                "ordem_util": ordem,
                "fim_de_semana": fim_semana,
                "feriado": feriado,
            })
        meses.append({
            "mes": mes,
            "nome": MESES[mes - 1],
            "dias_uteis": uteis,
            "quinto_dia_util": quinto,
            "decimo_dia_util": decimo,
            "dias": dias,
        })
    return {
        "ano": ano,
        "total_dias_uteis": sum(m["dias_uteis"] for m in meses),
        "feriados": [{"data": d.isoformat(), "nome": n} for d, n in fer.items()],
        "meses": meses,
    }
