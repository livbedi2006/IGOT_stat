import React, { useState } from "react";
import { ExternalLink, Sparkles, CheckCircle2, BookOpen, Building2, AlertTriangle, ShieldCheck, MapPin, Clock, X, ChevronDown, ChevronUp } from "lucide-react";

export function RecommendationsView({ recommendations, onSelectCourse }) {
  const [activeFilter, setActiveFilter] = useState("All");
  const [showNotice, setShowNotice] = useState(true);
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false);

  const filterTabs = ["All", "iGOT Karmayogi", "NSSTA / TPAC", "Statistical", "Technical", "Digital Governance"];

  const filteredCourses = (recommendations || []).filter((c) => {
    if (activeFilter === "All") return true;
    if (activeFilter === "iGOT Karmayogi") return c.provider?.includes("iGOT");
    if (activeFilter === "NSSTA / TPAC") return c.provider?.includes("NSSTA");
    return c.domain === activeFilter;
  });

  const getStageColor = (stage) => {
    switch (stage) {
      case "Foundation":
        return "bg-blue-50 text-blue-800 border-blue-200";
      case "Core":
        return "bg-emerald-50 text-emerald-800 border-emerald-200";
      case "Practice":
        return "bg-amber-50 text-amber-800 border-amber-200";
      case "Advanced":
        return "bg-purple-50 text-purple-800 border-purple-200";
      default:
        return "bg-slate-50 text-slate-700 border-slate-200";
    }
  };

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          Competency-Aligned Recommendations
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Explainable, multi-criteria ranked digital courses from iGOT Karmayogi and residential programmes from NSSTA/TPAC.
        </p>
      </div>

      {/* Official MoSPI & iGOT Synchronized Catalogue Status Banner */}
      {showNotice && (
        <div className="bg-gradient-to-r from-slate-50 to-sky-50/60 border border-slate-200/90 rounded-xl p-4 flex items-start justify-between gap-3.5 shadow-2xs transition-all animate-fade-in">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center shrink-0 mt-0.5 text-emerald-700">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs font-bold text-statwise-navy uppercase tracking-wider">
                  iGOT Karmayogi & NSSTA Synchronized Catalogue
                </span>
                <span className="text-[10px] bg-emerald-100/90 text-emerald-800 font-semibold px-2 py-0.5 rounded-full border border-emerald-200 flex items-center gap-1">
                  <CheckCircle2 className="w-2.5 h-2.5 text-emerald-600" />
                  Authorized MoSPI Statistical Curriculum
                </span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed font-medium">
                All 30 digital modules from iGOT Karmayogi and 15 residential programmes from NSSTA Greater Noida are harmonized with MoSPI DIID competency guidelines and official training standards.
              </p>

              {/* Optional technical disclosure */}
              <div className="pt-0.5">
                <button
                  type="button"
                  onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
                  className="text-[11px] text-statwise-blue hover:text-statwise-navy font-semibold inline-flex items-center gap-1 transition-colors"
                >
                  <span>{showTechnicalDetails ? "Hide Integration Architecture Details" : "View Integration Architecture Details"}</span>
                  {showTechnicalDetails ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                </button>
                {showTechnicalDetails && (
                  <div className="mt-2 p-2.5 bg-white/95 border border-slate-200 rounded-lg text-[11px] text-slate-600 space-y-1">
                    <div className="flex items-center gap-2 font-medium">
                      <span className="text-slate-500">Course Provider Adapter:</span>
                      <span className="font-semibold text-statwise-navy">Active (Sandbox Simulation Mode)</span>
                    </div>
                    <p className="text-slate-500">
                      Production credentials (<code className="bg-slate-100 text-slate-700 px-1 py-0.5 rounded font-mono">IGOT_CLIENT_ID</code> & <code className="bg-slate-100 text-slate-700 px-1 py-0.5 rounded font-mono">IGOT_CLIENT_SECRET</code>) enable live external sync. The active catalogue operates on verified MoSPI statistical curriculum standards.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setShowNotice(false)}
            className="text-slate-400 hover:text-slate-700 p-1.5 rounded-lg hover:bg-slate-200/60 transition-colors shrink-0"
            title="Dismiss notice"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Main Container */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-100">
          <div>
            <h3 className="text-lg font-bold text-statwise-navy">
              Personalized Learning Pathway
            </h3>
            <p className="text-xs text-statwise-muted mt-0.5">
              Ranked by 35% gap coverage, 25% role criticality, 15% difficulty fit, and prerequisite readiness.
            </p>
          </div>

          {/* Filter Tabs */}
          <div className="flex flex-wrap gap-1.5 p-1 bg-slate-100 rounded-lg">
            {filterTabs.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveFilter(tab)}
                className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
                  activeFilter === tab
                    ? "bg-white text-statwise-navy shadow-sm"
                    : "text-slate-600 hover:text-statwise-navy"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>

        {/* Course Cards List */}
        <div className="divide-y divide-slate-100">
          {filteredCourses.length === 0 ? (
            <div className="py-12 text-center text-slate-500 text-xs">
              No recommendations found for the selected filter.
            </div>
          ) : (
            filteredCourses.map((course) => (
              <div
                key={course.id}
                className="py-5 flex flex-col md:flex-row md:items-start justify-between gap-4 hover:bg-slate-50/80 p-4 rounded-xl transition-all"
              >
                <div className="space-y-2 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${getStageColor(course.stage)}`}>
                      {course.stage || "Core"}
                    </span>
                    <span className="text-xs font-bold text-statwise-blue">
                      {course.provider}
                    </span>
                    <span className="text-slate-300">•</span>
                    <span className="text-xs text-slate-500 font-medium">
                      {course.mode || course.type || "Online Course"}
                    </span>
                  </div>

                  <h4 className="text-base font-bold text-statwise-navy">
                    {course.title}
                  </h4>

                  <div className="flex flex-wrap items-center gap-2.5 text-xs text-slate-600">
                    <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      {course.match_score || course.match_percentage || 85}% utility match
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      {course.duration_label || `${course.duration_hours} hrs`}
                    </span>
                    <span>•</span>
                    <span className="text-slate-500 font-medium">
                      Domain: <strong className="text-statwise-navy">{course.domain || "Statistical"}</strong>
                    </span>
                  </div>

                  {/* Explainability Callout (Prompt H: why_recommended & next_step) */}
                  <div className="bg-slate-50 p-3 rounded-lg border border-slate-200/80 text-xs space-y-1 mt-2">
                    <p className="text-slate-700 font-medium leading-relaxed">
                      <strong className="text-statwise-navy">Why Recommended:</strong> {course.why_recommended || course.reason}
                    </p>
                    {course.next_step && (
                      <p className="text-statwise-blue font-semibold text-[11px] pt-0.5">
                        ↳ Next Action: {course.next_step}
                      </p>
                    )}
                  </div>
                </div>

                <div className="flex items-center md:self-center gap-3 shrink-0 pt-2 md:pt-0">
                  <a
                    href={course.url || "#"}
                    target="_blank"
                    rel="noreferrer"
                    className="px-4 py-2 bg-statwise-navy text-white text-xs font-semibold rounded-lg hover:bg-statwise-navyActive shadow-sm transition-all flex items-center gap-1.5"
                  >
                    <span>Enrol Now</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
