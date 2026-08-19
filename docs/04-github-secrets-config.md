# 🔐 Configuración de Secretos y Ambientes en GitHub

Para garantizar que los pipelines de CI/CD operen de forma segura sin exponer credenciales sensibles, se deben configurar los siguientes **GitHub Actions Secrets** y **GitHub Environments**.

---

## 🗄️ Tabla de Secretos Requeridos en GitHub

Navega a tu repositorio en GitHub: **Settings > Secrets and variables > Actions > Repository secrets**.

| Nombre del Secreto | Descripción | Ejemplo / Valor |
| :--- | :--- | :--- |
| `SNYK_TOKEN` | Token de API de Snyk para escaneos de SCA, SAST y Contenedores | `a1b2c3d4-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `SEMGREP_APP_TOKEN` | Token de Semgrep para reporte en Cloud y reglas comunitarias/pro | `sec_xxxxxxxxxxxxxxxxxxxxxxxx` |
| `GCP_REGION` | Región de GCP donde se despliegan Artifact Registry y Cloud Run | `us-central1` |
| `GCP_ARTIFACT_REPO` | Nombre del repositorio en GCP Artifact Registry | `devsecops-apps` |
| `GCP_SERVICE_NAME` | Nombre base del servicio en Google Cloud Run | `secure-api` |

---

## 🎯 Secretos Específicos por Ambiente (GitHub Environments)

Recomendamos configurar dos ambientes en GitHub (**Settings > Environments**): `qa` y `production`.

### 1. Ambiente `qa` (Environment Secrets)
| Secreto | Descripción |
| :--- | :--- |
| `GCP_PROJECT_ID_QA` | ID del proyecto de Google Cloud para QA (e.g. `empresa-devsecops-qa`) |
| `GCP_WIF_PROVIDER_QA` | Resource Name del Workload Identity Provider en QA |
| `GCP_SA_EMAIL_QA` | Email de la Service Account para despliegues de QA |

### 2. Ambiente `production` (Environment Secrets)
| Secreto | Descripción |
| :--- | :--- |
| `GCP_PROJECT_ID_PROD` | ID del proyecto de Google Cloud para Producción (e.g. `empresa-devsecops-prod`) |
| `GCP_WIF_PROVIDER_PROD` | Resource Name del Workload Identity Provider en Producción |
| `GCP_SA_EMAIL_PROD` | Email de la Service Account para despliegues de Producción |

> 🛡️ **Protección de Producción:** En el entorno `production` de GitHub, activa **Required reviewers** para que cualquier despliegue a producción requiera aprobación manual de un Tech Lead o DevOps Engineer antes de ejecutarse.
