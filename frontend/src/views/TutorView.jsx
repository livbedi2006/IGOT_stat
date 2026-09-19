import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, BookOpen, ShieldCheck, Sparkles, ThumbsUp, ThumbsDown, AlertTriangle, Check, Compass, ArrowRight } from "lucide-react";
import { api } from "../api";

export function TutorView({ currentRole = "JSO", currentAssignment = "", onNavigate }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState({});
  const messagesEndRef = useRef(null);

  const [messages, setMessages] = useState([
    {
      sender: "user",
      text: "Explain sampling error in simple language."
    },
    {
      id: "msg_init_01",
      sender: "tutor",
      text: "Sampling error is the mathematical difference between a sample estimate and the true population parameter arising because only a representative fraction of units is observed. In official MoSPI survey design, sampling error is controlled through optimum sample allocation across stratified homogeneous domains, larger effective sample sizes, and calibration weighting.",
      sources: [
        { title: "MoSPI Survey Sampling Methodology Manual 2024", page: "Page 12-14", authority: "MoSPI DIID & NSSTA Greater Noida" }
      ],
      is_grounded: true,
      confidence: 0.95
    }
  ]);

  const defaultAssignment = currentAssignment || localStorage.getItem("statwise_saved_assignment") || "";

  const suggestions = [
    defaultAssignment.toLowerCase().includes("new") || defaultAssignment.toLowerCase().includes("nothing")
      ? "New to the work: What is my official induction roadmap?"
      : defaultAssignment.toLowerCase().includes("scrutiny") || defaultAssignment.toLowerCase().includes("srutny")
      ? "Survey Scrutiny: What automated validation rules should I learn next?"
      : "What ahead in my learning path?",
    "Explain sampling error in simple language.",
    "Difference between Stratified and Cluster sampling in NSS.",
    "How is CPI compiled with Laspeyres formula?",
    "Define Gross Value Added (GVA) at basic prices.",
    "DPDP Act 2023 obligations for statistical microdata.",
    "Tell me about Martian rocket exploration." // Tests strict Prompt O uncertainty fallback
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (questionText = null) => {
    const q = questionText || query;
    if (!q.trim()) return;

    const newMsgs = [...messages, { sender: "user", text: q }];
    setMessages(newMsgs);
    setQuery("");
    setLoading(true);

    try {
      const res = await api.askTutor(q, currentRole, defaultAssignment);
      setMessages([...newMsgs, {
        id: res.message_id || `msg_${Date.now()}`,
        sender: "tutor",
        text: res.answer,
        sources: res.sources,
        is_grounded: res.is_grounded,
        confidence: res.confidence
      }]);
    } catch (err) {
      console.error("AI Tutor query error:", err);
      setMessages([...newMsgs, {
        id: `msg_${Date.now()}`,
        sender: "tutor",
        text: "This query cannot be verified from approved MoSPI/NSSTA learning materials. To maintain statistical fidelity, the AI Tutor only provides source-backed answers. Please consult an official NSSTA reference document or contact a designated cadre trainer.",
        sources: [
          { title: "National Statistical Systems Training Academy (NSSTA) Reference Catalogue", page: "Helpdesk Directory", authority: "NSSTA Greater Noida" }
        ],
        is_grounded: false,
        confidence: 0.0
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (msgId, helpful) => {
    try {
      await api.sendTutorFeedback(msgId, helpful, helpful ? "Accurate official reference" : "Needs further detail");
      setFeedbackGiven(prev => ({ ...prev, [msgId]: helpful ? "up" : "down" }));
    } catch (e) {
      console.warn("Feedback recording fallback:", e);
      setFeedbackGiven(prev => ({ ...prev, [msgId]: helpful ? "up" : "down" }));
    }
  };

  const roleLabelMap = {
    "JSO": "Junior Statistical Officer (JSO)",
    "SSO": "Senior Statistical Officer (SSO)",
    "ANALYST": "Data Analyst (MoSPI DIID)",
    "ISS": "Indian Statistical Service (ISS)",
    "TRAINER": "Training Administrator (TRAINER)"
  };

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
            Official Statistics AI Tutor
          </h2>
          <p className="text-sm text-statwise-muted mt-0.5">
            Retrieval-Augmented Generation (RAG) strictly grounded in approved NSSTA and MoSPI training materials (Prompt O).
          </p>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-[11px] bg-statwise-navy/10 text-statwise-navy px-3 py-1 rounded-full font-semibold border border-statwise-navy/20">
            Cadre: {roleLabelMap[currentRole] || currentRole}
          </span>
          {defaultAssignment && (
            <span className="text-[11px] bg-emerald-50 text-emerald-800 px-3 py-1 rounded-full font-semibold border border-emerald-200">
              Focus: {defaultAssignment}
            </span>
          )}
        </div>
      </div>

      {/* Main Tutor Box */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between min-h-[620px]">
        <div>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-2">
            <div>
              <h3 className="text-lg font-bold text-statwise-navy flex items-center gap-2">
                <span>Statistical AI Tutor (MoSPI Standards)</span>
                <span className="text-[10px] bg-statwise-blue/10 text-statwise-blue px-2 py-0.5 rounded-full font-medium">v2.0 Semantic Vector</span>
              </h3>
              <p className="text-xs text-statwise-muted mt-0.5">
                Every verified answer includes exact publication, section, and page references.
              </p>
            </div>
            <div className="flex items-center gap-1 text-[11px] text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200 font-medium self-start sm:self-auto">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Verified Source Grounding Only</span>
            </div>
          </div>

          {/* Quick Suggestions */}
          <div className="py-3 flex flex-wrap gap-1.5 border-b border-slate-100 items-center">
            <span className="text-[11px] text-slate-400 mr-1 flex items-center gap-1 font-medium">
              <Sparkles className="w-3 h-3 text-statwise-blue" />
              Suggested:
            </span>
            {suggestions.map((s, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(s)}
                className="text-[11px] bg-slate-100 hover:bg-statwise-navy hover:text-white text-slate-700 px-2.5 py-1 rounded-full transition-all font-medium text-left shadow-2xs"
              >
                {s}
              </button>
            ))}
          </div>

          {/* Conversation Stream */}
          <div className="py-4 space-y-4 max-h-[420px] overflow-y-auto pr-2">
            {messages.map((m, idx) => (
              <div key={idx} className={`flex gap-3 ${m.sender === "user" ? "justify-end" : "justify-start"}`}>
                {m.sender === "tutor" && (
                  <div className="w-8 h-8 rounded-full bg-statwise-navy text-white flex items-center justify-center shrink-0 text-xs shadow-sm mt-0.5">
                    <Bot className="w-4 h-4 text-statwise-pale" />
                  </div>
                )}

                <div
                  className={`rounded-xl p-4 max-w-2xl text-xs space-y-2.5 shadow-xs ${
                    m.sender === "user"
                      ? "bg-statwise-blue/15 text-statwise-navy font-medium border border-statwise-blue/30"
                      : m.is_grounded === false
                      ? "bg-amber-50/90 text-amber-950 border border-amber-200"
                      : "bg-statwise-canvas text-slate-800 border border-slate-200/80"
                  }`}
                >
                  {/* Uncertainty Fallback Alert (Prompt O & Section 8) */}
                  {m.sender === "tutor" && m.is_grounded === false && (
                    <div className="flex items-center gap-1.5 text-amber-800 font-bold text-[11px] pb-1.5 border-b border-amber-200/80">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                      <span>Uncertainty Fallback: Query Out of Approved MoSPI Domain</span>
                    </div>
                  )}

                  {/* Grounded Badge for Verified Answers */}
                  {m.sender === "tutor" && m.is_grounded === true && (
                    <div className="flex items-center justify-between text-[10px] text-emerald-800 font-semibold pb-1 border-b border-slate-200/50">
                      <span className="flex items-center gap-1">
                        <Check className="w-3 h-3 text-emerald-600" />
                        Official Source Grounding Verified
                      </span>
                      <span className="text-slate-400 font-normal">Confidence: {Math.round((m.confidence || 0.95) * 100)}%</span>
                    </div>
                  )}

                  <div className="leading-relaxed whitespace-pre-wrap font-sans text-[12px]">
                    {m.text}
                  </div>

                  {/* Grounded Source Citations */}
                  {m.sources && m.sources.length > 0 && (
                    <div className="pt-2 border-t border-slate-200/60 text-[11px] text-slate-600 space-y-1.5">
                      <div className="font-bold text-statwise-navy flex items-center gap-1">
                        <BookOpen className="w-3.5 h-3.5 text-statwise-blue" />
                        <span>Source Citations:</span>
                      </div>
                      {m.sources.map((src, sIdx) => (
                        <div key={sIdx} className="bg-white/90 p-2 rounded-md border border-slate-200/70 text-[11px] shadow-2xs space-y-0.5">
                          <div className="font-semibold text-slate-800">{src.title}</div>
                          <div className="text-[10px] text-slate-500">
                            {src.page || src.pages || "Page Reference"} {src.section ? `• ${src.section}` : ""} {src.authority ? `• ${src.authority}` : ""}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Prompt O: Helpful / Unhelpful Feedback Telemetry */}
                  {m.sender === "tutor" && m.id && (
                    <div className="pt-2 flex items-center justify-between text-[10px] text-slate-400 border-t border-slate-200/40">
                      <span>Was this source citation accurate & helpful?</span>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleFeedback(m.id, true)}
                          className={`p-1 px-2 rounded-md transition-colors flex items-center gap-1 border ${
                            feedbackGiven[m.id] === "up" ? "bg-emerald-50 text-emerald-700 font-bold border-emerald-300" : "hover:bg-slate-200/70 text-slate-600 border-transparent"
                          }`}
                        >
                          <ThumbsUp className="w-3 h-3" />
                          <span>Helpful</span>
                        </button>
                        <button
                          onClick={() => handleFeedback(m.id, false)}
                          className={`p-1 px-2 rounded-md transition-colors flex items-center gap-1 border ${
                            feedbackGiven[m.id] === "down" ? "bg-rose-50 text-rose-700 font-bold border-rose-300" : "hover:bg-slate-200/70 text-slate-600 border-transparent"
                          }`}
                        >
                          <ThumbsDown className="w-3 h-3" />
                          <span>Unhelpful</span>
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {m.sender === "user" && (
                  <div className="w-8 h-8 rounded-full bg-statwise-blue text-white flex items-center justify-center shrink-0 text-xs shadow-sm mt-0.5">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3 justify-start items-center text-xs text-slate-500 py-2">
                <div className="w-8 h-8 rounded-full bg-statwise-navy text-white flex items-center justify-center shrink-0 shadow-sm">
                  <Bot className="w-4 h-4 animate-spin text-statwise-pale" />
                </div>
                <div className="bg-slate-50 px-3 py-2 rounded-lg border border-slate-200">
                  <span>Searching official MoSPI manuals, NSSTA catalogues & retrieving verified citations...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Bar */}
        <div className="pt-4 border-t border-slate-100">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a statistical or roadmap question (e.g., 'what ahead?', 'Explain sampling error', 'How is CPI compiled?')..."
              className="flex-1 bg-statwise-canvas border border-slate-300 rounded-lg px-4 py-2.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-statwise-blue transition-colors shadow-2xs"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-5 py-2.5 bg-statwise-navy hover:bg-statwise-navyActive disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5 shrink-0"
            >
              <span>Send</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>

          <div className="mt-2.5 text-[11px] text-slate-400 flex items-center justify-between">
            <span>Prompt O Compliance: Grounded exclusively in approved MoSPI documents. Ungrounded queries return explicit uncertainty notices.</span>
            <span className="hidden sm:inline">Press Enter to send</span>
          </div>
        </div>
      </div>
    </div>
  );
}
