# 🌿 Estrategia de Ramas y Git Flow Corporativo

Este repositorio implementa un modelo de flujo de trabajo seguro adaptado para CI/CD continuo en Google Cloud Platform con validaciones automáticas de seguridad.

---

## 🌳 Arquitectura de Ramas

```
   (feature/login) ───────────┐ (PR + Snyk/Semgrep Gates)
                              ▼
                           [ qa ] ──────────▶ Despliegue a GCP QA
                              │
                              ▼ (PR a Producción + Aprobación)
                           [ main ] ────────▶ Despliegue a GCP Producción
```

---

## 📌 Definición de Ramas

| Rama | Propósito | Ambiente GCP Destino | Tipo de Despliegue |
| :--- | :--- | :--- | :--- |
| `feature/*`, `fix/*` | Desarrollo de funcionalidades o fixes | Local / Antigravity | N/A (Solo PR Security Gate) |
| `qa` | Integración y pruebas de calidad | Proyecto GCP QA | Automático al hacer push/merge a `qa` |
| `main` | Código listo para producción | Proyecto GCP Producción | Automático al hacer push/merge a `main` tras validaciones estrictas |

---

## 🔒 Políticas de Protección de Ramas en GitHub

Para las ramas `main` y `qa`, se deben configurar las siguientes reglas en GitHub:
1. **Require a pull request before merging**: Exigir al menos una aprobación de revisión de código (Code Review).
2. **Require status checks to pass before merging**:
   - `snyk-security-scan` (Snyk SAST & SCA).
   - `semgrep-security-scan` (Semgrep SAST & Secrets).
   - `test` (Tests unitarios y de integración).
3. **Require branches to be up to date before merging**.
4. **Do not allow bypassing the above settings**.

---

## ✍️ Estándar de Mensajes de Commit (Conventional Commits)

Cada commit debe incluir el prefijo correspondiente:
- `feat:` Nueva funcionalidad para el usuario.
- `fix:` Corrección de un bug.
- `sec:` Mejoras o parches específicos de seguridad.
- `docs:` Cambios o adiciones exclusivamente de documentación.
- `refactor:` Refactorización de código sin alterar su comportamiento funcional.
- `test:` Adición o corrección de pruebas unitarias.
- `ci:` Modificaciones en pipelines de GitHub Actions o scripts de despliegue.
