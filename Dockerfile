FROM python:3.12-alpine

ARG APP_VERSION=dev
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000 APP_VERSION=${APP_VERSION}
WORKDIR /app
COPY app/ /app/

RUN adduser -D -H appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:${PORT}/healthz || exit 1
CMD ["python", "server.py"]
