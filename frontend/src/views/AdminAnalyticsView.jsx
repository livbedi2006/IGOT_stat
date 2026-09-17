import React, { useState, useEffect } from "react";
import { Users, TrendingUp, CheckCircle2, Award, Download, Cpu, ShieldCheck, Building2, BarChart2 } from "lucide-react";
import { MLDiagnosticsModal } from "../components/MLDiagnosticsModal";
import { api } from "../api";

export function AdminAnalyticsView() {
  const [orgData, setOrgData] = useState(null);
  const [diagnostics, setDiagnostics] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);

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
    total_officials: 8115,
    avg_mastery_pct: 64,
    gaps_closed_pct: 38,
    completion_rate_pct: 72
  };

  const competencyDist = orgData?.competency_distribution || [
    { domain: "Statistical", average_mastery: 68 },
    { domain: "Technical", average_mastery: 54 },
    { domain: "Digital Governance", average_mastery: 62 },
    { domain: "Behavioural", average_mastery: 72 }
  ];

  const heatmaps = orgData?.department_heatmaps || [
    { dept: "Data Informatics & Innovation (DIID)", officials: 420, mastery: 71, critical_gap: "AI / ML & SDMX", risk: "Low" },
    { dept: "Field Operations Division (FOD)", officials: 3850, mastery: 61, critical_gap: "CAPI Auditing & Sampling Error", risk: "Medium" },
    { dept: "National Accounts Division (NAD)", officials: 680, mastery: 76, critical_gap: "Supply-Use Table Balancing", risk: "Low" },
    { dept: "Price Statistics Division (PSD)", officials: 540, mastery: 67, critical_gap: "Geometric Item Imputation", risk: "Low" }
  ];

  const handleExportCSV = () => {
    const csvContent = "data:text/csv;charset=utf-8," +
      "Department,Total Officials,Average Mastery,Critical Gap,Risk Level\n" +
      heatmaps.map(h => `"${h.dept}",${h.officials},${h.mastery}%,"${h.critical_gap}",${h.risk}`).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "MoSPI_Competency_Heatmap_Report.csv");
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="space-y-6">
      {/* Header matching Screenbook */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
            Admin Analytics
          </h2>
          <p className="text-sm text-statwise-muted mt-0.5">
            Organization-wide capacity-building intelligence
          </p>
        </div>

        <div className="flex items-center gap-2">
          {/* Button to inspect ML Overfitting Validation */}
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-3.5 py-2 bg-white border border-statwise-blue text-statwise-navy hover:bg-statwise-blue/10 text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5"
          >
            <Cpu className="w-4 h-4 text-statwise-blue" />
            <span>Inspect ML Model Diagnostics</span>
          </button>

          <button
            onClick={handleExportCSV}
            className="px-4 py-2 bg-statwise-navy hover:bg-statwise-navyActive text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Main Container */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm space-y-6">
        <div>
          <h3 className="text-lg font-bold text-statwise-navy">
            Administrator dashboard
          </h3>
          <p className="text-xs text-statwise-muted mt-0.5">
            Monitor competency distribution, training effectiveness and emerging needs.
          </p>
        </div>

        {/* 4 KPI Cards matching Screenbook */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 bg-statwise-canvas rounded-xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Officials</span>
            <div className="text-3xl font-bold text-statwise-navy mt-2">
              {kpis.total_officials.toLocaleString()}
            </div>
            <p className="text-xs text-statwise-muted mt-1 font-medium">Active profiles across India</p>
          </div>

          <div className="p-4 bg-statwise-canvas rounded-xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg mastery</span>
            <div className="text-3xl font-bold text-statwise-navy mt-2">
              {kpis.avg_mastery_pct}%
            </div>
            <p className="text-xs text-statwise-muted mt-1 font-medium">Across all 4 domains</p>
          </div>

          <div className="p-4 bg-statwise-canvas rounded-xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Gaps closed</span>
            <div className="text-3xl font-bold text-statwise-navy mt-2">
              {kpis.gaps_closed_pct}%
            </div>
            <p className="text-xs text-emerald-600 mt-1 font-medium">This quarter (+12% YoY)</p>
          </div>

          <div className="p-4 bg-statwise-canvas rounded-xl border border-slate-200">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Completion</span>
            <div className="text-3xl font-bold text-statwise-navy mt-2">
              {kpis.completion_rate_pct}%
            </div>
            <p className="text-xs text-statwise-muted mt-1 font-medium">Assigned TPAC learning</p>
          </div>
        </div>

        {/* Mid Row: Competency Distribution vs Emerging Skill Demand */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
          {/* Left: Competency distribution */}
          <div className="lg:col-span-6 p-5 bg-statwise-canvas rounded-xl border border-slate-200 flex flex-col justify-between">
            <div>
              <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider mb-4">
                Competency distribution
              </h4>

              <div className="space-y-3.5">
                {competencyDist.map((item, idx) => (
                  <div key={idx}>
                    <div className="flex justify-between text-xs font-medium text-slate-700 mb-1">
                      <span>{item.domain}</span>
                      <span className="font-bold text-statwise-navy">{item.average_mastery}%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-statwise-blue h-2 rounded-full"
                        style={{ width: `${item.average_mastery}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-4 mt-4 border-t border-slate-200/80 text-[11px] text-slate-500">
              Aggregated across 8,000+ statistical cadres (JSO, SSO, ISS).
            </div>
          </div>

          {/* Right: Emerging skill demand (Predictive ML Forecast) */}
          <div className="lg:col-span-6 p-5 bg-statwise-canvas rounded-xl border border-slate-200 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider">
                  Emerging skill demand (Forecast)
                </h4>
                <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">
                  Regularized ML
                </span>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">AI / ML for Official Stats</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+42%</span>
                </div>
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">Python for Microdata Wrangling</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+31%</span>
                </div>
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">Data Privacy & DPDP Act 2023</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+24%</span>
                </div>
                <div className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200">
                  <span className="text-xs font-semibold text-statwise-navy">GIS & Spatial Sampling</span>
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">+20%</span>
                </div>
              </div>
            </div>

            <div className="pt-4 mt-4 border-t border-slate-200/80 text-[11px] text-slate-500">
              Forecast based on roles, upcoming census projects and gap trends.
            </div>
          </div>
        </div>

        {/* Department Heatmap Table */}
        <div className="pt-2">
          <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider mb-3">
            Department Competency Heatmap
          </h4>

          <div className="overflow-x-auto rounded-lg border border-slate-200">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 text-slate-700 font-semibold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="p-3">Department / Division</th>
                  <th className="p-3">Officials</th>
                  <th className="p-3">Avg Mastery</th>
                  <th className="p-3">Critical Competency Gap</th>
                  <th className="p-3">Risk Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white text-slate-700">
                {heatmaps.map((h, i) => (
                  <tr key={i} className="hover:bg-slate-50/80 transition-colors">
                    <td className="p-3 font-semibold text-statwise-navy">{h.dept}</td>
                    <td className="p-3">{h.officials}</td>
                    <td className="p-3">
                      <div className="flex items-center gap-2">
                        <span className="font-bold">{h.mastery}%</span>
                        <div className="w-16 bg-slate-200 rounded-full h-1.5 overflow-hidden">
                          <div className="bg-statwise-blue h-1.5 rounded-full" style={{ width: `${h.mastery}%` }}></div>
                        </div>
                      </div>
                    </td>
                    <td className="p-3 text-slate-600">{h.critical_gap}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${h.risk === "Low" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"}`}>
                        {h.risk} Risk
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="pt-2 text-xs text-slate-400">
          Administrators see aggregated competency, completion and emerging-skill indicators without exposing unnecessary personal data.
        </div>
      </div>

      {/* ML Diagnostics Modal */}
      <MLDiagnosticsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        diagnostics={diagnostics}
      />
    </div>
  );
}
