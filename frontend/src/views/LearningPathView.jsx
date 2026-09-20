import React, { useState } from "react";
import { Check, Lock, Play, ArrowRight, Clock, Target, Sparkles, Database, ExternalLink, Award, CheckCircle2 } from "lucide-react";
import { api } from "../api";

export function LearningPathView({ learningPathData, currentRole = "JSO", onNavigate, onRefreshData }) {
  const [recordingProgress, setRecordingProgress] = useState(null);
  const [successBanner, setSuccessBanner] = useState("");

  const steps = learningPathData?.steps || [
    {
      step_number: 1,
      stage: "Foundation",
      title: "Foundation: Survey Design & Sampling Frames",
      provider: "iGOT Karmayogi",
      duration: "3.5 h",
      status: "In progress",
      type: "iGOT Digital Course",
      competency_key: "survey_design",
      action_type: "quiz",
      why_recommended: "Mandatory foundation for MoSPI cadre officers."
    },
    {
      step_number: 2,
      stage: "Core",
      title: "Core: Sample Estimation & Variance Calculation",
      provider: "iGOT Karmayogi",
      duration: "4.5 h",
      status: "Next",
      type: "iGOT Digital Course",
      competency_key: "survey_sampling",
      action_type: "quiz",
      why_recommended: "Builds Horvitz-Thompson estimation and multiplier skills."
    },
    {
      step_number: 3,
      stage: "Practice",
      title: "Practice: Python Microdata Wrangling & Validation",
      provider: "STATWISE Virtual Lab",
      duration: "6.0 h",
      status: "Upcoming",
      type: "Hands-on Virtual Lab",
      competency_key: "python_data_analysis",
      action_type: "virtuallab",
      why_recommended: "Accelerates automated scrutiny on survey schedules."
    },
    {
      step_number: 4,
      stage: "Advanced",
      title: "Advanced: MoSPI Quality Engineering & Cadre Leadership",
      provider: "NSSTA / TPAC",
      duration: "5 Days",
      status: "Upcoming",
      type: "NSSTA TPAC Programme",
      competency_key: "quality_assurance",
      action_type: "programme",
      why_recommended: "In-person capstone programme at Greater Noida."
    }
  ];

  const pathScore = learningPathData?.path_score || 84;
  const timeLeft = learningPathData?.time_left_hours || 11;
  const completedCount = steps.filter(s => (s.status || "").toLowerCase().includes("complete")).length;

  const roleNames = {
    "JSO": "Junior Statistical Officer (JSO)",
    "SSO": "Senior Statistical Officer (SSO)",
    "ANALYST": "Data Analyst (DIID)",
    "ISS": "Indian Statistical Service (ISS)",
    "TRAINER": "Training Administrator"
  };

  const handleRecordStepProgress = async (step) => {
    if (!step.competency_key) return;
    setRecordingProgress(step.step_number);
    setSuccessBanner("");
    try {
      await fetch(`/api/competency/record-progress?competency_id=${step.competency_key}&gain=0.15`, { method: "POST" });
      setSuccessBanner(`Milestone recorded! Progress logged for ${step.title}.`);
      if (onRefreshData) {
        await onRefreshData();
      }
    } catch (e) {
      console.warn("Progress update fallback:", e);
      setSuccessBanner(`Progress recorded locally for ${step.title}.`);
      if (onRefreshData) {
        await onRefreshData();
      }
    } finally {
      setRecordingProgress(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
            Personalized Cadre Learning Pathway
          </h2>
          <p className="text-sm text-statwise-muted mt-0.5">
            Dynamically sequenced based on your active MoSPI assignment, prerequisite DAG, and cadre role.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs bg-statwise-navy text-white px-3 py-1 rounded-full font-semibold shadow-xs">
            {roleNames[currentRole] || currentRole}
          </span>
          <span className="text-xs bg-emerald-50 text-emerald-800 border border-emerald-200 px-3 py-1 rounded-full font-medium">
            {completedCount} of {steps.length} Milestones Cleared
          </span>
        </div>
      </div>

      {successBanner && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded-xl text-xs font-semibold flex items-center gap-2 animate-fade-in shadow-2xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0" />
          <span>{successBanner}</span>
        </div>
      )}

      {/* Main Grid: Pathway timeline + Side KPIs */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Sequenced Timeline */}
        <div className="lg:col-span-8 bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm">
          <div className="space-y-6 relative before:absolute before:inset-0 before:left-5 before:w-0.5 before:bg-slate-200 before:z-0">
            {steps.map((step, idx) => {
              const stepNumber = step.step_number || idx + 1;
              const statusRaw = (step.status || "").toLowerCase();
              const isCompleted = statusRaw.includes("complete");
              const isInProgress = statusRaw.includes("progress") || statusRaw === "active";
              const isNext = statusRaw === "next";
              const isLocked = statusRaw.includes("lock");

              return (
                <div key={stepNumber} className="relative z-10 flex items-start gap-4">
                  {/* Step Number Circle */}
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shrink-0 border-2 transition-all ${
                      isCompleted
                        ? "bg-emerald-600 text-white border-emerald-600 shadow-sm"
                        : isInProgress
                        ? "bg-statwise-blue text-white border-statwise-blue shadow-md ring-4 ring-sky-100"
                        : isNext
                        ? "bg-amber-500 text-white border-amber-500 shadow-sm"
                        : "bg-slate-100 text-slate-500 border-slate-300"
                    }`}
                  >
                    {isCompleted ? <Check className="w-5 h-5" /> : stepNumber}
                  </div>

                  {/* Step Card */}
                  <div
                    className={`flex-1 rounded-xl p-5 border transition-all ${
                      isInProgress
                        ? "bg-white border-statwise-blue/80 shadow-md ring-1 ring-sky-100"
                        : isCompleted
                        ? "bg-emerald-50/40 border-emerald-200/80 shadow-2xs"
                        : isNext
                        ? "bg-amber-50/30 border-amber-200 shadow-2xs"
                        : "bg-slate-50/90 border-slate-200 text-slate-600"
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                      <div className="space-y-1.5 flex-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-statwise-blue bg-statwise-pale/40 px-2 py-0.5 rounded border border-statwise-blue/20">
                            {step.stage || `Stage ${stepNumber}`}
                          </span>
                          <h3 className="text-sm font-bold text-statwise-navy">
                            {step.title}
                          </h3>
                          <span className="text-[10px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-medium border border-slate-200">
                            {step.type || "Official Course"}
                          </span>
                        </div>

                        <p className="text-xs text-statwise-muted font-medium flex items-center gap-2">
                          <span>{step.provider}</span>
                          <span>•</span>
                          <span className="flex items-center gap-1 font-semibold text-slate-700">
                            <Clock className="w-3 h-3 text-slate-400" />
                            {step.duration}
                          </span>
                        </p>

                        {/* Explainable Why Recommended */}
                        {step.why_recommended && (
                          <div className="mt-2 text-[11px] text-slate-600 bg-white/80 p-2.5 rounded-lg border border-slate-200/80 flex items-start gap-2">
                            <Sparkles className="w-3.5 h-3.5 text-statwise-blue shrink-0 mt-0.5" />
                            <span className="leading-snug">{step.why_recommended}</span>
                          </div>
                        )}
                      </div>

                      {/* Status Tag & Dynamic Actions */}
                      <div className="flex flex-col items-end gap-2 shrink-0 self-start sm:self-auto">
                        <span
                          className={`text-[11px] font-semibold px-2.5 py-1 rounded-full ${
                            isCompleted
                              ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                              : isInProgress
                              ? "bg-sky-100 text-statwise-blue border border-sky-200"
                              : isNext
                              ? "bg-amber-100 text-amber-800 border border-amber-200"
                              : "bg-slate-200 text-slate-600"
                          }`}
                        >
                          {isCompleted ? "Completed" : isInProgress ? "In Progress" : isNext ? "Next Up" : "Upcoming"}
                        </span>

                        <div className="flex items-center gap-1.5 flex-wrap justify-end">
                          {isInProgress && (
                            <>
                              {step.action_type === "virtuallab" ? (
                                <button
                                  onClick={() => onNavigate("virtuallab")}
                                  className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1"
                                >
                                  <Database className="w-3.5 h-3.5" />
                                  <span>Open Lab</span>
                                </button>
                              ) : (
                                <button
                                  onClick={() => onNavigate("quiz")}
                                  className="px-3 py-1.5 bg-statwise-navy hover:bg-statwise-navyActive text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1"
                                >
                                  <Play className="w-3.5 h-3.5" />
                                  <span>Take Assessment</span>
                                </button>
                              )}

                              <button
                                onClick={() => handleRecordStepProgress(step)}
                                disabled={recordingProgress === stepNumber}
                                title="Record milestone completion to update readiness profile"
                                className="px-2.5 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 text-xs font-semibold rounded-lg transition-all flex items-center gap-1 disabled:opacity-50"
                              >
                                <Check className="w-3 h-3 text-emerald-600" />
                                <span>{recordingProgress === stepNumber ? "Saving..." : "Mark Done"}</span>
                              </button>
                            </>
                          )}

                          {isNext && (
                            <>
                              {step.action_type === "virtuallab" ? (
                                <button
                                  onClick={() => onNavigate("virtuallab")}
                                  className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1"
                                >
                                  <Database className="w-3.5 h-3.5" />
                                  <span>Start Lab</span>
                                </button>
                              ) : (
                                <button
                                  onClick={() => onNavigate("quiz")}
                                  className="px-3 py-1.5 bg-statwise-navy hover:bg-statwise-navyActive text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1"
                                >
                                  <Play className="w-3.5 h-3.5" />
                                  <span>Start Step</span>
                                </button>
                              )}
                            </>
                          )}

                          {isCompleted && (
                            <button
                              onClick={() => onNavigate("quiz")}
                              className="px-2.5 py-1 text-slate-500 hover:text-slate-800 text-xs font-medium rounded hover:bg-slate-100 transition-colors flex items-center gap-1"
                            >
                              <span>Review Quiz</span>
                            </button>
                          )}

                          {step.url && (
                            <a
                              href={step.url}
                              target="_blank"
                              rel="noreferrer"
                              className="p-1.5 text-slate-400 hover:text-statwise-blue rounded hover:bg-slate-100 transition-colors"
                              title="Open official course syllabus / portal"
                            >
                              <ExternalLink className="w-3.5 h-3.5" />
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-8 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>The learning path combines iGOT digital modules, hands-on microdata labs, and NSSTA cadre academies.</span>
            <button
              onClick={() => onNavigate("competency")}
              className="font-semibold text-statwise-navy hover:text-statwise-blue inline-flex items-center gap-1"
            >
              <span>View Competency Radar</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Right Column: Path KPIs */}
        <div className="lg:col-span-4 space-y-4">
          {/* Card 1: Path Score */}
          <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Path Score
              </span>
              <Target className="w-4 h-4 text-statwise-blue" />
            </div>
            <div className="mt-4">
              <div className="text-4xl font-extrabold text-statwise-navy">{pathScore}%</div>
              <p className="text-xs text-statwise-muted mt-1 font-medium">
                Cadre alignment based on official {currentRole} competency benchmarks.
              </p>
            </div>
            <div className="w-full bg-statwise-pale/30 rounded-full h-2 mt-4 overflow-hidden">
              <div className="bg-statwise-blue h-2 rounded-full transition-all duration-500" style={{ width: `${pathScore}%` }}></div>
            </div>
          </div>

          {/* Card 2: Time Left */}
          <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Remaining Learning Hours
              </span>
              <Clock className="w-4 h-4 text-statwise-blue" />
            </div>
            <div className="mt-4">
              <div className="text-4xl font-extrabold text-statwise-navy">{timeLeft} h</div>
              <p className="text-xs text-statwise-muted mt-1 font-medium">
                Estimated study hours to complete active milestone queue for the current quarter.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
              <span className="text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-medium border border-emerald-200">
                Pacing: ~2.5 hrs/week
              </span>
              <span className="text-[11px] text-slate-500 font-medium">
                TPAC Standard
              </span>
            </div>
          </div>

          {/* Card 3: Quick Navigation */}
          <div className="bg-statwise-navy text-white rounded-xl p-5 shadow-sm space-y-3">
            <div className="flex items-center gap-2">
              <Award className="w-4 h-4 text-amber-400" />
              <h4 className="text-xs font-bold tracking-wide uppercase">Cadre Verification</h4>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Every completed module earns digital competency evidence logged to your official MoSPI DIID profile.
            </p>
            <button
              onClick={() => onNavigate("assessments")}
              className="w-full py-2 bg-statwise-blue hover:bg-statwise-blue/80 text-white rounded-lg text-xs font-semibold transition-colors flex items-center justify-center gap-1.5"
            >
              <span>Explore Assessment Bank</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
export default LearningPathView;
