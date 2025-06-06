from __future__ import annotations
import random
from typing import List
from models import Car, FlagEvent, roll
from raceParams import rules


class RaceEngine:
    CarCls = Car

    def __init__(self, cars: List[Car]):
        self.cars: List[Car] = cars
        self.turn: int = 0
        self.logs: List[str] = []

    def _log(self, txt: str) -> None:
        self.logs.append(f"[Tour {self.turn}] {txt}")

    def commentary(self, car: Car, ev: FlagEvent) -> None:
        if ev & FlagEvent.PUNCTURE:  self._log(f"{car.pilot} crève un pneu")
        if ev & FlagEvent.REPAIRED:  self._log(f"{car.pilot} répare ses pneus")
        if ev & FlagEvent.NO_REPAIR: self._log(f"{car.pilot} échoue à réparer ses pneus")
        if ev & FlagEvent.REFUELED:  self._log(f"{car.pilot} refait le plein")
        if ev & FlagEvent.NO_REFUEL: self._log(f"{car.pilot} rate son ravitaillement")
        if ev & FlagEvent.OUT_OF_GAS: self._log(f"{car.pilot} n’a plus d’essence")
        if ev & FlagEvent.MOVED:
            km_traveled = 20 if ev & FlagEvent.TURBO else 10
            self._log(f"{car.pilot} avance de {km_traveled} km (total {car.km})")
        if ev & FlagEvent.FINISHED:  self._log(f"🚩 {car.pilot} franchit l’arrivée")

    def step(self) -> None:
        self.turn += 1
        random.shuffle(self.cars)

        for car in self.cars:
            if car.km >= rules.finish:
                continue
            turbo = (car.turbo_ok and car.km >= rules.finish / 2
                     and car.tank >= rules.gas * 2)
            ev = car.drive(turbo)
            self.commentary(car, ev)

            for other in self.cars:
                if other is car or other.km >= rules.finish: continue
                if abs(car.km - other.km) <= 10 and roll(0.25):
                    car.damaged = other.damaged = True
                    self._log(f"{car.pilot} percute {other.pilot}")

        old = {car.id: car.rank for car in self.cars}
        self.cars.sort(key=lambda car: car.km, reverse=True)
        for i, car in enumerate(self.cars, 1):
            if old.get(car.id, i) > i:
                self._log(f"{car.pilot} prend la {i}ᵉ place")
            car.rank = i

    @property
    def finished(self) -> bool:
        return any(c.km >= rules.finish for c in self.cars)

    def run(self) -> List[str]:
        while not self.finished:
            self.step()
        self._log("Voici le résultat final !")
        for c in self.cars:
            self._log(f"{c.rank} – {c.pilot} : {c.km} km")
        return self.logs
