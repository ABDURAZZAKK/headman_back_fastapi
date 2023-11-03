from fastapi import WebSocket



class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {1: []}

    async def connect(self, websocket: WebSocket, chat_id):
        await websocket.accept()
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id):
        self.active_connections[chat_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_all_chats(self, message: str):
        for chat in self.active_connections.keys():
            for connection in self.active_connections[chat]:
                await connection.send_text(message)

    async def broadcast(self, message: str, chat_id):
        for connection in self.active_connections[chat_id]:
            await connection.send_text(message)



