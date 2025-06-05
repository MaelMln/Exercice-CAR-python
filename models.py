from dataclasses import dataclass
import random
from raceParams import punctureChance, consumptionChance, distanceTraveledWhileDamaged, distanceTraveled, \
    gasConsumption, repairChance, refuelChance, distanceToWinTheRace

def prob(p):
    return random.random() < p


@dataclass
class Car:
    id: int
    tankCapacity: int
    kmTraveled: int
    wheelOk: bool = True
    color: str = "undefined"
    rank: int = 0
    sound: str = "VROUUUUUUM"
    turbo: bool = True
    damaged: bool = False
    refueled: bool = False
    win: bool = False

    def drive(self):
        if not self.wheelOk:
            if not self.tryRepairWheel():
                return self

        if self.tankCapacity == 0:
            if not self.tryRefuel():
                return self

        if prob(punctureChance):
            self.wheelOk = False
            print(f"La voiture {self.color} a crevé ses pneus !")
            return self

        prev_km = self.kmTraveled
        if prob(consumptionChance):
            self.tankCapacity -= gasConsumption

        if self.damaged:
            self.kmTraveled += distanceTraveledWhileDamaged
            self.damaged = False
        else:
            self.kmTraveled += distanceTraveled

        delta = self.kmTraveled - prev_km
        self.makeSound()
        print(f"La voiture {self.color} a avancé de {delta} km (total : {self.kmTraveled} km)")

        if self.kmTraveled >= distanceToWinTheRace:
            self.win = True
        return self

    def turboDrive(self):
        if self.kmTraveled >= distanceToWinTheRace / 2:
            if self.tankCapacity < gasConsumption * 2:
                print("Not enough tank capacity to activate turbo")
                return self

            prev_km = self.kmTraveled
            self.kmTraveled += distanceTraveled * 2
            self.tankCapacity -= gasConsumption * 2
            self.turbo = False

            delta = self.kmTraveled - prev_km
            print(f"La voiture {self.color} déclenche le turbo et avance de {delta} km (total : {self.kmTraveled} km)")

            if self.kmTraveled >= distanceToWinTheRace:
                self.win = True
        return self

    def makeSound(self):
        print(f"{self.sound} {self.color}")

    def tryRepairWheel(self) -> bool:
        if prob(repairChance):
            self.wheelOk = True
            print(f"La voiture {self.color} regonfle ses pneus !")
            return True
        print(f"La voiture {self.color} rate la réparation de ses pneus !")
        return False

    def tryRefuel(self) -> bool:
        if prob(refuelChance):
            self.tankCapacity += gasConsumption * 2
            self.refueled = True
            print(f"La voiture {self.color} remet de l'essence !")
            return True
        print(f"La voiture {self.color} verse son essence à côté du réservoir !")
        return False