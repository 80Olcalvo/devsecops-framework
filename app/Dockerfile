# =============================================================================
# Stage 1: Build & Dependencies
# =============================================================================
FROM python:3.11-slim-bullseye AS builder

WORKDIR /build

ENV PYTHONTDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# =============================================================================
# Stage 2: Final Hardened Runtime Image
# =============================================================================
FROM python:3.11-slim-bullseye AS runtime

# Crear usuario y grupo no privilegiado (Principio de menor privilegio)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin -d /app appuser

WORKDIR /app

ENV PYTHONTDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.local/bin:$PATH" \
    PORT=8000

# Copiar dependencias de Python instaladas desde la etapa builder
COPY --from=builder --chown=appuser:appgroup /root/.local /app/.local

# Copiar código fuente
COPY --chown=appuser:appgroup . /app/

# Cambiar a usuario no root
USER 10001:10001

EXPOSE 8000

# Health check integrado en el contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
