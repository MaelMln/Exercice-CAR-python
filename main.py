from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from cars import loadCars, save_cars
from engine import RaceEngine
from raceParams import rules


class CarCreate(BaseModel):
    pilot: str
    color: str
    tank: int = Field(..., ge=1, le=30)


class CarUpdate(BaseModel):
    pilot: str | None = None
    color: str | None = None
    tank: int | None = Field(None, ge=1, le=30)


class RulesPatch(BaseModel):
    puncture: float | None = Field(None, ge=0, le=1)
    repair: float | None = Field(None, ge=0, le=1)
    refuel: float | None = Field(None, ge=0, le=1)
    consume: float | None = Field(None, ge=0, le=1)
    gas: int | None = Field(None, ge=1)
    step: int | None = Field(None, ge=1)
    step_dmg: int | None = Field(None, ge=1)
    finish: int | None = Field(None, ge=1)


app = FastAPI()
engine = RaceEngine(loadCars())
sent_ptr = 0

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.websocket("/ws/race")
async def websocket_race(ws: WebSocket):
    global sent_ptr
    sent_ptr = 0
    await ws.accept()
    try:
        while not engine.finished:
            engine.step()
            await ws.send_json(
                {
                    "cars": [car.__dict__ for car in engine.cars],
                    "events": engine.logs[sent_ptr:],
                }
            )
            sent_ptr = len(engine.logs)
        await ws.send_json(
            {
                "cars": [car.__dict__ for car in engine.cars],
                "events": engine.logs[sent_ptr:] + ["[FIN]"],
            }
        )
    except WebSocketDisconnect:
        pass


@app.post("/step")
async def step():
    before = len(engine.logs)

    if not engine.finished:
        engine.step()

    new_events = engine.logs[before:]

    return {
        "cars": [car.__dict__ for car in engine.cars],
        "events": new_events,
        "finished": engine.finished
    }


@app.post("/reset")
async def reset():
    global engine, sent_ptr

    cars = loadCars()

    for car in cars:
        car.km = 0
        car.rank = 0
        car.tank = max(car.tank, 1)
        car.wheel_ok = True
        car.turbo_ok = True
        car.damaged = False

    engine = RaceEngine(cars)
    sent_ptr = 0
    return {"status": "ok"}


def next_id() -> int:
    return max((car.id for car in engine.cars), default=0) + 1


@app.get("/cars", response_model=list[dict])
async def list_cars():
    return [car.__dict__ for car in engine.cars]


@app.post("/cars", status_code=201, response_model=dict)
async def create_car(payload: CarCreate):
    if len(engine.cars) >= 12:
        raise HTTPException(400, "Limite de 12 voitures atteinte")

    data = payload.model_dump()
    data["id"] = next_id()
    data["km"] = 0
    data["rank"] = len(engine.cars) + 1

    new_car = engine.CarCls(**data)
    engine.cars.append(new_car)

    save_cars(engine.cars)
    return new_car.__dict__


@app.put("/cars/{car_id}", response_model=dict)
async def update_car(car_id: int, payload: CarUpdate):
    data = payload.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(400, "Aucun champ fourni")

    for car in engine.cars:
        if car.id == car_id:
            for field, value in data.items():
                setattr(car, field, value)
            save_cars(engine.cars)
            return car.__dict__
    raise HTTPException(404, f"Voiture {car_id} introuvable")


@app.delete("/cars/{car_id}", status_code=204)
async def delete_car(car_id: int):
    for index, current_car in enumerate(engine.cars):
        if current_car.id == car_id:
            del engine.cars[index]
            for new_rank, car in enumerate(sorted(engine.cars, key=lambda x: x.km, reverse=True), 1):
                car.rank = new_rank
            save_cars(engine.cars)
            return
    raise HTTPException(404, f"Voiture {car_id} introuvable")


@app.get("/rules", response_model=dict)
async def get_rules():
    return rules.model_dump()


@app.patch("/rules", response_model=dict)
async def patch_rules(patch: RulesPatch):
    changes = patch.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(400, "Aucun champ fourni")
    for field, value in changes.items():
        setattr(rules, field, value)
    return {"status": "ok", "rules": rules.model_dump()}
