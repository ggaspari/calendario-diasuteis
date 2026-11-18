"""Servidor HTTP mínimo (somente biblioteca padrão)."""
from __future__ import annotations

import json
import os
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from feriados import calendario

STATIC = Path(__file__).parent / "static"
VERSAO = os.environ.get("APP_VERSION", "dev")


def _flag(qs: dict, nome: str) -> bool:
    return qs.get(nome, ["0"])[0].lower() in ("1", "true", "sim", "on")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/calendario":
            return self._api(parse_qs(url.query))
        if url.path == "/healthz":
            return self._json(200, {"status": "ok", "versao": VERSAO})
        return super().do_GET()

    def end_headers(self):
        # Evita que o navegador continue exibindo uma versão antiga da página.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def _api(self, qs):
        try:
            ano = int(qs.get("ano", [date.today().year])[0])
            if not 1900 <= ano <= 2200:
                raise ValueError
        except ValueError:
            return self._json(400, {"erro": "ano inválido (use 1900–2200)"})
        dados = calendario(ano, _flag(qs, "carnaval"), _flag(qs, "corpus_christi"))
        return self._json(200, dados)

    def _json(self, status, obj):
        corpo = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


def main():
    porta = int(os.environ.get("PORT", "8000"))
    print(f"Servindo em http://0.0.0.0:{porta}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", porta), Handler).serve_forever()


if __name__ == "__main__":
    main()
