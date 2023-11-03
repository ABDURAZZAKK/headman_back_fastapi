import json
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from services.chat_services import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.get("/", response_class=FileResponse)
async def chat_page():
    return FileResponse("endpoints/templates/chat.html")

@router.websocket("/ws/{client_name}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, client_name: str, chat_id: int):
    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            time = str(datetime.now())
            await manager.broadcast(
                json.dumps({"sender": client_name, "data": data, "time": time}), chat_id
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
        await manager.broadcast(
            json.dumps({"sender": f"Client #{client_name}", "data": "left the chat"}),
            chat_id,
        )

