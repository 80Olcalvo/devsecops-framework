# ☁️ Configuración de Proyectos en Google Cloud Platform (QA y Producción)

Este documento describe la arquitectura de infraestructura en Google Cloud y cómo configurar **Workload Identity Federation (WIF)** para que GitHub Actions se autentique sin requerir claves de cuenta de servicio (service account keys) de larga duración.

---

## 🏛️ Arquitectura Multi-Proyecto en GCP

Para mantener aislamiento estricto de seguridad, se utilizan dos proyectos independientes:
1. **Proyecto GCP QA (`empresa-app-qa`)**: Ambiente de pruebas de integración y pre-lanzamiento.
2. **Proyecto GCP Producción (`empresa-app-prod`)**: Ambiente de producción con alta disponibilidad y acceso restringido.

---

## 🔧 Paso 1: Habilitar APIs en Cada Proyecto

Ejecuta en Cloud Shell o tu terminal local con `gcloud`:

```bash
gcloud services enable \
    artifactregistry.googleapis.com \
    run.googleapis.com \
    iamcredentials.googleapis.com \
    sts.googleapis.com \
    --project=TU_PROYECTO_GCP_ID
```

---

## 🔑 Paso 2: Configurar Workload Identity Federation (WIF)

Workload Identity Federation permite a GitHub Actions asumir una Service Account de GCP de forma segura usando tokens OpenID Connect (OIDC).

### 1. Crear el Workload Identity Pool:
```bash
gcloud iam workload-identity-pools create "github-pool" \
    --project="TU_PROYECTO_GCP_ID" \
    --location="global" \
    --display-name="GitHub Actions Pool"
```

### 2. Crear el Provider en el Pool:
```bash
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
    --project="TU_PROYECTO_GCP_ID" \
    --location="global" \
    --workload-identity-pool="github-pool" \
    --display-name="GitHub Provider" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
    --attribute-condition="assertion.repository_owner == 'TU_ORGANIZACION_GITHUB'"
```

### 3. Crear la Service Account para GitHub Actions:
```bash
gcloud iam service-accounts create "github-deployer" \
    --project="TU_PROYECTO_GCP_ID" \
    --display-name="GitHub Actions Deployer"
```

### 4. Asignar Roles Necesarios a la Service Account:
```bash
# Permisos para Cloud Run
gcloud projects add-iam-policy-binding "TU_PROYECTO_GCP_ID" \
    --member="serviceAccount:github-deployer@TU_PROYECTO_GCP_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

# Permisos para Artifact Registry
gcloud projects add-iam-policy-binding "TU_PROYECTO_GCP_ID" \
    --member="serviceAccount:github-deployer@TU_PROYECTO_GCP_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

# Permisos de Service Account User
gcloud iam service-accounts add-iam-policy-binding \
    "github-deployer@TU_PROYECTO_GCP_ID.iam.gserviceaccount.com" \
    --member="serviceAccount:github-deployer@TU_PROYECTO_GCP_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 5. Vincular el Provider con la Service Account:
```bash
gcloud iam service-accounts add-iam-policy-binding \
    "github-deployer@TU_PROYECTO_GCP_ID.iam.gserviceaccount.com" \
    --project="TU_PROYECTO_GCP_ID" \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/TU_ORG/TU_REPO"
```

---

## 📦 Paso 3: Crear el Repositorio en Artifact Registry

```bash
gcloud artifacts repositories create devsecops-apps \
    --project="TU_PROYECTO_GCP_ID" \
    --repository-format=docker \
    --location=us-central1 \
    --description="Repositorio Docker de aplicaciones seguras"
```
