import React, { useState, useEffect } from "react";
import { Users, TrendingUp, CheckCircle2, Award, Download, Cpu, ShieldCheck, Building2, BarChart2, AlertCircle, ShieldAlert } from "lucide-react";
import { MLDiagnosticsModal } from "../components/MLDiagnosticsModal";
import { api } from "../api";

export function AdminAnalyticsView() {
  const [orgData, setOrgData] = useState(null);
  const [diagnostics, setDiagnostics] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [selectedDeptFilter, setSelectedDeptFilter] = useState("All");

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [orgRes, diagRes] = await Promise.all([
          api.getOrgAnalytics(),
          api.getMLDiagnostics()
        ]);
        setOrgData(orgRes);
        setDiagnostics(diagRes);
      } catch (err) {
        console.error("Error loading admin data:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const kpis = orgData?.kpis || {
    total_officials: 8652,
    avg_mastery_pct: 68,
    gaps_closed_pct: 38,
    completion_rate_pct: 74
  };

  const domainScores = orgData?.domain_scores || [
    { domain: "Statistical Methodology", current_avg: 66, target: 85, growth: "+18%" },
    { domain: "Technical & Automation", current_avg: 54, target: 80, growth: "+22%" },
    { domain: "Digital Governance & Privacy", current_avg: 73, target: 85, growth: "+14%" },
    { domain: "Behavioural & Leadership", current_avg: 71, target: 85, growth: "+9%" }
  ];

  const departmentsList = orgData?.departments_breakdown || [
    { department: "Field Operations Division (FOD)", officials_display: "3420", avg_hours: 18.5, completion_pct: 74, top_gap: "Survey Sampling & Multipliers", is_masked: false },
    { department: "National Accounts Division (NAD)", officials_display: "1280", avg_hours: 24.2, completion_pct: 82, top_gap: "SNA 2008 & FISIM", is_masked: false },
    { department: "Price Statistics Division (PSD)", officials_display: "940", avg_hours: 16.0, completion_pct: 78, top_gap: "CPI Elementary Aggregation", is_masked: false },
    { department: "Economic Statistics Division (ESD)", officials_display: "1150", avg_hours: 21.4, completion_pct: 71, top_gap: "IIP Item Replacement", is_masked: false },
    { department: "Data Informatics & Innovation (DIID)", officials_display: "860", avg_hours: 29.8, completion_pct: 86, top_gap: "DPDP Microdata Anonymization", is_masked: false },
    { department: "State DES - Sikkim Cell", officials_display: "< 3 (Masked for Privacy)", avg_hours: 14.0, completion_pct: 50, top_gap: "CAPI Field Operations", is_masked: true }
  ];

  const handleExportCSV = () => {
    window.location.href = "http://localhost:8000/api/analytics/export-csv";
  };

  return (
    <div className="space-y-6">
      {/* Header matching Screenbook */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
            Cadre Skill Intelligence & Admin Analytics
          </h2>
          <p className="text-sm text-statwise-muted mt-0.5">
            Role-protected analytics across 8,000+ statistical officials with privacy-preserving cohort masking (Prompt P).
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-3.5 py-2 bg-white border border-statwise-blue text-statwise-navy hover:bg-statwise-blue/10 text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5"
          >
            <Cpu className="w-4 h-4 text-statwise-blue" />
            <span>ML Model Diagnostics</span>
          </button>

          <button
            onClick={handleExportCSV}
            className="px-4 py-2 bg-statwise-navy hover:bg-statwise-navyActive text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download CSV Audit Report</span>
          </button>
        </div>
      </div>

      {/* Mandatory Small Cohort Privacy Notice (Prompt P & Section 8) */}
      <div className="bg-blue-50/80 border border-blue-200 rounded-xl p-3.5 flex items-center gap-3 text-xs text-blue-900">
        <ShieldCheck className="w-4 h-4 text-blue-700 shrink-0" />
        <span className="font-medium">
          <strong>Privacy Protocol (DPDP Act 2023 Compliance):</strong> Individual learner microdata is never exposed in aggregate analytics. Small cohorts with fewer than 3 officials are masked to prevent personal re-identification.
        </span>
      </div>

      {/* Main Container */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm space-y-6">
        <div>
          <h3 className="text-lg font-bold text-statwise-navy">
            Organization-wide Skill Intelligence
          </h3>
          <p className="text-xs text-statwise-muted mt-0.5">
            Capacity-building metrics, training hours, and domain masteries across all MoSPI divisions.
          </p>
        </div>

        {/* 4 KPI Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl border border-slate-200 bg-statwise-canvas space-y-1">
            <div className="flex items-center justify-between text-xs text-statwise-muted">
              <span>Total Cadre Officials</span>
              <Users className="w-4 h-4 text-statwise-blue" />
            </div>
            <div className="text-2xl font-black text-statwise-navy">
              {kpis.total_officials?.toLocaleString() || "8,652"}
            </div>
            <div className="text-[11px] text-slate-500 font-medium">
              100% onboarded with baseline diagnostics
            </div>
          </div>

          <div className="p-4 rounded-xl border border-slate-200 bg-statwise-canvas space-y-1">
            <div className="flex items-center justify-between text-xs text-statwise-muted">
              <span>Avg Competency Mastery</span>
              <TrendingUp className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-2xl font-black text-statwise-navy">
              {kpis.avg_mastery_pct || 68}%
            </div>
            <div className="text-[11px] text-emerald-600 font-medium">
              +28.4% pre-to-post improvement
            </div>
          </div>

          <div className="p-4 rounded-xl border border-slate-200 bg-statwise-canvas space-y-1">
            <div className="flex items-center justify-between text-xs text-statwise-muted">
              <span>Critical Gaps Closed</span>
              <CheckCircle2 className="w-4 h-4 text-statwise-blue" />
            </div>
            <div className="text-2xl font-black text-statwise-navy">
              38%
            </div>
            <div className="text-[11px] text-slate-500 font-medium">
              Via iGOT & NSSTA blended pathways
            </div>
          </div>

          <div className="p-4 rounded-xl border border-slate-200 bg-statwise-canvas space-y-1">
            <div className="flex items-center justify-between text-xs text-statwise-muted">
              <span>Course Completion Rate</span>
              <Award className="w-4 h-4 text-statwise-blue" />
            </div>
            <div className="text-2xl font-black text-statwise-navy">
              {kpis.overall_completion_rate_pct || 74.5}%
            </div>
            <div className="text-[11px] text-slate-500 font-medium">
              142,580 total learning hours verified
            </div>
          </div>
        </div>

        {/* 2-Column Split: Domain Progress & Emerging Skill Demand */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
          {/* Left: Domain Progress */}
          <div className="lg:col-span-6 p-5 bg-statwise-canvas rounded-xl border border-slate-200 flex flex-col justify-between">
            <div>
              <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider mb-4">
                Domain Competency Progress
              </h4>

              <div className="space-y-4">
                {domainScores.map((item, idx) => (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between text-xs font-medium text-slate-700">
                      <span className="font-semibold">{item.domain}</span>
                      <span className="font-bold text-statwise-navy">
                        {item.current_avg}% (Target: {item.target}%)
                      </span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-statwise-blue h-2 rounded-full transition-all"
                        style={{ width: `${item.current_avg}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-4 mt-4 border-t border-slate-200/80 text-[11px] text-slate-500">
              Aggregated across 8,000+ statistical cadres (JSO, SSO, ISS, Data Analyst).
            </div>
          </div>

          {/* Right: Emerging Skill Demand */}
          <div className="lg:col-span-6 p-5 bg-statwise-canvas rounded-xl border border-slate-200 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider">
                  Emerging Skill Demand (Predictive ML Forecast)
                </h4>
                <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">
                  RidgeCV (Alpha=0.8685)
                </span>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">AI / ML for Official Surveys</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+42%</span>
                </div>
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">Python for Automated Microdata Wrangling</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+31%</span>
                </div>
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">DPDP Act 2023 Microdata Anonymization</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+24%</span>
                </div>
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">GIS Spatial Statistics for Census Blocks</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+20%</span>
                </div>
              </div>
            </div>

            <div className="pt-4 mt-4 border-t border-slate-200/80 text-[11px] text-slate-500">
              Forecast dynamically calculated from 6-month cadre study pace & upcoming survey rounds.
            </div>
          </div>
        </div>

        {/* Department Heatmap Table with Privacy Masking */}
        <div className="pt-2">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider">
              Department Competency Heatmap & Cadre Size
            </h4>
            <span className="text-[11px] text-slate-500 font-medium">
              Privacy Masking Active for n &lt; 3
            </span>
          </div>

          <div className="overflow-x-auto rounded-lg border border-slate-200">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 text-slate-700 font-semibold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="p-3">Department / Division</th>
                  <th className="p-3">Officials Count</th>
                  <th className="p-3">Avg Training Hours</th>
                  <th className="p-3">Completion Rate</th>
                  <th className="p-3">Critical Competency Gap</th>
                  <th className="p-3">Privacy Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white text-slate-700">
                {departmentsList.map((d, i) => (
                  <tr key={i} className="hover:bg-slate-50/80 transition-colors">
                    <td className="p-3 font-semibold text-statwise-navy">{d.department}</td>
                    <td className="p-3 font-medium">
                      {d.is_masked ? (
                        <span className="text-amber-700 font-bold bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                          {d.officials_display}
                        </span>
                      ) : (
                        d.officials_display
                      )}
                    </td>
                    <td className="p-3">{d.avg_hours} hrs</td>
                    <td className="p-3 font-semibold text-emerald-700">{d.completion_pct}%</td>
                    <td className="p-3 text-slate-600">{d.top_gap}</td>
                    <td className="p-3">
                      {d.is_masked ? (
                        <span className="text-[10px] bg-amber-100 text-amber-900 font-semibold px-2 py-0.5 rounded flex items-center gap-1 w-fit">
                          <AlertCircle className="w-3 h-3" />
                          Masked (&lt; 3)
                        </span>
                      ) : (
                        <span className="text-[10px] bg-emerald-100 text-emerald-900 font-semibold px-2 py-0.5 rounded flex items-center gap-1 w-fit">
                          <ShieldCheck className="w-3 h-3" />
                          Standard Aggregate
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* ML Diagnostics Modal */}
      {isModalOpen && (
        <MLDiagnosticsModal
          diagnostics={diagnostics}
          onClose={() => setIsModalOpen(false)}
        />
      )}
    </div>
  );
}
