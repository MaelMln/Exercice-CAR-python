"""Règles paramétrables de la course."""
from pydantic import BaseModel, Field


class Rules(BaseModel):
    puncture: float = Field(0.05, ge=0, le=1)
    repair: float = Field(0.33, ge=0, le=1)
    refuel: float = Field(0.125, ge=0, le=1)
    consume: float = Field(0.80, ge=0, le=1)

    gas: int = Field(1, ge=1)
    step: int = Field(10, ge=1)
    step_dmg: int = Field(5, ge=1)
    finish: int = Field(100, ge=1)

    class Config:
        validate_assignment = True


rules = Rules()