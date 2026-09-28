# Real-Time Brand Reputation Monitoring System 🚀

A full-stack, AI-powered Brand Reputation & Sentiment Monitoring System built with **Python (FastAPI)**, **React + Vite**, **Tailwind CSS**, **Recharts**, and **Scikit-Learn NLP**.

---

## 🌟 Features & Key Deliverables

- **🟢 Phase 1: Project Setup & Database** — SQLite/SQLAlchemy schema for Brands, Articles, Topics, Entities, Alerts, and Reputation Scores.
- **🟢 Phase 2: Multi-Source Web Scraping** — Requests + BeautifulSoup scraper for live news (Google News RSS), reviews (Trustpilot/G2), blogs (Medium/Dev.to), and forums (Reddit/Hacker News).
- **🟢 Phase 3: NLP Preprocessing Pipeline** — HTML sanitization, regex noise removal, tokenization, stopword filtering, and lemmatization using NLTK.
- **🟢 Phase 4: Machine Learning Sentiment Analysis** — TF-IDF vectorization (unigrams + bigrams) with a trained **Logistic Regression classifier** predicting Positive (🟢), Neutral (🟡), and Negative (🔴) mentions.
- **🟢 Phase 5: Emotion Detection System** — Classifies brand mentions into 6 core human emotions: **Joy, Anger, Sadness, Fear, Surprise, Disgust**.
- **🟢 Phase 6: Topic & Named Entity Recognition (NER)** — Topic modeling and NER categorizing mentions into Brand, Product, Person, Organization, and Location entities.
- **🟢 Phase 7: Reputation Analytics Engine** — Normalized Reputation Score formula (`0-100`), weighted by source reliability (`News: 0.95`, `Reviews: 0.85`, `Blogs: 0.75`), moving averages, and Z-score anomaly detection.
- **🟢 Phase 8: Real-Time Monitoring & WebSockets** — Async background monitor checking sources & pushing live stream updates (`new_mention`, `alert_triggered`, `score_updated`) over WebSocket connections (`/ws/brand/{id}`).
- **🟢 Phase 9: AI Summary Generation** — Executive NLP synthesis producing one-sentence brand health digests, key drivers, risk factors, and recommended action items.
- **🟢 Phase 10: FastAPI REST API** — Fully typed endpoints with Swagger documentation.
- **🟢 Phase 11: Modern React Dashboard** — Dark mode glassmorphic UI with real-time radial score gauge, sentiment donut chart, trend moving average area chart, emotion radar spectrum, topics cloud, filterable mentions table, and active alert feeds.
- **🟢 Phase 12: Testing Suite** — Pytest unit and integration tests covering NLP processing, ML sentiment classification, emotion detection, and reputation analytics.
- **🟢 Phase 13: Containerization & Deployment** — `Dockerfile` for backend & frontend + `docker-compose.yml`.

---

## 🏗️ Architecture & Technology Stack

```
           ┌─────────────────────────────────────────┐
           │        React + Vite Frontend            │
           │  (Tailwind CSS, Recharts, Lucide Icons) │
           └────────────────────┬────────────────────┘
                                │ (HTTP REST / WebSocket)
                                ▼
           ┌─────────────────────────────────────────┐
           │           FastAPI Backend               │
           │  (/api/brand/search, /ws/brand/{id})    │
           └────────┬──────────────────────┬─────────┘
                    │                      │
                    ▼                      ▼
┌───────────────────────────────┐  ┌───────────────────────────────┐
│     NLP / ML Engine           │  │      Web Scraper & RSS        │
│  - TF-IDF + Logistic Reg.     │  │  - BeautifulSoup4 & Requests  │
│  - 6-Emotion Spectrum         │  │  - Google News RSS Feed       │
│  - Topic Modeling & NER       │  │  - Multi-Source Simulation    │
└───────────────────────────────┘  └───────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### 2. Backend Setup & Server Execution

```bash
# Navigate to workspace root
cd backend

# Install Dependencies
pip install -r requirements.txt

# Run Pytest Test Suite
$env:PYTHONPATH="."
pytest tests/

# Start FastAPI Dev Server
uvicorn app.main:app --reload --port 8000
```
- Interactive API Swagger Documentation: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup & Execution

```bash
# Navigate to frontend folder
cd frontend

# Install Dependencies
npm install

# Start Vite Dev Server
npm run dev
```
- Open browser at `http://localhost:3000`

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/brand/search` | Search or initialize brand monitoring (scrapes & runs NLP) |
| `GET` | `/api/brands` | List all monitored brands |
| `GET` | `/api/brand/{id}/dashboard` | Returns full dashboard overview (scores, charts, mentions, alerts) |
| `GET` | `/api/brand/{id}/sentiment` | Returns sentiment percentages & count breakdown |
| `GET` | `/api/brand/{id}/trends` | Returns moving average sentiment trend points |
| `GET` | `/api/brand/{id}/topics` | Returns topic clusters & extracted named entities |
| `GET` | `/api/brand/{id}/alerts` | Returns brand alerts & anomaly notifications |
| `GET` | `/api/brand/{id}/summary` | Returns AI executive summary digest |
| `POST` | `/api/brand/{id}/scrape-now` | Triggers an immediate web scrape pass |
| `PUT` | `/api/alert/{alert_id}/read` | Marks an alert as read/dismissed |
| `WS` | `/ws/brand/{id}` | WebSocket endpoint for live telemetric streaming |

---

## 🐳 Docker Deployment

To run both backend and frontend using Docker Compose:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:80`
- Backend API: `http://localhost:8000`
