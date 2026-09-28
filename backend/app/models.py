from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    articles = relationship("Article", back_populates="brand", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="brand", cascade="all, delete-orphan")
    entities = relationship("Entity", back_populates="brand", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="brand", cascade="all, delete-orphan")
    scores = relationship("ReputationScore", back_populates="brand", cascade="all, delete-orphan")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    source_type = Column(String(50), default="News")  # News, Review, Blog, Forum, Social
    url = Column(String(500), nullable=True)
    publication_date = Column(DateTime, default=datetime.utcnow)
    
    # NLP Analysis outputs
    sentiment = Column(String(20), nullable=False)  # Positive, Neutral, Negative
    sentiment_score = Column(Float, default=0.0)  # Range -1.0 to 1.0
    emotion = Column(String(30), default="Joy")  # Joy, Anger, Sadness, Fear, Surprise, Disgust
    topics_json = Column(Text, nullable=True)  # JSON array of topic strings
    entities_json = Column(Text, nullable=True)  # JSON object/array of extracted entities
    reliability_score = Column(Float, default=0.8)  # 0.0 to 1.0
    
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="articles")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    name = Column(String(100), nullable=False)
    mention_count = Column(Integer, default=1)
    avg_sentiment_score = Column(Float, default=0.0)
    keywords_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="topics")


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    name = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)  # Brand, Product, Person, Organization, Location
    count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="entities")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)  # negative_spike, volume_surge, score_drop, viral_topic
    severity = Column(String(20), default="warning")  # info, warning, critical
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="alerts")


class ReputationScore(Base):
    __tablename__ = "reputation_scores"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    score = Column(Float, nullable=False)  # Normalized 0 - 100
    positive_pct = Column(Float, nullable=False)
    neutral_pct = Column(Float, nullable=False)
    negative_pct = Column(Float, nullable=False)
    trend_direction = Column(String(20), default="stable")  # up, down, stable
    health_status = Column(String(30), default="Good")  # Excellent, Good, Fair, Warning, Critical
    timestamp = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="scores")
