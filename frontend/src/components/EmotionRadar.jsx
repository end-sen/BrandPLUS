import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { Smile, Frown, Zap, Flame, AlertCircle, Sparkles } from 'lucide-react';

export default function EmotionRadar({ emotionData }) {
  if (!emotionData) return null;

  const data = [
    { subject: 'Joy', value: emotionData.joy || 0, fullMark: 100 },
    { subject: 'Anger', value: emotionData.anger || 0, fullMark: 100 },
    { subject: 'Sadness', value: emotionData.sadness || 0, fullMark: 100 },
    { subject: 'Fear', value: emotionData.fear || 0, fullMark: 100 },
    { subject: 'Surprise', value: emotionData.surprise || 0, fullMark: 100 },
    { subject: 'Disgust', value: emotionData.disgust || 0, fullMark: 100 },
  ];

  const total = Object.values(emotionData).reduce((a, b) => a + b, 0) || 1;

  const getDominantEmotion = () => {
    let dominant = 'joy';
    let maxV = -1;
    for (const [em, val] of Object.entries(emotionData)) {
      if (val > maxV) {
        maxV = val;
        dominant = em;
      }
    }
    return dominant.toUpperCase();
  };

  return (
    <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-between glass-card-hover">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-purple-400" />
          <h3 className="font-bold text-sm text-white">Emotion Radar Spectrum</h3>
        </div>
        <div className="px-2.5 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 text-[11px] font-bold">
          Dominant: {getDominantEmotion()}
        </div>
      </div>

      <div className="w-full h-56">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
            <PolarGrid stroke="#334155" opacity={0.6} />
            <PolarAngleAxis dataKey="subject" stroke="#cbd5e1" fontSize={11} fontWeight={600} />
            <PolarRadiusAxis angle={30} domain={[0, 'auto']} stroke="#475569" fontSize={9} />
            <Radar name="Emotion Mentions" dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.4} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
              itemStyle={{ color: '#c084fc', fontWeight: 'bold' }}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Footer Emotion Pills */}
      <div className="grid grid-cols-6 gap-1 pt-3 border-t border-slate-800/80 text-center text-[10px]">
        <div>
          <span className="block text-slate-400 font-medium">Joy</span>
          <span className="font-bold text-emerald-400">{emotionData.joy || 0}</span>
        </div>
        <div>
          <span className="block text-slate-400 font-medium">Anger</span>
          <span className="font-bold text-rose-400">{emotionData.anger || 0}</span>
        </div>
        <div>
          <span className="block text-slate-400 font-medium">Sad</span>
          <span className="font-bold text-sky-400">{emotionData.sadness || 0}</span>
        </div>
        <div>
          <span className="block text-slate-400 font-medium">Fear</span>
          <span className="font-bold text-amber-400">{emotionData.fear || 0}</span>
        </div>
        <div>
          <span className="block text-slate-400 font-medium">Surp</span>
          <span className="font-bold text-purple-400">{emotionData.surprise || 0}</span>
        </div>
        <div>
          <span className="block text-slate-400 font-medium">Disg</span>
          <span className="font-bold text-orange-400">{emotionData.disgust || 0}</span>
        </div>
      </div>
    </div>
  );
}
