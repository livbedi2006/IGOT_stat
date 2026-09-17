/**
 * STATWISE API Client
 * Connects to the FastAPI backend with structured error handling and graceful mock fallbacks.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      },
      ...options
    });
    if (!res.ok) {
      throw new Error(`API error ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.warn(`API call failed for ${endpoint}:`, err.message);
    throw err;
  }
}

export const api = {
  // Auth & Profile
  getProfile: () => request("/api/competency/profile"),
  switchRole: (roleCode) => request("/api/auth/switch-role", {
    method: "POST",
    body: JSON.stringify({ role_code: roleCode })
  }),

  // Learning Path & Recommendations
  getLearningPath: () => request("/api/courses/learning-path"),
  getRecommendations: (filter = "All") => request(`/api/courses/recommendations?filter_tag=${encodeURIComponent(filter)}`),

  // Assessments & Quizzes
  getActiveQuiz: (quizId) => request(quizId ? `/api/mcq/active-quiz?quiz_id=${quizId}` : "/api/mcq/active-quiz"),
  submitQuiz: (payload) => request("/api/quiz/submit", {
    method: "POST",
    body: JSON.stringify(payload)
  }),
  generateMCQ: async (formData) => {
    // Multipart form upload
    const res = await fetch(`${API_BASE_URL}/api/mcq/generate`, {
      method: "POST",
      body: formData
    });
    return await res.json();
  },
  exportMCQ: (assessmentId, format) => request("/api/mcq/export", {
    method: "POST",
    body: JSON.stringify({ assessment_id: assessmentId, format })
  }),

  // AI Proctoring
  sendProctoringTelemetry: (telemetry) => request("/api/proctoring/analyze-frame", {
    method: "POST",
    body: JSON.stringify(telemetry)
  }),

  // AI Tutor
  askTutor: (query) => request("/api/tutor/chat", {
    method: "POST",
    body: JSON.stringify({ query })
  }),

  // Admin & ML Diagnostics
  getOrgAnalytics: () => request("/api/analytics/organization"),
  getSkillPredictions: () => request("/api/analytics/predictions"),
  getMLDiagnostics: () => request("/api/analytics/diagnostics"),

  // Virtual Lab Datasets
  getDataset: (name) => request(`/api/datasets/${name}`),
  verifyExercise: (exerciseId, answer) => request("/api/datasets/verify-exercise", {
    method: "POST",
    body: JSON.stringify({ exercise_id: exerciseId, user_answer: answer })
  })
};
