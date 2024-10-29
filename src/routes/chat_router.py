import logging
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from starlette import status

app = FastAPI()

logger = logging.getLogger(__name__)

connected_users: Dict[str, WebSocket] = {}
group_subscribers: Dict[str, List[WebSocket]] = {}


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket, username: str = Query(...)) -> None:
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
    await websocket.accept()
    connected_users[username] = websocket
    logger.info(f"Connected user: {username}")

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "direct_message":
                recipient = data.get("to")
                message = data.get("msg")
                if recipient in connected_users:
                    await connected_users[recipient].send_json(
                        {"action": "direct_message", "from": username, "msg": message}
                    )

            elif action == "group_message":
                group_name = data.get("to")
                message = data.get("msg")
                if group_name in group_subscribers:
                    for subscriber in group_subscribers[group_name]:
                        await subscriber.send_json(
                            {"action": "group_message", "to": group_name, "from": username, "msg": message}
                        )

    except WebSocketDisconnect:
        logger.info(f"Disconnected user: {username}")
        if username in connected_users:
            del connected_users[username]
        for subscribers in group_subscribers.values():
            if websocket in subscribers:
                subscribers.remove(websocket)
