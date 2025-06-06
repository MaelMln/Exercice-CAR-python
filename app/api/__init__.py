"""Sous‑paquet des routes FastAPI."""
from fastapi import APIRouter

from .cars import router as cars_router
from .race import router as race_router
from .rules import router as rules_router

router = APIRouter()
router.include_router(cars_router, prefix="/cars", tags=["Cars"])
router.include_router(race_router, tags=["Race"])
router.include_router(rules_router, prefix="/rules", tags=["Rules"])