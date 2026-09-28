import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function TrendAndAlerts({ trendData, alerts, onMarkAlertRead }) {
  return (
    <section className="primary-grid" aria-label="Trend and alerts">
      {/* 1. Trend Chart */}
      <article className="card trend-card">
        <div className="section-header trend-heading">
          <div>
            <div className="card-kicker">REPUTATION HEALTH</div>
            <h2>Sentiment over time</h2>
            <p className="section-subtitle">Reputation score and negative conversation trajectory</p>
          </div>
        </div>

        <div className="chart-legend" style={{ marginTop: '12px', marginBottom: '12px' }}>
          <span><i className="legend-line score-line"></i> Reputation Score</span>
          <span><i className="legend-line negative-line"></i> Negative Share (%)</span>
        </div>

        <div className="chart-container" style={{ height: '200px' }}>
          {trendData && trendData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#315ce7" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#315ce7" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#e96870" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#e96870" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="timestamp" stroke="#94a3b8" fontSize={10} tickLine={false} />
                <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={10} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', borderColor: '#e2e8f0', fontSize: '11px' }}
                />
                <Area type="monotone" dataKey="score" stroke="#315ce7" strokeWidth={2.5} fillOpacity={1} fill="url(#colorScore)" name="Reputation Score" />
                <Area type="monotone" dataKey="negative_pct" stroke="#e96870" strokeWidth={1.8} strokeDasharray="3 3" fillOpacity={1} fill="url(#colorNeg)" name="Negative %" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-slate-400 text-xs">
              Collecting trend telemetry points...
            </div>
          )}
        </div>
      </article>

      {/* 2. Alerts List */}
      <article className="card alert-card">
        <div className="section-header alert-heading">
          <div>
            <div className="card-kicker">NEEDS YOUR ATTENTION</div>
            <h2>Emerging issues <span className="alert-count-badge">{alerts ? alerts.length : 0}</span></h2>
          </div>
        </div>

        <div className="alert-list" style={{ marginTop: '12px', display: 'grid', gap: '8px' }}>
          {alerts && alerts.length > 0 ? (
            alerts.slice(0, 4).map((alert) => (
              <div key={alert.id} className="alert-row" style={{ opacity: alert.is_read ? 0.6 : 1 }}>
                <div className={`alert-icon ${alert.severity === 'critical' ? 'red' : 'amber'}`}>
                  !
                </div>
                <div className="alert-copy">
                  <strong>{alert.title}</strong>
                  <span>{alert.message}</span>
                </div>
                {!alert.is_read && (
                  <button
                    onClick={() => onMarkAlertRead(alert.id)}
                    className="text-xs text-indigo-600 hover:underline ml-2"
                  >
                    Dismiss
                  </button>
                )}
              </div>
            ))
          ) : (
            <div className="text-xs text-slate-400 py-6 text-center">
              No active critical alerts detected for this brand.
            </div>
          )}
        </div>
      </article>
    </section>
  );
}
