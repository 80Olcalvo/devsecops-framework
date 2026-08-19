"""Suite de pruebas unitarias para el microservicio base.

Verifica:
- Comportamiento de los endpoints /healthz y /api/v1/echo.
- Inyección correcta de cabeceras de seguridad HTTP.
- Validación y rechazo de cargas útiles maliciosas o inválidas.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthz_endpoint() -> None:
    """Verifica que el endpoint /healthz devuelva HTTP 200 y formato esperado."""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data
    assert "version" in data


def test_security_headers_present() -> None:
    """Valida que el middleware inyecte las cabeceras HTTP de seguridad requeridas."""
    response = client.get("/healthz")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert "Strict-Transport-Security" in response.headers
    assert "Content-Security-Policy" in response.headers


def test_secure_echo_valid_payload() -> None:
    """Verifica el procesamiento correcto de un payload válido."""
    payload = {"message": "Prueba de DevSecOps con Antigravity"}
    response = client.post("/api/v1/echo", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["processed_message"] == "Prueba de DevSecOps con Antigravity"
    assert "sender_ip_safe" in data


def test_secure_echo_empty_payload_rejected() -> None:
    """Verifica que payloads vacíos sean rechazados por validación Pydantic."""
    response = client.post("/api/v1/echo", json={"message": ""})
    assert response.status_code == 422  # Unprocessable Entity
