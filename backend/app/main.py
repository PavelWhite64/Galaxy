"""
FastAPI application entry point.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import settings
from .database import engine, Base, get_db

# Import routers
from app.api.auth import router as auth_router
from app.api.plots import router as plots_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Virtual Social World Platform API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(plots_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Добро пожаловать в API Виртуального Социального Мира",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with DB connection test."""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# Create tables for development (use Alembic in production)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
