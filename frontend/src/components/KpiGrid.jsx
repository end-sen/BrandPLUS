import React from 'react';

export default function KpiGrid({ dashboardData }) {
  const currentScore = dashboardData?.current_score;
  const sentDist = dashboardData?.sentiment_distribution || {};
  const activeAlerts = dashboardData?.active_alerts || [];

  const scoreVal = currentScore ? Math.round(currentScore.score) : 0;
  const healthStatus = currentScore?.health_status || 'Fair';

  const isHealthy = scoreVal >= 70;
  const statusClass = isHealthy ? 'healthy' : 'needs-attention';

  return (
    <section className="kpi-grid" aria-label="Reputation summary">
      {/* 1. Reputation Score */}
      <article className="card score-card">
        <div className="kpi-top">
          <span className="kpi-label">REPUTATION SCORE</span>
          <span className={`score-status ${statusClass}`}>
            {healthStatus}
          </span>
        </div>
        <div className="score-main">
          <div className="score-number">{scoreVal}</div>
          <div className="score-denom">/ 100</div>
        </div>
        <div className="score-footer">
          <span className={scoreVal >= 50 ? 'positive-change' : 'negative-change'}>
            {scoreVal >= 50 ? '↑ Positive Balance' : '↓ Attention Required'}
          </span>
          <div className="score-gauge" aria-hidden="true">
            <div className="gauge-track">
              <div
                className="gauge-fill"
                style={{
                  width: `${scoreVal}%`,
                  background: isHealthy ? '#13a57d' : scoreVal >= 50 ? '#db9a29' : '#e96870'
                }}
              ></div>
            </div>
            <span>100</span>
          </div>
        </div>
      </article>

      {/* 2. Total Mentions */}
      <article className="card metric-card">
        <div className="kpi-top">
          <span className="kpi-label">TOTAL MENTIONS</span>
          <span className="metric-icon blue-icon">
            <svg viewBox="0 0 24 24"><path d="M20.2 11.5a8.2 8.2 0 0 1-8.4 8.2 9.2 9.2 0 0 1-3.6-.7l-4.4 1.2 1.2-4.2a8.1 8.1 0 1 1 15.2-4.5Z"/></svg>
          </span>
        </div>
        <div className="metric-value">{sentDist.total ? sentDist.total.toLocaleString() : '0'}</div>
        <div className="metric-foot">
          <span className="positive-change">↑ Live Indexed</span>
          <span>across news & social</span>
        </div>
      </article>

      {/* 3. Positive Sentiment */}
      <article className="card metric-card">
        <div className="kpi-top">
          <span className="kpi-label">POSITIVE SENTIMENT</span>
          <span className="metric-icon green-icon">
            <svg viewBox="0 0 24 24"><path d="M7 14s1.5 2 5 2 5-2 5-2M8 9h.01M16 9h.01"/><circle cx="12" cy="12" r="9"/></svg>
          </span>
        </div>
        <div className="metric-value">{sentDist.positive_pct || 0}<span className="metric-unit">%</span></div>
        <div className="metric-foot">
          <span className="positive-change">↑ {sentDist.positive || 0} positive mentions</span>
        </div>
      </article>

      {/* 4. Active Issues / Alerts */}
      <article className="card metric-card issue-metric">
        <div className="kpi-top">
          <span className="kpi-label">ACTIVE ALERTS</span>
          <span className="metric-icon coral-icon">
            <svg viewBox="0 0 24 24"><path d="m12 4 9 16H3L12 4Z"/><path d="M12 9v5M12 17h.01"/></svg>
          </span>
        </div>
        <div className="metric-value">{activeAlerts.length}</div>
        <div className="metric-foot">
          <span className="negative-change">
            {activeAlerts.filter(a => !a.is_read).length} unread alerts
          </span>
        </div>
      </article>
    </section>
  );
}
