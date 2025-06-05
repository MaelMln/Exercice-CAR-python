from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from cars import cars
from race import oneRacingTurn, endRace

app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.websocket("/ws/race")
async def websocket_race(websocket: WebSocket):
    await websocket.accept()
    try:
        while not endRace(cars):
            oneRacingTurn(cars)
            await websocket.send_json([car.__dict__ for car in cars])
    except WebSocketDisconnect:
        print("Client déconnecté")
