import React from 'react';

export default function Sidebar({ currentBrand, activeTab, setActiveTab, alertCount = 0 }) {
  return (
    <aside className="sidebar" aria-label="Main navigation">
      <a className="brand-lockup" href="#overview" style={{ padding: '4px 0', marginBottom: '28px' }} onClick={(e) => { e.preventDefault(); setActiveTab('overview'); }}>
        <img src="/icon.png" style={{ height: '42px', width: 'auto', objectFit: 'contain' }} alt="BrandPlus Real-Time Reputation Platform" />
      </a>

      <div className="workspace-label">WORKSPACE</div>
      <nav className="primary-nav">
        <button 
          className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          <svg viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="4" rx="1.4"/><rect x="13.5" y="10.5" width="7" height="10" rx="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.6"/></svg>
          <span>Overview</span>
        </button>

        <button 
          className={`nav-link ${activeTab === 'mentions' ? 'active' : ''}`}
          onClick={() => setActiveTab('mentions')}
        >
          <svg viewBox="0 0 24 24"><path d="M20.2 11.5a8.2 8.2 0 0 1-8.4 8.2 9.2 9.2 0 0 1-3.6-.7l-4.4 1.2 1.2-4.2a8.1 8.1 0 1 1 15.2-4.5Z"/><path d="M8 11h.01M12 11h.01M16 11h.01"/></svg>
          <span>Mentions</span>
        </button>

        <button 
          className={`nav-link ${activeTab === 'topics' ? 'active' : ''}`}
          onClick={() => setActiveTab('topics')}
        >
          <svg viewBox="0 0 24 24"><path d="M4 5.5h16M4 12h11M4 18.5h7"/><circle cx="18" cy="12" r="2"/><circle cx="14" cy="18.5" r="2"/></svg>
          <span>Topics</span>
        </button>

        <button 
          className={`nav-link ${activeTab === 'alerts' ? 'active' : ''}`}
          onClick={() => setActiveTab('alerts')}
        >
          <svg viewBox="0 0 24 24"><path d="M18 8.5a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4"/></svg>
          <span>Alerts</span>
          {alertCount > 0 && <span className="nav-count alert-count">{alertCount}</span>}
        </button>

        <button 
          className={`nav-link ${activeTab === 'sources' ? 'active' : ''}`}
          onClick={() => setActiveTab('sources')}
        >
          <svg viewBox="0 0 24 24"><path d="M4 19.5V10M10 19.5V4.5M16 19.5v-7M22 19.5V7"/></svg>
          <span>Sources</span>
        </button>
      </nav>

      <div className="sidebar-divider"></div>
      <div className="workspace-label">ACTIVE MONITORING</div>
      <div className="watching-card">
        <div className="watching-logo">
          {currentBrand ? currentBrand.name.charAt(0).toUpperCase() : 'B'}
        </div>
        <div className="watching-copy">
          <strong>{currentBrand ? currentBrand.name : 'BrandPulse'}</strong>
          <span><i className="refresh-dot"></i> Live Stream Connected</span>
        </div>
      </div>

      <div className="sidebar-spacer"></div>

      <div className="sidebar-bottom">
        <div className="plan-chip">
          <span className="plan-spark">✦</span>
          <div>
            <strong>Insight Enterprise Plan</strong>
            <small>Real-Time Scraper Active</small>
          </div>
        </div>

        <div className="user-profile">
          <div className="avatar">BP</div>
          <div className="user-copy">
            <strong>Admin Console</strong>
            <small>Brand Administrator</small>
          </div>
        </div>
      </div>
    </aside>
  );
}
