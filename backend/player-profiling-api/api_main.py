from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from services.integration_service import IntegrationService

app = FastAPI(
    title=settings.app_name,
    description="Unified API layer for player profiling, ML analytics, and visualization integration.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = IntegrationService()


@app.get("/")
def root():
    return service.ok({
        "service": settings.app_name,
        "docs": "/docs",
        "health": f"{settings.api_prefix}/health"
    })


@app.get("/api/v1/health")
def health():
    return service.ok(service.health())


@app.get("/api/v1/players/compare")
def compare(player1: str, player2: str):
    return service.ok(service.compare(player1, player2))


@app.get("/api/v1/players/{player_id}")
def player(player_id: str):
    return service.ok(service.player(player_id))

# =========================
# 🟢 原子API（新增重点）
# =========================

@app.get("/api/v1/players/{player_id}/features")
def features(player_id: str):
    return service.ok(service.features(player_id))


@app.get("/api/v1/players/{player_id}/embedding")
def embedding(player_id: str):
    return service.ok(service.embedding(player_id))


@app.get("/api/v1/players/{player_id}/cluster")
def cluster(player_id: str):
    return service.ok(service.cluster(player_id))


@app.get("/api/v1/players/{player_id}/similarity")
def similarity(player_id: str, top_k: int = 5):
    return service.ok(service.similarity(player_id, top_k))


@app.get("/api/v1/players/{player_id}/trend")
def trend(player_id: str):
    return service.ok(service.trend(player_id))


@app.get("/api/v1/players/{player_id}/explanation")
def explanation(player_id: str):
    return service.ok(service.explanation(player_id))


# =========================
# 🔵 聚合API（保留）
# =========================

@app.get("/api/v1/players/{player_id}/profile")
def profile(player_id: str):
    return service.ok(service.get_player_profile(player_id))


@app.get("/api/v1/players/{player_id}/dashboard")
def dashboard(player_id: str):
    return service.ok(service.get_dashboard(player_id))
