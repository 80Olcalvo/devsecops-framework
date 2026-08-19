# Protocolo de Seguridad: Puertas de Verificación Snyk y Semgrep

Este documento define el protocolo operativo exacto que Antigravity debe seguir antes de finalizar la generación de código y proceder al commit/push.

---

## 🔍 Paso 1: Escaneo con Snyk (Filtro Primario)

Antigravity debe invocar las herramientas de Snyk vía MCP o CLI:

1. **Escaneo de Código Fuente (SAST):**
   - Ejecutar `snyk_code_scan` en el directorio de la aplicación (`app/`).
   - Identificar vulnerabilidades como CWE-89 (SQL Injection), CWE-79 (XSS), CWE-22 (Path Traversal), CWE-798 (Hardcoded Credentials), o deserializaciones inseguras.
2. **Escaneo de Dependencias (SCA):**
   - Ejecutar `snyk_sca_scan` sobre los manifiestos de dependencias (`requirements.txt`, `package.json`, `go.mod`, etc.).
   - Verificar si existen CVEs públicos en bibliotecas de terceros y sugerir o aplicar la versión mínima segura parchada.
3. **Remediación Automatizada:**
   - Si se detecta algún hallazgo de severidad `CRITICAL`, `HIGH` o `MEDIUM`, el agente debe refactorizar el código de inmediato.
   - Re-ejecutar el escaneo para verificar que el reporte sea limpio (`0 issues found`).

---

## 🔍 Paso 2: Escaneo con Semgrep (Filtro Secundario)

Una vez superado el filtro de Snyk, Antigravity debe ejecutar la validación con Semgrep:

1. **Validación de Reglas de Seguridad (SAST Avanzado):**
   - Reglas de `p/security-audit`, `p/owasp-top-ten`, `p/secrets`, y reglas específicas del framework (e.g. `p/fastapi`, `p/python`).
2. **Control de Fugas de Secretos:**
   - Detección de claves de API, tokens de GCP/AWS, certificados privados o credenciales en texto plano.
3. **Control de Buenas Prácticas de Arquitectura y Configuración:**
   - Detección de `CORS` permisivo con `*` junto con credenciales.
   - Detección de modo debug (`DEBUG = True`) activo en configuración productiva.
   - Detección de manejo inseguro de excepciones (e.g., captura genérica sin logueo seguro).

---

## 📋 Criterios de Aceptación Pre-Commit

- [ ] `snyk_code_scan`: 0 vulnerabilidades Críticas / Altas / Medias.
- [ ] `snyk_sca_scan`: Todas las dependencias en versiones sin CVEs conocidos de impacto.
- [ ] `semgrep`: 0 alertas de seguridad o secretos expuestos.
- [ ] Tests unitarios locales ejecutados y pasando al 100%.
