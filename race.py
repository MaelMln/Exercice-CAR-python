import random

from raceParams import distanceToWinTheRace

turn = 0

def accident(moving_car, car2) :
    if random.random() < 0.25 :
        moving_car.damaged = True
        car2.damaged = True
        return True
    else :
        return False

def refreshLeaderboard(cars):
    current_order = sorted(cars, key=lambda c: c.rank)
    current_pos   = {car.id: idx for idx, car in enumerate(current_order)}

    new_order = sorted(cars, key=lambda c: c.kmTraveled, reverse=True)

    for new_idx, car in enumerate(new_order):
        prev_idx = current_pos[car.id]

        if new_idx < prev_idx:
            for k in range(new_idx, prev_idx):
                overtaken_car = current_order[k]
                print(f"La voiture {car.color} dépasse la voiture {overtaken_car.color} !")

    for rank, car in enumerate(new_order, start=1):
        car.rank = rank

    return new_order


def triggerAccident(moving_car, cars):
    for other_car in cars:
        if other_car is moving_car :
            continue
        distance = abs(moving_car.kmTraveled - other_car.kmTraveled)
        if distance <= 10:
            if accident(moving_car, other_car):
                print(f"La voiture {moving_car.color} percute la voiture {other_car.color} !")
                return True
    return False

def racingFacts(car):
    if car.tankCapacity == 0:
        print(f"La voiture {car.color} n'a plus d'essence !")
    if not car.wheelOk:
        print (f"La voiture {car.color} a crevé ses pneus !")
    if car.refueled:
        print(f"La voiture {car.color} a fait le plein d'essence !")
        car.refueled = False

def showFinalResult(cars):
    ordered = sorted(cars, key=lambda c: c.rank)
    for car in ordered:
        print(f"{car.rank} – {car.color} : {car.kmTraveled} km")


def oneRacingTurn(cars):
    global turn
    turn += 1
    print(f"\n===== TOUR {turn} =====")

    for car in cars:
        if car.win:
            continue
        if car.kmTraveled >= distanceToWinTheRace / 2 and car.turbo:
            car.turboDrive()
            print(f"La voiture {car.color} appuie sur le champignon !")
        else:
            car.drive()

        triggerAccident(car, cars)
        racingFacts(car)

    refreshLeaderboard(cars)


def race(cars):
    while not endRace(cars):
        oneRacingTurn(cars)

    refreshLeaderboard(cars)
    print("Voici le résultat final !")
    showFinalResult(cars)

def endRace(cars):
    return any(car.win for car in cars)