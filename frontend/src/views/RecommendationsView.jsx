import React, { useState } from "react";
import { ExternalLink, Sparkles, CheckCircle2, BookOpen, Building2 } from "lucide-react";

export function RecommendationsView({ recommendations, onSelectCourse }) {
  const [activeFilter, setActiveFilter] = useState("All");

  const filterTabs = ["All", "iGOT", "NSSTA / TPAC", "Technical", "Statistical", "Digital Governance"];

  const filteredCourses = (recommendations || []).filter((c) => {
    if (activeFilter === "All") return true;
    if (activeFilter === "iGOT") return c.provider?.includes("iGOT");
    if (activeFilter === "NSSTA / TPAC") return c.provider?.includes("NSSTA");
    return c.domain === activeFilter;
  });

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          Recommendations
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Relevant iGOT courses and NSSTA/TPAC programmes tailored to your competency profile.
        </p>
      </div>

      {/* Main Container */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-100">
          <div>
            <h3 className="text-lg font-bold text-statwise-navy">
              Recommended for you
            </h3>
            <p className="text-xs text-statwise-muted mt-0.5">
              Every recommendation includes a reason and competency outcome.
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
        <div className="divide-y divide-slate-100 mt-4">
          {filteredCourses.length === 0 ? (
            <div className="py-12 text-center text-slate-500 text-xs">
              No courses found for selected filter.
            </div>
          ) : (
            filteredCourses.map((course) => (
              <div
                key={course.id}
                className="py-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/70 p-3 rounded-lg transition-colors"
              >
                <div className="space-y-1 flex-1">
                  <div className="flex items-center gap-2">
                    <h4 className="text-base font-bold text-statwise-navy">
                      {course.title}
                    </h4>
                  </div>
                  <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
                    <span className="text-statwise-blue font-semibold">{course.provider}</span>
                    <span>•</span>
                    <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      {course.match_percentage || 85}% match
                    </span>
                    <span>•</span>
                    <span>{course.duration_label || `${course.duration_hours} h`}</span>
                    <span>•</span>
                    <span className="text-slate-400">{course.domain}</span>
                  </div>
                  <p className="text-xs text-slate-600 font-normal pt-1">
                    {course.reason}
                  </p>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <button
                    onClick={() => onSelectCourse ? onSelectCourse(course) : alert(`Course selected: ${course.title}`)}
                    className="px-5 py-2 bg-statwise-navy text-white text-xs font-semibold rounded-lg hover:bg-statwise-navyActive shadow-sm transition-all flex items-center gap-1.5"
                  >
                    <span>View</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="mt-6 pt-4 border-t border-slate-100 text-xs text-slate-400">
          Recommendations show why each course is relevant, which competency it addresses and where it comes from.
        </div>
      </div>
    </div>
  );
}
