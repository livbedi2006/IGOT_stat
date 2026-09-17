import React from "react";
import { ShieldCheck, UserCheck, UserCog, ChevronDown } from "lucide-react";

export function Header({ currentRole, onRoleChange, learner, onOpenIdentifyModal }) {
  const displayName = learner?.name || "Statistical Officer";
  const displayDesignation = learner?.designation || (currentRole === "SSO" ? "Senior Statistical Officer" : currentRole === "ISS" ? "Director / ISS Officer" : "Junior Statistical Officer");
  const avatarLetter = displayName ? displayName.charAt(0).toUpperCase() : "O";

  return (
    <header className="bg-statwise-navy text-white border-b border-statwise-navyActive px-6 py-3 flex items-center justify-between sticky top-0 z-30 shadow-sm">
      {/* Brand & Ministry Header */}
      <div className="flex items-center gap-4">
        {/* Emblem Badge */}
        <div className="w-10 h-10 rounded-md bg-statwise-navyActive border border-statwise-blue/40 flex items-center justify-center font-bold text-lg text-white shadow-inner">
          <span className="text-amber-400 text-xs">सत्यमेव</span>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-base font-semibold tracking-wide text-white">STATWISE</h1>
            <span className="text-[10px] bg-statwise-blue/30 text-statwise-pale px-2 py-0.5 rounded border border-statwise-blue/40 font-medium">
              MoSPI • DIID
            </span>
          </div>
          <p className="text-xs text-slate-300 font-normal">
            AI Skill Intelligence Platform • Ministry of Statistics and Programme Implementation
          </p>
        </div>
      </div>

      {/* Right controls: Role switcher & Profile badge */}
      <div className="flex items-center gap-4">
        {/* Role Switcher */}
        <div className="flex items-center bg-statwise-navyActive/80 rounded-lg px-3 py-1.5 border border-slate-700/60 text-xs">
          <span className="text-slate-400 mr-2">Cadre Role:</span>
          <select
            value={currentRole}
            onChange={(e) => onRoleChange(e.target.value)}
            className="bg-transparent text-white font-medium focus:outline-none cursor-pointer pr-1"
          >
            <option value="JSO" className="bg-statwise-navy text-white">Junior Statistical Officer (JSO)</option>
            <option value="SSO" className="bg-statwise-navy text-white">Senior Statistical Officer (SSO)</option>
            <option value="ISS" className="bg-statwise-navy text-white">ISS Officer / Director (Admin)</option>
          </select>
        </div>

        {/* Security / DPDP Act Badge */}
        <div className="hidden md:flex items-center gap-1.5 text-xs text-emerald-300 bg-emerald-950/40 border border-emerald-700/50 px-2.5 py-1 rounded-md">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>DPDP 2023 Compliant</span>
        </div>

        {/* User profile pill with Switch Profile Trigger */}
        <button
          onClick={onOpenIdentifyModal}
          title="Click to change Officer Name or Cadre Role"
          className="flex items-center gap-3 pl-2 border-l border-slate-700/60 hover:bg-white/5 py-1 px-2 rounded-lg transition-all text-left group"
        >
          <div className="text-right hidden sm:block">
            <div className="text-xs font-semibold text-white leading-tight group-hover:text-statwise-pale transition-colors flex items-center gap-1 justify-end">
              <span>{displayName}</span>
              <UserCog className="w-3 h-3 text-slate-400 group-hover:text-amber-400" />
            </div>
            <div className="text-[11px] text-statwise-pale leading-tight">{displayDesignation}</div>
          </div>
          <div className="w-8 h-8 rounded-full bg-statwise-blue text-white font-semibold text-xs flex items-center justify-center border border-white/20 shadow-sm group-hover:ring-2 group-hover:ring-amber-400/50 transition-all">
            {avatarLetter}
          </div>
        </button>
      </div>
    </header>
  );
}
export default Header;
