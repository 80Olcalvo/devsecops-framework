# Reglas Globales de Antigravity - Framework Corporativo de Desarrollo Seguro (DevSecOps)

Este archivo define las políticas estrictas y mandatorias para **Google Antigravity (IDE / Antigravity 2.0)** al generar, modificar o auditar código en este repositorio.

---

## 🛡️ DIRECTIVA MANDATORIA 1: Doble Filtro de Seguridad Pre-Commit / Pre-Push

Antes de dar por finalizada cualquier tarea de codificación o preparar un commit/push hacia el repositorio (ramas `feature/*`, `qa` o `main`), Antigravity DEBE ejecutar el ciclo de doble validación de seguridad mediante las herramientas MCP disponibles:

### 1. Primer Filtro: Snyk (SCA & SAST)
- Ejecutar análisis estático de código fuente con la herramienta MCP de Snyk (`snyk_code_scan`).
- Ejecutar análisis de dependencias de terceros y vulnerabilidades conocidas con `snyk_sca_scan`.
- Si se detectan vulnerabilidades de severidad **Media**, **Alta** o **Crítica**, Antigravity debe corregirlas de forma autónoma antes de proseguir.
- Volver a ejecutar el escaneo hasta que el resultado esté limpio o mitigado.

### 2. Segundo Filtro: Semgrep (SAST & Reglas Personalizadas)
- Ejecutar análisis con Semgrep para detectar patrones inseguros, fugas de secretos (hardcoded credentials), inyecciones (SQLi, XSS, SSRF, Command Injection), configuraciones inseguras de frameworks y anti-patrones de arquitectura.
- Cualquier hallazgo debe ser subsanado de inmediato en el código fuente.

> ⛔ **REGLA DE BLOQUEO:** Ningún código con vulnerabilidades conocidas sin mitigar puede ser propuesto para commit o integración.

---

## 📝 DIRECTIVA MANDATORIA 2: Documentación Integral en Cada Commit / Push

Todo cambio, adición de características, refactorización o corrección de bugs DEBE incluir su correspondiente documentación completa, la cual se enviará **conjuntamente con el código** en el mismo commit/push:

1. **A Nivel de Código:**
   - Docstrings estructurados en todas las clases, funciones, módulos y endpoints (describiendo parámetros, tipos de retorno, excepciones posibles y contexto de seguridad).
   - Comentarios explicativos en lógica de negocio no trivial o decisiones de diseño.
2. **A Nivel de Arquitectura y Especificación:**
   - Actualizar los archivos en el directorio `/docs` si se introducen nuevos módulos, dependencias o flujos.
   - Mantener al día la especificación OpenAPI/Swagger y esquemas de datos.
3. **A Nivel de Control de Versiones:**
   - Mensajes de commit semánticos siguiendo el estándar [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `fix:`, `sec:`, `docs:`, `refactor:`).
   - Resumen de cambios y justificación de seguridad en el cuerpo del commit.

---

## 🚀 Flujo de Trabajo y Entornos (Git Flow & GCP)

- **Rama `qa`**: Apunta al proyecto de **GCP QA**. Todo push o merge a `qa` desencadena el pipeline de GitHub Actions `.github/workflows/cd-qa.yml`.
- **Rama `main`**: Apunta al proyecto de **GCP Producción**. Todo push o merge a `main` desencadena `.github/workflows/cd-prod.yml` tras superar todas las puertas de seguridad.
- **Gestión de Secretos**: Ningún secreto, token, clave API o credencial de servicio debe incluirse en el código ni en los archivos de configuración versionados. Todos los secretos deben consumirse mediante variables de entorno inyectadas por GitHub Secrets / Secret Manager de GCP.

---

## 🧩 Ecosistema MCP en Antigravity

- **Generador de Código & Asistente:** Google Antigravity (IDE / 2.0).
- **1er Filtro de Seguridad:** Snyk.io (MCP & GitHub Actions).
- **2do Filtro de Seguridad:** Semgrep.dev (MCP & GitHub Actions).
- **Control de Versiones & PRs:** GitHub MCP Server (`@modelcontextprotocol/server-github`).
- **Nube e Infraestructura:** Google Cloud MCP Server (`@google-cloud/mcp-server`).
- **CI/CD:** GitHub Actions + GitHub Environments.
- **Cloud Provider:** Google Cloud Platform (Proyectos independientes QA y Producción).
