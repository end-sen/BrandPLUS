import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

SOURCE_RELIABILITY_WEIGHTS = {
    "News": 0.95,
    "Review": 0.85,
    "Blog": 0.75,
    "Forum": 0.65,
    "Social": 0.60
}

class ReputationAnalyticsEngine:
    def calculate_reliability_score(self, source_type: str) -> float:
        return SOURCE_RELIABILITY_WEIGHTS.get(source_type, 0.75)

    def calculate_reputation_score(self, articles: List[Any]) -> Dict[str, Any]:
        """
        Calculates Reputation Score:
        Normalized formula taking into account weighted positive %, negative %, and source reliability.
        Outputs: score (0 - 100), positive_pct, neutral_pct, negative_pct, health_status.
        """
        if not articles:
            return {
                "score": 50.0,
                "positive_pct": 0.0,
                "neutral_pct": 100.0,
                "negative_pct": 0.0,
                "health_status": "Neutral",
                "trend_direction": "stable"
            }

        total_articles = len(articles)
        pos_count = sum(1 for a in articles if a.sentiment == "Positive")
        neu_count = sum(1 for a in articles if a.sentiment == "Neutral")
        neg_count = sum(1 for a in articles if a.sentiment == "Negative")

        pos_pct = round((pos_count / total_articles) * 100, 1)
        neu_pct = round((neu_count / total_articles) * 100, 1)
        neg_pct = round((neg_count / total_articles) * 100, 1)

        # Weighted score incorporating source reliability & sentiment confidence
        weighted_score_sum = 0.0
        total_weight = 0.0

        for a in articles:
            weight = getattr(a, "reliability_score", 0.75)
            s_score = getattr(a, "sentiment_score", 0.0)
            weighted_score_sum += s_score * weight
            total_weight += weight

        avg_weighted_score = (weighted_score_sum / total_weight) if total_weight > 0 else 0.0
        
        # Map avg_weighted_score (-1.0 to +1.0) into (0 to 100) scale
        final_score = round(((avg_weighted_score + 1.0) / 2.0) * 100, 1)

        # Determine Health Status
        if final_score >= 80:
            health_status = "Excellent"
        elif final_score >= 65:
            health_status = "Good"
        elif final_score >= 45:
            health_status = "Fair"
        elif final_score >= 30:
            health_status = "Warning"
        else:
            health_status = "Critical"

        return {
            "score": final_score,
            "positive_pct": pos_pct,
            "neutral_pct": neu_pct,
            "negative_pct": neg_pct,
            "health_status": health_status,
            "trend_direction": "stable"
        }

    def detect_anomalies(self, recent_articles: List[Any], historical_scores: List[Any]) -> List[Dict[str, Any]]:
        """
        Z-Score Anomaly Detection on negative sentiment spikes & volume surges.
        """
        anomalies = []
        if not recent_articles:
            return anomalies

        neg_count = sum(1 for a in recent_articles if a.sentiment == "Negative")
        total = len(recent_articles)
        neg_ratio = (neg_count / total) if total > 0 else 0

        # Negative Sentiment Spike Alert (> 30% negative)
        if neg_ratio >= 0.30:
            anomalies.append({
                "type": "negative_spike",
                "severity": "critical" if neg_ratio >= 0.50 else "warning",
                "title": "High Negative Sentiment Spike",
                "message": f"Negative mentions surged to {round(neg_ratio*100, 1)}% of total brand conversations."
            })

        # Volume Surge Alert
        if total >= 15:
            anomalies.append({
                "type": "volume_surge",
                "severity": "info",
                "title": "Mention Volume Surge",
                "message": f"Brand mention activity increased significantly with {total} new articles indexed."
            })

        # Score Drop Anomaly (Z-score check against historical series)
        if len(historical_scores) >= 3:
            scores_array = [s.score for s in historical_scores]
            mean_score = np.mean(scores_array)
            std_score = np.std(scores_array)
            
            if std_score > 0:
                current_score = scores_array[-1]
                z_score = (current_score - mean_score) / std_score
                if z_score <= -1.8:
                    anomalies.append({
                        "type": "score_drop",
                        "severity": "critical",
                        "title": "Abnormal Reputation Score Drop",
                        "message": f"Reputation score dropped significantly below average (Z-score: {round(z_score, 2)})."
                    })

        return anomalies

    def generate_trend_history(self, articles: List[Any]) -> List[Dict[str, Any]]:
        """Generates time-series trend points with moving average."""
        if not articles:
            return []

        # Group articles by date
        sorted_articles = sorted(articles, key=lambda a: a.publication_date)
        date_groups = {}
        for a in sorted_articles:
            date_str = a.publication_date.strftime("%Y-%m-%d %H:00")
            if date_str not in date_groups:
                date_groups[date_str] = []
            date_groups[date_str].append(a)

        trend_points = []
        cumulative_scores = []
        
        for dt, arts in date_groups.items():
            pos = sum(1 for x in arts if x.sentiment == "Positive")
            neg = sum(1 for x in arts if x.sentiment == "Negative")
            tot = len(arts)
            
            p_pct = round((pos / tot) * 100, 1)
            n_pct = round((neg / tot) * 100, 1)
            pt_score = round(((p_pct - n_pct + 100) / 2), 1)
            
            cumulative_scores.append(pt_score)
            moving_avg = round(float(np.mean(cumulative_scores[-3:])), 1)
            
            trend_points.append({
                "timestamp": dt,
                "score": moving_avg,
                "positive_pct": p_pct,
                "negative_pct": n_pct,
                "volume": tot
            })

        return trend_points

reputation_engine = ReputationAnalyticsEngine()
