import sys
import os

# Ensure backend directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from ml.skill_forecasting_model import SkillForecastingEngine
from ml.blooms_classifier import BloomsTaxonomyClassifier
from ml.proctoring_detector import ProctoringAnomalyDetector
from services.competency_service import CompetencyService
from services.mcq_service import mcq_service, MCQService
from services.igot_adapter import igot_course_provider, DISCLAIMER_TEXT
from services.nssta_adapter import nssta_programme_service
from services.igot_nssta_service import course_catalogue_service
from services.upload_service import upload_service
from services.mcq_validator import mcq_validator
from services.tutor_service import tutor_service
from services.dataset_service import DatasetService
from services.analytics_service import admin_analytics_service
from services.security_service import SecurityHeadersMiddleware, rate_limiter, security_audit_logger


app = FastAPI(
    title="STATWISE - MoSPI AI Skill Intelligence Platform",
    description="Official statistical capacity building & competency intelligence API for MoSPI DIID (SIH Problem Statement 26101).",
    version="2.0.0"
)

# Prompt Q: Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Enable CORS for local React/Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate singleton core services
competency_svc = CompetencyService()
dataset_svc = DatasetService()
forecasting_engine = SkillForecastingEngine()
proctoring_detector = ProctoringAnomalyDetector()


# --- Pydantic Request Models ---
class FrameTelemetryRequest(BaseModel):
    face_count: int = 1
    gaze_deviation_deg: float = 0.0
    is_tab_focused: bool = True
    audio_db_level: float = 25.0
    voice_detected: bool = False

class TutorChatRequest(BaseModel):
    query: str

class TutorFeedbackRequest(BaseModel):
    message_id: str
    helpful: bool
    user_comment: Optional[str] = None

class SwitchRoleRequest(BaseModel):
    role_code: str  # "JSO", "SSO", "ANALYST", "ISS", "TRAINER"

class OnboardingProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    official_email: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    current_assignment: Optional[str] = None
    experience_years: Optional[float] = None
    qualification: Optional[str] = None
    preferred_language: Optional[str] = None
    previous_training: Optional[str] = None
    career_goal: Optional[str] = None

class QuizSubmissionRequest(BaseModel):
    assessment_id: str
    answers: Dict[str, str]
    proctoring_violations_count: int = 0
    final_integrity_score: float = 95.0

class ExerciseVerificationRequest(BaseModel):
    exercise_id: str
    user_answer: str

class MCQExportRequest(BaseModel):
    assessment_id: str
    format: str = "json"  # "json", "qti", "moodle", "csv"

class ApproveMCQRequest(BaseModel):
    trainer_id: str = "trainer_dr_sunita"

class RejectMCQRequest(BaseModel):
    reason: str
    trainer_id: str = "trainer_dr_sunita"

class UpdateMCQRequest(BaseModel):
    question: Optional[str] = None
    options: Optional[List[Dict[str, str]]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    competency_key: Optional[str] = None
    difficulty: Optional[str] = None

class CreateQuizRequest(BaseModel):
    title: str
    question_ids: List[str]
    duration_minutes: int = 25
    passing_score: int = 60
    assigned_cohort: str = "JSO_SSO_Cadre"
    trainer_id: str = "trainer_dr_sunita"

class CreateProgrammeRequest(BaseModel):
    title: str
    source: str = "NSSTA Greater Noida / MoSPI TPAC"
    description: str
    competencies: List[str]
    target_role: List[str]
    level: str = "Intermediate"
    mode: str = "Classroom"
    duration: str = "5 Days"
    location: str = "NSSTA Campus, Greater Noida, UP"
    schedule: str = "2026-11-01 to 2026-11-05"
    nomination_method: str = "Official Cadre Administrative Allocation"
    prerequisites: List[str] = []
    official_source_reference: str = "NSSTA Annual Training Calendar 2025-26"


# --- Health & Baseline Checks ---
@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "STATWISE MoSPI AI Learning Platform",
        "problem_statement_id": "26101",
        "organization": "MoSPI DIID",
        "version": "2.0.0",
        "environment_baseline": {
            "igot_adapter": igot_course_provider.get_provider_status()["adapter_mode"],
            "nssta_programmes": len(nssta_programme_service.list_programmes(verified_only=False)),
            "approved_mcqs": len(mcq_service.question_bank),
            "quizzes": len(mcq_service.quizzes)
        }
    }


# --- Auth & Profile Endpoints (Prompt B) ---
@app.get("/api/auth/me")
def get_current_user():
    return competency_svc.get_profile()

@app.post("/api/auth/switch-role")
def switch_user_role(req: SwitchRoleRequest, request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    rate_limiter.check_rate_limit("login", client_ip)
    profile = competency_svc.set_role(req.role_code)
    security_audit_logger.log_event(
        event_type="ROLE_SWITCH",
        user_id=profile["learner"]["id"],
        user_role=req.role_code,
        action=f"Switched role to {req.role_code}",
        ip_address=client_ip
    )
    return profile

@app.put("/api/auth/profile")
def update_learner_profile(req: OnboardingProfileUpdateRequest, request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    updates = req.dict(exclude_unset=True)
    updated = competency_svc.update_onboarding_profile(updates)
    user_id = updated["learner"].get("id") or updated["learner"].get("user_id") or "usr_livjot_26101"
    user_role = updated["learner"].get("role") or updated["learner"].get("role_code") or "JSO"
    security_audit_logger.log_event(
        event_type="PROFILE_UPDATE",
        user_id=user_id,
        user_role=user_role,
        action="Updated onboarding profile fields",
        ip_address=client_ip,
        details=updates
    )
    return updated


# --- Competency Framework & Gap Engine (Prompts C & D) ---
@app.get("/api/competency/profile")
def get_competency_profile():
    return competency_svc.get_profile()

@app.get("/api/competency/gaps")
def get_prioritized_gaps():
    prof = competency_svc.get_profile()
    return {
        "top_gaps": prof["top_gaps"],
        "all_gaps": prof["all_gaps"],
        "gap_ranking_formula": "Priority = 0.45*NormGap + 0.30*Criticality + 0.15*Relevance + 0.10*Urgency",
        "active_role": prof["learner"]["role"]
    }

@app.post("/api/competency/record-progress")
def record_learning_progress(competency_id: str = Query(...), gain: float = Query(0.08)):
    return competency_svc.record_learning_progress(competency_id, mastery_gain=gain)


# --- iGOT Provider Adapter Endpoints (Prompt F) ---
@app.get("/api/igot/courses")
def list_igot_courses(
    query: Optional[str] = None,
    difficulty: Optional[str] = None,
    language: Optional[str] = None
):
    filters = {}
    if difficulty:
        filters["difficulty"] = difficulty
    if language:
        filters["language"] = language
    courses = igot_course_provider.fetch_courses(query, filters)
    status = igot_course_provider.get_provider_status()
    return {
        "provider": status["provider_name"],
        "adapter_mode": status["adapter_mode"],
        "disclaimer": status["disclaimer"],
        "total_returned": len(courses),
        "courses": courses
    }

@app.get("/api/igot/status")
def get_igot_provider_status():
    return igot_course_provider.get_provider_status()

@app.post("/api/igot/sync")
def sync_igot_catalogue():
    return igot_course_provider.sync_catalogue()


# --- NSSTA/TPAC Programme Catalogue Endpoints (Prompt G) ---
@app.get("/api/nssta/programmes")
def list_nssta_programmes(
    competency: Optional[str] = None,
    target_role: Optional[str] = None,
    mode: Optional[str] = None,
    level: Optional[str] = None,
    all_records: bool = False
):
    progs = nssta_programme_service.list_programmes(
        competency=competency,
        target_role=target_role,
        mode=mode,
        level=level,
        verified_only=(not all_records)
    )
    return {
        "total": len(progs),
        "official_source": "National Statistical Systems Training Academy (NSSTA), Greater Noida",
        "programmes": progs
    }

@app.post("/api/nssta/programmes")
def create_nssta_programme(req: CreateProgrammeRequest):
    data = req.dict()
    created = nssta_programme_service.create_programme(data)
    security_audit_logger.log_event(
        event_type="ADMIN_CREATE",
        user_id="admin_mospi",
        user_role="ADMIN",
        action=f"Created NSSTA programme {created['programme_id']}"
    )
    return created

@app.put("/api/nssta/programmes/{programme_id}/verify")
def verify_nssta_programme(programme_id: str):
    verified = nssta_programme_service.verify_programme(programme_id)
    if not verified:
        raise HTTPException(status_code=404, detail=f"Programme {programme_id} not found.")
    security_audit_logger.log_event(
        event_type="ADMIN_VERIFY",
        user_id="admin_mospi",
        user_role="ADMIN",
        action=f"Verified NSSTA programme {programme_id}"
    )
    return verified

@app.delete("/api/nssta/programmes/{programme_id}")
def delete_nssta_programme(programme_id: str):
    success = nssta_programme_service.delete_programme(programme_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Programme {programme_id} not found.")
    return {"status": "DELETED", "programme_id": programme_id}


# --- Course Recommendations & Learning Path (Prompts H & I) ---
@app.get("/api/courses/recommendations")
def get_course_recommendations(filter_tag: str = Query("All")):
    prof = competency_svc.get_profile()
    gaps_dict = {g["id"]: g["gap_ratio"] for g in prof["all_gaps"]}
    completed = prof["learner"]["completed_competencies"]
    recs = course_catalogue_service.get_recommendations(
        gaps_dict=gaps_dict,
        completed_competencies=completed,
        filter_tag=filter_tag,
        target_role=prof["learner"]["role"],
        department=prof["learner"]["department"]
    )
    return {
        "filter": filter_tag,
        "count": len(recs),
        "disclaimer": DISCLAIMER_TEXT,
        "recommendations": recs
    }

@app.get("/api/courses/learning-path")
def get_learning_path():
    prof = competency_svc.get_profile()
    completed = prof["learner"]["completed_competencies"]
    return course_catalogue_service.get_learning_path(completed)


# --- Document Upload Endpoints (Prompt J) ---
@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    access_level: str = Form("RESTRICTED_TRAINING"),
    request: Request = None
):
    client_ip = request.client.host if request and request.client else "127.0.0.1"
    rate_limiter.check_rate_limit("upload", client_ip)
    meta = await upload_service.save_uploaded_file(
        file=file,
        uploader_id="trainer_dr_sunita",
        uploader_role="TRAINER",
        access_level=access_level
    )
    security_audit_logger.log_event(
        event_type="UPLOAD",
        user_id="trainer_dr_sunita",
        user_role="TRAINER",
        action=f"Uploaded {meta['filename']}",
        ip_address=client_ip,
        details={"file_hash": meta["file_hash"], "size_kb": meta["file_size_kb"]}
    )
    return meta

@app.get("/api/documents/list")
def list_documents():
    return upload_service.list_documents(user_role="TRAINER")


# --- MCQ Generation, Quality Validator & Trainer Review (Prompts K, L, M) ---
@app.post("/api/mcq/generate")
async def generate_mcq_from_document(
    file: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None),
    num_questions: int = Form(5),
    target_difficulty: str = Form("Mixed"),
    request: Request = None
):
    client_ip = request.client.host if request and request.client else "127.0.0.1"
    rate_limiter.check_rate_limit("mcq_generate", client_ip)

    extracted_text = ""
    filename = "Official_Training_Document.pdf"
    if file:
        filename = file.filename
        content = await file.read()
        if filename.lower().endswith(".pdf"):
            extracted_text = mcq_service.extract_text_from_pdf(content)
        else:
            extracted_text = content.decode("utf-8", errors="ignore")
    elif raw_text:
        extracted_text = raw_text
        filename = "Pasted_Training_Text.txt"

    assessment = mcq_service.generate_mcqs(
        document_text=extracted_text,
        filename=filename,
        num_questions=num_questions,
        target_difficulty=target_difficulty
    )
    security_audit_logger.log_event(
        event_type="MCQ_GENERATE",
        user_id="trainer_dr_sunita",
        user_role="TRAINER",
        action=f"Generated {assessment['total_generated']} draft questions from {filename}",
        ip_address=client_ip
    )
    return assessment

@app.post("/api/mcq/validate")
def validate_single_mcq(mcq_payload: Dict[str, Any]):
    return mcq_validator.validate_mcq(mcq_payload)

@app.get("/api/mcq/questions")
def list_questions(
    status: Optional[str] = None,
    competency: Optional[str] = None
):
    return mcq_service.list_questions(status=status, competency_key=competency)

@app.post("/api/mcq/questions/{question_id}/approve")
def approve_question(question_id: str, req: ApproveMCQRequest, request: Request = None):
    client_ip = request.client.host if request and request.client else "127.0.0.1"
    res = mcq_service.approve_question(question_id, trainer_id=req.trainer_id)
    security_audit_logger.log_event(
        event_type="APPROVAL",
        user_id=req.trainer_id,
        user_role="TRAINER",
        action=f"Approved question {question_id}",
        ip_address=client_ip
    )
    return res

@app.post("/api/mcq/questions/{question_id}/reject")
def reject_question(question_id: str, req: RejectMCQRequest, request: Request = None):
    client_ip = request.client.host if request and request.client else "127.0.0.1"
    res = mcq_service.reject_question(question_id, reason=req.reason, trainer_id=req.trainer_id)
    security_audit_logger.log_event(
        event_type="REJECTION",
        user_id=req.trainer_id,
        user_role="TRAINER",
        action=f"Rejected question {question_id} reason: {req.reason}",
        ip_address=client_ip
    )
    return res

@app.post("/api/mcq/questions/{question_id}/regenerate")
def regenerate_question(question_id: str):
    return mcq_service.regenerate_question(question_id)

@app.put("/api/mcq/questions/{question_id}")
def update_question(question_id: str, req: UpdateMCQRequest):
    return mcq_service.update_question(question_id, req.dict(exclude_unset=True))

@app.post("/api/mcq/create-quiz")
def create_quiz_from_approved_questions(req: CreateQuizRequest):
    return mcq_service.create_quiz_from_approved(
        title=req.title,
        question_ids=req.question_ids,
        duration_minutes=req.duration_minutes,
        passing_score=req.passing_score,
        assigned_cohort=req.assigned_cohort,
        trainer_id=req.trainer_id
    )


# --- Learner Quiz & Evidence Updates (Prompt N) ---
@app.get("/api/mcq/active-quiz")
def get_active_quiz(quiz_id: Optional[str] = None):
    return mcq_service.get_assessment(quiz_id or "quiz_survey_sampling_101")

@app.post("/api/mcq/export")
def export_mcqs(req: MCQExportRequest):
    fmt = req.format.lower()
    security_audit_logger.log_event(
        event_type="EXPORT",
        user_id="trainer_dr_sunita",
        user_role="TRAINER",
        action=f"Exported quiz {req.assessment_id} in {fmt.upper()} format"
    )
    if fmt == "qti":
        qti_xml = mcq_service.export_to_qti(req.assessment_id)
        return Response(content=qti_xml, media_type="application/xml")
    elif fmt == "moodle":
        moodle_xml = mcq_service.export_to_moodle_xml(req.assessment_id)
        return Response(content=moodle_xml, media_type="application/xml")
    elif fmt == "csv":
        csv_data = mcq_service.export_to_csv(req.assessment_id)
        return Response(content=csv_data, media_type="text/csv")
    else:
        json_data = mcq_service.export_to_json(req.assessment_id)
        return Response(content=json_data, media_type="application/json")

@app.post("/api/quiz/submit")
def submit_quiz(req: QuizSubmissionRequest):
    quiz = mcq_service.get_assessment(req.assessment_id)
    questions = quiz["questions"]
    correct_count = 0
    detailed_results = []

    for q in questions:
        user_choice = req.answers.get(q["id"])
        is_correct = (user_choice == q["correct_answer"])
        if is_correct:
            correct_count += 1
        detailed_results.append({
            "question_id": q["id"],
            "question": q["question"],
            "user_choice": user_choice,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "grounding": q["grounding"],
            "explanation": q["explanation"]
        })

    score_pct = int(round((correct_count / len(questions)) * 100)) if questions else 0
    passed = score_pct >= quiz.get("passing_score", 60)

    # Prompt N: Update competency evidence ONLY from approved quizzes!
    if passed:
        comp_key = quiz.get("competency_key") or "survey_sampling"
        competency_svc.record_learning_progress(comp_key, mastery_gain=0.10, hours_added=0.5)
        if comp_key not in competency_svc.learner_state["completed_competencies"]:
            competency_svc.learner_state["completed_competencies"].append(comp_key)

    return {
        "score_percentage": score_pct,
        "correct_count": correct_count,
        "total_questions": len(questions),
        "passing_score": quiz.get("passing_score", 60),
        "passed": passed,
        "proctoring_status": "Verified Clean" if req.final_integrity_score >= 80 else "Flagged for Audit Review",
        "detailed_results": detailed_results,
        "updated_profile": competency_svc.get_profile()
    }


# --- Proctoring Anomaly Telemetry ---
@app.post("/api/proctoring/analyze-frame")
def analyze_proctoring_frame(req: FrameTelemetryRequest):
    return proctoring_detector.analyze_frame_event(
        face_count=req.face_count,
        gaze_deviation_deg=req.gaze_deviation_deg,
        is_tab_focused=req.is_tab_focused,
        audio_db_level=req.audio_db_level,
        voice_detected=req.voice_detected
    )


# --- Source-Grounded AI Tutor & Feedback (Prompt O) ---
@app.post("/api/tutor/chat")
def chat_with_tutor(req: TutorChatRequest, request: Request = None):
    client_ip = request.client.host if request and request.client else "127.0.0.1"
    rate_limiter.check_rate_limit("tutor_chat", client_ip)
    return tutor_service.answer_query(req.query)

@app.post("/api/tutor/feedback")
def submit_tutor_feedback(req: TutorFeedbackRequest):
    return tutor_service.record_feedback(
        message_id=req.message_id,
        helpful=req.helpful,
        user_comment=req.user_comment
    )

@app.get("/api/tutor/metrics")
def get_tutor_metrics():
    return tutor_service.get_feedback_summary()


# --- Administrator Analytics & Privacy Masking (Prompt P) ---
@app.get("/api/analytics/organization")
def get_organization_analytics(
    department: Optional[str] = None,
    role: Optional[str] = None,
    domain: Optional[str] = None
):
    return admin_analytics_service.get_organization_metrics(
        department_filter=department,
        role_filter=role,
        domain_filter=domain,
        mask_small_cohorts=True
    )

@app.get("/api/analytics/export-csv")
def export_analytics_csv():
    security_audit_logger.log_event(
        event_type="EXPORT",
        user_id="admin_mospi",
        user_role="ADMIN",
        action="Exported organization analytics CSV report"
    )
    csv_text = admin_analytics_service.generate_csv_report()
    return PlainTextResponse(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=statwise_admin_analytics_report.csv"}
    )

@app.get("/api/security/audit-trail")
def get_security_audit_trail(limit: int = 50):
    return {
        "total_events": len(security_audit_logger.audit_log),
        "events": security_audit_logger.get_audit_trail(limit)
    }


# --- ML Diagnostics & Forecast Models ---
@app.get("/api/ml/forecast-gap")
def get_skill_forecast(horizon_months: int = Query(6, ge=1, le=24)):
    prof = competency_svc.get_profile()
    top_gaps = prof["top_gaps"]
    forecasts = []
    for g in top_gaps:
        fc = forecasting_engine.forecast_skill_gap(
            current_gap_ratio=g["gap_ratio"],
            horizon_months=horizon_months,
            weekly_study_hours=3.5,
            cadre_priority=g["priority_score"]
        )
        forecasts.append({"competency_id": g["id"], "competency_name": g["name"], "forecast": fc})

    cv_report = forecasting_engine.cross_validate()
    return {
        "horizon_months": horizon_months,
        "model_architecture": "Regularized Ridge Regression with Empirical CV Validation",
        "cross_validation_proof": cv_report,
        "forecasts": forecasts
    }

@app.get("/api/ml/blooms-diagnostics")
def get_blooms_diagnostics():
    return blooms_classifier.evaluate_model()


# --- Virtual Labs & MCP Synthetic Datasets ---
@app.get("/api/labs/datasets/summary")
def get_dataset_summary(name: str = Query("plfs")):
    return dataset_svc.get_dataset_summary(name)

@app.get("/api/labs/exercises")
def get_lab_exercises():
    return dataset_svc.get_virtual_lab_exercises()

@app.post("/api/labs/verify-exercise")
def verify_lab_exercise(req: ExerciseVerificationRequest):
    return dataset_svc.verify_exercise(req.exercise_id, req.user_answer)
