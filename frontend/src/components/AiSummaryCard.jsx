import React from 'react';

export default function AiSummaryCard({ summary, brandName }) {
  if (!summary) return null;

  return (
    <section className="card ai-summary-card" aria-label="AI Executive Summary">
      <div className="section-header" style={{ marginBottom: '14px' }}>
        <div>
          <div className="card-kicker">AI REPUTATION DIGEST • NLP INTELLIGENCE</div>
          <h2 style={{ fontSize: '16px', color: '#0f172a', fontWeight: '800' }}>
            Executive Summary for {brandName}
          </h2>
        </div>
        <span className="sample-badge">✦ AI Synthesized Digest</span>
      </div>

      <div className="ai-digest-banner" style={{ background: '#f8fafc', borderLeft: '4px solid #315ce7', borderRadius: '10px', padding: '14px 18px', fontSize: '13px', color: '#1e293b', fontWeight: '600', lineHeight: '1.5', marginBottom: '20px' }}>
        "{summary.one_sentence_digest}"
      </div>

      <div className="ai-columns" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
        {/* Key Positive Drivers */}
        <div className="ai-column" style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.03)' }}>
          <div className="ai-col-title positive" style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontWeight: '750', color: '#13a57d', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            <span style={{ width: '26px', height: '26px', borderRadius: '7px', background: '#eaf8f2', color: '#13a57d', display: 'grid', placeItems: 'center', flex: 'none' }}>
              <svg style={{ width: '15px', height: '15px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7" /></svg>
            </span>
            Key Positive Drivers
          </div>
          <ul className="ai-list" style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: '10px' }}>
            {summary.key_drivers && summary.key_drivers.map((driver, idx) => (
              <li key={idx} style={{ fontSize: '11px', color: '#334155', lineHeight: '1.45', position: 'relative', paddingLeft: '14px' }}>
                <span style={{ position: 'absolute', left: '0', top: '1px', color: '#13a57d', fontWeight: 'bold' }}>✓</span>
                {driver}
              </li>
            ))}
          </ul>
        </div>

        {/* Risk Factors & Threats */}
        <div className="ai-column" style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.03)' }}>
          <div className="ai-col-title risk" style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontWeight: '750', color: '#e96870', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            <span style={{ width: '26px', height: '26px', borderRadius: '7px', background: '#fff0f0', color: '#e96870', display: 'grid', placeItems: 'center', flex: 'none' }}>
              <svg style={{ width: '15px', height: '15px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </span>
            Risk Factors & Threats
          </div>
          <ul className="ai-list" style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: '10px' }}>
            {summary.risk_factors && summary.risk_factors.map((risk, idx) => (
              <li key={idx} style={{ fontSize: '11px', color: '#334155', lineHeight: '1.45', position: 'relative', paddingLeft: '14px' }}>
                <span style={{ position: 'absolute', left: '0', top: '1px', color: '#e96870', fontWeight: 'bold' }}>!</span>
                {risk}
              </li>
            ))}
          </ul>
        </div>

        {/* Recommended Action Items */}
        <div className="ai-column" style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.03)' }}>
          <div className="ai-col-title action" style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontWeight: '750', color: '#315ce7', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            <span style={{ width: '26px', height: '26px', borderRadius: '7px', background: '#eff3ff', color: '#315ce7', display: 'grid', placeItems: 'center', flex: 'none' }}>
              <svg style={{ width: '15px', height: '15px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </span>
            Recommended Action Items
          </div>
          <ul className="ai-list" style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: '10px' }}>
            {summary.action_items && summary.action_items.map((act, idx) => (
              <li key={idx} style={{ fontSize: '11px', color: '#334155', lineHeight: '1.45', position: 'relative', paddingLeft: '14px' }}>
                <span style={{ position: 'absolute', left: '0', top: '1px', color: '#315ce7', fontWeight: 'bold' }}>→</span>
                {act}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
