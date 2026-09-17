import React from "react";
import { ArrowRight, BookOpen, Clock, Target, TrendingUp, AlertCircle, CheckCircle2 } from "lucide-react";

export function OverviewView({ profileData, onNavigate }) {
  const kpis = profileData?.kpis || {
    overall_readiness: 68,
    priority_gaps_count: 6,
    urgent_gaps_count: 3,
    learning_hours: 24.5,
    quiz_accuracy: 82
  };

  const domainHealth = profileData?.domain_health || {
    Statistical: 68,
    Technical: 54,
    "Digital Governance": 62,
    Behavioural: 72
  };

  const learnerName = profileData?.learner?.name ? profileData.learner.name.split(" ")[0] : "Officer";

  return (
    <div className="space-y-6">
      {/* Top Welcome Title */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          Welcome, {profileData?.learner?.name || "Statistical Officer"}
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Your next best learning action is ready.
        </p>
      </div>

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Overall Readiness */}
        <div className="bg-white rounded-xl p-4 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-statwise-muted uppercase tracking-wider">Overall readiness</span>
            <Target className="w-4 h-4 text-statwise-blue" />
          </div>
          <div className="mt-3">
            <div className="text-3xl font-bold text-statwise-navy">{kpis.overall_readiness}%</div>
            <div className="text-xs text-statwise-muted mt-1 flex items-center justify-between">
              <span>Target: 85%</span>
              <span className="text-[11px] font-medium text-emerald-600">On Track</span>
            </div>
            <div className="w-full bg-statwise-pale/30 rounded-full h-1.5 mt-2 overflow-hidden">
              <div
                className="bg-statwise-blue h-1.5 rounded-full transition-all duration-500"
                style={{ width: `${kpis.overall_readiness}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Card 2: Priority Gaps */}
        <div className="bg-white rounded-xl p-4 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-statwise-muted uppercase tracking-wider">Priority gaps</span>
            <AlertCircle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-3">
            <div className="text-3xl font-bold text-statwise-navy">
              {String(kpis.priority_gaps_count).padStart(2, '0')}
            </div>
            <div className="text-xs text-amber-600 font-medium mt-1">
              {kpis.urgent_gaps_count} urgent gaps flagged
            </div>
            <div className="w-full bg-amber-100 rounded-full h-1.5 mt-2 overflow-hidden">
              <div
                className="bg-amber-500 h-1.5 rounded-full"
                style={{ width: `${(kpis.urgent_gaps_count / Math.max(kpis.priority_gaps_count, 1)) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Card 3: Learning Hours */}
        <div className="bg-white rounded-xl p-4 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-statwise-muted uppercase tracking-wider">Learning hours</span>
            <Clock className="w-4 h-4 text-statwise-blue" />
          </div>
          <div className="mt-3">
            <div className="text-3xl font-bold text-statwise-navy">{kpis.learning_hours} h</div>
            <div className="text-xs text-statwise-muted mt-1">This quarter (TPAC quota: 30h)</div>
            <div className="w-full bg-statwise-pale/30 rounded-full h-1.5 mt-2 overflow-hidden">
              <div
                className="bg-statwise-blue h-1.5 rounded-full"
                style={{ width: `${Math.min(100, (kpis.learning_hours / 30) * 100)}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Card 4: Quiz Accuracy */}
        <div className="bg-white rounded-xl p-4 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-statwise-muted uppercase tracking-wider">Quiz accuracy</span>
            <TrendingUp className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-3">
            <div className="text-3xl font-bold text-statwise-navy">{kpis.quiz_accuracy}%</div>
            <div className="text-xs text-emerald-600 font-medium mt-1">+9% this month</div>
            <div className="w-full bg-emerald-100 rounded-full h-1.5 mt-2 overflow-hidden">
              <div
                className="bg-emerald-600 h-1.5 rounded-full"
                style={{ width: `${kpis.quiz_accuracy}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Recommended Next Step & Skill Health */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Recommended next step Hero Card */}
        <div className="lg:col-span-7 bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Recommended next step
              </span>
              <span className="text-[11px] bg-sky-50 text-statwise-blue border border-sky-200 px-2 py-0.5 rounded font-medium">
                High Priority
              </span>
            </div>

            <h3 className="text-xl font-bold text-statwise-navy leading-snug">
              Survey Sampling for Official Statistics
            </h3>
            <p className="text-xs text-statwise-muted mt-1 font-medium">
              iGOT course • Intermediate • 4 hours
            </p>

            {/* Match Indicator */}
            <div className="mt-5 p-4 bg-statwise-canvas rounded-lg border border-statwise-pale/40">
              <div className="flex items-center justify-between text-xs font-semibold text-statwise-navy mb-1.5">
                <span>62% competency match</span>
                <span className="text-statwise-blue">Addresses Priority Gap</span>
              </div>
              <div className="w-full bg-statwise-pale/30 rounded-full h-2 overflow-hidden">
                <div className="bg-statwise-blue h-2 rounded-full" style={{ width: "62%" }}></div>
              </div>
              <p className="text-[11px] text-slate-500 mt-2">
                Closes sampling multiplier calculation and Horvitz-Thompson variance gaps identified in your profile.
              </p>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
            <span className="text-[11px] text-slate-400">
              Based on role, progress and department priorities
            </span>
            <button
              onClick={() => onNavigate("pathway")}
              className="inline-flex items-center gap-2 px-4 py-2 bg-statwise-navy text-white text-xs font-semibold rounded-lg hover:bg-statwise-navyActive shadow-sm transition-all"
            >
              <span>Open learning path</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Right Column: Skill health progress bars */}
        <div className="lg:col-span-5 bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Skill health
              </span>
              <span className="text-[11px] text-slate-400">4 Cadre Domains</span>
            </div>

            <div className="space-y-4">
              {/* Statistical */}
              <div>
                <div className="flex justify-between text-xs font-medium text-slate-700 mb-1">
                  <span>Statistical</span>
                  <span className="font-semibold text-statwise-navy">{domainHealth.Statistical || 68}%</span>
                </div>
                <div className="w-full bg-statwise-pale/30 rounded-full h-2 overflow-hidden">
                  <div className="bg-statwise-blue h-2 rounded-full" style={{ width: `${domainHealth.Statistical || 68}%` }}></div>
                </div>
              </div>

              {/* Technical */}
              <div>
                <div className="flex justify-between text-xs font-medium text-slate-700 mb-1">
                  <span>Technical</span>
                  <span className="font-semibold text-statwise-navy">{domainHealth.Technical || 54}%</span>
                </div>
                <div className="w-full bg-statwise-pale/30 rounded-full h-2 overflow-hidden">
                  <div className="bg-amber-500 h-2 rounded-full" style={{ width: `${domainHealth.Technical || 54}%` }}></div>
                </div>
              </div>

              {/* Digital governance */}
              <div>
                <div className="flex justify-between text-xs font-medium text-slate-700 mb-1">
                  <span>Digital governance</span>
                  <span className="font-semibold text-statwise-navy">{domainHealth["Digital Governance"] || 62}%</span>
                </div>
                <div className="w-full bg-statwise-pale/30 rounded-full h-2 overflow-hidden">
                  <div className="bg-sky-600 h-2 rounded-full" style={{ width: `${domainHealth["Digital Governance"] || 62}%` }}></div>
                </div>
              </div>

              {/* Behavioural */}
              <div>
                <div className="flex justify-between text-xs font-medium text-slate-700 mb-1">
                  <span>Behavioural</span>
                  <span className="font-semibold text-statwise-navy">{domainHealth.Behavioural || 72}%</span>
                </div>
                <div className="w-full bg-statwise-pale/30 rounded-full h-2 overflow-hidden">
                  <div className="bg-emerald-600 h-2 rounded-full" style={{ width: `${domainHealth.Behavioural || 72}%` }}></div>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end">
            <button
              onClick={() => onNavigate("competency")}
              className="text-xs font-semibold text-statwise-blue hover:text-statwise-navy flex items-center gap-1 transition-colors"
            >
              View radar breakdown &rarr;
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
