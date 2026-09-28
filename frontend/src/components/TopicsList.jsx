import React from 'react';
import { MessageSquare, Tag } from 'lucide-react';

export default function TopicsList({ topics }) {
  if (!topics || topics.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-center items-center text-slate-400 text-xs">
        <Tag className="w-6 h-6 text-slate-600 mb-2" />
        <span>No topic clusters detected yet.</span>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-between glass-card-hover">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <MessageSquare className="w-4 h-4 text-indigo-400" />
          <h3 className="font-bold text-sm text-white">Top Discussion Topics</h3>
        </div>
        <span className="text-[11px] text-slate-400 font-medium">{topics.length} topics</span>
      </div>

      <div className="space-y-2.5 overflow-y-auto max-h-56 pr-1">
        {topics.map((t, idx) => {
          const isPositive = t.avg_sentiment_score > 0.15;
          const isNegative = t.avg_sentiment_score < -0.15;

          return (
            <div
              key={t.id || idx}
              className="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all text-xs"
            >
              <div className="flex items-center space-x-2.5 overflow-hidden">
                <span className="w-6 h-6 rounded-lg bg-indigo-500/10 text-indigo-400 font-bold flex items-center justify-center text-[10px] shrink-0">
                  #{idx + 1}
                </span>
                <span className="font-semibold text-slate-200 truncate">{t.name}</span>
              </div>

              <div className="flex items-center space-x-2 shrink-0">
                <span className="text-slate-400 text-[11px]">{t.mention_count} mentions</span>
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                    isPositive
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      : isNegative
                      ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                      : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                  }`}
                >
                  {isPositive ? '🟢 Pos' : isNegative ? '🔴 Neg' : '🟡 Neu'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
