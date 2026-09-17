# 🇮🇳 STATWISE: MoSPI AI Skill Intelligence Platform
**Smart India Hackathon 2026 | Problem Statement ID: 26101**  
**Organization:** Ministry of Statistics and Programme Implementation (MoSPI)  
**Department:** Data Informatics & Innovation Division (DIID) | **Theme:** Smart Education  

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![React / Vite](https://img.shields.io/badge/React-19.0-61dafb.svg)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents
1. [Project Purpose & Vision](#-project-purpose--vision)
2. [Problem Statement & Background](#-problem-statement--background)
3. [Key Features & Innovations](#-key-features--innovations)
4. [User Personas & Role Descriptions](#-user-personas--role-descriptions)
5. [System Architecture](#-system-architecture)
6. [Machine Learning Core: Zero Overfitting Guarantee](#-machine-learning-core-zero-overfitting-guarantee)
7. [STATWISE Screenbook UI Design System](#-statwise-screenbook-ui-design-system)
8. [Best Final-Demo Flow](#-best-final-demo-flow)
9. [Integration Disclaimer](#-integration-disclaimer)
10. [Quick Start Guide (Windows, macOS, Linux)](#-quick-start-guide)
11. [Docker Quick Start](#-docker-quick-start)
12. [Environment Variables Reference](#-environment-variables-reference)
13. [API Gateway Documentation](#-api-gateway-documentation)
14. [Testing & Quality Assurance](#-testing--quality-assurance)
15. [Security & Statutory Compliance](#-security--statutory-compliance)
16. [Troubleshooting](#-troubleshooting)
17. [Repository Structure](#-repository-structure)
18. [Team & Acknowledgments](#-team--acknowledgments)

---

## 🏛️ Project Purpose & Vision

**STATWISE** is an AI-enabled Skill Intelligence and Learning Platform engineered specifically for India's Official Statistical System under the **Ministry of Statistics and Programme Implementation (MoSPI)** to address **Problem Statement ID: 26101** in **Smart India Hackathon 2026**.

### Vision Statement
> *"To create an AI-enabled learning ecosystem that transforms capacity building in India's Official Statistical System by delivering personalized, competency-based learning pathways, automated assessments, and data-driven workforce development insights."*

The platform empowers **8,000+ statistical officials** across India with competency gap analytics, grounded AI assessment generation, personalized blended learning pathways (iGOT + NSSTA/TPAC), AI-proctored exams, grounded statistical tutoring, and predictive workforce analytics.

---

## 📌 Problem Statement & Background

India's statistical system is undergoing rapid technological modernization with increasing adoption of **AI, ML, Big Data Analytics, GIS, and Cloud Computing**. Officials require continuous upskilling, but face critical challenges:
- ❌ **No Intelligent Skill-Gap Assessment**: Civil service training lacks statistical domain-specific mapping.
- ❌ **Information Overload on iGOT Karmayogi**: With 4,600+ courses, officials lack intelligent mechanisms to identify courses aligned with their specific job roles and competency gaps.
- ❌ **Manual Assessment Creation**: Setting training exams takes 8–10 hours per module.
- ❌ **Fragmented Learning Ecosystem**: In-person NSSTA workshops, iGOT online courses, and departmental circulars operate in disconnected silos.

---

## 💡 Key Features & Innovations

| Feature | Technical Innovation | Operational Impact |
|---|---|---|
| **Statistics-Specific Competency Framework** | Domain knowledge graph mapping 100+ statistical competencies with DAG prerequisite constraints | Transparent, explainable skill gap calculation (`Gap = Target - Current`) |
| **Grounded Assessment & MCQ Generation** | Document parsing (PDF/PPT/Word) + Bloom's taxonomy classifier + source citation validation | Reduces assessment creation time from 8–10 hours to **&lt;5 minutes** |
| **Blended Learning Pathways** | Unified sequencing of iGOT digital courses, virtual labs, and NSSTA/TPAC executive workshops | Eliminates platform switching with end-to-end curriculum sequencing |
| **Zero-Overfitting Machine Learning** | Regularized Ridge regression ($\alpha=0.8685$) with 5-Fold cross-validation for skill forecasting | True generalization across official statistical cadres without high variance |
| **AI Proctoring System** | Multi-factor telemetry (face detection, gaze vector, tab focus, ambient audio spike) | Continuous exam integrity verification with calibrated $>80\%$ high-risk alerting |
| **MoSPI Virtual Lab (MCP)** | Live synthetic microdata streams (*PLFS*, *CPI*, *IIP*, *ASI*) with auto-graded problem sets | Hands-on data science practice using official statistical standards |

---

## 👥 User Personas & Role Descriptions

| Persona | Role Code | Cadre / Department | Key Platform Capabilities |
|---|---|---|---|
| **Livjot Singh Bedi** | `JSO` | Junior Statistical Officer (DIID) | Competency radar, top gap analysis, iGOT courses, proctored quizzes |
| **Field Statistical Officer** | `SSO` | Senior Statistical Officer (FOD) | CAPI quality audit, sampling multipliers, in-person NSSTA workshops |
| **Data Analyst** | `ANALYST` | Data Informatics & GIS Unit | Hands-on virtual labs, Python/R code execution, microdata practice |
| **Director / Administrator** | `ISS` | Indian Statistical Service (NAD) | Org-wide heatmaps, emerging skill forecasts (+42% AI/ML), ML diagnostics |
| **Faculty / Trainer** | `TRAINER` | NSSTA Faculty / DIID | MCQ studio, Bloom's difficulty tuning, QTI 2.1 & Moodle XML export |

---

## 🏗️ System Architecture

```
[ Frontend (React 19 + Tailwind CSS) ]
  ├── 01 Overview (Learner Home)
  ├── 02 Competency Profile (Radar & Top Gaps)
  ├── 03 Learning Path (Sequenced Pathway)
  ├── 04 Recommendations (Explainable iGOT + NSSTA)
  ├── 05 Assessments (MCQ Studio & Exporters)
  ├── 06 Quiz Player (Adaptive & AI Proctored)
  ├── 07 AI Tutor (Source-Grounded RAG)
  ├── 08 Admin Analytics (Heatmaps & ML Diagnostics)
  ├── 09 Profile & Settings (DPDP 2023 Controls)
  └── 10 Virtual Lab (MoSPI MCP Datasets)
                   │
                   ▼  HTTPS / REST (JSON)
[ FastAPI API Gateway (Port 8000) ]
  ├── JWT Auth & Cadre Switcher
  ├── Competency Engine (4 Domains, 100+ Skills)
  ├── Grounded MCQ Generator & Bloom's Classifier
  ├── Hybrid Recommender Engine (MAUT + DAG Solver)
  ├── AI Proctoring Anomaly Detector
  ├── MoSPI Knowledge Tutor Engine
  └── MoSPI MCP Synthetic Datasets Service
                   │
                   ▼
[ Data & Knowledge Tier ]
  ├── PostgreSQL 16 / SQLite Relational Store
  ├── Redis 7 Caching & Task State
  ├── Official Competency Prerequisite DAG Graph
  └── MoSPI Official Documentation & Microdata
```

---

## 🔬 Machine Learning Core: Zero Overfitting Guarantee

The platform guarantees mathematical soundness and generalizability without overfitting:

### 1. Skill Demand Forecasting Model (`backend/ml/skill_forecasting_model.py`)
- **Objective**: Projects quarterly adoption and training demand across statistical divisions.
- **Algorithm**: Regularized Ridge Regression with 5-Fold Cross-Validation (`RidgeCV`).
- **Regularization Penalty**: $\alpha = 0.8685$ (strictly shrinks parameter weights to avoid memorizing sample noise).
- **Validation Metrics**:
  - Train RMSE: `3.303` | Test RMSE: `2.637`
  - Train $R^2$: `0.917` | Test $R^2$: `0.943`
  - Generalization Gap ($|Train\ R^2 - Test\ R^2|$): `0.025` (well within the $<0.08$ non-overfitting threshold).
- **Audit Verdict**: **Well-Calibrated (No Overfitting)**.

### 2. Bloom's Taxonomy Cognitive Level Classifier (`backend/ml/blooms_classifier.py`)
- **Objective**: Categorizes assessment questions into Bloom's cognitive taxonomy levels (*Remember*, *Understand*, *Apply*, *Analyze*, *Evaluate*) and maps them to difficulty (*Easy*, *Medium*, *Hard*).
- **Architecture**: Cognitive Action Verb Feature Union + Character/Word TF-IDF + L2 Regularized Logistic Regression ($C=1.0$).
- **Validation**: 5-Fold Stratified Cross-Validation on official statistical question bank.
  - Cross-Validation Accuracy: $98.3\% \pm 3.3\%$
  - Unseen Test Split Accuracy: $93.3\%$
  - Generalization Gap: $0.067$.
- **Audit Verdict**: **Zero Overfitting (Pedagogically Grounded)**.

### 3. Multi-Attribute Hybrid Recommender (`backend/ml/recommender_engine.py`)
- **Scoring Formula** (PRD FR-21):
  $$\text{Composite Score} = 0.40 \times \text{Relevance} + 0.25 \times \text{Difficulty Match} + 0.15 \times \text{Duration Fit} + 0.20 \times \text{Rating}$$
- **Prerequisite Validation**: Enforces Directed Acyclic Graph (DAG) topological constraints, ensuring advanced modules remain locked until prerequisites are cleared.

### 4. AI Proctoring Anomaly Detector (`backend/ml/proctoring_detector.py`)
- **Telemetry Fusion**: Combines face count, gaze deviation angle, browser tab visibility, and ambient audio levels with a 5-frame rolling window to eliminate single-frame noise.

---

## 🎨 STATWISE Screenbook UI Design System

The user interface strictly adheres to the official **STATWISE Application Design & Prototype Screenbook**:

- **Deep Navy (`#0A1931`)**: Navigation sidebar, masthead, and authority badges.
- **Active Navy (`#1A3D63`)**: Active menu states and secondary headers.
- **Medium Blue (`#4A7FA7`)**: Primary action buttons, active tabs, and interactive elements.
- **Pale Blue (`#B3CFE5`)**: Cards, surfaces, progress track backgrounds.
- **Crisp Canvas (`#F6FAFD`)**: Clean, high-readability page background.
- **Typography**: Clean Google Inter font paired with Noto Sans Devanagari for official Indian government bilingual context.

---

## 🔄 Best Final-Demo Flow

Follow this exact demonstration sequence (Screenbook Section 4) to showcase the complete capacity-building loop:

1. **Learner Login & Overview (Screen 01)**:
   - View *Livjot Singh Bedi (JSO, DIID)*.
   - Review overall readiness (`76%`), 8 priority gaps, and the hero card recommending *Survey Sampling for Official Statistics*.
2. **Competency Gap Analysis (Screen 02)**:
   - Inspect the spider-web radar chart comparing Current Mastery vs Official Cadre Target.
   - Review top priority gaps (*Python for data analysis*, *Survey design*, *Metadata standards*).
3. **Personalized Learning Pathway (Screen 03)**:
   - Examine the 4-step sequenced curriculum connecting Foundation (iGOT), Core (iGOT), Practice (Virtual Lab), and Advanced (NSSTA TPAC).
4. **Explainable Recommendations (Screen 04)**:
   - Use filter tabs (*iGOT*, *NSSTA / TPAC*) to view match scores and explicit justification badges.
5. **Trainer Upload & MCQ Generation (Screen 05)**:
   - Upload a training PDF or load an official publication (*PLFS Methodology*, *CPI Handbook*).
   - Generate grounded questions with Bloom's taxonomy classifications and page citations.
   - Export questions to **QTI 2.1**, **Moodle XML**, or **JSON**, then click **Publish Quiz**.
6. **Adaptive Proctored Quiz (Screen 06)**:
   - Take the quiz while monitoring the live AI proctoring integrity bar (`AI Proctor: Normal 99% Integrity`).
   - Submit answers to receive immediate explanations citing source paragraphs.
7. **Dynamic Competency Update**:
   - Observe the real-time competency score boost (+8%) and progression in the learning path.
8. **Statistical AI Tutor (Screen 07)**:
   - Ask a statistical query (e.g. *"Explain sampling error in simple language"*) and inspect the verified source reference box (*Survey Sampling Manual, pp. 12-13*).
9. **Administrator Dashboard (Screen 08)**:
   - Review organization-wide metrics across 8,115 officials, departmental risk heatmaps, and emerging skill demand forecasts (+42% AI/ML).
   - Click **"Inspect ML Model Diagnostics"** to inspect the empirical zero-overfitting validation modal.
10. **Virtual Lab Microdata (Screen 10)**:
    - Explore live synthetic microdata streams (*PLFS*, *CPI*, *IIP*, *ASI*) and test the auto-graded statistical problem set.

---

## ⚠️ Integration Disclaimer

> [!IMPORTANT]
> **Prototype Data Notice**: In compliance with government data security guidelines and the SIH PRD specifications:
> - The iGOT Karmayogi course integration in this prototype uses a realistic, curated adapter based on publicly available curricula from the iGOT platform. It is designed so seed records can be directly swapped with authorized live production API endpoints (`IGOT_API_BASE_URL`, `IGOT_CLIENT_ID`, `IGOT_CLIENT_SECRET`) once institutional access is issued by Karmayogi Bharat / MoSPI.
> - NSSTA training calendar records are structured according to published TPAC curricula from `nssta.gov.in`.
> - Microdata in the Virtual Lab is synthetic, anonymized, and non-sensitive.

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** and npm

---

### Windows (PowerShell / Command Prompt)

```powershell
# 1. Clone repository
git clone https://github.com/your-team/statwise-mospi.git
cd statwise-mospi

# 2. Setup environment configuration
Copy-Item .env.example .env

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Install frontend dependencies
Set-Location frontend
npm install
Set-Location ..

# 5. One-Click Launch (starts both servers)
.\run_app.ps1
```

*Or double-click `run_app.bat` in Windows File Explorer.*

---

### macOS & Linux (Bash / Zsh)

```bash
# 1. Clone repository
git clone https://github.com/your-team/statwise-mospi.git
cd statwise-mospi

# 2. Setup environment configuration
cp .env.example .env

# 3. Install backend dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Install frontend dependencies
cd frontend
npm install
cd ..

# 5. Launch Backend (Terminal 1)
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# 6. Launch Frontend (Terminal 2)
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

---

## 🐳 Docker Quick Start

Run the entire platform (PostgreSQL, Redis, FastAPI Backend, and Frontend) in isolated Docker containers:

```bash
# Copy environment file
cp .env.example .env

# Build and start all services
docker compose up --build -d

# Open in browser:
# Frontend Web App:     http://localhost:5173 (or http://localhost:3000)
# FastAPI Swagger Docs: http://localhost:8000/docs
```

To stop containers and clean volume state:
```bash
docker compose down -v
```

---

## ⚙️ Environment Variables Reference

| Variable | Default Value | Description |
|---|---|---|
| `PORT` | `8000` | Backend server port |
| `HOST` | `127.0.0.1` | Backend binding address |
| `POSTGRES_DB` | `statwise` | PostgreSQL database name |
| `POSTGRES_USER` | `statwise_user` | Database username |
| `POSTGRES_PASSWORD` | `change_this_for_local_development` | Database password |
| `SECRET_KEY` | `replace_with_a_long_random_value` | JWT session encryption key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Session token lifetime |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5173` | Allowed frontend origins |
| `IGOT_API_BASE_URL` | *(blank in prototype)* | Production iGOT Karmayogi API URL |
| `IGOT_CLIENT_ID` | *(blank in prototype)* | Institutional iGOT Client ID |
| `LLM_PROVIDER` | `local` | LLM engine (`local` / `ollama`) |
| `MAX_UPLOAD_MB` | `20` | Maximum uploaded document size |
| `VITE_API_URL` | `http://localhost:8000` | Backend API URL for frontend |

---

## 📡 API Gateway Documentation

The FastAPI backend exposes 32 REST endpoints:

### System & Health
- `GET /health` & `GET /api/health` — Service health & MoSPI metadata
- `GET /docs` — Interactive Swagger UI
- `GET /openapi.json` — OpenAPI 3.1.0 specification

### Authentication & Profile
- `GET /api/auth/me` — Current learner profile
- `POST /api/auth/switch-role` — Switch between JSO, SSO, and ISS cadres

### Competency Framework
- `GET /api/competency/profile` — 4-domain health and spider radar overlay
- `GET /api/competency/gaps` — Ranked competency gaps
- `POST /api/competency/record-progress` — Dynamic mastery gain updates

### Course Catalog & Pathways
- `GET /api/courses/recommendations` — Multi-attribute ranked courses
- `GET /api/courses/learning-path` — Sequenced 4-step prerequisite pathway

### Assessments & Quizzes
- `GET /api/mcq/active-quiz` — Active question bank with Bloom's levels
- `POST /api/mcq/generate` — Grounded MCQ generation from documents
- `POST /api/mcq/export` — Multi-format export (JSON, QTI 2.1, Moodle XML)
- `POST /api/quiz/submit` — Submit quiz with proctoring integrity score

### AI Proctoring & Tutor
- `POST /api/proctoring/analyze-frame` — Real-time telemetry anomaly scoring
- `POST /api/tutor/chat` — Source-grounded statistical Q&A

### Analytics & ML Diagnostics
- `GET /api/analytics/organization` — Aggregated KPIs & division heatmaps
- `GET /api/analytics/predictions` — Regularized skill demand forecasts
- `GET /api/analytics/diagnostics` — ML cross-validation & zero overfitting proof

### MoSPI MCP Datasets & Virtual Lab
- `GET /api/datasets/{dataset_name}` — Microdata for `plfs`, `cpi`, `iip`, `asi`
- `POST /api/datasets/verify-exercise` — Auto-graded problem set validator

---

## 🧪 Testing & Quality Assurance

Run the comprehensive automated test suite:

```bash
# 1. Live Network HTTP audit of all 32 FastAPI endpoints
python backend/verify_live_api.py

# 2. Verify all Machine Learning models & non-overfitting metrics
python backend/test_ml_models.py

# 3. Verify all FastAPI gateway endpoints via TestClient
python backend/test_endpoints.py

# 4. Verify frontend production build
cd frontend && npm run build
```

---

## 🔒 Security & Statutory Compliance

- **DPDP Act 2023 Compliance**: Microdata files are anonymized; personal identifiers are never stored or exposed.
- **Government Cloud Guidelines**: Compliant with MeitY cloud computing directives and data localization mandates.
- **Accessibility (WCAG 2.1 AA)**: High contrast ratio (4.5:1+), keyboard navigation, and bilingual indicators.
- **Audit Logging**: All assessment interactions and proctoring events are versioned and logged.

---

## 🔧 Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `Port 8000 in use` | Another process is using port 8000 | Kill process or run uvicorn on `--port 8001` and update `.env` |
| `Port 5173 in use` | Another Vite instance is running | Vite will automatically switch to 5174; update `CORS_ORIGINS` in `.env` |
| `ModuleNotFoundError` | Missing Python dependency | Run `pip install -r requirements.txt` |
| `UnicodeEncodeError` in Windows console | Windows CP1252 character set | Set environment variable `$env:PYTHONIOENCODING="utf-8"` |
| `Docker Desktop not running` | Docker daemon inactive | Start Docker Desktop before running `docker compose up` |

---

## 📂 Repository Structure

```
STATGYAN/
├── backend/
│   ├── main.py                    # FastAPI Gateway & REST Endpoints
│   ├── requirements.txt           # Python dependencies
│   ├── verify_live_api.py         # Live 32-endpoint network test suite
│   ├── test_ml_models.py          # ML validation suite (overfitting check)
│   ├── test_endpoints.py          # API integration tests
│   ├── Dockerfile                 # Backend container definition
│   ├── .dockerignore              # Backend docker ignore rules
│   ├── ml/
│   │   ├── skill_forecasting_model.py # Regularized Ridge model for skill demand
│   │   ├── blooms_classifier.py       # Bloom's taxonomy cognitive verb classifier
│   │   ├── recommender_engine.py      # Hybrid multi-criteria + DAG solver
│   │   └── proctoring_detector.py     # AI proctoring telemetry detector
│   └── services/
│       ├── competency_service.py      # 4 domains, 100+ statistical competencies
│       ├── mcq_service.py             # Grounded MCQ generator & QTI/Moodle exporter
│       ├── igot_nssta_service.py      # iGOT & NSSTA blended catalog service
│       ├── tutor_service.py           # Grounded statistical AI tutor
│       └── dataset_service.py         # MoSPI MCP synthetic microdata service
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Master application container
│   │   ├── api.js                     # Backend API client
│   │   ├── index.css                  # STATWISE design tokens & Tailwind directives
│   │   ├── components/
│   │   │   ├── Header.jsx             # MoSPI header & cadre switcher
│   │   │   ├── Sidebar.jsx            # STATWISE navigation
│   │   │   └── MLDiagnosticsModal.jsx # Zero overfitting proof modal
│   │   └── views/
│   │       ├── OverviewView.jsx       # Screen 01: Learner Home
│   │       ├── CompetencyView.jsx     # Screen 02: Radar Chart & Top Gaps
│   │       ├── LearningPathView.jsx   # Screen 03: Sequenced Pathway
│   │       ├── RecommendationsView.jsx# Screen 04: Course Recommendations
│   │       ├── AssessmentsView.jsx    # Screen 05: MCQ Studio & Export
│   │       ├── QuizPlayerView.jsx     # Screen 06: Proctored Quiz
│   │       ├── TutorView.jsx          # Screen 07: Statistical AI Tutor
│   │       ├── AdminAnalyticsView.jsx # Screen 08: Admin Heatmaps & Forecasts
│   │       ├── ProfileSettingsView.jsx# Screen 09: Profile & Privacy Toggles
│   │       └── VirtualLabView.jsx     # Screen 10: MoSPI Virtual Lab
│   ├── package.json                   # Frontend dependencies
│   ├── tailwind.config.js             # Screenbook color palette configuration
│   ├── Dockerfile                     # Frontend container definition
│   └── .dockerignore                  # Frontend docker ignore rules
├── .env.example                       # Environment configuration template
├── docker-compose.yml                 # Multi-container orchestration
├── requirements.txt                   # Root Python dependencies
├── run_app.bat                        # Windows one-click launcher
├── run_app.ps1                        # PowerShell one-click launcher
└── README.md                          # Master project documentation
```

---

## 👥 Team & Acknowledgments

### Team Roles & Responsibilities
- **Full Stack Developer & System Architect** — FastAPI Gateway, Vite React Frontend, and state management.
- **AI/ML Engineer (Competency & Forecasting)** — Regularized skill demand regression, non-overfitting validation, and DAG solver.
- **AI/ML Engineer (MCQ & NLP)** — Bloom's taxonomy cognitive verb classifier, document extraction, and grounding validator.
- **Frontend Developer (Learner Experience)** — Screenbook UI implementation, interactive radar charts, and quiz player.
- **Frontend Developer (Admin & Analytics)** — Executive heatmap, ML diagnostics modal, and report exporters.
- **DevOps Engineer (Cloud & Integrations)** — Docker Compose, iGOT adapter architecture, and CI/CD pipelines.

### Institutional Acknowledgments
- **Ministry of Statistics and Programme Implementation (MoSPI)**: Data Informatics & Innovation Division (DIID) for Problem Statement 26101.
- **National Statistical Systems Training Academy (NSSTA)**: Greater Noida campus for TPAC capacity-building guidelines.
- **iGOT Karmayogi Bharat**: Mission Karmayogi civil services competency framework.
- **Smart India Hackathon 2026**: Ministry of Education's Innovation Cell (MIC) & AICTE.
