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

# Orígenes permitidos — agrega todos los que uses
origins = [
    "http://localhost:5173",    # React con Vite
    "http://localhost:3000",    # React con CRA
    "http://localhost:4200",    # Angular (por si acaso)
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    settings.CORS_ALLOWED_ORIGINS,  
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
