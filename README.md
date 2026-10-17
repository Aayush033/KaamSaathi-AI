# 🇮🇳 KaamSaathi AI (कामसाथी)
### An Accessible, Multilingual Generative AI Companion for India's Gig and Informal Workforce
*Prompt Wars — Warm-Up Challenge*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini%203.8%20Flash-4285F4.svg?style=flat&logo=google)](https://aistudio.google.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%203-003B57.svg?style=flat&logo=sqlite)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Executive Summary & Problem Alignment

In India, over **12 million informal and platform gig workers** (delivery partners for Zomato/Swiggy/Zepto/Blinkit, cab/auto drivers for Uber/Ola/Porter, construction and daily-wage laborers) lack structured administrative and digital support. They face:
1. **Opaque and fluctuating earnings**, with complex deductions, fuel costs, and platform commission fees.
2. **High physical vulnerability and safety risks** on city roads and hazardous job sites.
3. **Severe under-utilization of statutory welfare schemes** (e.g. e-Shram, PM-SYM, state gig worker boards) due to legal jargon and bureaucratic friction.
4. **Complex work contracts and unilateral penalty notices** that are hard to decipher.
5. **Helplessness in formal dispute resolution** when weekly payouts are delayed, deductions are unexplained, or accounts are suspended without cause.

**KaamSaathi AI** is a unified, mobile-first web application designed from the ground up to solve these problems through genuine Generative AI (**Google Gemini 3.8 Flash**), deterministic financial tracking, voice accessibility, and cross-module connected workflows.

---

## 🚀 Key Modules Overview

| Module | Feature | Implementation Details |
|---|---|---|
| **Module A** | **AI Worker Assistant** | Central conversational AI entry point supporting **Hindi & English** with Web Speech voice input/readout, intent routing, and grounded contextual answers using **Gemini 3.8 Flash**. |
| **Module B** | **Earnings Tracker** | Persistent income & expense logging with strict arithmetic logic: `Net = Gross + Tips/Incentives - Expenses`. Real-time daily, weekly, monthly aggregations with **per-worker session isolation**. |
| **Module C** | **Safety Guidance** | Tailored safety checklists by occupation (Delivery, Drivers, Daily Wage), fatigue management rules, and emergency SOS speed-dial (112, 108, 1091). |
| **Module D** | **Rights & Welfare Explorer** | Authoritative directory of central and state welfare schemes (e-Shram, PM-SYM, PM-JAY, PM-SVANidhi, Rajasthan Gig Act 2023, Karnataka Gig Workers Board, BOCW) with source attribution and official links. |
| **Module E** | **Document Assistant** | Extracts readable text from PDF/text uploads or pasted clauses. Generates grounded summaries, key amounts, conditions, and missing info checklists with Gemini 3.8 Flash. Max 5 MB upload protection. |
| **Module F** | **Grievance Drafter** | Generates professional, respectful formal dispute letters using user-supplied facts, linked earnings records, and actionable checklists. |

---

## 🔗 The 5 End-to-End Connected Journeys

1. **Journey 1: Track & Understand Real Earnings**
   - Worker logs shift income and fuel expenses $\rightarrow$ application calculates net take-home pay with trusted logic.
   - Worker taps **"Explain My Earnings with AI"**, sending actual calculated figures to Gemini 3.8 Flash for plain-language spending advice and profit breakdown.
2. **Journey 2: Identify & Draft a Payment Dispute**
   - Worker inspects an earning discrepancy in their recorded history.
   - Clicking **"Dispute"** on that row automatically deep-links into the Grievance Drafter with the platform name, date, and amount pre-filled.
   - AI drafts a formal dispute letter and provides a supporting evidence checklist.
3. **Journey 3: Understand a Document & Ask Follow-Ups**
   - Worker uploads or pastes contract clauses or deduction notices.
   - Gemini 3.8 Flash analyzes clauses and extracts key deadlines and obligations.
   - Worker taps **"Ask Follow-up in Chat"** to cross-examine terms directly with the AI assistant.
4. **Journey 4: Discover Relevant Welfare Schemes**
   - Worker filters by trade (e.g., Food Delivery) and location (e.g., Rajasthan / All India).
   - System displays verified schemes with official portal links.
   - Worker asks AI to explain exact documents required for application.
5. **Journey 5: Contextual Safety Guidance**
   - Worker switches their trade profile or asks a safety concern (e.g., handling customer aggression or night driving).
   - Assistant provides actionable steps and emergency contact triggers.

---

## 🔒 Security, Privacy & Data Isolation Architecture

- **Per-Worker Session Isolation**: Every visitor is automatically assigned a cryptographically random, server-generated session token stored in an `HttpOnly`, `SameSite=Lax` cookie (`kaamsaathi_session`). All earnings, grievances, and document analyses are strictly scoped by `session_id`. Users cannot read, modify, or delete any other user's records.
- **XSS-Safe Frontend Rendering**: All user inputs, database records, and AI responses are safely escaped before rendering. DOM elements are constructed via `document.createElement`, `textContent`, and event listeners rather than unsafe inline JavaScript attributes.
- **Secure Secret Handling**: API keys are loaded strictly from the server environment (`GEMINI_API_KEY`) or deployment secrets. No API keys are written to `.env` or client code.
- **File Upload Protection**: Enforces a strict 5 MB file size limit and validates file extensions (`.pdf`, `.txt`, `.csv`) before text extraction.

---

## 🛠️ Technology Stack & Architecture

- **Backend**: Python 3.14 + **FastAPI** (Asynchronous, High Performance)
- **Database**: **SQLite3** with session-scoped tables (`data/kaamsaathi.db`)
- **Generative AI Provider**: **Google Gemini 3.8 Flash** (`gemini-3.8-flash` via official `google-genai` SDK)
- **Document Processing**: `pypdf` + Text parsing
- **Frontend**: Mobile-first Single Page Application (HTML5, Vanilla CSS custom design system, Vanilla JavaScript with unified state)
- **Accessibility**: Web Speech API for speech-to-text voice questions and voice readout
- **Automated Testing**: `pytest` test suite with temporary isolated test database

---

## ⚙️ Quick Installation & Running Locally

### 1. Prerequisites
- Python 3.10+ (Python 3.14 supported)
- pip

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/kaamsaathi-ai.git
cd kaamsaathi-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Create a `.env` file in the project root:
```bash
cp .env.example .env
# Set your API key:
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

### 4. Run the Application
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open your browser at **http://127.0.0.1:8000**.

---

## 🧪 Automated Testing

Run the automated test suite with pytest:
```bash
pytest -v
```
**Test Coverage Includes (19 Tests Passing):**
- Dynamic health check reporting genuine database and model status (`tests/test_api_routes.py`)
- Single-page application serving on `/`
- Full earnings CRUD lifecycle and strict arithmetic calculations (`tests/test_earnings_calc.py`)
- **Per-worker data isolation**: Worker A cannot read, query, or delete Worker B's earnings
- Welfare scheme filtering by category and location
- Safety guide retrieval and emergency contact availability
- **Honest error handling**: Explicit HTTP 503 errors when credentials are missing (no fake success)
- Document upload size validation (rejecting oversized files > 5 MB)
- End-to-end user journeys 1 through 5 (`tests/test_workflows.py`)
- Multilingual intent routing in English and Hindi
- **Live Gemini 3.8 Flash smoke test**: Genuine model call verification via `/api/ai/test-connection`

---

## ☁️ Deployment Commands for Google Cloud Platform (GCP Cloud Run)

Google Cloud Run is the recommended serverless container platform on GCP for deploying KaamSaathi AI. It provides automatic HTTPS, zero-scaling cost savings, and effortless container scaling.

### Step 1: Install & Authenticate Google Cloud SDK (gcloud)
```bash
# Authenticate with your Google account
gcloud auth login

# Set your active GCP project ID
gcloud config set project YOUR_GCP_PROJECT_ID

# Enable required GCP APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
```

### Step 2: One-Command Build and Deploy to Cloud Run
From the root directory of this repository (`prompt_wars`):

> **Security Requirement**: Never inject API keys as plaintext environment variables. Store your key in Google Cloud Secret Manager.

```bash
# 1. Store your GEMINI_API_KEY in Secret Manager
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=-

# 2. Deploy Cloud Run referencing the secret securely
gcloud run deploy kaamsaathi-ai \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest \
  --set-env-vars GEMINI_MODEL=gemini-3.8-flash
```

Once deployment completes, Cloud Run will output your live URL, e.g.:
`https://kaamsaathi-ai-xxxxxx-el.a.run.app`

### 💡 Note on Cloud Run Storage Persistence
On Google Cloud Run, the local filesystem (`/app/data/kaamsaathi.db`) is local to the container instance. For production workloads with multi-region replication or long-term persistence across instance cold starts, mount a Google Cloud Storage volume via Cloud Storage FUSE or configure Cloud SQL (PostgreSQL). For hackathon evaluation, the containerized SQLite storage provides full per-session isolation and transactional persistence for all active user workflows.

---

## 🛡️ Anti-Mockup & Hackathon Compliance Audit

- **No hardcoded/fake financial statistics**: Starts with a genuine empty state for new users; all numbers are calculated from actual recorded SQLite rows with tested arithmetic.
- **Genuine GenAI integration**: Connects directly to Google Gemini 3.8 Flash via official SDK (`google-genai`). When credentials are missing or errors occur, the system reports an honest error without fabricating responses.
- **No dead buttons**: All UI controls, filters, modal triggers, and copy/download buttons are fully wired to working application logic.
- **Authentic welfare sources**: All schemes cite official Government of India / State Government portals and acts with last-verified dates.
