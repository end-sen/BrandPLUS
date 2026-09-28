import React, { useState } from 'react';

export default function Topbar({ onSearchBrand, onTriggerScrape, isScraping, currentBrandName }) {
  const [searchInput, setSearchInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      onSearchBrand(searchInput.trim());
      setSearchInput('');
    }
  };

  const presets = ['Aditya University', 'Tesla', 'Apple', 'Microsoft', 'OpenAI'];

  return (
    <header className="topbar">
      <div className="breadcrumbs">
        <span>Workspace</span>
        <span className="crumb-slash">/</span>
        <strong>{currentBrandName || 'Overview'}</strong>
      </div>

      <div className="topbar-actions">
        {/* Quick Search Form */}
        <form onSubmit={handleSubmit} className="brand-search-form">
          <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            className="brand-search-input"
            placeholder="Search any brand or university..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          <button type="submit" className="monitor-btn">
            Monitor
          </button>
        </form>

        {/* Live Scrape Now trigger */}
        <button
          onClick={onTriggerScrape}
          disabled={isScraping}
          className="scrape-btn"
          title="Triggers an immediate live web scrape pass"
        >
          <svg className={`w-3.5 h-3.5 ${isScraping ? 'animate-spin text-indigo-600' : 'text-slate-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>{isScraping ? 'Scraping...' : 'Scrape Now'}</span>
        </button>

        <span className="data-notice">
          <i className="refresh-dot"></i> Live Stream Feed
        </span>
      </div>
    </header>
  );
}
