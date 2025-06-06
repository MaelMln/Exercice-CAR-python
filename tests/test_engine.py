from app.core.engine import RaceEngine
from app.core.models import Car


def test_race_finishes():
    cars = [Car(id=1, pilot="Test", color="red", tank=20)]
    engine = RaceEngine(cars, finish=20)
    engine.run()
    assert engine.finished
    assert cars[0].rank == 1