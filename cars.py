import json
from models import Car

def loadCars(file: str = 'cars.json'):
    with open(file) as json_file:
        cars = json.load(json_file)
    all_cars = []
    for car in cars:
        all_cars.append(
            Car(
                **car
            )
        )
    return all_cars

cars = loadCars()