import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { PieChart as PieIcon } from 'lucide-react';

const COLORS = {
  Positive: '#10b981',
  Neutral: '#f59e0b',
  Negative: '#f43f5e',
};

export default function SentimentChart({ sentimentDist }) {
  if (!sentimentDist) return null;

  const data = [
    { name: 'Positive', value: sentimentDist.positive || 0, percentage: sentimentDist.positive_pct || 0 },
    { name: 'Neutral', value: sentimentDist.neutral || 0, percentage: sentimentDist.neutral_pct || 0 },
    { name: 'Negative', value: sentimentDist.negative || 0, percentage: sentimentDist.negative_pct || 0 },
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const pData = payload[0];
      return (
        <div className="bg-slate-900 border border-slate-700 p-2.5 rounded-lg shadow-xl text-xs">
          <p className="font-bold text-white flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: pData.payload.fill }} />
            <span>{pData.name} Sentiment</span>
          </p>
          <p className="text-slate-300 mt-1">
            Count: <span className="font-semibold text-white">{pData.value}</span> ({pData.payload.percentage}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-between glass-card-hover">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <PieIcon className="w-4 h-4 text-indigo-400" />
          <h3 className="font-bold text-sm text-white">Sentiment Distribution</h3>
        </div>
        <span className="text-[11px] text-slate-400 font-medium">{sentimentDist.total || 0} mentions</span>
      </div>

      <div className="w-full h-56">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={80}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name]} stroke="rgba(15, 23, 42, 0.8)" strokeWidth={2} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value) => <span className="text-xs text-slate-300 font-medium">{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Footer stats list */}
      <div className="grid grid-cols-3 gap-2 pt-3 border-t border-slate-800/80 text-center text-xs">
        <div>
          <span className="block text-[10px] text-slate-400 font-semibold">Positive</span>
          <span className="font-bold text-emerald-400">{sentimentDist.positive_pct}%</span>
        </div>
        <div>
          <span className="block text-[10px] text-slate-400 font-semibold">Neutral</span>
          <span className="font-bold text-amber-400">{sentimentDist.neutral_pct}%</span>
        </div>
        <div>
          <span className="block text-[10px] text-slate-400 font-semibold">Negative</span>
          <span className="font-bold text-rose-400">{sentimentDist.negative_pct}%</span>
        </div>
      </div>
    </div>
  );
}
