"""Lecture / écriture du fichier JSON de voitures."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .models import Car
from ..settings import settings


def load_cars(file: str | Path | None = None) -> List[Car]:
    file = Path(file or settings.data_path)
    if not file.exists():
        return []
    raw = json.loads(file.read_text())
    return [
        Car(
            id=item["id"],
            pilot=item["pilot"],
            color=item["color"],
            tank=item["tankCapacity"],
            km=item.get("kmTraveled", 0),
            rank=item.get("rank", 0),
        )
        for item in raw
    ]


def save_cars(cars: List[Car], file: str | Path | None = None) -> None:
    file = Path(file or settings.data_path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(
        json.dumps(
            [
                {
                    "id": c.id,
                    "pilot": c.pilot,
                    "tankCapacity": c.tank,
                    "kmTraveled": c.km,
                    "wheelOk": c.wheel_ok,
                    "color": c.color,
                    "rank": c.rank,
                }
                for c in cars
            ],
            indent=2,
            ensure_ascii=False,
        )
    )