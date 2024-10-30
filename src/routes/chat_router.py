import logging
import sys
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from starlette import status

app = FastAPI()

logger = logging.getLogger(__name__)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

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
            logger.info(f"Received message: {data}")
            action = data.get("action")

            if action == "direct_message":
                recipient = data.get("to")
                message = data.get("msg")
                if recipient in connected_users:
                    try:
                        await connected_users[recipient].send_json(
                            {"action": "direct_message", "from": username, "msg": message}
                        )
                    except Exception as e:
                        logger.error(f"Error sending direct message: {e}", exc_info=True)

            elif action == "group_message":
                group_name = data.get("to")
                message = data.get("msg")
                logger.info(f"Group message received by server: {message}")
                logger.info(f"group subscrbiber are{group_subscribers}")
                if group_name in group_subscribers:
                    for subscriber in group_subscribers[group_name]:
                        try:
                            logger.info(f"Subscriber: {subscriber}")
                            await subscriber.send_json(
                                {"action": "group_message", "to": group_name, "from": username, "msg": message}
                            )
                        except Exception as e:
                            logger.error(f"Error sending group message: {e}", exc_info=True)
                            continue
                    logger.info("message sent to group")
            elif action == "group_subscribe":
                group_name = data.get("group")
                if group_name in group_subscribers:
                    group_subscribers[group_name].append(websocket)
                else:
                    group_subscribers[group_name] = [websocket]
                logger.info(f"Group subscriber action result: {group_name}")

    except WebSocketDisconnect:
        logger.info(f"Disconnected user: {username}")
        if username in connected_users:
            del connected_users[username]
        for subscribers in group_subscribers.values():
            if websocket in subscribers:
                subscribers.remove(websocket)
