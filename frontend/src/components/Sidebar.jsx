import React from "react";
import {
  LayoutDashboard,
  Radar,
  Route,
  Sparkles,
  FileCheck2,
  HelpCircle,
  Bot,
  BarChart3,
  UserCog,
  Database
} from "lucide-react";

export function Sidebar({ activeTab, onSelectTab }) {
  const menuItems = [
    { id: "overview", label: "Overview", icon: LayoutDashboard, badge: null },
    { id: "competency", label: "Competency Profile", icon: Radar, badge: null },
    { id: "pathway", label: "Learning Path", icon: Route, badge: "Active" },
    { id: "recommendations", label: "Recommendations", icon: Sparkles, badge: "New" },
    { id: "assessments", label: "Assessments", icon: FileCheck2, badge: null },
    { id: "quiz", label: "Quiz Player", icon: HelpCircle, badge: "Proctored" },
    { id: "tutor", label: "AI Tutor", icon: Bot, badge: "Grounded" },
    { id: "analytics", label: "Admin Analytics", icon: BarChart3, badge: null },
    { id: "virtuallab", label: "Virtual Lab (MCP)", icon: Database, badge: "Live Data" },
    { id: "profile", label: "Profile & Settings", icon: UserCog, badge: null },
  ];

  return (
    <aside className="w-64 bg-statwise-navy text-white flex flex-col justify-between shrink-0 min-h-[calc(100vh-61px)] border-r border-statwise-navyActive">
      <div className="py-4">
        {/* Navigation Items */}
        <nav className="space-y-1 px-3">
          <div className="px-3 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Capacity Building
          </div>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? "bg-statwise-navyActive text-white border-l-4 border-statwise-blue shadow-sm"
                    : "text-slate-300 hover:text-white hover:bg-statwise-navyActive/50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? "text-statwise-blue" : "text-slate-400"}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span
                    className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                      item.badge === "Proctored"
                        ? "bg-amber-900/50 text-amber-300 border border-amber-700/50"
                        : item.badge === "Grounded"
                        ? "bg-sky-900/50 text-sky-200 border border-sky-700/50"
                        : item.badge === "Live Data"
                        ? "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50"
                        : "bg-statwise-blue/30 text-statwise-pale"
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Sidebar Footer */}
      <div className="p-4 border-t border-slate-800/80 text-xs text-slate-400 bg-statwise-navy/80">
        <div className="font-medium text-slate-300">STATWISE Platform</div>
        <p className="text-[11px] text-slate-400 mt-0.5">
          MoSPI • Official Statistics Capacity Building
        </p>
        <div className="mt-2 text-[10px] text-slate-500">
          SIH 2026 • Problem ID: 26101
        </div>
      </div>
    </aside>
  );
}
