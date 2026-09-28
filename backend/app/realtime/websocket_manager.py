import asyncio
import json
import logging
from typing import Dict, List, Set
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        # Map brand_id -> set of active WebSockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, brand_id: int, websocket: WebSocket):
        await websocket.accept()
        if brand_id not in self.active_connections:
            self.active_connections[brand_id] = set()
        self.active_connections[brand_id].add(websocket)
        logger.info(f"WebSocket connected for brand_id {brand_id}. Total listeners: {len(self.active_connections[brand_id])}")

    def disconnect(self, brand_id: int, websocket: WebSocket):
        if brand_id in self.active_connections:
            self.active_connections[brand_id].discard(websocket)
            if not self.active_connections[brand_id]:
                del self.active_connections[brand_id]
        logger.info(f"WebSocket disconnected for brand_id {brand_id}")

    async def broadcast_to_brand(self, brand_id: int, event_type: str, data: dict):
        """Broadcasts event payload to all clients listening to a specific brand."""
        if brand_id not in self.active_connections:
            return
            
        payload = {
            "event": event_type,  # 'new_mention', 'alert_triggered', 'score_updated'
            "data": data
        }
        
        dead_sockets = set()
        for websocket in list(self.active_connections[brand_id]):
            try:
                await websocket.send_json(payload)
            except Exception as e:
                logger.warning(f"Error sending payload to websocket: {e}")
                dead_sockets.add(websocket)

        for ws in dead_sockets:
            self.disconnect(brand_id, ws)

ws_manager = WebSocketManager()
