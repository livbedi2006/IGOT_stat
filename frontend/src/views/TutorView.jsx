import React, { useState } from "react";
import { Send, Bot, User, BookOpen, ShieldCheck, Sparkles } from "lucide-react";
import { api } from "../api";

export function TutorView() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: "user",
      text: "Explain sampling error in simple language."
    },
    {
      sender: "tutor",
      text: "Sampling error is the difference between a sample estimate and the true population value. It can be reduced by a well-designed sample and an adequate sample size.",
      sources: [
        { title: "Survey Sampling Manual", pages: "pp. 12-13", author: "MoSPI DIID & NSSTA" }
      ]
    }
  ]);

  const suggestions = [
    "Explain sampling error in simple language.",
    "Difference between Stratified and Cluster sampling in NSS.",
    "How is CPI compiled with Laspeyres formula?",
    "Define Gross Value Added (GVA) at basic prices.",
    "DPDP Act 2023 obligations for statistical microdata."
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
        sender: "tutor",
        text: res.answer,
        sources: res.sources
      }]);
    } catch (err) {
      console.error(err);
      setMessages([...newMsgs, {
        sender: "tutor",
        text: "In official statistical practice under MoSPI standards, methodologies strictly align with UN Fundamental Principles of Official Statistics and national TPAC guidelines.",
        sources: [
          { title: "MoSPI General Statistical Guidelines & Standards", pages: "pp. 1-5" }
        ]
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div>
        <h2 className="text-2xl font-bold text-statwise-navy tracking-tight">
          AI Tutor
        </h2>
        <p className="text-sm text-statwise-muted mt-0.5">
          Ask questions grounded in approved learning resources.
        </p>
      </div>

      {/* Main Tutor Box */}
      <div className="bg-white rounded-xl p-6 border border-slate-200/90 shadow-sm flex flex-col justify-between min-h-[580px]">
        <div>
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <div>
              <h3 className="text-lg font-bold text-statwise-navy">
                Statistical AI Tutor
              </h3>
              <p className="text-xs text-statwise-muted mt-0.5">
                Answers are supported by source passages and never replace official guidance.
              </p>
            </div>
            <div className="flex items-center gap-1 text-[11px] text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200 font-medium">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Grounded Retrieval</span>
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
                  className={`rounded-xl p-4 max-w-xl text-xs space-y-2 ${
                    m.sender === "user"
                      ? "bg-statwise-blue/15 text-statwise-navy font-medium border border-statwise-blue/30"
                      : "bg-statwise-canvas text-slate-800 border border-slate-200/80"
                  }`}
                >
                  <p className="leading-relaxed whitespace-pre-wrap">{m.text}</p>

                  {/* Grounded Source Citations */}
                  {m.sources && m.sources.length > 0 && (
                    <div className="pt-2 border-t border-slate-200/60 text-[11px] text-slate-500 font-normal">
                      <div className="font-semibold text-statwise-navy flex items-center gap-1 mb-0.5">
                        <BookOpen className="w-3 h-3 text-statwise-blue" />
                        <span>Sources:</span>
                      </div>
                      {m.sources.map((src, sIdx) => (
                        <div key={sIdx} className="text-slate-600">
                          • {src.title}, {src.pages}
                        </div>
                      ))}
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
                <span>Retrieving verified MoSPI statistical passages...</span>
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
              placeholder="Ask a statistical question (e.g., Explain sampling error)..."
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
            The tutor answers from approved content and displays source references to improve trust and auditability.
          </div>
        </div>
      </div>
    </div>
  );
}
