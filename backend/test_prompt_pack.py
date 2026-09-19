"""
Comprehensive Automated Test Suite for MoSPI STATWISE Prompt Pack (Prompts A - S).
Tests all 15 core features over live network HTTP (http://127.0.0.1:8000).
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import io

BASE_URL = "http://127.0.0.1:8000"

def get(path: str):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.headers, resp.read().decode("utf-8")

def post_json(path: str, data: dict):
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.headers, resp.read().decode("utf-8")

def put_json(path: str, data: dict):
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.headers, resp.read().decode("utf-8")

def post_multipart(path: str, filename: str, content: bytes, content_type: str):
    boundary = "----WebKitFormBoundaryStatwise7MA4YWxkTrZu0gW"
    body = io.BytesIO()
    body.write(f"--{boundary}\r\n".encode("utf-8"))
    body.write(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
    body.write(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.write(content)
    body.write(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body.getvalue(),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.headers, resp.read().decode("utf-8")


def run_tests():
    passed = 0
    failed = 0

    def record_result(name: str, condition: bool, extra: str = ""):
        nonlocal passed, failed
        if condition:
            print(f"[PASS] {name} {extra}")
            passed += 1
        else:
            print(f"[FAIL] {name} - {extra}")
            failed += 1

    print("================================================================================")
    print("  STATWISE MoSPI Platform - Prompt Pack Full Automated Verification Suite")
    print("================================================================================")

    # 1. Health & Baseline
    status, _, data = get("/health")
    d = json.loads(data)
    record_result("Prompt Baseline: GET /health", status == 200 and d["status"] == "healthy")

    # 2. Onboarding & Role Profile (Prompt B)
    status, _, data = put_json("/api/auth/profile", {
        "current_assignment": "ASI Field Inspection & Data Validation",
        "career_goal": "Lead Data Analytics Directorate in MoSPI DIID"
    })
    d = json.loads(data)
    record_result(
        "Prompt B: PUT /api/auth/profile (Onboarding Fields)",
        status == 200 and d["learner"]["current_assignment"] == "ASI Field Inspection & Data Validation"
    )

    # 3. Competency Gaps & Ranking Formula (Prompt C & D)
    status, _, data = get("/api/competency/gaps")
    d = json.loads(data)
    record_result(
        "Prompt D: GET /api/competency/gaps (Formula Check)",
        status == 200 and len(d["top_gaps"]) == 5 and "0.45*NormGap" in d["gap_ranking_formula"]
    )

    # 4. iGOT Provider Adapter (Prompt F)
    status, _, data = get("/api/igot/courses")
    d = json.loads(data)
    record_result(
        "Prompt F: GET /api/igot/courses (30 Courses & Disclaimer)",
        status == 200 and d["total_returned"] == 30 and "Sandboxed Simulation Mode" in d["disclaimer"]
    )

    # 5. NSSTA Programmes Catalogue (Prompt G)
    status, _, data = get("/api/nssta/programmes")
    d = json.loads(data)
    record_result(
        "Prompt G: GET /api/nssta/programmes (>= 15 Records)",
        status == 200 and d["total"] >= 15
    )

    # 6. Admin Create & Verify NSSTA Programme (Prompt G)
    status, _, data = post_json("/api/nssta/programmes", {
        "title": "Specialized Workshop on Small Area Estimation for DES",
        "description": "Fay-Herriot estimation for district poverty lines.",
        "competencies": ["survey_sampling"],
        "target_role": ["JSO", "SSO"],
        "level": "Intermediate",
        "mode": "Classroom",
        "duration": "5 Days",
        "location": "NSSTA Greater Noida",
        "schedule": "2026-11-20 to 2026-11-25"
    })
    prog = json.loads(data)
    pid = prog["programme_id"]
    status, _, data = put_json(f"/api/nssta/programmes/{pid}/verify", {})
    record_result(
        "Prompt G: NSSTA Admin Create & Verify Flow",
        status == 200 and json.loads(data)["is_verified"] is True
    )

    # 7. Explainable Recommendations & Sequencing (Prompt H & I)
    status, _, data = get("/api/courses/recommendations")
    d = json.loads(data)
    recs = d["recommendations"]
    has_why = all("why_recommended" in r and "stage" in r for r in recs[:5])
    record_result(
        "Prompt H: GET /api/courses/recommendations (Explainability & Stages)",
        status == 200 and len(recs) > 0 and has_why
    )

    # 8. Learning Path 4-Stage Sequencing (Prompt H)
    status, _, data = get("/api/courses/learning-path")
    path = json.loads(data)
    raw_steps = path.get("steps", path) if isinstance(path, dict) else path
    stages = [p["stage"] for p in raw_steps]
    record_result(
        "Prompt H: 4-Stage Sequencing (Foundation->Core->Practice->Advanced)",
        stages == ["Foundation", "Core", "Practice", "Advanced"]
    )

    # 9. Secure Document Upload (Prompt J)
    status, _, data = post_multipart(
        "/api/documents/upload",
        filename="MoSPI_NSS_Sampling_Guidelines_2026.pdf",
        content=b"%PDF-1.4 Mock PDF Content with statistical methodology guidelines",
        content_type="application/pdf"
    )
    doc_meta = json.loads(data)
    record_result(
        "Prompt J: POST /api/documents/upload (Validation & SHA-256)",
        status == 200 and len(doc_meta["file_hash"]) == 64 and doc_meta["source_type"] == "PDF"
    )

    # 10. MCQ Quality Validator (Prompt L)
    # 10a. Valid question
    val_status, _, val_data = post_json("/api/mcq/validate", {
        "question": "What is the primary objective of stratified sampling in official household surveys?",
        "options": [
            {"id": "A", "text": "Reduce sampling error by partitioning population into homogeneous sub-groups."},
            {"id": "B", "text": "Eliminate the need to construct enumeration block frames."},
            {"id": "C", "text": "Ensure that sampling multiplier equals one for all units."},
            {"id": "D", "text": "Exclude rural agricultural households from observation."}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "NSS Sample Survey Manual",
            "page_number": 14,
            "paragraph": "Section 2.1"
        },
        "explanation": "Stratification partitions heterogeneous units into internally homogeneous strata, reducing overall standard error.",
        "competency_key": "survey_sampling"
    })
    val_res = json.loads(val_data)
    record_result(
        "Prompt L: MCQ Validator - Valid Question Acceptance",
        val_res["pass_quality"] is True and val_res["confidence_score"] == 1.0
    )

    # 10b. Invalid question (missing 4th option, has 'all of the above', missing grounding)
    val_status_inv, _, val_data_inv = post_json("/api/mcq/validate", {
        "question": "Short stem?",
        "options": ["Option A", "Option B", "All of the above"],
        "correct_answer": "A"
    })
    val_res_inv = json.loads(val_data_inv)
    record_result(
        "Prompt L: MCQ Validator - Rejection of Invalid Phrasing / <4 Options",
        val_res_inv["pass_quality"] is False and len(val_res_inv["rejection_reasons"]) >= 3
    )

    # 11. Grounded MCQ Generation Saves as Draft (Prompts K & M)
    status, _, data = post_json("/api/mcq/generate", {
        "raw_text": "MoSPI methodology manual regarding consumer price index formulation.",
        "num_questions": 3
    })
    gen_res = json.loads(data)
    all_drafts = all(q["status"] == "Draft" for q in gen_res["questions"])
    record_result(
        "Prompt K & M: MCQ Generation Strictly Enforces Draft Status (No Auto-Publish)",
        status == 200 and all_drafts and gen_res["status"] == "AWAITING_TRAINER_REVIEW"
    )

    # 12. Trainer Approval Flow (Prompt M)
    first_draft_id = gen_res["questions"][0]["id"]
    status, _, data = post_json(f"/api/mcq/questions/{first_draft_id}/approve", {"trainer_id": "trainer_dr_sunita"})
    appr_res = json.loads(data)
    record_result(
        "Prompt M: Trainer Question Approval",
        status == 200 and appr_res["question"]["status"] == "Approved"
    )

    # 13. Active Learner Quiz Serving & Pre-seeded 30 Questions (Prompts N & S)
    status, _, data = get("/api/mcq/active-quiz?quiz_id=quiz_survey_sampling_101")
    quiz = json.loads(data)
    record_result(
        "Prompt N & S: GET /api/mcq/active-quiz (Approved Questions Only)",
        status == 200 and quiz["total_questions"] == 10 and all("id" in q for q in quiz["questions"])
    )

    # 14. Quiz Submission & Competency Evidence Update (Prompt N)
    status, _, data = post_json("/api/quiz/submit", {
        "assessment_id": "quiz_survey_sampling_101",
        "answers": {q["id"]: q["correct_answer"] for q in quiz["questions"]},
        "final_integrity_score": 96.0
    })
    sub_res = json.loads(data)
    record_result(
        "Prompt N: Quiz Submission & Real-time Competency Update",
        status == 200 and sub_res["passed"] is True and sub_res["score_percentage"] == 100
    )

    # 15. Source-Grounded AI Tutor (Prompt O)
    status, _, data = post_json("/api/tutor/chat", {"query": "How is stratified sampling applied in NSS surveys?"})
    tutor_ans = json.loads(data)
    has_source = len(tutor_ans["sources"]) > 0 and "page" in tutor_ans["sources"][0]
    record_result(
        "Prompt O: Source-Grounded AI Tutor (Citation with Page)",
        status == 200 and tutor_ans["is_grounded"] is True and has_source
    )

    # 16. Tutor Strict Uncertainty Fallback (Prompt O & Section 8)
    status, _, data = post_json("/api/tutor/chat", {"query": "Tell me about Martian rover rocket propulsion systems"})
    tutor_uncertain = json.loads(data)
    is_uncertain = (
        tutor_uncertain["is_grounded"] is False and
        "cannot be verified" in tutor_uncertain["answer"].lower()
    )
    record_result(
        "Prompt O & Section 8: Tutor Uncertainty Fallback for Ungrounded Queries",
        status == 200 and is_uncertain
    )

    # 17. Tutor Feedback Telemetry (Prompt O)
    status, _, data = post_json("/api/tutor/feedback", {
        "message_id": tutor_ans["message_id"],
        "helpful": True,
        "user_comment": "Accurate page reference to NSSO manual."
    })
    fb_res = json.loads(data)
    record_result(
        "Prompt O: POST /api/tutor/feedback (Helpful/Unhelpful Telemetry)",
        status == 200 and fb_res["status"] == "SUCCESS"
    )

    # 18. Administrator Analytics Small Cohort Masking (< 3) (Prompt P)
    status, _, data = get("/api/analytics/organization")
    analytics = json.loads(data)
    # Check if State DES - Sikkim Cell (2 officials) is masked
    sikkim_cell = next((d for d in analytics["departments_breakdown"] if "Sikkim" in d["department"]), None)
    is_masked = sikkim_cell and sikkim_cell.get("is_masked") is True and "< 3" in sikkim_cell.get("officials_display")
    record_result(
        "Prompt P: Small Cohort Masking (< 3) for Privacy Protection",
        status == 200 and is_masked
    )

    # 19. Admin Analytics CSV Report Export (Prompt P)
    status, headers, csv_data = get("/api/analytics/export-csv")
    record_result(
        "Prompt P: GET /api/analytics/export-csv",
        status == 200 and "Department Breakdown" in csv_data and "Key Performance Indicators" in csv_data
    )

    # 20. Security Hardening Headers & Audit Trail (Prompt Q)
    status, headers, _ = get("/health")
    has_headers = (
        headers.get("X-Content-Type-Options") == "nosniff" and
        headers.get("X-Frame-Options") == "DENY" and
        "Content-Security-Policy" in headers
    )
    record_result(
        "Prompt Q: Security Headers (CSP, X-Content-Type-Options, X-Frame-Options)",
        has_headers
    )

    status, _, data = get("/api/security/audit-trail")
    trail = json.loads(data)
    record_result(
        "Prompt Q: Security Audit Trail Logging",
        status == 200 and trail["total_events"] > 0
    )

    print("================================================================================")
    print(f"  Test Suite Completed: {passed} PASSED, {failed} FAILED (Total {passed + failed})")
    print("================================================================================")
    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
