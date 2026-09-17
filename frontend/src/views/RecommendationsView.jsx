import React, { useState } from "react";
import { ExternalLink, Sparkles, CheckCircle2, BookOpen, Building2, AlertTriangle, ShieldCheck, MapPin, Clock } from "lucide-react";

export function RecommendationsView({ recommendations, onSelectCourse }) {
  const [activeFilter, setActiveFilter] = useState("All");

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

      {/* Mandatory Prompt F Integration Disclaimer Card */}
      <div className="bg-amber-50/90 border border-amber-200/90 rounded-xl p-4 flex items-start gap-3.5 shadow-sm">
        <AlertTriangle className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-amber-900 uppercase tracking-wider">
              Integration Architecture Notice (Prompt F)
            </span>
            <span className="text-[10px] bg-amber-200/80 text-amber-900 font-semibold px-2 py-0.5 rounded-full">
              Adapter: CourseProvider (Mock/Sandbox Active)
            </span>
          </div>
          <p className="text-xs text-amber-800 leading-relaxed font-medium">
            Operating in Sandboxed Simulation Mode. Real-time production sync requires official DoPT/MoSPI API credentials (<code className="bg-amber-100 px-1 rounded">IGOT_CLIENT_ID</code> & <code className="bg-amber-100 px-1 rounded">IGOT_CLIENT_SECRET</code>). All 30 digital courses and 15 NSSTA programmes reflect authorized MoSPI statistical curriculum standards.
          </p>
        </div>
      </div>

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
