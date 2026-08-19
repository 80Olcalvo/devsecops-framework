# Protocolo de Documentación Obligatoria en Cada Commit / Push

Este documento estandariza los requisitos obligatorios de documentación que Antigravity debe generar y adjuntar en cada iteración de desarrollo.

---

## 📌 Principio Rector
**"Ningún código se considera completado si no cuenta con su documentación sincronizada y versionada en el mismo commit."**

---

## 1. Documentación a Nivel de Código Fuente

### 1.1 Docstrings Estandarizados (Google / Sphinx Style)
Cada función, método, clase y módulo debe incluir:
- **Descripción clara y concisa** del propósito funcional y contexto de negocio.
- **`Args` / Parámetros:** Tipo, descripción y restricciones/validaciones esperadas.
- **`Returns` / Retorno:** Tipo de dato y significado del resultado retornado.
- **`Raises` / Excepciones:** Lista exhaustiva de excepciones controladas y condiciones bajo las cuales se disparan.
- **`Security Considerations`:** Explicación de cómo se validan las entradas (sanitización, autorización, límites de tasa).

### 1.2 Comentarios en Línea Explicativos
- Evitar comentarios redundantes que solo repitan la sintaxis.
- Enfocarse en el **"Por qué"** y las decisiones de diseño o mitigaciones de seguridad implementadas.

---

## 2. Documentación a Nivel de Proyecto y Arquitectura

Si la tarea modifica la estructura, agrega endpoints o cambia dependencias:
1. **Directorio `/docs`:**
   - Actualizar los diagramas o guías técnicas relacionadas.
2. **Documentación de APIs (OpenAPI / Swagger):**
   - Asegurar que los modelos Pydantic / DTOs tengan `Field(description=..., examples=...)`.
   - Especificar códigos de respuesta HTTP (200, 400, 401, 403, 404, 500) con sus respectivos esquemas.
3. **Variables de Entorno:**
   - Si se añade una nueva variable de entorno, documentarla inmediatamente en `docs/04-github-secrets-config.md` y en `.env.example`.

---

## 3. Formato del Commit y Changelog

Cada commit debe estructurarse con la especificación Conventional Commits:

```text
<tipo>(<alcance>): <descripción concisa>

[Cuerpo detallado con justificación técnica y decisiones de seguridad]

Docs:
- Actualizados docstrings en app/api/v1/auth.py
- Actualizada guía de configuración en docs/04-github-secrets-config.md

Security:
- Validado con Snyk Code Scan (0 issues)
- Validado con Semgrep ruleset (0 issues)
```
