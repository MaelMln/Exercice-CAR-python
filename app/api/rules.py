"""Endpoint de consultation / mise à jour des règles."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..core.rules import rules, Rules

router = APIRouter()


class RulesPatch(BaseModel):
    puncture: float | None = Field(None, ge=0, le=1)
    repair: float | None = Field(None, ge=0, le=1)
    refuel: float | None = Field(None, ge=0, le=1)
    consume: float | None = Field(None, ge=0, le=1)
    gas: int | None = Field(None, ge=1)
    step: int | None = Field(None, ge=1)
    step_dmg: int | None = Field(None, ge=1)
    finish: int | None = Field(None, ge=1)


@router.get("", response_model=Rules)
async def get_rules():
    return rules


@router.patch("", response_model=Rules)
async def patch_rules(patch: RulesPatch):
    changes = patch.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(400, "Aucun champ fourni")
    for k, v in changes.items():
        setattr(rules, k, v)
    return rules