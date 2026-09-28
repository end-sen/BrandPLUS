import React, { useState } from 'react';
import { Newspaper, ExternalLink, Filter, Search, ShieldCheck } from 'lucide-react';

export default function MentionsTable({ mentions }) {
  const [filterSentiment, setFilterSentiment] = useState('All');
  const [filterSource, setFilterSource] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  if (!mentions || mentions.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-6 text-center text-slate-400 text-xs">
        <Newspaper className="w-8 h-8 text-slate-600 mx-auto mb-2" />
        <span>No articles or mentions collected yet.</span>
      </div>
    );
  }

  const sources = ['All', ...new Set(mentions.map((m) => m.source_type || m.source))];

  const filteredMentions = mentions.filter((m) => {
    const matchesSentiment = filterSentiment === 'All' || m.sentiment === filterSentiment;
    const matchesSource = filterSource === 'All' || m.source_type === filterSource || m.source === filterSource;
    const matchesQuery =
      !searchQuery ||
      m.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.source.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesSentiment && matchesSource && matchesQuery;
  });

  return (
    <div className="glass-card rounded-2xl p-6 glass-card-hover">
      
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-5">
        <div className="flex items-center space-x-2">
          <Newspaper className="w-5 h-5 text-indigo-400" />
          <div>
            <h3 className="font-bold text-base text-white">Live Mentions & Media Index</h3>
            <p className="text-xs text-slate-400">Scraped across news, reviews, blogs, and technical forums</p>
          </div>
        </div>

        {/* Filter Toolbar */}
        <div className="flex flex-wrap items-center gap-2.5 text-xs">
          
          {/* Search Input */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search mentions..."
              className="bg-slate-900 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
          </div>

          {/* Sentiment Filter */}
          <select
            value={filterSentiment}
            onChange={(e) => setFilterSentiment(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500 font-medium"
          >
            <option value="All">All Sentiments</option>
            <option value="Positive">🟢 Positive</option>
            <option value="Neutral">🟡 Neutral</option>
            <option value="Negative">🔴 Negative</option>
          </select>

          {/* Source Filter */}
          <select
            value={filterSource}
            onChange={(e) => setFilterSource(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500 font-medium"
          >
            {sources.map((s) => (
              <option key={s} value={s}>{s === 'All' ? 'All Sources' : s}</option>
            ))}
          </select>

          <span className="text-[11px] text-slate-400 font-semibold px-2 py-1 bg-slate-900 rounded-lg border border-slate-800">
            {filteredMentions.length} items
          </span>
        </div>
      </div>

      {/* Mentions Table / List */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px] tracking-wider">
              <th className="py-3 px-3">Sentiment</th>
              <th className="py-3 px-3">Title & Summary Snippet</th>
              <th className="py-3 px-3">Source & Type</th>
              <th className="py-3 px-3">Emotion</th>
              <th className="py-3 px-3">Reliability</th>
              <th className="py-3 px-3 text-right">Link</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filteredMentions.map((m, idx) => {
              const isPos = m.sentiment === 'Positive';
              const isNeg = m.sentiment === 'Negative';

              return (
                <tr key={m.id || idx} className="hover:bg-slate-900/50 transition-colors group">
                  
                  {/* Sentiment Badge */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    <span
                      className={`inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-[11px] font-bold border ${
                        isPos
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                          : isNeg
                          ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                          : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                      }`}
                    >
                      <span>{isPos ? '🟢 Pos' : isNeg ? '🔴 Neg' : '🟡 Neu'}</span>
                    </span>
                  </td>

                  {/* Title & Snippet */}
                  <td className="py-3 px-3 max-w-md">
                    <p className="font-bold text-slate-200 group-hover:text-indigo-300 transition-colors line-clamp-1">
                      {m.title}
                    </p>
                    <p className="text-[11px] text-slate-400 line-clamp-2 mt-0.5 leading-relaxed">
                      {m.text}
                    </p>
                  </td>

                  {/* Source */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    <div className="font-semibold text-slate-300">{m.source}</div>
                    <span className="text-[10px] text-slate-400 bg-slate-800 px-1.5 py-0.5 rounded font-mono">
                      {m.source_type || 'News'}
                    </span>
                  </td>

                  {/* Emotion */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    <span className="px-2 py-0.5 rounded bg-purple-950/40 text-purple-300 border border-purple-500/20 text-[10px] font-semibold">
                      {m.emotion || 'Joy'}
                    </span>
                  </td>

                  {/* Reliability Score */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    <div className="flex items-center space-x-1 text-slate-300">
                      <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
                      <span className="font-semibold">{Math.round((m.reliability_score || 0.8) * 100)}%</span>
                    </div>
                  </td>

                  {/* Direct Link */}
                  <td className="py-3 px-3 text-right whitespace-nowrap">
                    {m.url ? (
                      <a
                        href={m.url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg bg-indigo-600/10 hover:bg-indigo-600 text-indigo-400 hover:text-white transition-all text-[11px] font-semibold"
                      >
                        <span>Read</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <span className="text-slate-600">-</span>
                    )}
                  </td>

                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

    </div>
  );
}
