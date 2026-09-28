import React from 'react';
import { Bot, CheckCircle2, AlertOctagon, Zap, ShieldCheck } from 'lucide-react';

export default function AiSummary({ summary, brandName }) {
  if (!summary) return null;

  const {
    one_sentence_digest = "",
    key_drivers = [],
    risk_factors = [],
    action_items = [],
    overall_health = "Good"
  } = summary;

  return (
    <div className="glass-card rounded-2xl p-6 glass-card-hover border-indigo-500/20 relative overflow-hidden">
      
      {/* Background ambient gradient flare */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center">
            <Bot className="w-4 h-4 text-indigo-400" />
          </div>
          <div>
            <h3 className="font-extrabold text-base text-white flex items-center space-x-2">
              <span>AI Executive Reputation Digest</span>
              <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                NLP Intelligence
              </span>
            </h3>
            <p className="text-xs text-slate-400">Automated executive summary generated for {brandName}</p>
          </div>
        </div>

        <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>{overall_health} Health</span>
        </div>
      </div>

      {/* One Sentence Digest Banner */}
      <div className="bg-slate-900/90 border border-indigo-500/30 rounded-xl p-4 mb-5 shadow-inner">
        <p className="text-xs md:text-sm font-semibold text-indigo-100 leading-relaxed italic">
          "{one_sentence_digest}"
        </p>
      </div>

      {/* 3 Columns: Drivers, Risks, Action Items */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 text-xs">
        
        {/* Key Drivers */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center space-x-1.5 text-emerald-400 font-bold border-b border-slate-800 pb-2">
            <CheckCircle2 className="w-4 h-4" />
            <span>Key Positive Drivers</span>
          </div>
          <ul className="space-y-1.5 text-slate-300 list-disc list-inside">
            {key_drivers.map((d, i) => (
              <li key={i} className="leading-relaxed">{d}</li>
            ))}
          </ul>
        </div>

        {/* Risk Factors */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center space-x-1.5 text-rose-400 font-bold border-b border-slate-800 pb-2">
            <AlertOctagon className="w-4 h-4" />
            <span>Risk Factors & Threats</span>
          </div>
          <ul className="space-y-1.5 text-slate-300 list-disc list-inside">
            {risk_factors.map((r, i) => (
              <li key={i} className="leading-relaxed">{r}</li>
            ))}
          </ul>
        </div>

        {/* Action Items */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center space-x-1.5 text-amber-400 font-bold border-b border-slate-800 pb-2">
            <Zap className="w-4 h-4" />
            <span>Recommended Action Items</span>
          </div>
          <ul className="space-y-1.5 text-slate-300 list-disc list-inside">
            {action_items.map((a, i) => (
              <li key={i} className="leading-relaxed">{a}</li>
            ))}
          </ul>
        </div>

      </div>
    </div>
  );
}
