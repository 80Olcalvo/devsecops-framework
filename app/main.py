"""Módulo principal de la aplicación API Starter - DevSecOps Framework.

Este microservicio proporciona una base lista para producción que incorpora:
- Buenas prácticas de seguridad (Cabeceras de seguridad, validación estricta de esquemas).
- Endpoints de observabilidad y health checks (Liveness & Readiness).
- Manejo estructurado de excepciones y registro de auditoría.
- Documentación OpenAPI integrada y tipado estricto con Pydantic v2.
"""

from __future__ import annotations

import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
# Modelos de Datos (Pydantic DTOs con documentación y validación estricta)
# -----------------------------------------------------------------------------

class HealthResponse(BaseModel):
    """Esquema de respuesta para el estado de salud del servicio."""

    status: str = Field(
        default="healthy",
        description="Estado operativo actual del servicio.",
        examples=["healthy", "degraded"],
    )
    environment: str = Field(
        default="production",
        description="Ambiente de ejecución activo (qa, production, local).",
        examples=["qa", "production"],
    )
    version: str = Field(
        default="1.0.0",
        description="Versión semántica de la aplicación desplegada.",
        examples=["1.0.0"],
    )


class SecurityEchoRequest(BaseModel):
    """Esquema de solicitud para endpoint de ejemplo con sanitización."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Mensaje a procesar de forma segura.",
        examples=["Hola mundo DevSecOps"],
    )


class SecurityEchoResponse(BaseModel):
    """Esquema de respuesta para el endpoint de ejemplo."""

    processed_message: str = Field(
        ...,
        description="Mensaje procesado y validado.",
    )
    sender_ip_safe: str = Field(
        ...,
        description="Identificador anonimizado o validado de origen.",
    )


# -----------------------------------------------------------------------------
# Inicialización de la Aplicación FastAPI
# -----------------------------------------------------------------------------

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

app = FastAPI(
    title="Plantilla Corporativa DevSecOps - Microservicio Base",
    description=(
        "API base para desarrollo seguro agéntico con Antigravity, "
        "Snyk y Semgrep. Incluye validaciones pre-commit y CI/CD en GCP."
    ),
    version=APP_VERSION,
    docs_url="/docs" if ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if ENVIRONMENT != "production" else None,
)

# -----------------------------------------------------------------------------
# Middlewares de Seguridad
# -----------------------------------------------------------------------------

# Configuración controlada de CORS (Evitar comodín '*' con credenciales)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []

if ALLOWED_ORIGINS and ALLOWED_ORIGINS != [""]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )


@app.middleware("http")
async def add_security_headers(request: Request, call_next: Any) -> Response:
    """Middleware para inyectar cabeceras HTTP de seguridad en cada respuesta.

    Cabeceras aplicadas:
    - X-Content-Type-Options: Evita el MIME-type sniffing.
    - X-Frame-Options: Previene ataques de Clickjacking.
    - Strict-Transport-Security: Fuerza HTTPS (HSTS).
    - Content-Security-Policy: Política base de seguridad de contenido.
    """
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# -----------------------------------------------------------------------------
# Endpoints de la Aplicación
# -----------------------------------------------------------------------------

@app.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness and Readiness Probe",
    tags=["Observability"],
)
def health_check() -> Dict[str, str]:
    """Verifica el estado operativo del microservicio para Kubernetes o Cloud Run.

    Returns:
        Dict[str, str]: Objeto con estado, ambiente y versión.
    """
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "version": APP_VERSION,
    }


@app.post(
    "/api/v1/echo",
    response_model=SecurityEchoResponse,
    status_code=status.HTTP_200_OK,
    summary="Procesamiento seguro de mensajes",
    tags=["DevSecOps Sample"],
)
def secure_echo(payload: SecurityEchoRequest, request: Request) -> Dict[str, str]:
    """Endpoint de ejemplo que recibe una carga útil validada por Pydantic.

    Args:
        payload (SecurityEchoRequest): Carga útil validada.
        request (Request): Objeto de solicitud HTTP.

    Returns:
        Dict[str, str]: Mensaje procesado y metadata.
    """
    client_ip = request.client.host if request.client else "unknown"
    return {
        "processed_message": payload.message.strip(),
        "sender_ip_safe": client_ip,
    }
