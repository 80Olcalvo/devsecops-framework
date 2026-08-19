# 🚀 Guía de Incorporación para Desarrolladores (Onboarding)

¡Bienvenido al equipo de ingeniería! Esta guía te llevará paso a paso para configurar tu entorno de desarrollo agéntico seguro con **Google Antigravity**, **Snyk**, **Semgrep**, **GitHub** y **Google Cloud Platform (GCP)**.

---

## 🧭 Resumen del Stack

```
[ Antigravity IDE / 2.0 ]
       ├── 1° Filtro: Snyk MCP (SAST / SCA)
       └── 2° Filtro: Semgrep MCP (Security & Secrets)
                │
                ▼ (Pre-commit / Push)
      [ GitHub Repository ]
       ├── Rama `qa`  ──▶ CI/CD GitHub Actions ──▶ [ GCP Proyecto QA ]
       └── Rama `main` ──▶ CI/CD GitHub Actions ──▶ [ GCP Proyecto Producción ]
```

---

## 📋 Checklist de Incorporación

1. [ ] **Clonar o abrir el repositorio en Google Antigravity**:
   - Abrir la carpeta del proyecto en Antigravity IDE o mediante Antigravity 2.0 CLI (`agy`).
2. [ ] **Configurar Servidores MCP (Snyk y Semgrep)**:
   - Seguir las instrucciones en [02-antigravity-mcp-setup.md](02-antigravity-mcp-setup.md).
3. [ ] **Generar cuentas y tokens de acceso**:
   - Cuenta en [Snyk.io](https://snyk.io/) para obtener tu `SNYK_TOKEN`.
   - Cuenta en [Semgrep.dev](https://semgrep.dev/) para obtener tu `SEMGREP_APP_TOKEN`.
4. [ ] **Instalar el entorno virtual local de Python**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r app/requirements.txt
   ```
5. [ ] **Ejecutar pruebas locales**:
   ```bash
   pytest app/tests/ -v
   ```
6. [ ] **Familiarizarse con las directivas obligatorias de Antigravity**:
   - Leer [`GEMINI.md`](../GEMINI.md) y [`docs/03-branching-and-git-flow.md`](03-branching-and-git-flow.md).

---

## ⚡ Regla de Oro del Desarrollador

> **"Todo código generado por Antigravity debe pasar el doble filtro de seguridad (Snyk + Semgrep) y contener su respectiva documentación antes de solicitar revisión o hacer push."**
