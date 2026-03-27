# 🌍 AI-Driven Autonomous Travel Planner

An advanced, full-stack travel planning application powered by **Google Gemini AI**. This system automatically conducts research, verifies landmarks against real-world 2024 mapping data, and generates comprehensive multi-day itineraries.

## 🚀 Features

- **Autonomous Research**: Uses Gemini-1.5-Flash to research destinations.
- **Geographic Integrity**: Every landmark and hotel is fact-checked for real-world accuracy.
- **Interactive Itineraries**: Unique daily plans with logical routing (10-15km radius).
- **Hotel Intelligence**: Suggests Budget, Mid-range, and Luxury options with real-time highlights.
- **Car/Road Trip Mode**: Generates specific highway routes and waypoints.
- **Integrated Database**: SQLite-backed persistent storage for 40+ global destinations.

## 🛠️ Technology Stack

- **Frontend**: Next.js 15, React 19, Tailwind CSS.
- **Backend**: FastAPI (Python), SQLAlchemy, Pydantic.
- **AI Engine**: Google Generative AI (Gemini).
- **Authentication**: JWT-based Secure Auth (Register/Login/Me).

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🛡️ Database Seeding
To populate your local database with 500+ curated landmarks:
```bash
python backend/seed_db.py
```

## 📝 License
MIT License. Created with ❤️ by Antigravity AI.
