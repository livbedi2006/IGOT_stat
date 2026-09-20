import React, { useState } from "react";
import { UserCheck, ShieldCheck, Building2, Briefcase, Award, ArrowRight, X } from "lucide-react";

export function UserIdentificationModal({ isOpen, onClose, onIdentify, initialProfile, canDismiss = false }) {
  const [name, setName] = useState(
    initialProfile?.name || localStorage.getItem("statwise_saved_name") || ""
  );
  const [role, setRole] = useState(
    initialProfile?.role_code || localStorage.getItem("statwise_saved_role") || "JSO"
  );
  const [department, setDepartment] = useState(
    initialProfile?.department || localStorage.getItem("statwise_saved_dept") || "Data Informatics & Innovation Division (DIID)"
  );
  const [assignment, setAssignment] = useState(
    initialProfile?.current_assignment || localStorage.getItem("statwise_saved_assignment") || "Official Statistical Analysis & Data Scrutiny"
  );
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  React.useEffect(() => {
    if (isOpen) {
      if (initialProfile?.name || localStorage.getItem("statwise_saved_name")) {
        setName(initialProfile?.name || localStorage.getItem("statwise_saved_name") || "");
      }
      if (initialProfile?.role_code || localStorage.getItem("statwise_saved_role")) {
        setRole(initialProfile?.role_code || localStorage.getItem("statwise_saved_role") || "JSO");
      }
      if (initialProfile?.department || localStorage.getItem("statwise_saved_dept")) {
        setDepartment(initialProfile?.department || localStorage.getItem("statwise_saved_dept") || "Data Informatics & Innovation Division (DIID)");
      }
      if (initialProfile?.current_assignment || localStorage.getItem("statwise_saved_assignment")) {
        setAssignment(initialProfile?.current_assignment || localStorage.getItem("statwise_saved_assignment") || "Official Statistical Analysis & Data Scrutiny");
      }
    }
  }, [isOpen, initialProfile]);

  if (!isOpen) return null;

  const cadreOptions = [
    {
      code: "JSO",
      title: "Junior Statistical Officer (JSO)",
      cadre: "Subordinate Statistical Service (SSS)",
      desc: "Focus on primary data collection, sampling, tabulation, and preliminary validation."
    },
    {
      code: "SSO",
      title: "Senior Statistical Officer (SSO)",
      cadre: "Subordinate Statistical Service (SSS)",
      desc: "Focus on supervisory inspections, quality frameworks, and intermediate econometrics."
    },
    {
      code: "ISS",
      title: "Director / ISS Officer (Admin)",
      cadre: "Indian Statistical Service (ISS)",
      desc: "Focus on policy formulation, national accounts, macro indicators, and organizational leadership."
    }
  ];

  const departments = [
    "Data Informatics & Innovation Division (DIID)",
    "National Accounts Division (NAD)",
    "Price Statistics Division (PSD)",
    "Survey Design & Research Division (SDRD)",
    "Field Operations Division (FOD)",
    "Economic Statistics Division (ESD)",
    "Coordination & Publication Division (CPD)",
    "National Statistical Systems Training Academy (NSSTA)"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Please enter your name to personalize your statistical learning dashboard.");
      return;
    }
    setError("");
    setSubmitting(true);
    try {
      await onIdentify({
        name: name.trim(),
        role_code: role,
        department,
        current_assignment: assignment
      });
    } catch (err) {
      console.error("Failed to set identification:", err);
      setError("Failed to save profile. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-xl w-full overflow-hidden transition-all transform scale-100">
        {/* Government Authority Banner */}
        <div className="bg-statwise-navy text-white px-6 py-5 border-b border-statwise-navyActive flex items-start justify-between">
          <div className="flex items-center gap-3.5">
            <div className="w-11 h-11 rounded-lg bg-statwise-navyActive border border-amber-400/40 flex items-center justify-center font-bold text-amber-400 shadow-inner">
              <span className="text-xs tracking-tight">सत्यमेव</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold tracking-wide">STATWISE Identification</h2>
                <span className="text-[10px] bg-statwise-blue/40 text-statwise-pale px-2 py-0.5 rounded border border-statwise-blue/50 font-semibold">
                  MoSPI Cadre
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-0.5">
                Ministry of Statistics & Programme Implementation • DIID
              </p>
            </div>
          </div>
          {canDismiss && (
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
              title="Close"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Informative Guidance */}
        <div className="bg-statwise-canvas px-6 py-3 border-b border-slate-200 flex items-center gap-2.5 text-xs text-statwise-navy">
          <ShieldCheck className="w-4 h-4 text-emerald-600 flex-shrink-0" />
          <span>
            Please provide your <strong>Name</strong> and <strong>Cadre Role</strong> to tailor your personalized competency radar, learning pathway, and assessments.
          </span>
        </div>

        {/* Identification Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg font-medium">
              {error}
            </div>
          )}

          {/* Officer Name Field */}
          <div>
            <label className="block text-xs font-bold text-statwise-navy uppercase tracking-wider mb-1.5">
              Officer Full Name <span className="text-rose-500">*</span>
            </label>
            <div className="relative">
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name (e.g. Statistical Officer, Rajesh Kumar)"
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-lg text-sm text-statwise-navy placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-statwise-blue focus:bg-white font-medium"
              />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Your name will appear across your MoSPI competency records and assessment certificates.
            </p>
          </div>

          {/* Cadre Designation Selection */}
          <div>
            <label className="block text-xs font-bold text-statwise-navy uppercase tracking-wider mb-2">
              Select Official Cadre / Role <span className="text-rose-500">*</span>
            </label>
            <div className="grid grid-cols-1 gap-2.5">
              {cadreOptions.map((opt) => (
                <div
                  key={opt.code}
                  onClick={() => setRole(opt.code)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all flex items-start gap-3 ${
                    role === opt.code
                      ? "bg-statwise-pale/30 border-statwise-blue ring-1 ring-statwise-blue"
                      : "bg-slate-50/70 border-slate-200 hover:border-slate-300 hover:bg-slate-50"
                  }`}
                >
                  <input
                    type="radio"
                    name="cadre_role"
                    checked={role === opt.code}
                    onChange={() => setRole(opt.code)}
                    className="mt-1 text-statwise-blue focus:ring-statwise-blue cursor-pointer"
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-statwise-navy">{opt.title}</span>
                      <span className="text-[10px] bg-white border border-slate-200 text-statwise-blue px-2 py-0.5 rounded font-medium">
                        {opt.cadre}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-600 mt-0.5 leading-snug">
                      {opt.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Department / Division */}
          <div>
            <label className="block text-xs font-bold text-statwise-navy uppercase tracking-wider mb-1.5">
              MoSPI Division / Directorate
            </label>
            <div className="relative">
              <select
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-lg text-xs font-medium text-statwise-navy focus:outline-none focus:ring-2 focus:ring-statwise-blue focus:bg-white cursor-pointer"
              >
                {departments.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Current Assignment */}
          <div>
            <label className="block text-xs font-bold text-statwise-navy uppercase tracking-wider mb-1.5">
              Current Assignment / Focus Area
            </label>
            <input
              type="text"
              value={assignment}
              onChange={(e) => setAssignment(e.target.value)}
              placeholder="e.g. Household Consumer Expenditure Survey Scrutiny"
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-lg text-xs font-medium text-statwise-navy placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-statwise-blue focus:bg-white"
            />
          </div>

          {/* Action Buttons */}
          <div className="pt-2 flex items-center justify-end gap-3 border-t border-slate-100">
            {canDismiss && (
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-medium text-slate-600 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
              >
                Cancel
              </button>
            )}
            <button
              type="submit"
              disabled={submitting || !name.trim()}
              className="px-5 py-2.5 bg-statwise-blue hover:bg-statwise-navyActive text-white text-xs font-bold rounded-lg shadow-sm hover:shadow transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span>{submitting ? "Configuring Dashboard..." : "Enter STATWISE Dashboard"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
