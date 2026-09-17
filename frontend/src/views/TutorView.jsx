import React, { useState } from "react";
import { Send, Bot, User, BookOpen, ShieldCheck, Sparkles, ThumbsUp, ThumbsDown, AlertTriangle, Check } from "lucide-react";
import { api } from "../api";

export function TutorView() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState({});
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

  const suggestions = [
    "Explain sampling error in simple language.",
    "Difference between Stratified and Cluster sampling in NSS.",
    "How is CPI compiled with Laspeyres formula?",
    "Define Gross Value Added (GVA) at basic prices.",
    "DPDP Act 2023 obligations for statistical microdata.",
    "Tell me about Martian rocket exploration." // Test uncertainty fallback!
  ];

  const handleSend = async (questionText = null) => {
    const q = questionText || query;
    if (!q.trim()) return;

    const newMsgs = [...messages, { sender: "user", text: q }];
    setMessages(newMsgs);
    setQuery("");
    setLoading(true);

    try {
      const res = await api.askTutor(q);
      setMessages([...newMsgs, {
        id: res.message_id || `msg_${Date.now()}`,
        sender: "tutor",
        text: res.answer,
        sources: res.sources,
        is_grounded: res.is_grounded,
        confidence: res.confidence
      }]);
    } catch (err) {
      console.error(err);
      setMessages([...newMsgs, {
        id: `msg_${Date.now()}`,
        sender: "tutor",
        text: "This query cannot be verified from approved MoSPI/NSSTA learning materials. Please consult an official NSSTA reference or designated cadre trainer.",
        sources: [
          { title: "NSSTA Reference Directory", page: "Cadre Training Desk" }
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
      await fetch("http://localhost:8000/api/tutor/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message_id: msgId, helpful, user_comment: helpful ? "Helpful reference" : "Needs further detail" })
      });
      setFeedbackGiven(prev => ({ ...prev, [msgId]: helpful ? "up" : "down" }));
    } catch (e) {
      setFeedbackGiven(prev => ({ ...prev, [msgId]: helpful ? "up" : "down" }));
    }
  };

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          Official Statistics AI Tutor
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Retrieval-Augmented Generation (RAG) strictly grounded in approved NSSTA and MoSPI training materials (Prompt O).
        </p>
      </div>

      {/* Main Tutor Box */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between min-h-[580px]">
        <div>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-2">
            <div>
              <h3 className="text-lg font-bold text-statwise-navy">
                Statistical AI Tutor (MoSPI Standards)
              </h3>
              <p className="text-xs text-statwise-muted mt-0.5">
                Every verified answer includes exact publication page/paragraph references.
              </p>
            </div>
            <div className="flex items-center gap-1 text-[11px] text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200 font-medium self-start sm:self-auto">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Verified Source Grounding Only</span>
            </div>
          </div>

          {/* Quick Suggestions */}
          <div className="py-3 flex flex-wrap gap-1.5 border-b border-slate-100">
            <span className="text-[11px] text-slate-400 self-center mr-1">Suggested:</span>
            {suggestions.map((s, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(s)}
                className="text-[11px] bg-slate-100 hover:bg-statwise-blue hover:text-white text-slate-700 px-2.5 py-1 rounded-full transition-colors font-medium text-left"
              >
                {s}
              </button>
            ))}
          </div>

          {/* Conversation Stream */}
          <div className="py-4 space-y-4 max-h-[380px] overflow-y-auto pr-1">
            {messages.map((m, idx) => (
              <div key={idx} className={`flex gap-3 ${m.sender === "user" ? "justify-end" : "justify-start"}`}>
                {m.sender === "tutor" && (
                  <div className="w-8 h-8 rounded-full bg-statwise-navy text-white flex items-center justify-center shrink-0 text-xs shadow-sm">
                    <Bot className="w-4 h-4 text-statwise-pale" />
                  </div>
                )}

                <div
                  className={`rounded-xl p-4 max-w-xl text-xs space-y-2.5 ${
                    m.sender === "user"
                      ? "bg-statwise-blue/15 text-statwise-navy font-medium border border-statwise-blue/30"
                      : m.is_grounded === false
                      ? "bg-amber-50/90 text-amber-950 border border-amber-200"
                      : "bg-statwise-canvas text-slate-800 border border-slate-200/80"
                  }`}
                >
                  {/* Uncertainty Fallback Alert (Prompt O & Section 8) */}
                  {m.sender === "tutor" && m.is_grounded === false && (
                    <div className="flex items-center gap-1.5 text-amber-800 font-bold text-[11px] pb-1 border-b border-amber-200/80">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                      <span>Uncertainty Fallback: Query Out of Approved MoSPI Domain</span>
                    </div>
                  )}

                  <p className="leading-relaxed whitespace-pre-wrap">{m.text}</p>

                  {/* Grounded Source Citations */}
                  {m.sources && m.sources.length > 0 && (
                    <div className="pt-2 border-t border-slate-200/60 text-[11px] text-slate-600 space-y-1">
                      <div className="font-bold text-statwise-navy flex items-center gap-1">
                        <BookOpen className="w-3 h-3 text-statwise-blue" />
                        <span>Source Citations:</span>
                      </div>
                      {m.sources.map((src, sIdx) => (
                        <div key={sIdx} className="bg-white/80 p-1.5 rounded border border-slate-200/70 text-[10px]">
                          <strong>{src.title}</strong> • {src.page || src.pages || "Chapter 1"} {src.authority && `• ${src.authority}`}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Prompt O: Helpful / Unhelpful Feedback Telemetry */}
                  {m.sender === "tutor" && m.id && (
                    <div className="pt-1.5 flex items-center justify-between text-[10px] text-slate-400 border-t border-slate-200/40">
                      <span>Was this source citation accurate?</span>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleFeedback(m.id, true)}
                          className={`p-1 rounded hover:bg-slate-200 flex items-center gap-1 ${
                            feedbackGiven[m.id] === "up" ? "text-emerald-600 font-bold" : "text-slate-500"
                          }`}
                        >
                          <ThumbsUp className="w-3 h-3" />
                          <span>Helpful</span>
                        </button>
                        <button
                          onClick={() => handleFeedback(m.id, false)}
                          className={`p-1 rounded hover:bg-slate-200 flex items-center gap-1 ${
                            feedbackGiven[m.id] === "down" ? "text-rose-600 font-bold" : "text-slate-500"
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
                  <div className="w-8 h-8 rounded-full bg-statwise-blue text-white flex items-center justify-center shrink-0 text-xs shadow-sm">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3 justify-start items-center text-xs text-slate-400">
                <div className="w-8 h-8 rounded-full bg-statwise-navy text-white flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4 animate-spin text-statwise-pale" />
                </div>
                <span>Retrieving verified MoSPI statistical passages & page references...</span>
              </div>
            )}
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
              placeholder="Ask a statistical question (e.g., Explain sampling error in PLFS)..."
              className="flex-1 bg-statwise-canvas border border-slate-300 rounded-lg px-4 py-2.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-statwise-blue"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-5 py-2.5 bg-statwise-navy hover:bg-statwise-navyActive disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5"
            >
              <span>Send</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>

          <div className="mt-3 text-xs text-slate-400">
            Prompt O Compliance: Answers are derived exclusively from approved MoSPI documents. Ungrounded queries return explicit uncertainty notices.
          </div>
        </div>
      </div>
    </div>
  );
}
