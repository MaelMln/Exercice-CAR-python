"""Modèles métiers."""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import IntFlag, auto

from .rules import rules


def roll(prob: float) -> bool:  # helper
    return random.random() < prob


class FlagEvent(IntFlag):
    NONE = 0
    PUNCTURE = auto()
    REPAIRED = auto()
    NO_REPAIR = auto()
    REFUELED = auto()
    NO_REFUEL = auto()
    OUT_OF_GAS = auto()
    MOVED = auto()
    TURBO = auto()
    FINISHED = auto()


@dataclass
class Car:
    id: int
    pilot: str
    color: str
    tank: int
    km: int = 0
    rank: int = 0
    wheel_ok: bool = True
    turbo_ok: bool = True
    damaged: bool = False

    def drive(self, turbo: bool = False) -> FlagEvent:
        ev = FlagEvent.NONE

        if not self.wheel_ok:
            if roll(rules.repair):
                self.wheel_ok = True
                ev |= FlagEvent.REPAIRED
            else:
                ev |= FlagEvent.NO_REPAIR
                return ev

        if self.tank == 0:
            if roll(rules.refuel):
                self.tank += rules.gas * 2
                ev |= FlagEvent.REFUELED
            else:
                ev |= FlagEvent.NO_REFUEL | FlagEvent.OUT_OF_GAS
                return ev

        if roll(rules.puncture):
            self.wheel_ok = False
            ev |= FlagEvent.PUNCTURE
            return ev

        if roll(rules.consume):
            self.tank = max(0, self.tank - rules.gas)

        distance = rules.step * (2 if turbo else 1)
        if self.damaged:
            distance = rules.step_dmg
            self.damaged = False

        self.km += distance
        ev |= FlagEvent.MOVED
        if turbo:
            ev |= FlagEvent.TURBO

        if self.km >= rules.finish:
            ev |= FlagEvent.FINISHED
        return ev