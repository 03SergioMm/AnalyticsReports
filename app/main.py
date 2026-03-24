from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import reports

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Microservicio de analítica y reportes - Tetris Burguer",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router, prefix="/reports", tags=["Reports"])


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
