import React from 'react';
import { UserCheck, Building, MapPin, Box, ShieldAlert } from 'lucide-react';

export default function EntitiesList({ entities }) {
  if (!entities || entities.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-center items-center text-slate-400 text-xs">
        <Building className="w-6 h-6 text-slate-600 mb-2" />
        <span>No named entities extracted yet.</span>
      </div>
    );
  }

  const getEntityIcon = (type) => {
    switch (type) {
      case 'Person':
        return <UserCheck className="w-3.5 h-3.5 text-indigo-400" />;
      case 'Organization':
      case 'Brand':
        return <Building className="w-3.5 h-3.5 text-purple-400" />;
      case 'Location':
        return <MapPin className="w-3.5 h-3.5 text-emerald-400" />;
      default:
        return <Box className="w-3.5 h-3.5 text-amber-400" />;
    }
  };

  return (
    <div className="glass-card rounded-2xl p-5 h-full flex flex-col justify-between glass-card-hover">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <Building className="w-4 h-4 text-purple-400" />
          <h3 className="font-bold text-sm text-white">Extracted Named Entities (NER)</h3>
        </div>
        <span className="text-[11px] text-slate-400 font-medium">{entities.length} entities</span>
      </div>

      <div className="flex flex-wrap gap-2 overflow-y-auto max-h-56 p-1">
        {entities.map((e, idx) => (
          <div
            key={e.id || idx}
            className="flex items-center space-x-2 bg-slate-900/80 border border-slate-800 hover:border-indigo-500/40 px-3 py-1.5 rounded-xl text-xs transition-all"
          >
            {getEntityIcon(e.entity_type)}
            <span className="font-semibold text-slate-200">{e.name}</span>
            <span className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400 font-mono">
              {e.entity_type} ({e.count})
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
