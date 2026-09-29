import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import KpiGrid from './components/KpiGrid';
import AiSummaryCard from './components/AiSummaryCard';
import TrendAndAlerts from './components/TrendAndAlerts';
import SentimentAndTopics from './components/SentimentAndTopics';
import SourcesBreakdown from './components/SourcesBreakdown';
import MentionsFeed from './components/MentionsFeed';

export default function App() {
  const [currentBrand, setCurrentBrand] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [trendData, setTrendData] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [isLoading, setIsLoading] = useState(false);
  const [isScraping, setIsScraping] = useState(false);
  const [error, setError] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);
  const socketRef = useRef(null);

  // Initial load: search default brand 'Aditya University' or first brand
  useEffect(() => {
    handleSearchBrand('Aditya University');
  }, []);

  // WebSocket Connection management for live telemetry streaming
  useEffect(() => {
    if (!currentBrand) return;

    // Target deployed Render backend domain for WebSockets when hosted on Vercel
    let wsHost = window.location.host;
    if (window.location.hostname.includes('vercel.app')) {
      wsHost = 'brandplus.onrender.com';
    }
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${wsHost}/ws/brand/${currentBrand.id}`;

    let ws;
    try {
      ws = new WebSocket(wsUrl);
      socketRef.current = ws;

      ws.onopen = () => {
        console.log(`WebSocket connected to ${wsUrl}`);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);

          if (message.event === 'new_mention') {
            showToast(`⚡ New Mention: "${message.data.title.substring(0, 45)}..."`);
            loadDashboardData(currentBrand.id);
          } else if (message.event === 'score_updated') {
            showToast(`📈 Reputation score updated to ${message.data.score}`);
            loadDashboardData(currentBrand.id);
          } else if (message.event === 'alert_triggered') {
            showToast(`🚨 Alert Triggered: ${message.data.title}`);
            loadDashboardData(currentBrand.id);
          }
        } catch (err) {
          console.error('Error handling WebSocket message:', err);
        }
      };

      ws.onerror = () => {
        // Gracefully handle WebSocket connection attempt failure without unhandled console errors
      };
    } catch (e) {
      console.warn('WebSocket connection unavailable:', e);
    }

    return () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [currentBrand]);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  const handleSearchBrand = async (brandName) => {
    setIsLoading(true);
    setError(null);

    try {
      const searchResp = await fetch('/api/brand/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: brandName })
      });

      if (!searchResp.ok) {
        let errorMsg = `Failed to initialize brand monitoring (Server returned ${searchResp.status})`;
        try {
          const errData = await searchResp.json();
          if (errData && errData.detail) errorMsg = errData.detail;
        } catch (e) {
          if (searchResp.status === 500) {
            errorMsg = "Backend server connection failed (500). Make sure the FastAPI backend is running on http://127.0.0.1:8000.";
          }
        }
        throw new Error(errorMsg);
      }

      const brandObj = await searchResp.json();
      setCurrentBrand(brandObj);
      await loadDashboardData(brandObj.id);
    } catch (err) {
      console.error(err);
      setError(err.message || "Error fetching brand data");
    } finally {
      setIsLoading(false);
    }
  };

  const loadDashboardData = async (brandId) => {
    try {
      const [dashResp, trendResp] = await Promise.all([
        fetch(`/api/brand/${brandId}/dashboard`),
        fetch(`/api/brand/${brandId}/trends`)
      ]);

      if (dashResp.ok) {
        const dashData = await dashResp.json();
        setDashboardData(dashData);
      }
      if (trendResp.ok) {
        const trData = await trendResp.json();
        setTrendData(trData.trends || []);
      }
    } catch (err) {
      console.error("Error loading dashboard metrics:", err);
    }
  };

  const handleTriggerScrape = async () => {
    if (!currentBrand) return;
    setIsScraping(true);

    try {
      const resp = await fetch(`/api/brand/${currentBrand.id}/scrape-now`, {
        method: 'POST'
      });

      if (resp.ok) {
        const resData = await resp.json();
        showToast(`✨ ${resData.message}`);
        await loadDashboardData(currentBrand.id);
      }
    } catch (err) {
      console.error("Scrape failed:", err);
    } finally {
      setIsScraping(false);
    }
  };

  const handleMarkAlertRead = async (alertId) => {
    try {
      await fetch(`/api/alert/${alertId}/read`, { method: 'PUT' });
      if (currentBrand) {
        loadDashboardData(currentBrand.id);
      }
    } catch (err) {
      console.error("Failed to mark alert as read:", err);
    }
  };

  const presets = ['Aditya University', 'Tesla', 'Apple', 'Microsoft', 'OpenAI'];
  const activeAlertCount = dashboardData?.active_alerts ? dashboardData.active_alerts.filter(a => !a.is_read).length : 0;

  return (
    <div className="app-shell">
      {/* Sidebar Navigation */}
      <Sidebar
        currentBrand={currentBrand}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        alertCount={activeAlertCount}
      />

      {/* Main Content Area */}
      <main className="main-content">
        <Topbar
          onSearchBrand={handleSearchBrand}
          onTriggerScrape={handleTriggerScrape}
          isScraping={isScraping}
          currentBrandName={currentBrand ? currentBrand.name : ''}
        />

        <div className="page-wrap">
          {/* Header Title & Presets */}
          <section className="page-heading">
            <div>
              <div className="eyebrow">BRAND INTELLIGENCE • MONITORING OVERVIEW</div>
              <div className="heading-line">
                <h1>Reputation overview</h1>
                <span className="sample-badge">
                  <i className="refresh-dot"></i> Live Web Scraper Active
                </span>
              </div>
              <p className="page-subtitle">
                A clear view of public feedback & sentiment for <strong>{currentBrand ? currentBrand.name : 'Target Brand'}</strong>.
              </p>

              {/* Preset buttons */}
              <div className="preset-pills">
                <span className="text-[10px] text-slate-400 font-semibold mr-1">PRESETS:</span>
                {presets.map((p) => (
                  <button
                    key={p}
                    onClick={() => handleSearchBrand(p)}
                    className={`preset-pill ${currentBrand && currentBrand.name === p ? 'active' : ''}`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
          </section>

          {/* Global Error Banner */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-5 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>{error}</span>
              </div>
              <button onClick={() => setError(null)} className="text-red-500 font-bold hover:underline">Dismiss</button>
            </div>
          )}

          {/* Loading Overlay */}
          {isLoading ? (
            <div className="py-24 text-center">
              <div className="inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
              <p className="mt-3 text-xs text-slate-500 font-medium">Scraping web sources & running sentiment classification for {currentBrand ? currentBrand.name : 'brand'}...</p>
            </div>
          ) : (
            <>
              {/* Tab Views */}
              {activeTab === 'overview' && (
                <>
                  <KpiGrid dashboardData={dashboardData} />
                  <AiSummaryCard summary={dashboardData?.summary} brandName={currentBrand ? currentBrand.name : ''} />
                  <TrendAndAlerts trendData={trendData} alerts={dashboardData?.active_alerts} onMarkAlertRead={handleMarkAlertRead} />
                  <SentimentAndTopics dashboardData={dashboardData} />
                  <SourcesBreakdown articles={dashboardData?.recent_mentions} />
                  <MentionsFeed articles={dashboardData?.recent_mentions} />
                </>
              )}

              {activeTab === 'mentions' && (
                <MentionsFeed articles={dashboardData?.recent_mentions} />
              )}

              {activeTab === 'topics' && (
                <SentimentAndTopics dashboardData={dashboardData} />
              )}

              {activeTab === 'alerts' && (
                <TrendAndAlerts trendData={trendData} alerts={dashboardData?.active_alerts} onMarkAlertRead={handleMarkAlertRead} />
              )}

              {activeTab === 'sources' && (
                <SourcesBreakdown articles={dashboardData?.recent_mentions} />
              )}
            </>
          )}
        </div>
      </main>

      {/* Toast Notification Popup */}
      {toastMessage && (
        <div className="toast-container">
          <div className="toast-msg">
            <span>{toastMessage}</span>
          </div>
        </div>
      )}
    </div>
  );
}
