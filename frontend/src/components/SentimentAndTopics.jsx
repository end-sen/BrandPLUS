import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

export default function SentimentAndTopics({ dashboardData }) {
  const sentDist = dashboardData?.sentiment_distribution || {};
  const emotions = dashboardData?.emotion_distribution || {};
  const topics = dashboardData?.top_topics || [];
  const entities = dashboardData?.top_entities || [];

  const pieData = [
    { name: 'Positive', value: sentDist.positive || 0, color: '#13a57d' },
    { name: 'Neutral', value: sentDist.neutral || 0, color: '#94a3b8' },
    { name: 'Negative', value: sentDist.negative || 0, color: '#e96870' },
  ];

  const emotionList = [
    { name: 'Joy / Praise', key: 'joy', color: '#13a57d' },
    { name: 'Anger / Frustration', key: 'anger', color: '#e96870' },
    { name: 'Sadness / Disappointment', key: 'sadness', color: '#db9a29' },
    { name: 'Fear / Concern', key: 'fear', color: '#94a3b8' },
    { name: 'Surprise / News', key: 'surprise', color: '#315ce7' },
    { name: 'Disgust', key: 'disgust', color: '#64748b' },
  ];

  const totalEmotions = Object.values(emotions).reduce((a, b) => a + b, 0) || 1;

  return (
    <section className="insights-grid" aria-label="Sentiment and topic insights">
      {/* 1. Sentiment & Emotion Breakdown */}
      <article className="card sentiment-card">
        <div className="section-header">
          <div>
            <div className="card-kicker">THE CONVERSATION</div>
            <h2>Sentiment breakdown</h2>
          </div>
        </div>

        <div className="sentiment-layout">
          <div className="donut-wrap">
            <ResponsiveContainer width={112} height={112}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={36}
                  outerRadius={52}
                  paddingAngle={3}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="sentiment-legend">
            <div className="sentiment-row">
              <span className="sentiment-dot positive"></span>
              <span>Positive</span>
              <strong>{sentDist.positive_pct || 0}%</strong>
            </div>
            <div className="sentiment-row">
              <span className="sentiment-dot neutral"></span>
              <span>Neutral</span>
              <strong>{sentDist.neutral_pct || 0}%</strong>
            </div>
            <div className="sentiment-row">
              <span className="sentiment-dot negative"></span>
              <span>Negative</span>
              <strong>{sentDist.negative_pct || 0}%</strong>
            </div>
          </div>
        </div>

        <div className="emotion-divider"></div>

        <div className="emotion-heading">
          <strong>Emotions spectrum detected</strong>
        </div>

        <div className="emotion-list">
          {emotionList.map((em) => {
            const count = emotions[em.key] || 0;
            const pct = Math.round((count / totalEmotions) * 100);
            return (
              <div key={em.key} className="emotion-row">
                <span className="text-xs text-slate-600 truncate">{em.name}</span>
                <div className="emotion-track">
                  <div
                    className="emotion-fill"
                    style={{ width: `${pct}%`, background: em.color }}
                  ></div>
                </div>
                <span className="emotion-pct">{pct}%</span>
              </div>
            );
          })}
        </div>
      </article>

      {/* 2. Top Topics & Named Entities */}
      <article className="card topics-card">
        <div className="section-header">
          <div>
            <div className="card-kicker">WHAT PEOPLE TALK ABOUT</div>
            <h2>Top discussion topics & entities</h2>
          </div>
        </div>

        <div className="topic-list">
          {topics.length > 0 ? (
            topics.slice(0, 6).map((topic) => {
              const tone = topic.avg_sentiment_score > 0.15 ? 'positive' : topic.avg_sentiment_score < -0.15 ? 'negative' : 'neutral';
              return (
                <div key={topic.id} className="topic-row">
                  <span className="topic-name">{topic.name}</span>
                  <div className="topic-bar-track">
                    <div
                      className="topic-bar"
                      style={{ width: `${Math.min(100, topic.mention_count * 15)}%` }}
                    ></div>
                  </div>
                  <span className="topic-volume">{topic.mention_count}</span>
                  <span className={`topic-tone ${tone}`}>{tone}</span>
                </div>
              );
            })
          ) : (
            <div className="text-xs text-slate-400 py-6 text-center">
              Extracting topic clusters...
            </div>
          )}
        </div>

        {/* Named Entities Cloud */}
        {entities.length > 0 && (
          <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid #edf2f7' }}>
            <div className="card-kicker" style={{ marginBottom: '8px' }}>EXTRACTED NAMED ENTITIES</div>
            <div className="flex flex-wrap gap-1.5">
              {entities.slice(0, 8).map((e) => (
                <span key={e.id} className="text-xs bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full border border-slate-200">
                  {e.name} <span className="text-slate-400 text-[9px]">({e.entity_type})</span>
                </span>
              ))}
            </div>
          </div>
        )}
      </article>
    </section>
  );
}
