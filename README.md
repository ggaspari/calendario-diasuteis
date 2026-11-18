# Calendário de Dias Úteis

Aplicativo web que gera o calendário anual com:

- quantidade de dias úteis por mês e no ano;
- destaque do **5º** e do **10º** dia útil de cada mês;
- feriados nacionais brasileiros (fixos e móveis, calculados a partir da Páscoa).

Carnaval e Corpus Christi são pontos facultativos e podem ser ligados/desligados na interface.

## Rodando com Docker

```bash
docker build -t calendario-uteis .
docker run --rm -p 8000:8000 calendario-uteis
```

Acesse http://localhost:8000. A porta interna pode ser alterada com `-e PORT=...`.

## Instalando no CasaOS

A cada push na `main`, o GitHub Actions publica a imagem
`ghcr.io/ggaspari/calendario-diasuteis:latest` para amd64 e arm64.

1. No CasaOS, clique em **+** → **Install a customized app** → **Import**.
2. Cole o conteúdo de [`casaos/docker-compose.yml`](casaos/docker-compose.yml) e confirme.
3. Acesse `http://<ip-do-casaos>:8085`.

## Rodando sem Docker

```bash
cd app && python3 server.py
```

## API

`GET /api/calendario?ano=2026&carnaval=1&corpus_christi=1`

Retorna JSON com `total_dias_uteis`, `feriados` e `meses[]` (cada mês com `dias_uteis`,
`quinto_dia_util`, `decimo_dia_util` e a lista de `dias`, cada um com `ordem_util`).

`GET /healthz` — usado pelo HEALTHCHECK do container.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Feriados considerados

Confraternização Universal (1/1), Sexta-feira Santa, Tiradentes (21/4), Dia do Trabalho (1/5),
Independência (7/9), N. Sra. Aparecida (12/10), Finados (2/11), Proclamação da República (15/11),
Consciência Negra (20/11, a partir de 2024) e Natal (25/12).
Feriados estaduais e municipais não são incluídos.
