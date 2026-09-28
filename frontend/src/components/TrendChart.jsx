import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp } from 'lucide-react';

export default function TrendChart({ trendData }) {
  if (!trendData || trendData.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-center items-center text-slate-400 text-xs">
        <TrendingUp className="w-8 h-8 text-slate-600 mb-2 animate-bounce" />
        <span>Accumulating trend telemetry data...</span>
      </div>
    );
  }

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded-xl shadow-2xl text-xs space-y-1">
          <p className="font-bold text-slate-300 text-[11px] border-b border-slate-800 pb-1">{label}</p>
          {payload.map((p, idx) => (
            <p key={idx} className="flex items-center justify-between space-x-4">
              <span className="flex items-center space-x-1.5" style={{ color: p.color }}>
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: p.color }} />
                <span>{p.name}:</span>
              </span>
              <span className="font-bold text-white">{p.value}%</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-between glass-card-hover">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <TrendingUp className="w-4 h-4 text-emerald-400" />
          <h3 className="font-bold text-sm text-white">Reputation & Sentiment Moving Average</h3>
        </div>
        <span className="text-[11px] text-slate-400 font-medium">Time Series Telemetry</span>
      </div>

      <div className="w-full h-60">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorPos" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
            <XAxis dataKey="timestamp" stroke="#94a3b8" fontSize={10} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={10} domain={[0, 100]} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Legend verticalAlign="top" height={30} formatter={(val) => <span className="text-xs text-slate-300 font-medium">{val}</span>} />
            <Area type="monotone" dataKey="score" name="Reputation Score" stroke="#6366f1" strokeWidth={2.5} fillOpacity={1} fill="url(#colorScore)" />
            <Area type="monotone" dataKey="positive_pct" name="Positive %" stroke="#10b981" strokeWidth={1.5} fillOpacity={1} fill="url(#colorPos)" />
            <Area type="monotone" dataKey="negative_pct" name="Negative %" stroke="#f43f5e" strokeWidth={1.5} fillOpacity={1} fill="url(#colorNeg)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
