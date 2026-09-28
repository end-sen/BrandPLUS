from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class BrandBase(BaseModel):
    name: str

class BrandCreate(BrandBase):
    description: Optional[str] = None

class BrandResponse(BrandBase):
    id: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ArticleSchema(BaseModel):
    id: int
    title: str
    text: str
    source: str
    source_type: str
    url: Optional[str] = None
    publication_date: datetime
    sentiment: str
    sentiment_score: float
    emotion: str
    topics: List[str] = []
    entities: List[Dict[str, str]] = []
    reliability_score: float

    class Config:
        from_attributes = True

class ReputationScoreSchema(BaseModel):
    score: float
    positive_pct: float
    neutral_pct: float
    negative_pct: float
    trend_direction: str
    health_status: str
    timestamp: datetime

    class Config:
        from_attributes = True

class AlertSchema(BaseModel):
    id: int
    brand_id: int
    alert_type: str
    severity: str
    title: str
    message: str
    is_read: bool
    timestamp: datetime

    class Config:
        from_attributes = True

class TopicSchema(BaseModel):
    id: int
    name: str
    mention_count: int
    avg_sentiment_score: float
    keywords: List[str] = []

    class Config:
        from_attributes = True

class EntitySchema(BaseModel):
    id: int
    name: str
    entity_type: str
    count: int

    class Config:
        from_attributes = True

class SentimentDistribution(BaseModel):
    positive: int
    neutral: int
    negative: int
    total: int
    positive_pct: float
    neutral_pct: float
    negative_pct: float

class EmotionDistribution(BaseModel):
    joy: int
    anger: int
    sadness: int
    fear: int
    surprise: int
    disgust: int

class TrendPoint(BaseModel):
    timestamp: str
    score: float
    positive_pct: float
    negative_pct: float
    volume: int

class ExecutiveSummary(BaseModel):
    one_sentence_digest: str
    key_drivers: List[str]
    risk_factors: List[str]
    action_items: List[str]
    overall_health: str

class DashboardOverview(BaseModel):
    brand: BrandResponse
    current_score: ReputationScoreSchema
    sentiment_distribution: SentimentDistribution
    emotion_distribution: EmotionDistribution
    recent_mentions: List[ArticleSchema]
    top_topics: List[TopicSchema]
    top_entities: List[EntitySchema]
    active_alerts: List[AlertSchema]
    summary: ExecutiveSummary
