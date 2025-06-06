"""Endpoints CRUD sur les voitures."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..core.models import Car
from ..core.persistence import load_cars, save_cars

router = APIRouter()


class CarIn(BaseModel):
    pilot: str
    color: str
    tank: int = Field(..., ge=1, le=30)


class CarOut(BaseModel):
    id: int
    pilot: str
    color: str
    tank: int = Field(..., ge=1, le=30)
    km: int
    rank: int

    class Config:
        orm_mode = True


def _cars() -> List[Car]:
    return load_cars()


def _save(cars: List[Car]) -> None:
    save_cars(cars)


@router.get("", response_model=list[CarOut])
async def list_cars():
    return _cars()


@router.post("", response_model=CarOut, status_code=status.HTTP_201_CREATED)
async def create_car(payload: CarIn):
    cars = _cars()
    if len(cars) >= 12:
        raise HTTPException(400, "Limite de 12 voitures atteinte")
    next_id = max((c.id for c in cars), default=0) + 1
    new_car = Car(id=next_id, pilot=payload.pilot, color=payload.color, tank=payload.tank, rank=len(cars) + 1)
    cars.append(new_car)
    _save(cars)
    return new_car


@router.put("/{car_id}", response_model=CarOut)
async def update_car(car_id: int, payload: CarIn):
    cars = _cars()
    for car in cars:
        if car.id == car_id:
            car.pilot = payload.pilot
            car.color = payload.color
            car.tank = payload.tank
            _save(cars)
            return car
    raise HTTPException(404, "Voiture introuvable")


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int):
    cars = _cars()
    idx = next((i for i, c in enumerate(cars) if c.id == car_id), None)
    if idx is None:
        raise HTTPException(404, "Voiture introuvable")
    cars.pop(idx)
    for rank, car in enumerate(sorted(cars, key=lambda c: c.km, reverse=True), 1):
        car.rank = rank
    _save(cars)