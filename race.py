import random

from raceParams import rules

turn = 0


def accident(moving_car, car2):
    if random.random() < 0.25:
        moving_car.damaged = True
        car2.damaged = True
        return True
    else:
        return False


def refreshLeaderboard(cars, log):
    current_order = sorted(cars, key=lambda c: c.rank)
    current_pos = {car.id: idx for idx, car in enumerate(current_order)}

    new_order = sorted(cars, key=lambda c: c.kmTraveled, reverse=True)

    for new_idx, car in enumerate(new_order):
        prev_idx = current_pos[car.id]

        if new_idx < prev_idx:
            for k in range(new_idx, prev_idx):
                overtaken_car = current_order[k]
                log(f"{car.pilot} dépasse {overtaken_car.pilot} !")

    for rank, car in enumerate(new_order, start=1):
        car.rank = rank

    return new_order


def triggerAccident(moving_car, cars, log):
    for other_car in cars:
        if other_car is moving_car:
            continue
        distance = abs(moving_car.kmTraveled - other_car.kmTraveled)
        if distance <= 10:
            if accident(moving_car, other_car):
                log(f"{moving_car.pilot} percute la voiture de {other_car.pilot} !")
                return True
    return False


def racingFacts(car, log):
    if car.tankCapacity == 0:
        if not car.announced_empty:
            log(f"{car.pilot} n'a plus d'essence !")
            car.announced_empty = True
    else:
        car.announced_empty = False

    if not car.wheelOk:
        if not car.announced_flat:
            log(f"{car.pilot} a crevé ses pneus !")
            car.announced_flat = True
    else:
        car.announced_flat = False

    if car.refueled:
        log(f"{car.pilot} a fait le plein d'essence !")
        car.refueled = False


def oneRacingTurn(cars):
    global turn
    turn += 1
    events: list[str] = []

    def log(msg: str):
        events.append(f"[Tour {turn}] {msg}")
        print(msg)

    random.shuffle(cars)
    for car in cars:
        if car.win:
            continue
        if car.kmTraveled >= rules.finish / 2 and car.turbo and car.tankCapacity >= rules.gas * 2:
            car.turboDrive(log)
        else:
            car.drive(log)

        triggerAccident(car, cars, log)
        racingFacts(car, log)

    refreshLeaderboard(cars, log)
    return events


def race(cars, log):
    while not endRace(cars):
        oneRacingTurn(cars)

    refreshLeaderboard(cars, log)
    log("Voici le résultat final !")
    showFinalResult(cars, log)


def endRace(cars):
    return any(car.win for car in cars)


def showFinalResult(cars, log):
    ordered = sorted(cars, key=lambda c: c.rank)
    for car in ordered:
        log(f"{car.rank} – {car.pilot} : {car.kmTraveled} km")
