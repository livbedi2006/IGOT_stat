"""
AI Proctoring Anomaly Detector for STATWISE Online Assessments.
Evaluates multi-modal behavioral signals:
- Face Presence (0 = no face detected, 1 = single verified user, >1 = multi-person alert)
- Gaze Vector Deviation (degrees from center)
- Browser Tab Focus / Window Blur events
- Audio Spike / Ambient Speech activity

Calculates a calibrated composite anomaly score in [0, 100].
Signals > 80% are flagged as High Risk with explanation for audit review.
"""

from typing import Dict, Any, List
import numpy as np


class ProctoringAnomalyDetector:
    def __init__(self):
        # Calibrated weights for integrity factors
        self.w_face_absence = 35.0
        self.w_multiple_faces = 45.0
        self.w_gaze_deviation = 20.0
        self.w_tab_switch = 30.0
        self.w_audio_anomaly = 15.0

        # Smoothing window for consecutive frames to prevent single-frame flickering
        self.history_window = []
        self.window_size = 5

    def analyze_frame_event(
        self,
        face_count: int,
        gaze_deviation_deg: float,
        is_tab_focused: bool,
        audio_db_level: float = 25.0,
        voice_detected: bool = False
    ) -> Dict[str, Any]:
        """
        Analyzes a discrete proctoring frame/heartbeat event and computes risk metrics.
        """
        instant_risk = 0.0
        violations = []

        # 1. Face presence check
        if face_count == 0:
            instant_risk += self.w_face_absence
            violations.append("Candidate face not detected in frame")
        elif face_count > 1:
            instant_risk += self.w_multiple_faces
            violations.append(f"Multiple persons detected ({face_count} faces in frame)")

        # 2. Gaze tracking (normal gaze is within +/- 22 degrees of screen center)
        if abs(gaze_deviation_deg) > 28.0:
            gaze_penalty = min(self.w_gaze_deviation, (abs(gaze_deviation_deg) - 28.0) * 1.5)
            instant_risk += gaze_penalty
            violations.append(f"Gaze averted significantly ({round(gaze_deviation_deg, 1)}° off-center)")

        # 3. Browser tab / window monitoring
        if not is_tab_focused:
            instant_risk += self.w_tab_switch
            violations.append("Browser tab switch / focus lost during exam")

        # 4. Audio anomaly check
        if voice_detected or audio_db_level > 65.0:
            instant_risk += self.w_audio_anomaly
            violations.append("Background vocal activity or sound threshold exceeded")

        # Bound instant risk
        instant_risk = float(np.clip(instant_risk, 0.0, 100.0))

        # Temporal smoothing over rolling window
        self.history_window.append(instant_risk)
        if len(self.history_window) > self.window_size:
            self.history_window.pop(0)

        smoothed_risk = float(np.mean(self.history_window))
        integrity_score = round(max(0.0, 100.0 - smoothed_risk), 1)

        # Risk classification
        if smoothed_risk >= 80.0:
            risk_level = "High Risk"
            alert_active = True
        elif smoothed_risk >= 45.0:
            risk_level = "Medium Suspicion"
            alert_active = False
        else:
            risk_level = "Normal"
            alert_active = False

        return {
            "integrity_score": integrity_score,
            "anomaly_confidence_score": round(smoothed_risk, 1),
            "risk_level": risk_level,
            "is_flagged": alert_active,
            "active_violations": violations,
            "sensor_telemetry": {
                "face_count": face_count,
                "gaze_angle": round(gaze_deviation_deg, 1),
                "tab_active": is_tab_focused,
                "audio_level_db": round(audio_db_level, 1),
                "voice_flag": voice_detected
            }
        }
