import React from 'react';
import { ShieldCheck, TrendingUp, TrendingDown, Minus, ThumbsUp, ThumbsDown, AlertTriangle } from 'lucide-react';

export default function ScoreCard({ scoreData, brandName, sentimentDist }) {
  if (!scoreData) return null;

  const { score = 50, health_status = "Fair", positive_pct = 0, neutral_pct = 0, negative_pct = 0, trend_direction = "stable" } = scoreData;

  const getHealthBadge = (status) => {
    switch (status) {
      case 'Excellent':
        return { color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30', icon: ShieldCheck, glow: 'shadow-glow-emerald' };
      case 'Good':
        return { color: 'bg-teal-500/10 text-teal-400 border-teal-500/30', icon: ShieldCheck, glow: 'shadow-glow-emerald' };
      case 'Fair':
        return { color: 'bg-amber-500/10 text-amber-400 border-amber-500/30', icon: Minus, glow: '' };
      case 'Warning':
        return { color: 'bg-orange-500/10 text-orange-400 border-orange-500/30', icon: AlertTriangle, glow: 'shadow-glow-rose' };
      case 'Critical':
        return { color: 'bg-rose-500/10 text-rose-400 border-rose-500/30', icon: AlertTriangle, glow: 'shadow-glow-rose' };
      default:
        return { color: 'bg-slate-500/10 text-slate-400 border-slate-500/30', icon: Minus, glow: '' };
    }
  };

  const badge = getHealthBadge(health_status);
  const StatusIcon = badge.icon;

  // SVG Radial Gauge calculation
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className={`glass-card rounded-2xl p-6 relative overflow-hidden glass-card-hover ${badge.glow}`}>
      
      {/* Background ambient glow effect */}
      <div className="absolute -right-12 -top-12 w-40 h-40 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none" />

      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        
        {/* Left Column: Brand Info & Status */}
        <div className="flex-1 text-center md:text-left">
          <div className="flex items-center justify-center md:justify-start space-x-2 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Reputation Index</span>
            <div className={`flex items-center space-x-1 border px-2.5 py-0.5 rounded-full text-xs font-bold ${badge.color}`}>
              <StatusIcon className="w-3.5 h-3.5" />
              <span>{health_status}</span>
            </div>
          </div>

          <h2 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">{brandName}</h2>
          <p className="text-xs text-slate-400 mt-1 max-w-sm">
            Real-time aggregate index synthesized from multi-source sentiment, emotion metrics, and news reliability.
          </p>

          {/* Sentiment Breakdown Pills */}
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-2 mt-4">
            <div className="flex items-center space-x-1.5 bg-emerald-950/40 border border-emerald-500/20 px-3 py-1.5 rounded-xl">
              <ThumbsUp className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-xs text-slate-300 font-medium">Pos:</span>
              <span className="text-xs font-bold text-emerald-400">{positive_pct}%</span>
            </div>

            <div className="flex items-center space-x-1.5 bg-amber-950/40 border border-amber-500/20 px-3 py-1.5 rounded-xl">
              <Minus className="w-3.5 h-3.5 text-amber-400" />
              <span className="text-xs text-slate-300 font-medium">Neu:</span>
              <span className="text-xs font-bold text-amber-400">{neutral_pct}%</span>
            </div>

            <div className="flex items-center space-x-1.5 bg-rose-950/40 border border-rose-500/20 px-3 py-1.5 rounded-xl">
              <ThumbsDown className="w-3.5 h-3.5 text-rose-400" />
              <span className="text-xs text-slate-300 font-medium">Neg:</span>
              <span className="text-xs font-bold text-rose-400">{negative_pct}%</span>
            </div>
          </div>
        </div>

        {/* Right Column: Radial Gauge Score */}
        <div className="relative flex items-center justify-center">
          <svg className="w-36 h-36 transform -rotate-90">
            <circle
              cx="72"
              cy="72"
              r={radius}
              stroke="currentColor"
              strokeWidth="10"
              className="text-slate-800"
              fill="transparent"
            />
            <circle
              cx="72"
              cy="72"
              r={radius}
              stroke="url(#scoreGradient)"
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-1000 ease-out"
            />
            <defs>
              <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#6366f1" />
                <stop offset="50%" stopColor="#10b981" />
                <stop offset="100%" stopColor="#38bdf8" />
              </linearGradient>
            </defs>
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-black tracking-tight text-white">{score}</span>
            <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Score / 100</span>
          </div>
        </div>

      </div>
    </div>
  );
}
