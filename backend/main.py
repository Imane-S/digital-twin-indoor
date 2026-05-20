from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, redis_client
from models import Base, PersonPosition
from datetime import datetime, timezone
import json

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestión de clientes WebSocket conectados
connected_clients: list[WebSocket] = []

@app.post("/positions")
async def receive_positions(data: dict):
    """Recibe posiciones del módulo de detección"""
    db: Session = SessionLocal()
    positions = data.get("positions", [])

    # Guardar en PostgreSQL
    for p in positions:
        entry = PersonPosition(
            person_id=p["id"],
            x=p["x"],
            y=p["y"],
            confidence=p.get("confidence", 1.0)
        )
        db.add(entry)
    db.commit()
    db.close()

    # Guardar estado actual en Redis
    redis_client.set("current_positions", json.dumps(positions))

    # Difundir a todos los clientes WebSocket
    for client in connected_clients:
        await client.send_text(json.dumps({
            "type": "positions",
            "data": positions,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))

    return {"status": "ok", "count": len(positions)}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """Clientes frontend se conectan aquí"""
    await ws.accept()
    connected_clients.append(ws)
    try:
        # Enviar estado actual inmediatamente al conectarse
        current = redis_client.get("current_positions")
        if current:
            await ws.send_text(json.dumps({
                "type": "positions",
                "data": json.loads(current),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))
        while True:
            await ws.receive_text()  # mantener conexión viva
    except WebSocketDisconnect:
        connected_clients.remove(ws)


@app.get("/history")
def get_history():
    """Consulta el historial completo de posiciones"""
    db: Session = SessionLocal()
    records = db.query(PersonPosition).order_by(PersonPosition.timestamp.desc()).limit(100).all()
    db.close()
    return [
        {"id": r.id, "person_id": r.person_id, "x": r.x, "y": r.y,
         "confidence": r.confidence, "timestamp": r.timestamp.isoformat()}
        for r in records
    ]


@app.get("/health")
def health():
    return {"status": "running"}