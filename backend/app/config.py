import os

class Settings:
    PROJECT_NAME: str = "Real-Time Brand Reputation Monitoring System"

    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./reputation_monitor.db")
    
    # NLP & Scraping Settings
    MAX_SCRAPE_ARTICLES_PER_SOURCE: int = 15
    MONITORING_INTERVAL_SECONDS: int = 30
    
    # Claude / Gemini / OpenAI API Key (Optional)
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")  # 'claude', 'openai', 'gemini', or 'mock'

settings = Settings()
