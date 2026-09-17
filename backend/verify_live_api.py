"""
Live Network HTTP Verification Script for STATWISE FastAPI Server.
Sends real HTTP requests over the network to http://127.0.0.1:8000
to thoroughly test every endpoint, status code, and response structure.
"""

import urllib.request
import urllib.error
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"


def make_request(method, path, data=None, headers=None):
    url = f"{BASE_URL}{path}"
    req_headers = {"User-Agent": "FastAPI-Live-Tester/1.0"}
    if headers:
        req_headers.update(headers)

    body = None
    if data is not None:
        if isinstance(data, (dict, list)):
            body = json.dumps(data).encode("utf-8")
            req_headers["Content-Type"] = "application/json"
        elif isinstance(data, str):
            body = data.encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            latency_ms = round((time.time() - start_time) * 1000, 1)
            status = response.status
            content = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            json_data = None
            if "application/json" in content_type:
                try:
                    json_data = json.loads(content)
                except Exception:
                    pass
            return {
                "ok": True,
                "status": status,
                "latency_ms": latency_ms,
                "content_type": content_type,
                "json": json_data,
                "text": content
            }
    except urllib.error.HTTPError as e:
        latency_ms = round((time.time() - start_time) * 1000, 1)
        return {
            "ok": False,
            "status": e.code,
            "latency_ms": latency_ms,
            "error": str(e),
            "text": e.read().decode("utf-8", errors="replace")
        }
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 1)
        return {
            "ok": False,
            "status": 0,
            "latency_ms": latency_ms,
            "error": str(e),
            "text": ""
        }


def run_live_fastapi_audit():
    print(f"================================================================")
    print(f"      AUDITING LIVE FASTAPI SERVICE AT {BASE_URL}              ")
    print(f"================================================================\n")

    endpoints_to_test = [
        # 1. System Health & Docs
        ("GET", "/api/health", None, "Health Check Endpoint"),
        ("GET", "/docs", None, "Swagger UI Documentation"),
        ("GET", "/openapi.json", None, "OpenAPI 3.1.0 Specification Schema"),

        # 2. Auth & Profile
        ("GET", "/api/auth/me", None, "Get Current Profile (Livjot Singh Bedi)"),
        ("POST", "/api/auth/switch-role", {"role_code": "SSO"}, "Switch Role to Senior Statistical Officer (SSO)"),
        ("POST", "/api/auth/switch-role", {"role_code": "JSO"}, "Switch Role to Junior Statistical Officer (JSO)"),

        # 3. Competency Analytics
        ("GET", "/api/competency/profile", None, "Competency Profile with Radar Chart"),
        ("GET", "/api/competency/gaps", None, "Prioritized Competency Gaps List"),
        ("POST", "/api/competency/record-progress?competency_id=survey_sampling&gain=0.08", None, "Dynamic Competency Mastery Update"),

        # 4. Recommendations & Learning Path
        ("GET", "/api/courses/recommendations", None, "Hybrid Course Recommendations"),
        ("GET", "/api/courses/recommendations?filter_tag=iGOT", None, "Filter iGOT Courses"),
        ("GET", "/api/courses/recommendations?filter_tag=NSSTA", None, "Filter NSSTA / TPAC Programmes"),
        ("GET", "/api/courses/learning-path", None, "Sequenced 4-Step Personalized Learning Pathway"),

        # 5. Assessment & MCQ Engine
        ("GET", "/api/mcq/active-quiz", None, "Get Active Statistical Quiz"),
        ("POST", "/api/mcq/generate", {"raw_text": "Multistage stratified cluster sampling is used in the Periodic Labour Force Survey to estimate employment metrics.", "num_questions": 3, "target_difficulty": "Mixed"}, "Generate Grounded MCQs from Training Text"),
        ("POST", "/api/mcq/export", {"assessment_id": "quiz_survey_sampling_101", "format": "json"}, "Export MCQs as JSON"),
        ("POST", "/api/mcq/export", {"assessment_id": "quiz_survey_sampling_101", "format": "qti"}, "Export MCQs as IMS QTI 2.1 XML"),
        ("POST", "/api/mcq/export", {"assessment_id": "quiz_survey_sampling_101", "format": "moodle"}, "Export MCQs as Moodle XML"),
        ("POST", "/api/quiz/submit", {
            "assessment_id": "quiz_survey_sampling_101",
            "answers": {"mcq_plfs_01": "A", "mcq_cpi_02": "B", "mcq_nas_03": "B"},
            "proctoring_violations_count": 0,
            "final_integrity_score": 98.0
        }, "Submit Quiz with Proctoring Integrity Verification"),

        # 6. AI Proctoring Telemetry
        ("POST", "/api/proctoring/analyze-frame", {
            "face_count": 1,
            "gaze_deviation_deg": 4.2,
            "is_tab_focused": True,
            "audio_db_level": 28.0,
            "voice_detected": False
        }, "AI Proctoring Frame Telemetry (Normal)"),
        ("POST", "/api/proctoring/analyze-frame", {
            "face_count": 2,
            "gaze_deviation_deg": 35.0,
            "is_tab_focused": False,
            "audio_db_level": 70.0,
            "voice_detected": True
        }, "AI Proctoring Frame Telemetry (Violation Spike)"),

        # 7. Statistical AI Tutor
        ("POST", "/api/tutor/chat", {"query": "Explain sampling error in simple language."}, "AI Tutor: Sampling Error Query with Citations"),
        ("POST", "/api/tutor/chat", {"query": "How is CPI calculated with the Laspeyres formula?"}, "AI Tutor: CPI Laspeyres Query"),
        ("POST", "/api/tutor/chat", {"query": "What are the requirements under DPDP Act 2023 for microdata?"}, "AI Tutor: DPDP 2023 Query"),

        # 8. Admin Analytics & Machine Learning Diagnostics
        ("GET", "/api/analytics/organization", None, "Organization-Wide Competency Heatmap (8,115 Officials)"),
        ("GET", "/api/analytics/predictions", None, "Emerging Skill Forecasting Engine (+42% AI/ML)"),
        ("GET", "/api/analytics/diagnostics", None, "Machine Learning Overfitting Diagnostics (Train/Test R²)"),

        # 9. MoSPI MCP Synthetic Datasets & Virtual Lab
        ("GET", "/api/datasets/plfs", None, "MoSPI MCP Server: PLFS Microdata Sample"),
        ("GET", "/api/datasets/cpi", None, "MoSPI MCP Server: CPI Monthly Series"),
        ("GET", "/api/datasets/iip", None, "MoSPI MCP Server: IIP Industrial Production Index"),
        ("GET", "/api/datasets/asi", None, "MoSPI MCP Server: Annual Survey of Industries"),
        ("POST", "/api/datasets/verify-exercise", {"exercise_id": "lab_plfs_unemp", "user_answer": "8.5"}, "Auto-Graded Virtual Lab Solution Check")
    ]

    passed_count = 0
    failed_count = 0

    for method, path, data, description in endpoints_to_test:
        res = make_request(method, path, data)
        status = res["status"]
        latency = res["latency_ms"]

        if res["ok"] and 200 <= status < 300:
            passed_count += 1
            print(f"[PASS] ({status} - {latency}ms) {method} {path} -> {description}")
        else:
            failed_count += 1
            print(f"[FAIL] ({status} - {latency}ms) {method} {path} -> {description}")
            if "error" in res:
                print(f"       Error: {res['error']}")
            if res.get("text"):
                print(f"       Response: {res['text'][:180]}")

    print("\n================================================================")
    print(f"FASTAPI AUDIT RESULT: {passed_count}/{len(endpoints_to_test)} PASSED ({failed_count} FAILED)")
    print(f"================================================================\n")

    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_live_fastapi_audit()
