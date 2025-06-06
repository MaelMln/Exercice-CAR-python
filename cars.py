import json
from pathlib import Path
from models import Car

DATA_FILE = Path("cars.json")


def loadCars(file: Path | str = DATA_FILE) -> list[Car]:
    all_cars = json.loads(Path(file).read_text())
    return [Car(
        id=car["id"],
        pilot=car["pilot"],
        color=car["color"],
        tank=car["tankCapacity"],
        km=car.get("kmTraveled", 0),
        rank=car.get("rank", 0)
    ) for car in all_cars]


def car_to_json_dict(car: Car) -> dict:
    return {
        "id": car.id,
        "pilot": car.pilot,
        "tankCapacity": car.tank,
        "kmTraveled": car.km,
        "wheelOk": car.wheel_ok,
        "color": car.color,
        "rank": car.rank
    }


def save_cars(cars: list[Car], file: Path | str = DATA_FILE) -> None:
    data = [car_to_json_dict(car) for car in cars]
    Path(file).write_text(json.dumps(data, indent=2, ensure_ascii=False))


cars = loadCars()
