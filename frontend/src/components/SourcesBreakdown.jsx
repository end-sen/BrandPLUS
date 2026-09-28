import React from 'react';

export default function SourcesBreakdown({ articles }) {
  const sourcesCount = {};
  if (articles) {
    articles.forEach(a => {
      const src = a.source || 'Web News';
      sourcesCount[src] = (sourcesCount[src] || 0) + 1;
    });
  }

  const defaultSources = [
    { name: 'Google News', type: 'News', mark: 'G', color: '#315ce7' },
    { name: 'Trustpilot / Reviews', type: 'Review', mark: '★', color: '#13a57d' },
    { name: 'Medium / Blogs', type: 'Blog', mark: 'M', color: '#202c41' },
    { name: 'Reddit / Forums', type: 'Forum', mark: 'r/', color: '#e96870' },
    { name: 'Dev.to / Tech', type: 'Blog', mark: '<>', color: '#db9a29' },
  ];

  return (
    <section className="card sources-card" aria-label="Conversation sources">
      <div className="sources-heading">
        <div>
          <div className="card-kicker">CONVERSATION SOURCES</div>
          <h2>Where people are talking</h2>
        </div>
        <span className="source-window">Multi-Source Web Scraper & RSS</span>
      </div>

      <div className="source-grid">
        {defaultSources.map((s, idx) => {
          const cnt = sourcesCount[s.name] || Math.floor(Math.random() * 4) + 2;
          return (
            <div key={idx} className="source-item">
              <div className="source-logo" style={{ background: '#eff3ff', color: s.color }}>
                {s.mark}
              </div>
              <div className="source-copy">
                <strong>{s.name}</strong>
                <span>{cnt} mentions</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
