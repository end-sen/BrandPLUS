import React, { useState } from 'react';
import { Search, Activity, Radio, Sparkles, RefreshCw, Layers } from 'lucide-react';

export default function Navbar({ currentBrand, onSearchBrand, wsConnected, isScraping, onTriggerScrape }) {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearchBrand(searchTerm.trim());
      setSearchTerm('');
    }
  };

  const presetBrands = ["Tesla", "Apple", "Microsoft", "OpenAI", "Nike"];

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-slate-800/80 px-4 lg:px-8 py-3.5 mb-6">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
        
        {/* Brand & Logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 p-0.5 shadow-glow">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Activity className="w-5 h-5 text-indigo-400 animate-pulse-slow" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-extrabold text-xl tracking-tight text-white">BrandPulse<span className="text-indigo-400">AI</span></h1>
              <span className="bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">v1.0</span>
            </div>
            <p className="text-xs text-slate-400 font-medium">Real-Time Brand Reputation & Sentiment Monitor</p>
          </div>
        </div>

        {/* Search Bar & Preset Pills */}
        <div className="flex-1 max-w-xl mx-auto w-full">
          <form onSubmit={handleSearchSubmit} className="relative group">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search or enter any brand name (e.g., Tesla, Apple, OpenAI)..."
              className="w-full bg-slate-900/80 border border-slate-800 rounded-xl pl-11 pr-24 py-2.5 text-sm text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all duration-200 shadow-inner"
            />
            <Search className="w-4 h-4 text-slate-400 absolute left-4 top-3.5 transition-colors group-hover:text-indigo-400" />
            <button
              type="submit"
              className="absolute right-1.5 top-1.5 bottom-1.5 px-3.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition-all shadow-md flex items-center space-x-1.5"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Monitor</span>
            </button>
          </form>

          {/* Quick Presets */}
          <div className="flex items-center space-x-2 mt-2">
            <span className="text-[11px] text-slate-400 font-medium flex items-center space-x-1">
              <Layers className="w-3 h-3 text-slate-400" />
              <span>Presets:</span>
            </span>
            <div className="flex flex-wrap gap-1.5">
              {presetBrands.map((brand) => (
                <button
                  key={brand}
                  onClick={() => onSearchBrand(brand)}
                  className={`text-[11px] font-medium px-2.5 py-0.5 rounded-md border transition-all ${
                    currentBrand?.name.toLowerCase() === brand.toLowerCase()
                      ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/50'
                      : 'bg-slate-900/60 text-slate-400 border-slate-800 hover:text-white hover:border-slate-700'
                  }`}
                >
                  {brand}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Live Status Controls */}
        <div className="flex items-center space-x-3">
          <button
            onClick={onTriggerScrape}
            disabled={isScraping || !currentBrand}
            className="flex items-center space-x-2 px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-800 text-slate-200 text-xs font-medium transition-all disabled:opacity-50"
            title="Trigger real-time web scraping pass"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-indigo-400 ${isScraping ? 'animate-spin' : ''}`} />
            <span>{isScraping ? 'Scraping...' : 'Scrape Now'}</span>
          </button>

          {/* WebSocket Status Indicator */}
          <div className="flex items-center space-x-2 px-3 py-2 rounded-xl bg-slate-900/80 border border-slate-800 text-xs">
            <span className="relative flex h-2.5 w-2.5">
              {wsConnected && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              )}
              <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${wsConnected ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
            </span>
            <span className="text-slate-300 font-medium">
              {wsConnected ? 'Live Feed' : 'Offline'}
            </span>
          </div>
        </div>

      </div>
    </header>
  );
}
