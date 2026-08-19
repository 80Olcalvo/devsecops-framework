## 📋 Descripción del Cambio
<!-- Explica brevemente el propósito de este Pull Request y el problema que resuelve. -->

## 🛡️ Checklist de Seguridad DevSecOps (Obligatorio)
- [ ] **1er Filtro (Snyk)**: Se ejecutó `snyk_code_scan` y `snyk_sca_scan` en Antigravity sin hallazgos pendientes.
- [ ] **2do Filtro (Semgrep)**: Se ejecutó `semgrep` en Antigravity y no hay violaciones de reglas ni fuga de secretos.
- [ ] **Secretos**: No se incluyeron API keys, credenciales, tokens ni endpoints sensibles en texto plano.
- [ ] **Contenedor**: La imagen Docker sigue el principio de menor privilegio (non-root user) y multi-stage build.

## 📝 Checklist de Documentación (Obligatorio)
- [ ] Se incluyeron **docstrings** estructurados en todos los métodos, funciones y clases modificadas/creadas.
- [ ] Se actualizaron los esquemas de API / OpenAPI y modelos de datos asociados.
- [ ] Se actualizaron los documentos técnicos relevantes en `/docs` o `README.md`.
- [ ] Los mensajes de commit siguen la convención [Conventional Commits](https://www.conventionalcommits.org/).

## 🧪 Pruebas
- [ ] Pruebas unitarias añadidas o actualizadas (`pytest`).
- [ ] Todos los tests locales pasan exitosamente (`100% pass`).

---
*Generado y auditado con Antigravity + Snyk + Semgrep DevSecOps Framework*
