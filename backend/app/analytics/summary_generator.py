from typing import List, Dict, Any
from ..config import settings

class AISummaryGenerator:
    def generate_summary(
        self,
        brand_name: str,
        articles: List[Any],
        score_data: Dict[str, Any],
        topics: List[Any],
        alerts: List[Any]
    ) -> Dict[str, Any]:
        """
        Generates executive AI summaries using structured NLP synthesis.
        Provides high-level actionable brand intelligence.
        """
        score = score_data.get("score", 50.0)
        pos_pct = score_data.get("positive_pct", 0.0)
        neg_pct = score_data.get("negative_pct", 0.0)
        health = score_data.get("health_status", "Fair")

        top_topic_names = [t.name for t in topics[:3]] if topics else ["General Product Updates"]
        active_alert_msgs = [a.message for a in alerts if a.severity in ["critical", "warning"]]

        # 1. One-Sentence Digest
        if score >= 75:
            digest = f"{brand_name} maintains a strong positive brand reputation (Score: {score}/100) driven by favorable sentiment around {', '.join(top_topic_names)}."
        elif score >= 50:
            digest = f"{brand_name} holds a balanced market reputation (Score: {score}/100) with key interest in {', '.join(top_topic_names)}."
        else:
            digest = f"{brand_name} is facing reputation headwind (Score: {score}/100) with heightened negative mentions ({neg_pct}%) concerning {', '.join(top_topic_names)}."

        # 2. Key Drivers (Positive drivers)
        key_drivers = []
        pos_articles = [a for a in articles if a.sentiment == "Positive"]
        if pos_articles:
            for pa in pos_articles[:3]:
                key_drivers.append(f"Positive coverage in {pa.source}: '{pa.title[:65]}...'")
        else:
            key_drivers.append("Consistent baseline media presence across major tech and industry outlets.")

        # 3. Risk Factors (Negative drivers / Alerts)
        risk_factors = []
        if active_alert_msgs:
            risk_factors.extend(active_alert_msgs[:2])
        neg_articles = [a for a in articles if a.sentiment == "Negative"]
        if neg_articles:
            for na in neg_articles[:2]:
                risk_factors.append(f"Critical feedback from {na.source}: '{na.title[:65]}...'")
        if not risk_factors:
            risk_factors.append("No immediate critical risk factors detected in current mention window.")

        # 4. Action Items
        action_items = []
        if neg_pct > 25:
            action_items.append("Engage customer support and PR teams to address user complaints on forums and review channels.")
        if any("Security" in t for t in top_topic_names):
            action_items.append("Issue transparent technical status update to mitigate customer concern over security/uptime.")
        action_items.append("Capitalize on high positive sentiment by amplifying top news coverage on official social channels.")
        action_items.append("Monitor trend metrics over the next 24 hours for potential sentiment shifts.")

        return {
            "one_sentence_digest": digest,
            "key_drivers": key_drivers,
            "risk_factors": risk_factors,
            "action_items": action_items,
            "overall_health": health
        }

summary_generator = AISummaryGenerator()
