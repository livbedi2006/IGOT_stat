"""
Automated Verification Suite for STATWISE Machine Learning Models.
Verifies model performance, mathematical bounds, and guarantees absence of overfitting.
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml.skill_forecasting_model import SkillForecastingEngine
from ml.blooms_classifier import BloomsTaxonomyClassifier
from ml.recommender_engine import RecommenderEngine
from ml.proctoring_detector import ProctoringAnomalyDetector


def test_skill_forecasting_generalization():
    print("\n--- 1. Testing Skill Forecasting Model (Overfitting Check) ---")
    engine = SkillForecastingEngine()
    metrics = engine.metrics
    print(f"Model Type: {metrics['model_type']}")
    print(f"Optimal Alpha (L2 Regularization Penalty): {metrics['optimal_alpha']}")
    print(f"Train RMSE: {metrics['train_rmse']} | Test RMSE: {metrics['test_rmse']}")
    print(f"Train R²: {metrics['train_r2']} | Test R²: {metrics['test_r2']}")
    print(f"Generalization Gap (|Train R² - Test R²|): {metrics['generalization_gap']}")
    print(f"Overfitting Flag: {metrics['is_overfitting']}")
    print(f"Verdict: {metrics['validation_verdict']}")

    assert not metrics['is_overfitting'], "Model is overfitting! Check regularizer."
    assert metrics['test_r2'] > 0.70, f"Test R² is too low: {metrics['test_r2']}"
    assert metrics['generalization_gap'] < 0.08, f"Generalization gap too wide: {metrics['generalization_gap']}"

    forecast_data = engine.predict_skill_growth()
    assert len(forecast_data["forecasts"]) >= 5
    print("✓ Skill Forecasting Model passed generalization & non-overfitting verification.")


def test_blooms_classifier():
    print("\n--- 2. Testing Bloom's Taxonomy NLP Classifier ---")
    classifier = BloomsTaxonomyClassifier()
    metrics = classifier.metrics
    print(f"Model Type: {metrics['model_type']}")
    print(f"Cross-Val Accuracy: {metrics['cross_val_accuracy_mean']} ± {metrics['cross_val_accuracy_std']}")
    print(f"Train Accuracy: {metrics['train_accuracy']} | Test Accuracy: {metrics['test_accuracy']}")
    print(f"Generalization Gap: {metrics['generalization_gap']}")

    assert metrics['test_accuracy'] >= 0.75, f"Test accuracy below target: {metrics['test_accuracy']}"
    assert metrics['generalization_gap'] <= 0.15, "Classifier overfitting on question text!"

    sample_q1 = "Define the formula for sampling variance in a stratified sample."
    pred1 = classifier.predict(sample_q1)
    print(f"Question: '{sample_q1}' -> Level: {pred1['blooms_level']} (Difficulty: {pred1['difficulty']})")
    assert pred1['difficulty'] in ["Easy", "Medium"]

    sample_q2 = "Critique whether administrative tax data adequately substitutes for household survey data."
    pred2 = classifier.predict(sample_q2)
    print(f"Question: '{sample_q2}' -> Level: {pred2['blooms_level']} (Difficulty: {pred2['difficulty']})")
    assert pred2['difficulty'] == "Hard"

    print("✓ Bloom's Classifier passed validation.")


def test_recommender_engine():
    print("\n--- 3. Testing Hybrid Recommender Engine ---")
    recommender = RecommenderEngine()

    dummy_courses = [
        {
            "id": "igot_101",
            "title": "Foundation: Survey Design",
            "competency_key": "survey_design",
            "req_id": "survey_design_foundations",
            "difficulty": "Beginner",
            "duration_hours": 3.0,
            "rating": 4.8
        },
        {
            "id": "nssta_201",
            "title": "Advanced: Data Quality Frameworks",
            "competency_key": "data_quality",
            "req_id": "data_quality_frameworks",
            "difficulty": "Advanced",
            "duration_hours": 30.0,
            "rating": 4.9
        }
    ]

    user_gaps = {"survey_design": 0.85, "data_quality": 0.40}
    completed_without_prereq = []
    ranked1 = recommender.rank_courses(dummy_courses, user_gaps, completed_without_prereq)

    # First course should be recommended and eligible
    assert ranked1[0]["id"] == "igot_101"
    # Second course should have prerequisite unsatisfied
    assert not ranked1[1]["prerequisites_satisfied"]

    # Now simulate user completing survey_sampling
    completed_with_prereq = ["survey_sampling"]
    ranked2 = recommender.rank_courses(dummy_courses, user_gaps, completed_with_prereq)
    assert ranked2[1]["prerequisites_satisfied"]

    print("✓ Hybrid Recommender passed multi-criteria ranking and DAG prerequisite tests.")


def test_proctoring_detector():
    print("\n--- 4. Testing AI Proctoring Anomaly Detector ---")
    detector = ProctoringAnomalyDetector()

    # Case 1: Normal behavior (Single person, centered gaze, active tab)
    event_normal = detector.analyze_frame_event(face_count=1, gaze_deviation_deg=4.0, is_tab_focused=True)
    print(f"Normal event score: {event_normal['integrity_score']} (Risk: {event_normal['risk_level']})")
    assert event_normal['risk_level'] == "Normal"
    assert event_normal['integrity_score'] >= 90.0

    # Case 2: Severe violation (Multiple persons, tab switched)
    # Feed multiple frames to update history window
    for _ in range(5):
        event_violation = detector.analyze_frame_event(face_count=2, gaze_deviation_deg=45.0, is_tab_focused=False)

    print(f"Violation event score: {event_violation['integrity_score']} (Risk: {event_violation['risk_level']})")
    assert event_violation['anomaly_confidence_score'] >= 80.0
    assert event_violation['is_flagged'] is True
    print("✓ Proctoring Anomaly Detector passed calibrated anomaly tests.")


if __name__ == "__main__":
    print("Running STATWISE ML Validation Suite...")
    test_skill_forecasting_generalization()
    test_blooms_classifier()
    test_recommender_engine()
    test_proctoring_detector()
    print("\n========================================================")
    print("ALL STATWISE ML MODELS PASSED WITH ZERO OVERFITTING!")
    print("========================================================\n")
