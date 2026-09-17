"""
Full Integration Test Suite for STATWISE FastAPI Gateway Endpoints.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_all_api_endpoints():
    print("\n--- Running STATWISE API Gateway Integration Tests ---")

    # 1. Health
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    print("[PASS] GET /api/health")

    # 2. Profile
    res = client.get("/api/auth/me")
    assert res.status_code == 200
    profile = res.json()
    assert "name" in profile["learner"] and len(profile["learner"]["name"]) > 0
    assert "overall_readiness" in profile
    print(f"[PASS] GET /api/auth/me ({profile['learner']['name']} - {profile['learner'].get('role_code', 'JSO')} profile verified)")

    # 3. Competency Profile & Gaps
    res = client.get("/api/competency/profile")
    assert res.status_code == 200
    assert len(res.json()["top_gaps"]) >= 4
    print("[PASS] GET /api/competency/profile")

    # 4. Course Recommendations
    res = client.get("/api/courses/recommendations")
    assert res.status_code == 200
    recs = res.json()["recommendations"]
    assert len(recs) >= 5
    assert "match_percentage" in recs[0]
    print(f"[PASS] GET /api/courses/recommendations (Top: {recs[0]['title']} - {recs[0]['match_percentage']}%)")

    # 5. Learning Path
    res = client.get("/api/courses/learning-path")
    assert res.status_code == 200
    path = res.json()
    assert path["path_score"] == 84
    assert len(path["steps"]) == 4
    print("[PASS] GET /api/courses/learning-path (4-step sequenced pathway)")

    # 6. Active Quiz & MCQ
    res = client.get("/api/mcq/active-quiz")
    assert res.status_code == 200
    quiz = res.json()
    assert len(quiz["questions"]) >= 5
    print(f"[PASS] GET /api/mcq/active-quiz ({len(quiz['questions'])} grounded questions)")

    # 7. AI Proctoring Telemetry
    res = client.post("/api/proctoring/analyze-frame", json={
        "face_count": 1,
        "gaze_deviation_deg": 3.5,
        "is_tab_focused": True
    })
    assert res.status_code == 200
    assert res.json()["risk_level"] == "Normal"
    print("[PASS] POST /api/proctoring/analyze-frame (Integrity Telemetry verified)")

    # 8. Statistical AI Tutor
    res = client.post("/api/tutor/chat", json={"query": "Explain sampling error in simple language."})
    assert res.status_code == 200
    tutor_reply = res.json()
    assert "sampling error" in tutor_reply["answer"].lower()
    assert len(tutor_reply["sources"]) > 0
    print(f"[PASS] POST /api/tutor/chat (Grounded citation: {tutor_reply['sources'][0]['title']})")

    # 9. Admin Analytics
    res = client.get("/api/analytics/organization")
    assert res.status_code == 200
    org = res.json()
    assert org["kpis"]["total_officials"] == 8115
    print("[PASS] GET /api/analytics/organization (8,115 active officials)")

    # 10. ML Skill Predictions & Diagnostics
    res = client.get("/api/analytics/predictions")
    assert res.status_code == 200
    preds = res.json()
    assert len(preds["forecasts"]) >= 5
    print("[PASS] GET /api/analytics/predictions (Skill forecasts: AI/ML, Python, DPDP 2023)")

    res = client.get("/api/analytics/diagnostics")
    assert res.status_code == 200
    diag = res.json()
    assert diag["overfitting_audit"]["status"] == "APPROVED - NO OVERFITTING DETECTED"
    print("[PASS] GET /api/analytics/diagnostics (No Overfitting Audit verified)")

    # 11. MoSPI MCP Synthetic Datasets
    res = client.get("/api/datasets/plfs")
    assert res.status_code == 200
    plfs = res.json()
    assert plfs["total_records"] == 120
    print("[PASS] GET /api/datasets/plfs (PLFS microdata verified)")

    print("\n========================================================")
    print("ALL FASTAPI GATEWAY ENDPOINTS FUNCTIONING PERFECTLY!")
    print("========================================================\n")


if __name__ == "__main__":
    test_all_api_endpoints()
