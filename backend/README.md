# Virtual Social World Platform - Backend

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── hierarchy.py     # Galaxy, Planet, Territory, Plot, Object
│   │   ├── economy.py       # Credits, Stars, Transactions
│   │   └── governance.py    # Voting, Appeals, Rules
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── hierarchy.py
│   │   ├── economy.py
│   │   └── governance.py
│   ├── api/                 # API routers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── hierarchy.py
│   │   ├── economy.py
│   │   └── governance.py
│   ├── core/                # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py      # JWT, password hashing
│   │   ├── websocket.py     # WebSocket manager
│   │   └── rate_limiter.py  # Rate limiting
│   └── services/            # Business logic
│       ├── __init__.py
│       ├── auth_service.py
│       ├── hierarchy_service.py
│       ├── economy_service.py
│       └── governance_service.py
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

## Architecture Principles

1. **Determinism**: All logic is transparent, no AI moderation or random emissions
2. **Hierarchy**: Platform → Galaxy → Planet → Territory → Plot → Object
3. **Rule Inheritance**: Lower levels cannot violate upper levels
4. **Economy**: Soft (Credits) / Hard (Stars) with strict Faucet/Sink mechanisms
5. **Security**: JWT + refresh tokens, HTTPOnly cookies, Row-Level Security, rate limiting, anti-fraud

## Setup Instructions

1. Create virtual environment: `python3 -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables in `.env`
5. Run migrations: `alembic upgrade head`
6. Start server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
