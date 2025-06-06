"""Moteur de course."""
from __future__ import annotations

import random
import logging
from typing import List

from .models import Car, FlagEvent
from .rules import rules

logger = logging.getLogger(__name__)


class RaceEngine:
    def __init__(self, cars: List[Car], finish: int | None = None):
        self.cars: List[Car] = cars
        self.turn: int = 0
        self.logs: List[str] = []
        if finish is not None:
            rules.finish = finish

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------
    def _log(self, msg: str) -> None:
        self.logs.append(f"[Tour {self.turn}] {msg}")
        logger.debug(msg)

    def _commentary(self, car: Car, ev: FlagEvent) -> None:
        if ev & FlagEvent.PUNCTURE:
            self._log(f"{car.pilot} crève un pneu")
        if ev & FlagEvent.REPAIRED:
            self._log(f"{car.pilot} répare ses pneus")
        if ev & FlagEvent.NO_REPAIR:
            self._log(f"{car.pilot} échoue à réparer ses pneus")
        if ev & FlagEvent.REFUELED:
            self._log(f"{car.pilot} refait le plein")
        if ev & FlagEvent.NO_REFUEL:
            self._log(f"{car.pilot} rate son ravitaillement")
        if ev & FlagEvent.OUT_OF_GAS:
            self._log(f"{car.pilot} n’a plus d’essence")
        if ev & FlagEvent.MOVED:
            km_turn = rules.step * (2 if ev & FlagEvent.TURBO else 1)
            self._log(f"{car.pilot} avance de {km_turn} km (total {car.km})")
        if ev & FlagEvent.FINISHED:
            self._log(f"🚩 {car.pilot} franchit l’arrivée")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def step(self) -> None:
        self.turn += 1
        random.shuffle(self.cars)

        for car in self.cars:
            if car.km >= rules.finish:
                continue

            turbo = car.turbo_ok and car.km >= rules.finish / 2 and car.tank >= rules.gas * 2
            ev = car.drive(turbo)
            self._commentary(car, ev)

            # collisions
            for other in self.cars:
                if other is car or other.km >= rules.finish:
                    continue
                if abs(car.km - other.km) <= 10 and random.random() < 0.25:
                    car.damaged = other.damaged = True
                    self._log(f"{car.pilot} percute {other.pilot}")

        # classement
        previous_ranks = {c.id: c.rank for c in self.cars}
        self.cars.sort(key=lambda c: c.km, reverse=True)
        for i, car in enumerate(self.cars, 1):
            if previous_ranks.get(car.id, i) > i:
                self._log(f"{car.pilot} prend la {i}ᵉ place")
            car.rank = i

    @property
    def finished(self) -> bool:
        return any(c.km >= rules.finish for c in self.cars)

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def run(self) -> List[str]:
        while not self.finished:
            self.step()
        self._log("Voici le résultat final !")
        for car in self.cars:
            self._log(f"{car.rank} – {car.pilot} : {car.km} km")
        return self.logs