"""WebSocket + endpoints pas‑à‑pas."""
from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status

from ..core.engine import RaceEngine
from ..core.persistence import load_cars
from ..settings import settings

router = APIRouter()

action_engine: RaceEngine | None = None
sent_ptr = 0  # pointeur dans les logs pour le WS


@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset_race():
    global action_engine, sent_ptr
    action_engine = RaceEngine(load_cars())
    sent_ptr = 0
    return {"status": "ok"}


@router.post("/step")
async def step_once():
    if action_engine is None:
        await reset_race()
    assert action_engine  # mypy

    before = len(action_engine.logs)
    if not action_engine.finished:
        action_engine.step()
    new_events = action_engine.logs[before:]

    return {
        "cars": [c.__dict__ for c in action_engine.cars],
        "events": new_events,
        "finished": action_engine.finished,
    }


@router.websocket("/ws/race")
async def ws_race(ws: WebSocket):
    global sent_ptr, action_engine
    if action_engine is None:
        await reset_race()
    assert action_engine

    await ws.accept()
    try:
        while not action_engine.finished:
            action_engine.step()
            await ws.send_json({
                "cars": [c.__dict__ for c in action_engine.cars],
                "events": action_engine.logs[sent_ptr:],
            })
            sent_ptr = len(action_engine.logs)
        await ws.send_json({
            "cars": [c.__dict__ for c in action_engine.cars],
            "events": action_engine.logs[sent_ptr:] + ["[FIN]"],
        })
    except WebSocketDisconnect:
        pass