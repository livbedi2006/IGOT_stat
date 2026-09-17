import React, { useState } from "react";
import { User, Shield, CheckCircle2, Lock, Languages, Bell, Eye } from "lucide-react";

export function ProfileSettingsView({ learner, currentRole, onRoleChange }) {
  const [toggles, setToggles] = useState({
    rbac: true,
    historySync: true,
    notifications: true,
    citationsRequired: true,
    dpdpConsent: true
  });

  const handleToggle = (key) => {
    setToggles((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          Profile & Settings
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Role, preferences and secure account controls under official MoSPI IT policy.
        </p>
      </div>

      {/* Main Container */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm space-y-6">
        <div>
          <h3 className="text-lg font-bold text-statwise-navy">
            Your profile
          </h3>
          <p className="text-xs text-statwise-muted mt-0.5">
            Profile data improves competency mapping and personalized recommendations.
          </p>
        </div>

        {/* Two-Column Grid matching Screenbook */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          {/* Left Column: Professional Information */}
          <div className="md:col-span-6 p-5 bg-statwise-canvas rounded-xl border border-slate-200 space-y-4">
            <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider">
              Professional information
            </h4>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400 block text-[11px]">Name</span>
                <span className="font-bold text-statwise-navy text-sm">
                  {learner?.name || "Livjot Singh Bedi"}
                </span>
              </div>

              <div>
                <span className="text-slate-400 block text-[11px]">Designation</span>
                <span className="font-medium text-slate-800">
                  {learner?.designation || "Junior Statistical Officer"}
                </span>
              </div>

              <div>
                <span className="text-slate-400 block text-[11px]">Department / Division</span>
                <span className="font-medium text-slate-800">
                  {learner?.department || "Data Informatics & Innovation Division (DIID)"}
                </span>
              </div>

              <div>
                <span className="text-slate-400 block text-[11px]">Experience</span>
                <span className="font-medium text-slate-800">
                  {learner?.experience || "3 years"}
                </span>
              </div>

              <div>
                <span className="text-slate-400 block text-[11px]">Preferred language</span>
                <span className="font-medium text-slate-800">
                  {learner?.preferred_language || "English / Hindi"}
                </span>
              </div>

              <div className="pt-2">
                <label className="text-slate-400 block text-[11px] mb-1">Cadre Role Switcher</label>
                <select
                  value={currentRole}
                  onChange={(e) => onRoleChange(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-medium text-slate-800 focus:outline-none"
                >
                  <option value="JSO">Junior Statistical Officer (JSO)</option>
                  <option value="SSO">Senior Statistical Officer (SSO)</option>
                  <option value="ISS">ISS Officer (Director / Admin)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Right Column: Privacy & Access Toggles */}
          <div className="md:col-span-6 p-5 bg-statwise-canvas rounded-xl border border-slate-200 space-y-4">
            <h4 className="text-xs font-bold text-statwise-navy uppercase tracking-wider">
              Privacy & access
            </h4>

            <div className="space-y-3.5 text-xs">
              <div
                onClick={() => handleToggle("rbac")}
                className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 cursor-pointer hover:border-slate-300 transition-colors"
              >
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 className={`w-4 h-4 ${toggles.rbac ? "text-emerald-600" : "text-slate-300"}`} />
                  <span className="font-medium text-slate-800">Role-based access enabled</span>
                </div>
                <span className="text-[10px] text-slate-400">Strict RBAC</span>
              </div>

              <div
                onClick={() => handleToggle("historySync")}
                className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 cursor-pointer hover:border-slate-300 transition-colors"
              >
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 className={`w-4 h-4 ${toggles.historySync ? "text-emerald-600" : "text-slate-300"}`} />
                  <span className="font-medium text-slate-800">Learning history synced</span>
                </div>
                <span className="text-[10px] text-slate-400">iGOT API</span>
              </div>

              <div
                onClick={() => handleToggle("notifications")}
                className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 cursor-pointer hover:border-slate-300 transition-colors"
              >
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 className={`w-4 h-4 ${toggles.notifications ? "text-emerald-600" : "text-slate-300"}`} />
                  <span className="font-medium text-slate-800">Notifications enabled</span>
                </div>
                <span className="text-[10px] text-slate-400">TPAC Alerts</span>
              </div>

              <div
                onClick={() => handleToggle("citationsRequired")}
                className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 cursor-pointer hover:border-slate-300 transition-colors"
              >
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 className={`w-4 h-4 ${toggles.citationsRequired ? "text-emerald-600" : "text-slate-300"}`} />
                  <span className="font-medium text-slate-800">AI source citations required</span>
                </div>
                <span className="text-[10px] text-slate-400">Enforced</span>
              </div>

              <div
                onClick={() => handleToggle("dpdpConsent")}
                className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 cursor-pointer hover:border-slate-300 transition-colors"
              >
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 className={`w-4 h-4 ${toggles.dpdpConsent ? "text-emerald-600" : "text-slate-300"}`} />
                  <span className="font-medium text-slate-800">DPDP Act 2023 Consent Active</span>
                </div>
                <span className="text-[10px] text-emerald-700 font-semibold bg-emerald-50 px-1.5 py-0.5 rounded">Statutory</span>
              </div>
            </div>
          </div>
        </div>

        <div className="pt-2 text-xs text-slate-400">
          The profile page gives users control over role information, language preferences and privacy-related settings.
        </div>
      </div>
    </div>
  );
}
