import React from "react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  ResponsiveContainer,
  Tooltip
} from "recharts";
import { ShieldCheck, ArrowUpRight, Sparkles, Filter } from "lucide-react";

export function CompetencyView({ profileData, onNavigate }) {
  const radarData = profileData?.radar_chart || [
    { skill: "Survey", full_name: "Survey Design & Sampling", current: 62, target: 85 },
    { skill: "Python", full_name: "Python for Data Analysis", current: 48, target: 75 },
    { skill: "Metadata", full_name: "Metadata Standards (SDMX)", current: 55, target: 80 },
    { skill: "Leadership", full_name: "Leadership & Ethics", current: 70, target: 75 },
    { skill: "GIS", full_name: "GIS Fundamentals", current: 44, target: 70 },
    { skill: "Project Mgmt", full_name: "Statistical Project Management", current: 66, target: 80 }
  ];

  const topGaps = profileData?.top_gaps || [
    { id: "python_data_analysis", name: "Python for data analysis", current_mastery: 48, target_mastery: 75, domain: "Technical" },
    { id: "survey_design", name: "Survey design & sampling", current_mastery: 62, target_mastery: 85, domain: "Statistical" },
    { id: "metadata_standards", name: "Metadata standards (SDMX)", current_mastery: 55, target_mastery: 80, domain: "Digital Governance" },
    { id: "gis_fundamentals", name: "GIS fundamentals", current_mastery: 44, target_mastery: 70, domain: "Technical" },
    { id: "project_management", name: "Project management", current_mastery: 66, target_mastery: 80, domain: "Behavioural" }
  ];

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          Competency profile
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Evidence combines profile data, assessments and completed learning.
        </p>
      </div>

      {/* Main Grid: Radar Chart + Top Gaps */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Interactive Competency Radar */}
        <div className="lg:col-span-6 bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Competency Radar (Target vs Current)
              </span>
              <span className="text-[11px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">
                Official JSO Cadre Bar
              </span>
            </div>

            <div className="h-[340px] w-full mt-2">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData} outerRadius="75%">
                  <PolarGrid stroke="#E2E8F0" />
                  <PolarAngleAxis dataKey="skill" tick={{ fill: "#0A1931", fontSize: 12, fontWeight: 500 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#CBD5E1" tick={{ fontSize: 10 }} />
                  <Radar
                    name="Target Proficiency (Role Bar)"
                    dataKey="target"
                    stroke="#4A7FA7"
                    fill="#B3CFE5"
                    fillOpacity={0.35}
                    strokeWidth={2}
                    strokeDasharray="4 4"
                  />
                  <Radar
                    name="Current Mastery (Assessed)"
                    dataKey="current"
                    stroke="#0A1931"
                    fill="#0A1931"
                    fillOpacity={0.45}
                    strokeWidth={2.5}
                  />
                  <Tooltip
                    formatter={(val, name) => [`${val}%`, name]}
                    contentStyle={{ backgroundColor: "#FFFFFF", borderRadius: 8, borderColor: "#E2E8F0", fontSize: 12 }}
                  />
                  <Legend wrapperStyle={{ fontSize: 12, paddingTop: 10 }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
            <div className="flex items-center gap-1.5 text-slate-600">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>Role target overlay • Privacy protected under DPDP Act 2023</span>
            </div>
          </div>
        </div>

        {/* Right Column: Top Gaps List */}
        <div className="lg:col-span-6 bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-bold text-statwise-muted uppercase tracking-wider">
                Top gaps (Priority Ranked)
              </span>
              <span className="text-[11px] text-statwise-blue font-medium">
                Gap = Target - Current
              </span>
            </div>

            <div className="space-y-4">
              {topGaps.map((gap, idx) => {
                const gapDiff = Math.max(0, gap.target_mastery - gap.current_mastery);
                return (
                  <div key={gap.id || idx} className="p-3 bg-statwise-canvas rounded-lg border border-slate-200/80">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-semibold text-statwise-navy">
                        {gap.name}
                      </span>
                      <span className="text-[11px] text-amber-700 font-bold bg-amber-100/80 px-2 py-0.5 rounded">
                        {gapDiff}% gap
                      </span>
                    </div>

                    {/* Comparative Dual Progress Bar */}
                    <div className="space-y-1">
                      <div className="flex justify-between text-[11px] text-slate-500">
                        <span>Current: {gap.current_mastery}%</span>
                        <span>Target: {gap.target_mastery}%</span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-2 relative overflow-hidden">
                        {/* Target Marker Bar */}
                        <div
                          className="bg-statwise-pale h-2 absolute left-0 top-0 rounded-full"
                          style={{ width: `${gap.target_mastery}%` }}
                        ></div>
                        {/* Current Solid Bar */}
                        <div
                          className="bg-statwise-navy h-2 absolute left-0 top-0 rounded-full"
                          style={{ width: `${gap.current_mastery}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
            <span className="text-[11px] text-slate-500">
              Ordered by statutory criticality and career progression
            </span>
            <button
              onClick={() => onNavigate("recommendations")}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-statwise-blue text-white text-xs font-semibold rounded-lg hover:bg-statwise-navy transition-all shadow-sm"
            >
              <span>View tailored courses</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
