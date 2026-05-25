# 🧠 SentiAI — Customer Sentiment Intelligence Platform
https://ai-dashboard-lrek.onrender.com/

> A full-stack web application that classifies customer reviews as **Positive 😊**, **Negative 😠**, or **Neutral 😐** using NLP.

Built with **Python · Flask · NLTK/VADER · scikit-learn · Chart.js**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask)
![NLTK](https://img.shields.io/badge/NLTK-VADER-4CAF50?style=flat)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat)

---

## 📑 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Project Structure](#3-project-structure)
4. [Setup & Installation](#4-setup--installation)
5. [API Reference](#5-api-reference)
6. [How It Works](#6-how-it-works)
7. [SDLC](#7-software-development-life-cycle-sdlc)
8. [Agile Methodology](#8-agile-methodology)
9. [UML Diagrams](#9-uml-diagrams)
10. [Use Case Specifications](#10-use-case-specifications)
11. [Security Considerations](#11-security-considerations)
12. [Real-World Use Cases](#12-real-world-use-cases)
13. [Dependencies](#13-dependencies)
14. [Future Roadmap](#14-future-roadmap)
15. [Glossary](#15-glossary)
16. [Licence](#16-licence)

---

## 1. Project Overview

SentiAI is a full-stack web application that classifies customer reviews into **Positive**, **Negative**, or **Neutral** categories using Natural Language Processing. The platform is designed to help businesses gain actionable insights from unstructured customer feedback at scale.

The system uses **VADER** as its primary model out-of-the-box (no training data required), with an optional **Logistic Regression** classifier for domain-specific accuracy.

### System Architecture

| Layer | Technology | Responsibility |
|---|---|---|
| Presentation | HTML5, CSS3, JavaScript | UI, Chart.js visualisations |
| Application | Flask 3.0 (Python) | REST API, session management, routing |
| NLP Engine | NLTK VADER + scikit-learn | Text preprocessing, sentiment prediction |
| Report Layer | ReportLab | PDF report generation |
| Data Store | JSON flat-file | User credential storage |
| Email | smtplib / Gmail SMTP | Welcome email on registration |

---

## 2. Features

| Feature | Description |
|---|---|
| **Single review analysis** | Type or paste any review and classify it instantly |
| **Bulk analysis** | Paste multiple reviews (one per line) and analyse all at once |
| **CSV upload** | Upload a `.csv` file of reviews for batch processing |
| **PDF report** | Download a full sentiment report with charts and stats |
| **Bar / Pie / Trend charts** | Interactive Chart.js visualisations of results |
| **Filterable results list** | Filter classified reviews by sentiment type |
| **User authentication** | Secure login and signup with hashed passwords |
| **Welcome email** | Login credentials emailed on registration |
| **Custom ML model** | Train a Logistic Regression model on your own labelled data |

---

## 3. Project Structure

```
senti_ai/
├── app.py                  # Flask app, routes, API endpoints
├── sentiment_engine.py     # VADER + Logistic Regression NLP engine
├── report_generator.py     # ReportLab PDF generation
├── train_model.py          # CLI script to train custom ML model
├── requirements.txt        # Python dependencies
├── data/
│   ├── users.json          # User accounts (hashed passwords)
│   ├── sample_reviews.csv  # Sample reviews for demo/testing
│   └── ml_model.pkl        # Trained ML model (created post-training)
├── templates/
│   ├── landing.html        # Public landing page
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
│   └── dashboard.html      # Main authenticated dashboard
└── static/
    ├── css/
    │   └── style.css       # Dashboard stylesheet
    └── js/
        └── app.js          # Chart.js logic, API calls, filtering
```

---

## 4. Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/senti-ai.git
cd senti-ai
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv

# Activate:
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables (optional — for email)

```bash
export MAIL_USER=your@gmail.com
export MAIL_PASS=your_app_password
```

> **Note:** If email variables are not set, the app still works — the welcome email step will silently fail and log the error.

### Step 5 — Run the app

```bash
python app.py
```

### Step 6 — Open in browser

```
http://localhost:5000
```

### Production Deployment (Gunicorn + Nginx)

```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

## 5. API Reference

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/` | No | Landing page |
| GET | `/login` | No | Login page |
| GET | `/signup` | No | Signup page |
| GET | `/dashboard` | Yes | Main dashboard |
| POST | `/api/login` | No | Authenticate user |
| POST | `/api/signup` | No | Register new user |
| POST | `/api/analyse` | Yes | Analyse JSON list of reviews |
| POST | `/api/upload` | Yes | Upload and analyse a CSV file |
| POST | `/api/report` | Yes | Generate and download PDF report |
| GET | `/logout` | Yes | Clear session and redirect |

### Example — Analyse Reviews

```bash
curl -X POST http://localhost:5000/api/analyse \
  -H "Content-Type: application/json" \
  -d '{"reviews": ["Great product!", "Terrible service.", "It is okay."]}'
```

**Response:**

```json
{
  "results": [
    {"text": "Great product!", "sentiment": "Positive", "confidence": 87, "model": "VADER"},
    {"text": "Terrible service.", "sentiment": "Negative", "confidence": 79, "model": "VADER"},
    {"text": "It is okay.", "sentiment": "Neutral", "confidence": 63, "model": "VADER"}
  ],
  "summary": {
    "total": 3,
    "counts": {"Positive": 1, "Negative": 1, "Neutral": 1},
    "percentages": {"Positive": 33.3, "Negative": 33.3, "Neutral": 33.3},
    "dominant": "Positive"
  }
}
```

---

## 6. How It Works

### Step 1 — Text Cleaning (`_clean()`)

- Converts text to lowercase
- Removes URLs, HTML tags, and punctuation
- Strips extra whitespace

### Step 2 — Sentiment Classification

**Default: VADER** (no training required)

| Compound Score | Sentiment |
|---|---|
| ≥ 0.05 | Positive |
| ≤ -0.05 | Negative |
| Between | Neutral |

**Optional: Logistic Regression** (scikit-learn)

- TF-IDF vectorisation → Logistic Regression classifier
- Trained on your own labelled data via `train_model.py`
- Model saved to `data/ml_model.pkl` and auto-loaded on next start

### Step 3 — Training a Custom Model

```bash
# Prepare a CSV with columns: text, label
# label must be: Positive | Negative | Neutral

python train_model.py --data data/your_labelled_data.csv
```

Example CSV format:

```csv
text,label
"The service was amazing!",Positive
"Delivery was too slow.",Negative
"The product is okay.",Neutral
```

> If no `label` column is found, VADER auto-labels the data for demo training.

---

## 7. Software Development Life Cycle (SDLC)

SentiAI was built following the **Agile SDLC** model across iterative sprints.

### Phase 1 — Requirements Gathering
- Functional requirements: authentication, text input, CSV upload, sentiment classification, PDF export
- Non-functional requirements: response time < 2s, scalable to 1 000+ reviews per batch
- Constraints: open-source stack only, deployable on standard Linux VPS

### Phase 2 — System Design
- MVC-inspired architecture: Flask routes → SentimentEngine → report_generator
- Database design: flat JSON for MVP; schema ready for PostgreSQL migration
- UI wireframes: login, signup, dashboard with charts

### Phase 3 — Implementation (6 Sprints)

| Sprint | Goal | Key Deliverables |
|---|---|---|
| Sprint 1 | Foundation | Flask scaffold, routing, templates |
| Sprint 2 | NLP Core | VADER engine, text cleaning, prediction API |
| Sprint 3 | Dashboard UI | Chart.js charts, bulk analysis, filter list |
| Sprint 4 | Data I/O | CSV upload, PDF report download |
| Sprint 5 | Auth System | Login, signup, session, welcome email |
| Sprint 6 | ML Training | train_model.py, model persistence |

### Phase 4 — Testing

| Test Type | Scope | Method |
|---|---|---|
| Unit Testing | SentimentEngine methods | pytest / manual |
| Integration Testing | Flask route → engine → JSON | Postman, curl |
| UI Testing | Login, signup, dashboard flows | Manual + DevTools |
| Performance Testing | Bulk 500 reviews | Locust load test |
| Security Testing | Auth, session, input sanitisation | OWASP checklist |

### Phase 5 — Deployment
- Containerised with Docker (optional Compose for production)
- Environment variables via `.env` file
- Reverse proxy: Nginx + SSL

### Phase 6 — Maintenance
- Version control: Git / GitHub (branch-per-feature)
- NLTK data auto-downloaded on first run
- ML model versioned as `data/ml_model.pkl`

---

## 8. Agile Methodology

SentiAI followed the **Scrum** framework within Agile.

### Scrum Team Roles

| Role | Responsibilities |
|---|---|
| Product Owner | Defines user stories, prioritises backlog, accepts deliverables |
| Scrum Master | Facilitates ceremonies, removes blockers, enforces process |
| Dev Team | Designs, implements, and tests all features |

### Ceremonies

- **Sprint Planning (Monday):** select stories, estimate with story points
- **Daily Standups:** 15-minute syncs — done / planned / blockers
- **Sprint Review (Friday):** demo working software to product owner
- **Sprint Retrospective:** identify process improvements

### Definition of Done

- [ ] Feature implemented and tested on Chrome, Firefox, Edge
- [ ] API returns correct HTTP status codes and JSON schema
- [ ] No regressions in previously working flows
- [ ] Code reviewed and merged to `main`
- [ ] Documentation updated if applicable

---

## 9. UML Diagrams

### 9.1 Use Case Diagram

```
                         ┌──────────────────────────────────────────────────────┐
                         │                   SentiAI System                     │
  ┌──────────────┐       │                                                      │
  │    Guest     │───────│──▶ View Landing Page                                 │
  └──────────────┘       │──▶ Register Account                                  │
                         │──▶ Log In                                            │
                         │                                                      │
  ┌──────────────┐       │──▶ Analyse Single Review                             │
  │ Auth. User   │───────│──▶ Bulk Analyse (Paste)                              │
  └──────────────┘       │──▶ Upload CSV                                        │
                         │──▶ View Charts                                       │
                         │──▶ Download PDF Report                               │
                         │──▶ Log Out                                           │
                         │                                                      │
  ┌──────────────┐       │──▶ Preprocess Text                                   │
  │ NLP Engine   │───────│──▶ Predict Sentiment                                 │
  └──────────────┘       │──▶ Return Confidence Score                           │
                         │                                                      │
  ┌──────────────┐       │──▶ Send Welcome Email                                │
  │ Email Service│───────│                                                      │
  └──────────────┘       │                                                      │
                         │──▶ Train Custom Model                                │
  ┌──────────────┐       │──▶ Manage Users                                      │
  │   Developer  │───────│──▶ Configure Environment                             │
  └──────────────┘       └──────────────────────────────────────────────────────┘
```

---

### 9.2 Class Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SentimentEngine                              │
├─────────────────────────────────────────────────────────────────────┤
│ - vader : SentimentIntensityAnalyzer                                 │
│ - ml_model : Pipeline | None                                         │
├─────────────────────────────────────────────────────────────────────┤
│ + predict(text: str) : dict                                          │
│ + train(texts: list, labels: list) : str                             │
│ - _vader_predict(original, cleaned) : dict                           │
│ - _ml_predict(original, cleaned) : dict                              │
│ - _clean(text: str) : str                                            │
│ - _save_model() : void                                               │
│ - _load_model() : void                                               │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ uses
             ┌──────────────┴──────────────┐
             ▼                             ▼
  ┌──────────────────────┐    ┌──────────────────────────┐
  │   Flask App (app.py) │    │   report_generator.py    │
  ├──────────────────────┤    ├──────────────────────────┤
  │ engine: SentEngine   │    │ + generate_report(       │
  │ USERS_FILE: str      │    │     results, summary)    │
  ├──────────────────────┤    │   : bytes (PDF)          │
  │ + analyse()          │    └──────────────────────────┘
  │ + upload()           │
  │ + report()           │
  │ + api_login()        │
  │ + api_signup()       │
  │ - _build_summary()   │
  │ - _send_welcome_email│
  └──────────────────────┘
```

---

### 9.3 Sequence Diagram — Bulk Analysis

```
User        Browser         Flask (app.py)      SentimentEngine
 │              │                 │                    │
 │──paste ──────▶               │                    │
 │              │──POST /api/analyse──▶              │
 │              │                 │──predict(r1)──────▶
 │              │                 │◀──{sentiment...}──│
 │              │                 │──predict(r2)──────▶
 │              │                 │◀──{sentiment...}──│
 │              │                 │──_build_summary()  │
 │              │◀──JSON {results, summary}────────── │
 │◀──render charts─              │                    │
```

---

### 9.4 Activity Diagram — Signup Flow

```
[Start]
   │
   ▼
User fills name / email / password
   │
   ▼
Client-side validation
   │── Invalid ──▶ Show error (loop back)
   │
   ▼  Valid
POST /api/signup
   │
   ▼
Email already exists? ──Yes──▶ Return 409 Conflict
   │ No
   ▼
Hash password (SHA-256)
   │
   ▼
Save user to users.json
   │
   ▼
Send welcome email (async try/catch)
   │
   ▼
Set session cookie
   │
   ▼
Redirect to /dashboard
   │
[End]
```

---

### 9.5 State Diagram — Sentiment Prediction

```
              ┌────────────────────────────────────────────┐
              │           SentimentEngine.predict()         │
              └────────────────────────────────────────────┘
                                    │
                          Raw text input received
                                    │
                                    ▼
                           [Text Cleaning]
                   Lowercase → Strip URLs/HTML/punct
                   → Normalise whitespace
                                    │
                     ┌──────────────┴──────────────┐
                ml_model exists?              ml_model is None
                     │                             │
                     ▼                             ▼
             [ML Prediction]              [VADER Prediction]
         TF-IDF → LogReg.predict()    polarity_scores() → compound
         Returns: class + proba        ≥  0.05 → Positive
                                       ≤ -0.05 → Negative
                                       else    → Neutral
                     │                             │
                     └──────────────┬──────────────┘
                                    ▼
                    Return { text, sentiment,
                             confidence, scores, model }
```

---

## 10. Use Case Specifications

### UC-01 — Analyse Single Review

| Field | Detail |
|---|---|
| **Actor** | Authenticated User |
| **Preconditions** | User is logged in; dashboard loaded |
| **Trigger** | User enters review text and clicks Analyse |
| **Main Flow** | 1. Enter text in textarea → 2. POST /api/analyse → 3. Engine predicts → 4. Badge renders with confidence % |
| **Alternate Flow** | Empty input → client prevents submission; shows inline error |
| **Postconditions** | Result shown; review added to filterable results list |

---

### UC-02 — Bulk CSV Upload

| Field | Detail |
|---|---|
| **Actor** | Authenticated User |
| **Preconditions** | User has a `.csv` file with one text column |
| **Trigger** | User selects file via upload zone or drag-and-drop |
| **Main Flow** | 1. POST file to /api/upload → 2. Flask reads CSV, strips header → 3. Each row predicted → 4. Charts + list rendered |
| **Alternate Flow** | CSV with no text → 400 error "No text found in CSV" |
| **Postconditions** | Summary metrics updated; PDF download button shown |

---

### UC-03 — Download PDF Report

| Field | Detail |
|---|---|
| **Actor** | Authenticated User |
| **Preconditions** | At least one analysis has been run |
| **Trigger** | User clicks Download PDF Report |
| **Main Flow** | 1. POST results + summary to /api/report → 2. generate_report() builds PDF → 3. File streamed as download |
| **Alternate Flow** | No results in payload → 400 error "No results provided" |
| **Postconditions** | PDF saved as `sentiment_report_YYYYMMDD_HHMMSS.pdf` |

---

### UC-04 — User Registration

| Field | Detail |
|---|---|
| **Actor** | Guest |
| **Preconditions** | Email not already registered |
| **Trigger** | User submits signup form |
| **Main Flow** | 1. Visit /signup → 2. Enter details → 3. POST /api/signup → 4. Hash + save → 5. Email sent → 6. Redirect to dashboard |
| **Alternate Flow** | Duplicate email → 409 · Password < 6 chars → 400 |
| **Security Note** | Password stored as SHA-256 hash only |

---

### UC-05 — Train Custom ML Model

| Field | Detail |
|---|---|
| **Actor** | Developer / Admin |
| **Preconditions** | Labelled CSV (text, label) available; venv active |
| **Trigger** | `python train_model.py --data path/to/data.csv` |
| **Main Flow** | 1. Load CSV → 2. Auto-label if no label col → 3. 80/20 split → 4. TF-IDF + LogReg fit → 5. Save to ml_model.pkl |
| **Postconditions** | App switches to ML model; badge shows LogisticRegression |

---

## 11. Security Considerations

| Area | Current | Recommended Improvement |
|---|---|---|
| Password Storage | SHA-256 hash | Migrate to bcrypt / argon2 + salting |
| Session Security | Flask signed cookie | Add timeout, secure + httpOnly flags |
| Email Credentials | Environment variables | Use OAuth2 / App Passwords |
| User Data Store | Flat JSON file | Migrate to PostgreSQL |
| Input Sanitisation | CSV stripped; VADER handles raw text | Add HTML-escape on rendered user content |
| HTTPS | Not enforced in dev | Enforce via Nginx + Let's Encrypt |
| Welcome Email | Password in plain-text email | Remove password; use one-time link |
| CSRF Protection | Not implemented | Add Flask-WTF CSRF tokens |

> ⚠️ **Important:** Never commit `users.json`, `.env`, or `data/ml_model.pkl` to a public repository. Add them to `.gitignore`.

---

## 12. Real-World Use Cases

| Industry | Use Case | Benefit |
|---|---|---|
| Retail / E-commerce | Analyse product reviews from Takealot / Amazon | Identify top complaints; improve listings |
| Banking & Finance | Monitor customer complaint emails | Flag service failures; reduce churn |
| Telecom | Track Twitter/X mentions for MTN, Vodacom | Real-time brand sentiment monitoring |
| Hospitality | Process post-stay survey responses | Pinpoint service gaps; reward top staff |
| Healthcare | Analyse patient satisfaction surveys | Improve care quality; surface systemic issues |
| Government | Monitor public feedback on service portals | Data-driven policy response |

---

## 13. Dependencies

| Package | Version | Purpose | Licence |
|---|---|---|---|
| Flask | >=3.0.0 | Web framework, routing, sessions | BSD-3 |
| NLTK | >=3.8.1 | NLP toolkit — VADER sentiment | Apache 2.0 |
| scikit-learn | >=1.4.0 | TF-IDF + Logistic Regression | BSD-3 |
| pandas | >=2.0.0 | CSV loading, data manipulation | BSD-3 |
| numpy | >=1.26.0 | Numerical operations | BSD-3 |
| ReportLab | >=4.0.0 | PDF generation | BSD-3 |
| Chart.js (CDN) | 4.4.1 | Interactive browser charts | MIT |

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 14. Future Roadmap

- [ ] Migrate user store from JSON to PostgreSQL
- [ ] Add OAuth2 social login (Google, GitHub)
- [ ] Implement BERT / Transformer-based sentiment model
- [ ] Real-time analysis via WebSocket for live review streams
- [ ] REST API key management for third-party integrations
- [ ] Docker Compose with Nginx + Gunicorn (one-command deploy)
- [ ] Multi-language support (Zulu, Afrikaans, Swahili)
- [ ] Admin panel for user management and model retraining from the UI
- [ ] Slack / Microsoft Teams webhook alerts for negative sentiment spikes
- [ ] Exportable charts as PNG/SVG in addition to PDF

---

## 15. Glossary

| Term | Definition |
|---|---|
| **VADER** | Valence Aware Dictionary and sEntiment Reasoner — rule-based NLP model optimised for social media text |
| **Compound Score** | VADER's normalised aggregate score from -1.0 (most negative) to +1.0 (most positive) |
| **TF-IDF** | Term Frequency-Inverse Document Frequency — statistical measure for text feature extraction |
| **Logistic Regression** | Supervised ML classification algorithm used as the optional custom model |
| **Pipeline (sklearn)** | Chained sequence of transformers and estimators; here TF-IDF → LogReg |
| **Session** | Flask server-side state stored in a signed browser cookie (HMAC-SHA256) |
| **SHA-256** | Cryptographic hash function used to store user passwords |
| **SMTP SSL** | Simple Mail Transfer Protocol over TLS/SSL — used for Gmail outbound email |
| **SDLC** | Software Development Life Cycle — structured process for planning, building, and maintaining software |
| **Scrum** | Agile framework using fixed-length sprints, ceremonies, and defined roles |
| **UML** | Unified Modelling Language — standardised notation for software design diagrams |
| **DFD** | Data Flow Diagram — shows how data moves through a system |

---

## 16. Licence

```
MIT License

Copyright (c) 2026 SentiAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

---

<div align="center">

**SentiAI** — Customer Sentiment Intelligence Platform

Built with Python · Flask · NLTK · scikit-learn · Chart.js

</div>
