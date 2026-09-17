# STATWISE Implementation Task List

## Phase 1: Machine Learning & Analytics Engines (Non-overfitting ML Core)
- [x] Task 1.1: Implement regularized Skill Demand Forecasting Model (`backend/ml/skill_forecasting_model.py`) with cross-validation and diagnostics.
- [x] Task 1.2: Implement regularized Bloom's Taxonomy NLP Classifier (`backend/ml/blooms_classifier.py`).
- [x] Task 1.3: Implement Hybrid Recommendation Engine (`backend/ml/recommender_engine.py`) with multi-attribute scoring and DAG prerequisite solver.
- [x] Task 1.4: Implement AI Proctoring Anomaly Detector (`backend/ml/proctoring_detector.py`).
- [x] Task 1.5: Write unit and cross-validation tests (`backend/test_ml_models.py`) verifying generalization and absence of overfitting.

## Phase 2: Backend API & MoSPI Domain Services
- [x] Task 2.1: Implement Competency Framework Service (`backend/services/competency_service.py`) for 4 domains and 100+ competencies.
- [x] Task 2.2: Implement Grounded MCQ Generator Service (`backend/services/mcq_service.py`) with document parser, source citing, and QTI/JSON/Moodle export.
- [x] Task 2.3: Implement iGOT Karmayogi & NSSTA TPAC course catalogue service (`backend/services/igot_nssta_service.py`).
- [x] Task 2.4: Implement MoSPI Statistical Knowledge Tutor (`backend/services/tutor_service.py`).
- [x] Task 2.5: Implement MoSPI MCP Datasets Service (`backend/services/dataset_service.py`) for PLFS, CPI, IIP, ASI, NAS.
- [x] Task 2.6: Implement FastAPI API Gateway (`backend/main.py`) wiring all routes.
- [x] Task 2.7: Test all backend API endpoints (`backend/test_endpoints.py`).

## Phase 3: Frontend Web Application (STATWISE Screenbook Design System)
- [ ] Task 3.1: Initialize Vite React app with Tailwind CSS and install dependencies (`lucide-react`, `recharts`, `canvas-confetti`).
- [ ] Task 3.2: Configure STATWISE palette (`#0A1931`, `#1A3D63`, `#4A7FA7`, `#B3CFE5`, `#F6FAFD`) and typography.
- [ ] Task 3.3: Build shell navigation: MoSPI header, official emblems, user badge, and STATWISE sidebar.
- [ ] Task 3.4: Build Screen 01 - Overview (Learner Home with readiness KPIs, priority gaps, recommended next step, skill health).
- [ ] Task 3.5: Build Screen 02 - Competency Profile (Interactive Radar Chart, Target vs Mastery overlay, Top Gaps).
- [ ] Task 3.6: Build Screen 03 - Learning Path (Sequenced timeline: Foundation, Core, Practice, Advanced with status).
- [ ] Task 3.7: Build Screen 04 - Recommendations (Multi-criteria filterable catalogue with explainable match reasons).
- [ ] Task 3.8: Build Screen 05 - Assessments (Trainer/Admin MCQ studio with file drop, Bloom's difficulty selector, grounded preview, export).
- [ ] Task 3.9: Build Screen 06 - Proctored Quiz Player (Live webcam feed simulation, integrity monitor, instant feedback with citations).
- [ ] Task 3.10: Build Screen 07 - Statistical AI Tutor (Conversational grounded tutor with official MoSPI citations).
- [ ] Task 3.11: Build Screen 08 - Admin Analytics & Heatmaps (Org KPIs, department heatmap, emerging skill forecasts, ML model diagnostics modal).
- [ ] Task 3.12: Build Screen 09 - Profile & Settings (Official credentials, DPDP Act 2023 toggles, role switcher).
- [ ] Task 3.13: Build Screen 10 - MoSPI Virtual Lab (Interactive statistical exploration of PLFS, CPI, IIP data).

## Phase 4: Integration, Verification & Visual Quality
- [ ] Task 4.1: Connect frontend to FastAPI backend and verify real-time data flows.
- [ ] Task 4.2: Run automated end-to-end backend tests.
- [ ] Task 4.3: Verify all views using Browser Subagent and capture visual evidence for walkthrough.
