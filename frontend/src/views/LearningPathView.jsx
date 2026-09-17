import React from "react";
import { Check, Lock, Play, ArrowRight, Clock, Target, Sparkles, Database } from "lucide-react";

export function LearningPathView({ learningPathData, onNavigate }) {
  const steps = learningPathData?.steps || [
    {
      step_number: 1,
      title: "Foundation: Survey Design",
      provider: "iGOT",
      duration: "3 h",
      status: "Completed",
      type: "iGOT Course"
    },
    {
      step_number: 2,
      title: "Core: Survey Sampling",
      provider: "iGOT",
      duration: "4 h",
      status: "In progress",
      type: "iGOT Course"
    },
    {
      step_number: 3,
      title: "Practice: Python Data Cleaning",
      provider: "Virtual lab",
      duration: "2 h",
      status: "Next",
      type: "Hands-on Virtual Lab"
    },
    {
      step_number: 4,
      title: "Advanced: Data Quality Frameworks",
      provider: "NSSTA/TPAC",
      duration: "5 days",
      status: "Locked until step 2",
      type: "NSSTA TPAC Programme"
    }
  ];

  const pathScore = learningPathData?.path_score || 84;
  const timeLeft = learningPathData?.time_left_hours || 11;

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          Your personalized pathway
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Courses are ordered using prerequisites, role relevance and available time.
        </p>
      </div>

      {/* Main Grid: Pathway timeline + Side KPIs */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Sequenced Timeline */}
        <div className="lg:col-span-8 bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm">
          <div className="space-y-6 relative before:absolute before:inset-0 before:left-5 before:w-0.5 before:bg-slate-200 before:z-0">
            {steps.map((step) => {
              const isCompleted = step.status === "Completed";
              const isInProgress = step.status === "In progress";
              const isNext = step.status === "Next";
              const isLocked = step.status.includes("Locked");

              return (
                <div key={step.step_number} className="relative z-10 flex items-start gap-4">
                  {/* Step Number Circle */}
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shrink-0 border-2 transition-all ${
                      isCompleted
                        ? "bg-emerald-600 text-white border-emerald-600 shadow-sm"
                        : isInProgress
                        ? "bg-statwise-blue text-white border-statwise-blue shadow-md ring-4 ring-sky-100"
                        : isNext
                        ? "bg-amber-500 text-white border-amber-500 shadow-sm"
                        : "bg-slate-100 text-slate-400 border-slate-300"
                    }`}
                  >
                    {isCompleted ? <Check className="w-5 h-5" /> : step.step_number}
                  </div>

                  {/* Step Card */}
                  <div
                    className={`flex-1 rounded-xl p-4 border transition-all ${
                      isInProgress
                        ? "bg-white border-statwise-blue/80 shadow-md ring-1 ring-sky-100"
                        : isCompleted
                        ? "bg-emerald-50/40 border-emerald-200/80"
                        : isNext
                        ? "bg-amber-50/30 border-amber-200"
                        : "bg-slate-50 border-slate-200 text-slate-500 opacity-90"
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-sm font-bold text-statwise-navy">
                            {step.title}
                          </h3>
                          <span className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium border border-slate-200">
                            {step.type}
                          </span>
                        </div>
                        <p className="text-xs text-statwise-muted mt-0.5">
                          {step.provider} • {step.duration}
                        </p>
                      </div>

                      {/* Status Tag & Action */}
                      <div className="flex items-center gap-2 self-start sm:self-auto">
                        <span
                          className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                            isCompleted
                              ? "bg-emerald-100 text-emerald-800"
                              : isInProgress
                              ? "bg-sky-100 text-statwise-blue"
                              : isNext
                              ? "bg-amber-100 text-amber-800"
                              : "bg-slate-200 text-slate-600"
                          }`}
                        >
                          {step.status}
                        </span>

                        {isInProgress && (
                          <button
                            onClick={() => onNavigate("quiz")}
                            className="px-3 py-1 bg-statwise-navy text-white text-xs font-semibold rounded hover:bg-statwise-navyActive shadow-sm transition-colors flex items-center gap-1"
                          >
                            <Play className="w-3 h-3" />
                            <span>Continue</span>
                          </button>
                        )}

                        {isNext && (
                          <button
                            onClick={() => onNavigate("virtuallab")}
                            className="px-3 py-1 bg-amber-600 text-white text-xs font-semibold rounded hover:bg-amber-700 shadow-sm transition-colors flex items-center gap-1"
                          >
                            <Database className="w-3 h-3" />
                            <span>Open Lab</span>
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-8 pt-4 border-t border-slate-100 text-xs text-slate-500">
            The learning path combines online courses, practical activities and NSSTA/TPAC programmes in prerequisite order.
          </div>
        </div>

        {/* Right Column: Path KPIs */}
        <div className="lg:col-span-4 space-y-4">
          {/* Card 1: Path Score */}
          <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Path score
              </span>
              <Target className="w-4 h-4 text-statwise-blue" />
            </div>
            <div className="mt-4">
              <div className="text-4xl font-extrabold text-statwise-navy">{pathScore}%</div>
              <p className="text-xs text-statwise-muted mt-1 font-medium">
                Role alignment based on current JSO cadre competency guidelines
              </p>
            </div>
            <div className="w-full bg-statwise-pale/30 rounded-full h-2 mt-4 overflow-hidden">
              <div className="bg-statwise-blue h-2 rounded-full" style={{ width: `${pathScore}%` }}></div>
            </div>
          </div>

          {/* Card 2: Time Left */}
          <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Time left
              </span>
              <Clock className="w-4 h-4 text-statwise-blue" />
            </div>
            <div className="mt-4">
              <div className="text-4xl font-extrabold text-statwise-navy">{timeLeft} h</div>
              <p className="text-xs text-statwise-muted mt-1 font-medium">
                Estimated hours remaining this month to complete quarterly milestones
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100">
              <span className="text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-medium border border-emerald-200">
                Pacing: 2.5 hrs / week recommended
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
