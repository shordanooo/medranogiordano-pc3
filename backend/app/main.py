from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import proposals, users
import app.models.models  # noqa: F401  — registra modelos antes de create_all

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Voz del Ciudadano API",
    description="Plataforma para Iniciativas Legislativas Ciudadanas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(proposals.router)


@app.get("/")
def root():
    return {"message": "Voz del Ciudadano API v1.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
