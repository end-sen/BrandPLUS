import React, { useState } from 'react';

export default function MentionsFeed({ articles }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [sentimentFilter, setSentimentFilter] = useState('all');

  const filteredArticles = (articles || []).filter((art) => {
    const matchesSearch =
      art.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.source.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesSentiment =
      sentimentFilter === 'all' || art.sentiment.toLowerCase() === sentimentFilter.toLowerCase();

    return matchesSearch && matchesSentiment;
  });

  return (
    <section className="card mentions-card" aria-label="Recent mentions">
      <div className="mentions-top">
        <div>
          <div className="card-kicker">THE LATEST CONVERSATION</div>
          <h2>Recent mentions ({filteredArticles.length})</h2>
          <p className="section-subtitle">Real-time mentions across news, blogs, reviews & forums</p>
        </div>
      </div>

      <div className="mention-tools">
        <div className="search-box">
          <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="search"
            placeholder="Search mentions, keywords or topics..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="sentiment-select">
          <select value={sentimentFilter} onChange={(e) => setSentimentFilter(e.target.value)}>
            <option value="all">All Sentiment</option>
            <option value="positive">Positive</option>
            <option value="neutral">Neutral</option>
            <option value="negative">Negative</option>
          </select>
        </div>
      </div>

      <div className="mentions-list">
        {filteredArticles.length > 0 ? (
          filteredArticles.map((art) => {
            const sentLower = art.sentiment ? art.sentiment.toLowerCase() : 'neutral';
            return (
              <div key={art.id} className="mention-row">
                <div className="mention-source-icon">
                  {art.source ? art.source.charAt(0).toUpperCase() : 'N'}
                </div>
                <div className="mention-body">
                  <div className="mention-meta">
                    <strong>{art.source}</strong>
                    <span>• {art.source_type}</span>
                  </div>
                  <a
                    href={art.url || '#'}
                    target="_blank"
                    rel="noreferrer"
                    className="font-semibold text-slate-800 hover:text-indigo-600 block text-xs"
                  >
                    {art.title}
                  </a>
                  <p className="mention-excerpt">{art.text}</p>
                </div>
                <div className="text-right">
                  <span className={`sentiment-pill ${sentLower}`}>
                    {art.sentiment}
                  </span>
                  {art.emotion && (
                    <span className="block text-[10px] text-slate-400 mt-1 font-medium">
                      {art.emotion}
                    </span>
                  )}
                </div>
              </div>
            );
          })
        ) : (
          <div className="py-8 text-center text-slate-400 text-xs">
            No mentions match your search filter criteria.
          </div>
        )}
      </div>
    </section>
  );
}
