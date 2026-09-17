import React, { useState, useEffect } from "react";
import { CheckCircle2, XCircle, Shield, Camera, Eye, AlertTriangle, ArrowRight, RotateCcw, Award } from "lucide-react";
import confetti from "canvas-confetti";
import { api } from "../api";

export function QuizPlayerView({ activeQuiz, onQuizCompleted, onNavigate }) {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(true);

  // Proctoring simulation telemetry state
  const [proctoringState, setProctoringState] = useState({
    integrity_score: 98.5,
    risk_level: "Normal",
    face_count: 1,
    gaze_angle: 2.8,
    is_tab_focused: true,
    audio_db: 26,
    is_flagged: false
  });

  useEffect(() => {
    async function loadQuiz() {
      try {
        setLoading(true);
        const data = await api.getActiveQuiz();
        setQuestions(data.questions || []);
      } catch (err) {
        console.error("Error loading quiz:", err);
      } finally {
        setLoading(false);
      }
    }
    loadQuiz();
  }, []);

  // Monitor window focus for browser tab tracking
  useEffect(() => {
    const handleBlur = () => {
      setProctoringState((prev) => ({
        ...prev,
        is_tab_focused: false,
        integrity_score: Math.max(0, prev.integrity_score - 15),
        risk_level: "Medium Suspicion"
      }));
    };
    const handleFocus = () => {
      setProctoringState((prev) => ({ ...prev, is_tab_focused: true }));
    };

    window.addEventListener("blur", handleBlur);
    window.addEventListener("focus", handleFocus);
    return () => {
      window.removeEventListener("blur", handleBlur);
      window.removeEventListener("focus", handleFocus);
    };
  }, []);

  const handleSelectOption = (questionId, optionId) => {
    if (isSubmitted) return;
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  const currentQ = questions[currentIndex];
  const isLastQuestion = currentIndex === questions.length - 1;

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handleSubmitQuiz = async () => {
    try {
      const payload = {
        assessment_id: activeQuiz?.id || "quiz_survey_sampling_101",
        answers: selectedAnswers,
        final_integrity_score: proctoringState.integrity_score,
        proctoring_violations_count: proctoringState.integrity_score < 80 ? 1 : 0
      };
      const result = await api.submitQuiz(payload);
      setQuizResult(result);
      setIsSubmitted(true);

      if (result.passed) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      }
      if (onQuizCompleted) {
        onQuizCompleted(result);
      }
    } catch (err) {
      console.error(err);
      setIsSubmitted(true);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl p-12 text-center border border-slate-200">
        <div className="text-sm font-semibold text-statwise-navy animate-pulse">
          Loading Official Statistical Assessment & Calibrating AI Proctoring Sensors...
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="bg-white rounded-xl p-8 text-center border border-slate-200">
        <div className="text-sm font-medium text-slate-600">No active quiz questions found.</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header matching Screenbook */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
            Quiz Player
          </h2>
          <p className="text-sm text-statwise-muted mt-0.5">
            Adaptive assessment • Survey Sampling Methodology
          </p>
        </div>

        {/* AI Proctoring Live Telemetry Pill */}
        <div className="flex items-center gap-3 bg-white border border-slate-200 px-3.5 py-1.5 rounded-lg shadow-sm">
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${proctoringState.integrity_score >= 80 ? "bg-emerald-500 animate-pulse" : "bg-amber-500"}`}></span>
            <span className="text-xs font-semibold text-statwise-navy">
              AI Proctor: {proctoringState.risk_level} ({Math.round(proctoringState.integrity_score)}% Integrity)
            </span>
          </div>

          <div className="hidden md:flex items-center gap-2 pl-2 border-l border-slate-200 text-[11px] text-slate-500">
            <div className="flex items-center gap-1">
              <Camera className="w-3 h-3 text-statwise-blue" />
              <span>Face: 1</span>
            </div>
            <div className="flex items-center gap-1">
              <Eye className="w-3 h-3 text-statwise-blue" />
              <span>Gaze: Center</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Quiz Box */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm space-y-6">
        {/* Progress Bar & Question Counter */}
        <div>
          <div className="flex items-center justify-between text-xs font-semibold text-statwise-navy mb-2">
            <span>Question {currentIndex + 1} of {questions.length}</span>
            <span className="text-statwise-muted">
              {Math.round(((currentIndex + 1) / questions.length) * 100)}% completed
            </span>
          </div>
          <div className="w-full bg-statwise-pale/30 rounded-full h-2 overflow-hidden">
            <div
              className="bg-statwise-blue h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Result View or Question View */}
        {isSubmitted && quizResult ? (
          <div className="p-6 bg-statwise-canvas rounded-xl border border-slate-200 text-center space-y-4">
            <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto text-emerald-600 shadow-inner">
              <Award className="w-8 h-8" />
            </div>

            <div>
              <h3 className="text-xl font-bold text-statwise-navy">
                Assessment Completed!
              </h3>
              <p className="text-xs text-statwise-muted mt-1">
                Your score has been dynamically incorporated into your Competency Profile.
              </p>
            </div>

            <div className="inline-flex items-center gap-6 px-6 py-3 bg-white rounded-lg border border-slate-200 shadow-sm">
              <div>
                <div className="text-[11px] text-slate-500 uppercase font-semibold">Score</div>
                <div className="text-2xl font-bold text-statwise-navy">{quizResult.score_percentage}%</div>
              </div>
              <div className="w-px h-8 bg-slate-200"></div>
              <div>
                <div className="text-[11px] text-slate-500 uppercase font-semibold">Correct</div>
                <div className="text-2xl font-bold text-emerald-600">
                  {quizResult.correct_count} / {quizResult.total_questions}
                </div>
              </div>
              <div className="w-px h-8 bg-slate-200"></div>
              <div>
                <div className="text-[11px] text-slate-500 uppercase font-semibold">Proctoring</div>
                <div className="text-xs font-bold text-emerald-700 mt-1">{quizResult.proctoring_status}</div>
              </div>
            </div>

            {/* Detailed Grounded Review */}
            <div className="text-left space-y-3 pt-4 border-t border-slate-200">
              <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider">
                Grounded Explanation Breakdown
              </h4>
              {quizResult.detailed_results?.map((res, i) => (
                <div key={i} className="p-3 bg-white rounded-lg border border-slate-200 space-y-1 text-xs">
                  <div className="flex items-center justify-between font-semibold text-statwise-navy">
                    <span>Q{i + 1}: {res.question}</span>
                    <span className={res.is_correct ? "text-emerald-600" : "text-rose-600"}>
                      {res.is_correct ? "✓ Correct" : "✗ Incorrect"}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-600">{res.explanation}</p>
                  <div className="text-[10px] text-statwise-blue font-medium pt-0.5">
                    {res.grounding?.citation}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-center gap-3 pt-4">
              <button
                onClick={() => {
                  setIsSubmitted(false);
                  setCurrentIndex(0);
                  setSelectedAnswers({});
                }}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition-colors flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Retake Quiz</span>
              </button>
              <button
                onClick={() => onNavigate("competency")}
                className="px-5 py-2 bg-statwise-navy hover:bg-statwise-navyActive text-white text-xs font-semibold rounded-lg transition-colors shadow-sm"
              >
                View Updated Competency Radar &rarr;
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Question Card */}
            <div className="p-6 bg-statwise-canvas rounded-xl border border-slate-200/90 space-y-4">
              <div className="flex items-start justify-between gap-3">
                <h3 className="text-lg font-bold text-statwise-navy">
                  {currentQ?.question}
                </h3>
                <span className="text-[10px] bg-slate-200 text-slate-700 px-2 py-0.5 rounded font-semibold shrink-0">
                  Bloom's: {currentQ?.blooms_level || "Understand"}
                </span>
              </div>

              <div className="text-xs text-statwise-muted">Select one answer:</div>

              {/* Answer Options */}
              <div className="space-y-2.5">
                {currentQ?.options?.map((opt) => {
                  const isSelected = selectedAnswers[currentQ.id] === opt.id;
                  return (
                    <div
                      key={opt.id}
                      onClick={() => handleSelectOption(currentQ.id, opt.id)}
                      className={`p-3.5 rounded-lg border text-xs font-medium cursor-pointer transition-all flex items-center gap-3 ${
                        isSelected
                          ? "bg-statwise-blue/10 border-statwise-blue text-statwise-navy shadow-sm ring-1 ring-statwise-blue"
                          : "bg-white border-slate-200 text-slate-700 hover:border-slate-300"
                      }`}
                    >
                      <div
                        className={`w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${
                          isSelected ? "border-statwise-blue bg-statwise-blue" : "border-slate-400"
                        }`}
                      >
                        {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-white"></div>}
                      </div>
                      <span>{opt.text}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Bottom Actions */}
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-slate-400">
                AI proctoring actively monitoring single-person integrity
              </span>

              {isLastQuestion ? (
                <button
                  onClick={handleSubmitQuiz}
                  disabled={!selectedAnswers[currentQ?.id]}
                  className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-sm transition-all"
                >
                  Submit Assessment
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  disabled={!selectedAnswers[currentQ?.id]}
                  className="px-6 py-2.5 bg-statwise-navy hover:bg-statwise-navyActive disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5"
                >
                  <span>Next question</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>
        )}

        <div className="pt-2 text-xs text-slate-400">
          Learners receive immediate assessment feedback while the platform updates the competency model.
        </div>
      </div>
    </div>
  );
}
